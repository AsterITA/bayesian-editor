from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea


class Ui_CPTWindow(QtWidgets.QMainWindow):
    def __init__(self, graph_scene, nodeName, posterior=None):
        super().__init__()
        self.scene = graph_scene
        self.posterior = posterior
        self.nodeCPT = self.scene.bn.cpt(nodeName)  # CPT del nodo
        self.numParents = self.nodeCPT.nbrDim() - 1  # Numero di genitori
        self.nodeName = nodeName  # Nome del nodo
        self.scrollArea = QScrollArea()
        if self.nodeCPT.var_dims[-1] == 2:  # If it's a LabelizedVariable
            self.labelizedVariable = True
            self.sliders = []
            self.trueLabels = []
            self.falseLabels = []
        else:  # If it's a RangeVariable
            self.labelizedVariable = False
            self.boxes = []
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("CPT of " + self.nodeName)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.grid = QtWidgets.QGridLayout()
        # Metto il nome del nodo attuale in alto a destra nella griglia
        label = QtWidgets.QLabel()
        label.setFont(self.font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(self.nodeName)
        var = -1
        if self.posterior is None:
            if self.numParents > 0:
                emptyBox = QtWidgets.QLabel()  # Box vuoto in alto a sinistra nella griglia
                self.grid.addWidget(emptyBox, 0, 0, 1, self.numParents)
                self.grid.addWidget(label, 0, self.numParents, 1, 3)
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
                        if domain[
                            0] == '<':  # Nel caso si tratti di una labelizedVariable, di solito ci sono solo le label di vero e falso
                            domain = ["F", "T"]
                        else:  # Nel caso di una rangeVariable, inserisco nel domainSet tutte le label del dominio
                            domain = domain[1:-1].split(",")
                            domain = list(range(int(domain[0]), int(domain[1]) + 1))
                        domainSet.append(domain)
                self.genGrid(1, 0, domainSet)
            else:
                self.grid.addWidget(label, 0, 0, 1, 3)
        else:
            self.grid.addWidget(label, 0, 0, 1, 2)
        # Creo la riga del vero/falso affianco le variabili
        domains = self.scene.bn.variableFromName(self.nodeName).domain()
        if domains[
            0] == '<':  # Nel caso si tratti di una labelizedVariable, di solito ci sono solo le label di vero e falso
            domains = ["F", "T"]
        else:  # Nel caso di una rangeVariable, inserisco nel domainSet tutte le label del dominio
            domains = domains[1:-1].split(",")
            domains = list(range(int(domains[0]), int(domains[1]) + 1))

        for col_offset, domain in enumerate(domains, start=1):
            label = QtWidgets.QLabel()
            label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText(str(domain))
            self.grid.addWidget(label, 1, var + col_offset, 1, 1)
        if self.posterior is None:
            # Creo i box delle proabilità
            if self.labelizedVariable:
                self.genSliders()
            else:
                self.genBoxes()
            # Aggiungo il bottone per confermare il CPT e chiudere la finestra
            button = QtWidgets.QPushButton('OK', self)
            self.grid.addWidget(button, self.grid.rowCount(), 0, 1, self.grid.columnCount())
            button.clicked.connect(self.closeWindow)

            # Aggiungo comandi per l'inferenza
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout_2")
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
            self.grid.addLayout(self.verticalLayout, self.grid.rowCount(), 0, 1, self.grid.columnCount())
        else:
            posterior = self.posterior.__str__().split('/')
            falsePosterior = QtWidgets.QLabel()
            falsePosterior.setAlignment(QtCore.Qt.AlignCenter)
            falsePosterior.setText(posterior[0].split('::')[1])
            self.grid.addWidget(falsePosterior, 2, var + 1, 1, 1)
            truePosterior = QtWidgets.QLabel()
            truePosterior.setAlignment(QtCore.Qt.AlignCenter)
            truePosterior.setText(posterior[1].split('::')[1])
            self.grid.addWidget(truePosterior, 2, var + 2, 1, 1)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(self.grid)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(central_widget)
        self.setCentralWidget(self.scrollArea)

    def genBoxes(self):
        listCPT = self.nodeCPT.toarray()
        col = len(self.nodeCPT.var_names)
        n_rows = self.grid.rowCount() - 2
        defaultValue = 1 / self.nodeCPT.var_dims[-1]
        if n_rows == 0:
            n_rows += 1
        for row in range(n_rows):
            value = 0
            for i in range(self.nodeCPT.var_dims[-1]):
                value += listCPT[row][
                    i]  # Check if the sum of the values in the CPT is 1, otherwise it was not setted and the default value wil be setted
            for i in range(self.nodeCPT.var_dims[-1]):
                self.boxes[row][i].append(QtWidgets.QDoubleSpinBox())
                self.boxes[row][i].setMaximum(1)
                self.boxes[row][i].setMinimum(0)
                self.boxes[row][i].setSingleStep(0.01)
                if value != 1:  # Set the default value
                    self.boxes[row][i].setValue(defaultValue)
                else:  # Set the read value
                    self.boxes[row][i].setValue(listCPT[row][i])
                self.grid.addWidget(self.boxes[row][i], row + 2, col + i)

    def genSliders(self):
        splittedCPT = self.nodeCPT.__str__().split('/')
        col = self.grid.columnCount()
        n_rows = self.grid.rowCount() - 2
        if n_rows == 0:
            n_rows = n_rows + 1
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

    def closeWindow(self):
        probabilities = []
        for false, true in zip(self.falseLabels, self.trueLabels):
            probabilities.append(float(false.text()))
            probabilities.append(float(true.text()))
        self.nodeCPT.fillWith(probabilities)
        self.close()

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
