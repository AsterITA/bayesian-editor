from dataclasses import dataclass
from itertools import islice

import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from iteration_utilities import deepflatten
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import linspace
from scipy.stats import norm, maxwell
from sympy import var, lambdify, sympify


@dataclass
class HistogramArguments:
    function = None
    vmin = None
    vmax = None


class Ui_CPTWindow(QtWidgets.QMainWindow):
    def __init__(self, graph_scene, nodeName, posterior=None):
        super().__init__()
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.scene = graph_scene
        self.posterior = posterior
        self.nodeCPT = self.scene.bn.cpt(nodeName)  # CPT del nodo
        self.numParents = self.nodeCPT.nbrDim() - 1  # Numero di genitori
        self.nodeName = nodeName  # Nome del nodo
        self.scrollArea = QtWidgets.QScrollArea()
        self.grid = QtWidgets.QGridLayout()
        self.central_widget = QtWidgets.QWidget()
        self.setWindowTitle("CPT of " + self.nodeName)
        if self.nodeCPT.var_dims[-1] == 2:  # If it's a LabelizedVariable
            self.central_widget.setLayout(self.grid)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWidget(self.central_widget)
            self.setCentralWidget(self.scrollArea)
            self.labelizedVariable = True
            self.sliders = []
            self.trueLabels = []
            self.falseLabels = []
            self.setupLabelizedUI()
        else:  # If it's a RangeVariable
            self.labelizedVariable = False
            # a figure instance to plot on
            self.figure = plt.figure()
            # this is the Canvas Widget that displays the `figure`
            # it takes the `figure` instance as a parameter to __init__
            self.canvas = FigureCanvas(self.figure)

            # this is the Navigation widget
            # it takes the Canvas widget and a parent
            # self.toolbar = NavigationToolbar(self.canvas, self)
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout_2")
            self.central_widget.setLayout(self.verticalLayout)
            if self.posterior is None:
                self.scrollArea.setMinimumSize(670, 730)
            else:
                self.scrollArea.setMinimumSize(670, 550)
            self.scrollArea.setWidget(self.central_widget)
            self.setCentralWidget(self.scrollArea)
            self.HistogramArguments = []
            self.setupRangeUI()
            self.central_widget.adjustSize()

    def setupRangeUI(self):
        # Metto il nome del nodo attuale in alto a destra nella griglia
        label = QtWidgets.QLabel()
        label.setFont(self.font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(self.nodeName)
        self.verticalLayout.addWidget(label)
        if self.posterior is None:
            self.genVariables()
            label = QtWidgets.QLabel()
            label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText("Function")
            self.grid.addWidget(label, 1, self.numParents)
            label = QtWidgets.QLabel()
            label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText("Start")
            self.grid.addWidget(label, 1, self.numParents + 1)
            label = QtWidgets.QLabel()
            label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText("Stop")
            self.grid.addWidget(label, 1, self.numParents + 2)
            nrows = self.grid.rowCount()
            if self.numParents == 0:
                nrows += 1
            for index, row in enumerate(range(2, nrows)):
                self.HistogramArguments.append(HistogramArguments())
                self.HistogramArguments[index].function = QtWidgets.QComboBox()
                self.HistogramArguments[index].function.addItems(["Norm", "Maxwell", "Custom"])
                self.HistogramArguments[index].vmin = QtWidgets.QDoubleSpinBox()
                self.HistogramArguments[index].vmin.setRange(-1000, 1000)
                self.HistogramArguments[index].vmax = QtWidgets.QDoubleSpinBox()
                self.HistogramArguments[index].vmax.setRange(-1000, 1000)
                self.grid.addWidget(self.HistogramArguments[index].function, row, self.numParents)
                self.grid.addWidget(self.HistogramArguments[index].vmin, row, self.numParents + 1)
                self.grid.addWidget(self.HistogramArguments[index].vmax, row, self.numParents + 2)

            widget = QtWidgets.QWidget()
            widget.setLayout(self.grid)
            self.verticalLayout.addWidget(widget)
            # Aggiungo il bottone per confermare il CPT e chiudere la finestra
            horizontalLayout = QtWidgets.QHBoxLayout()
            button = QtWidgets.QPushButton('OK', self)
            button.clicked.connect(self.closeWindow)
            horizontalLayout.addWidget(button)
            button = QtWidgets.QPushButton('Apply', self)
            button.clicked.connect(self.applyCPT)
            horizontalLayout.addWidget(button)
            widget = QtWidgets.QWidget()
            widget.setLayout(horizontalLayout)
            self.verticalLayout.addWidget(widget)
        # self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        if self.posterior is None:
            self.setupInferenceLayout()
        self.plot()

    def plot(self):
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        # get the data from the CPT
        if self.posterior is None:
            cpt = self.nodeCPT
        else:
            cpt = self.posterior
        values = []
        for i in cpt.loopIn():
            values.append(cpt.get(i))
        # plot the data
        for line in self.make_chunks(values, cpt.var_dims[-1]):
            ax.plot(line)
        plt.title("P(" + self.nodeName + ")")
        if self.posterior is None:
            legendStr = ""
            for row in range(2, self.grid.rowCount()):
                if row != 2:
                    legendStr += ";"
                legendStr += "P(" + self.nodeName + "|"
                for col, variable in enumerate(cpt.var_names):
                    if variable != self.nodeName:
                        if col != 0:
                            legendStr += ", "
                        legendStr += variable + "=" + self.grid.itemAtPosition(row, col).widget().text()
                legendStr += ")"
            plt.legend(legendStr.split(";"), loc="best")
        # refresh canvas
        self.canvas.draw()

    def make_chunks(self, data, SIZE):
        it = iter(data)
        for i in range(0, len(data), SIZE):
            yield [k for k in islice(it, SIZE)]

    def setupLabelizedUI(self):
        # Metto il nome del nodo attuale in alto a destra nella griglia
        label = QtWidgets.QLabel()
        label.setFont(self.font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(self.nodeName)
        if self.posterior is None:
            if self.numParents > 0:
                emptyBox = QtWidgets.QLabel()  # Box vuoto in alto a sinistra nella griglia
                self.grid.addWidget(emptyBox, 0, 0, 1, self.numParents)
                self.grid.addWidget(label, 0, self.numParents, 1, 3)
                self.genVariables()
            else:
                self.grid.addWidget(label, 0, 0, 1, 3)
                # Creo i box delle proabilità
            self.genSliders()
            # Aggiungo il bottone per confermare il CPT e chiudere la finestra
            button = QtWidgets.QPushButton('OK', self)
            self.grid.addWidget(button, self.grid.rowCount(), 0, 1, self.grid.columnCount())
            button.clicked.connect(self.closeWindow)

            # Aggiungo comandi per l'inferenza
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout_2")
            self.setupInferenceLayout()
            self.grid.addLayout(self.verticalLayout, self.grid.rowCount(), 0, 1, self.grid.columnCount())
        else:
            self.grid.addWidget(label, 0, 0, 1, 2)
            posterior = self.posterior.__str__().split('/')
            falsePosterior = QtWidgets.QLabel()
            falsePosterior.setAlignment(QtCore.Qt.AlignCenter)
            falsePosterior.setText(posterior[0].split('::')[1])
            self.grid.addWidget(falsePosterior, 2, 0, 1, 1)
            truePosterior = QtWidgets.QLabel()
            truePosterior.setAlignment(QtCore.Qt.AlignCenter)
            truePosterior.setText(posterior[1].split('::')[1])
            self.grid.addWidget(truePosterior, 2, 1, 1, 1)
        # Creo la riga del vero/falso affianco le variabili
        for col_offset, domain in enumerate(["F", "T"]):
            label = QtWidgets.QLabel()
            label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText(str(domain))
            if col_offset == 1 and self.posterior is None:
                col_offset += 1  # Offset one more because of the sliders
            if self.posterior is None:
                self.grid.addWidget(label, 1, self.numParents + col_offset, 1, 1)
            else:
                self.grid.addWidget(label, 1, col_offset, 1, 1)

    def genVariables(self):
        # Creo la la riga delle variabili
        for var in range(self.numParents):
            label = QtWidgets.QLabel()
            label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText(self.nodeCPT.var_names[var])
            self.grid.addWidget(label, 1, var, 1, 1)

        # Creo la griglia dei vero/falso delle rispettive variabili sulla sinistra
        domainSet = []
        for parent in self.nodeCPT.var_names:
            if parent != self.nodeName:
                parent = self.scene.bn.variableFromName(parent)
                domain = parent.domain()
                if domain[0] == '<':  # Nel caso si tratti di una labelizedVariable,
                    # di solito ci sono solo le label di vero e falso
                    domain = ["F", "T"]
                else:  # Nel caso di una rangeVariable, inserisco nel domainSet tutte le label del dominio
                    domain = domain[1:-1].split(",")
                    domain = list(range(int(domain[0]), int(domain[1]) + 1))
                domainSet.append(domain)
        self.genGrid(1, 0, domainSet)

    def setupInferenceLayout(self):
        self.inference_header = QtWidgets.QLabel()
        self.inference_header.setFont(self.font)
        self.inference_header.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.inference_header.setObjectName("inference_header")
        self.verticalLayout.addWidget(self.inference_header)
        self.inferenceMode = QtWidgets.QComboBox()
        self.inferenceMode.addItems(["Lazy Propagation", "Shafer Shenoy", "Variable Elimination"])
        self.verticalLayout.addWidget(self.inferenceMode)
        self.inference_header.setText("-Inference-")
        self.inference_btn = QtWidgets.QPushButton()
        self.inference_btn.setObjectName("inference_CPT_btn")
        self.inference_btn.setText("MAKE INFERENCE")
        self.inference_btn.clicked.connect(
            lambda: self.scene.makeInference(self.nodeName, self.inferenceMode.currentIndex()))
        self.verticalLayout.addWidget(self.inference_btn)

    def genSliders(self):
        splittedCPT = self.nodeCPT.__str__().split('/')
        col = self.grid.columnCount()
        n_rows = self.grid.rowCount() - 2
        if n_rows <= 0:
            n_rows = 1
        cpt_counter = 0
        for row in range(n_rows):
            self.sliders.append(QtWidgets.QSlider(QtCore.Qt.Horizontal))
            self.trueLabels.append(QtWidgets.QLabel())
            self.falseLabels.append(QtWidgets.QLabel())
            self.sliders[row].setMaximum(100)
            self.sliders[row].setMinimum(0)
            self.sliders[row].setSingleStep(1)
            self.sliders[row].setTickInterval(10)
            self.sliders[row].setTickPosition(QtWidgets.QSlider.TicksBelow)
            true = float(splittedCPT[cpt_counter + 1].split('::')[1])
            false = float(splittedCPT[cpt_counter].split('::')[1])
            if false == 0 and true == 0:
                self.sliders[row].setValue(50)
                self.trueLabels[row].setText("0.5")
                self.falseLabels[row].setText("0.5")
            else:
                self.sliders[row].setValue(true * 100)
                self.trueLabels[row].setText(str(true))
                self.falseLabels[row].setText(str(false))
            self.sliders[row].setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sliders[row].valueChanged.connect(
                lambda sv, falseLabel=self.falseLabels[row], trueLabel=self.trueLabels[row]:
                self.updateSlidLabel(sv, falseLabel, trueLabel))
            self.grid.addWidget(self.falseLabels[row], row + 2, col - 3)
            self.grid.addWidget(self.sliders[row], row + 2, col - 2)
            self.grid.addWidget(self.trueLabels[row], row + 2, col - 1)
            cpt_counter = cpt_counter + 2

    def updateSlidLabel(self, sliderValue, falseLabel, trueLabel):
        value = sliderValue / 100
        falseLabel.setText(str(round(1 - value, 2)))  # Approssimo per evitare rappresentazioni imprecise del float
        trueLabel.setText(str(value))

    def updateCPT(self):
        probabilities = []
        if self.labelizedVariable:
            for false, true in zip(self.falseLabels, self.trueLabels):
                probabilities.append(float(false.text()))
                probabilities.append(float(true.text()))
            self.nodeCPT.fillWith(probabilities)
        else:
            # Calculate all the values
            functions = []
            for index, args in enumerate(self.HistogramArguments, start=1):
                function = args.function.currentIndex()
                if function == 0:
                    function = norm().pdf
                elif function == 1:
                    function = maxwell().pdf
                else:
                    function = self.getUserFunction(index)
                functions.append(self.normalize(function, args.vmin.value(), args.vmax.value()))
            # Flatten all the values in a single list
            functions = list(deepflatten(functions))
            # Update the cpt with the values
            for cpt, value in zip(self.nodeCPT.loopIn(), functions):
                self.nodeCPT.set(cpt, value)

    def closeWindow(self):
        self.updateCPT()
        self.close()

    def applyCPT(self):
        self.updateCPT()
        self.plot()

    def genGrid(self, firstRow, col, domains):
        if col >= len(domains):
            return
        else:
            numDomains = len(domains[col])
            nRows = 1
            for domain in domains[col:]:
                nRows *= len(domain)
            step = nRows / numDomains
            for row in range(1, nRows + 1):
                label = QtWidgets.QLabel()
                label.setFont(self.font)
                label.setAlignment(QtCore.Qt.AlignCenter)
                index = (row - 1) / step
                label.setText(str(domains[col][int(index)]))
                self.grid.addWidget(label, firstRow + row, col, 1, 1)
            for i in range(numDomains):
                self.genGrid(firstRow + i * step, col + 1, domains)

    # we truncate a pdf, so we need to normalize
    def normalize(self, rv, vmin, vmax):
        pdf = rv(linspace(vmin, vmax, self.nodeCPT.var_dims[-1]))
        return pdf / sum(pdf)

    def getUserFunction(self, index):
        var('x')
        while True:
            func, ok = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), 'Input Dialog',
                                                      'Enter function of row n° ' + str(
                                                          index) + ':')  # use dialog to get node value to be added
            if "x" in func:
                break
            else:
                print("All'interno della funzione ci dev'essere la variabile x, riprova")

        func = lambdify(x, sympify(func))
        print("Test funzione:")
        print("La tua funzione con input 2 da come risultato: {}\n\n".format(func(2)))
        return func
