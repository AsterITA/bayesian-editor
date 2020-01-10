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
        self.sliders = []
        self.trueLabels = []
        self.falseLabels = []
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
                self.genGrid(self.numParents, 1, 0)
            else:
                self.grid.addWidget(label, 0, 0, 1, 3)
        else:
            self.grid.addWidget(label, 0, 0, 1, 2)
        # Creo la riga del vero/falso affianco le variabili
        falseLabel = QtWidgets.QLabel()
        falseLabel.setFont(self.font)
        falseLabel.setAlignment(QtCore.Qt.AlignCenter)
        falseLabel.setText("F")
        self.grid.addWidget(falseLabel, 1, var + 1, 1, 1)
        trueLabel = QtWidgets.QLabel()
        trueLabel.setFont(self.font)
        trueLabel.setAlignment(QtCore.Qt.AlignCenter)
        trueLabel.setText("T")
        if self.posterior is None:
            self.grid.addWidget(trueLabel, 1, var + 3, 1, 1)
            # Creo i box delle proabilità
            self.genProbabilityBoxes()
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
            self.grid.addWidget(trueLabel, 1, var + 2, 1, 1)
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

    def genProbabilityBoxes(self):
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

    def genGrid(self, numParents, s_row, col):
        if numParents == 0:
            return
        else:
            n = 2 ** numParents
            for row in range(1, n + 1):
                label = QtWidgets.QLabel()
                label.setFont(self.font)
                label.setAlignment(QtCore.Qt.AlignCenter)
                if row <= n / 2:
                    label.setText("F")
                else:
                    label.setText("T")
                self.grid.addWidget(label, s_row + row, col, 1, 1)
            self.genGrid(numParents - 1, s_row, col + 1)
            self.genGrid(numParents - 1, s_row + n / 2, col + 1)
