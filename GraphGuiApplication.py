import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from GraphControlPanelGui import Ui_GraphControlWindow as GraphControlPanel
from GraphGuiClasses import GraphScene

''' Graph GUI 
  
    Author: Sharif Shaker
    Date: 4/29/2017
    
    Modified: 5/11/2017
    Changes made: Added functionality to change graph type between undirected graph and digraph by pressing a button on the panel.

    Description:
        This file contains various classes and functions for displaying a graphical representation of a graph.  The Graphical layout and 
        design was done using QtDesigner

'''


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")

        # setup central widget and main graphics area 
        self.MainWindow.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphView.setObjectName("graphView")

        # using the MainWindow passed into the funtion, add a graph scene 
        self.scene = self.MainWindow.graph_scene
        self.graphView.setScene(self.scene)

        # setup layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.graphView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 40, 0, 20)
        self.verticalLayout.setObjectName("verticalLayout")

        # large label for graph status information

        self.graph_info_lab = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph_info_lab.sizePolicy().hasHeightForWidth())
        self.graph_info_lab.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.graph_info_lab.setFont(font)
        self.graph_info_lab.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.graph_info_lab.setObjectName("graph_info_lab")
        self.verticalLayout.addWidget(self.graph_info_lab)

        # setup internal grid layout for graph status information
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setAlignment(QtCore.Qt.AlignTop)
        self.gridLayout_2.setContentsMargins(0, 5, -1, 5)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(55)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.node_count_lab = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.node_count_lab.setFont(font)
        self.node_count_lab.setObjectName("node_count_lab")
        self.gridLayout_2.addWidget(self.node_count_lab, 0, 0, 1, 1)
        self.edge_count_lab = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.edge_count_lab.setFont(font)
        self.edge_count_lab.setObjectName("edge_count_lab")
        self.gridLayout_2.addWidget(self.edge_count_lab, 1, 0, 1, 1)
        self.num_nodes_val = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.num_nodes_val.setFont(font)
        self.num_nodes_val.setObjectName("num_nodes_val")
        self.gridLayout_2.addWidget(self.num_nodes_val, 0, 1, 1, 1)
        self.num_edges_val = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.num_edges_val.setFont(font)
        self.num_edges_val.setObjectName("num_edges_val")
        self.gridLayout_2.addWidget(self.num_edges_val, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        # add button for pulling up control panel
        self.control_panel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.control_panel_btn.setObjectName("control_panel_btn")
        self.verticalLayout.addWidget(self.control_panel_btn)
        # add vertical layout to main horizontal layout
        self.horizontalLayout.addLayout(self.verticalLayout)

        # set as central widget
        self.MainWindow.setCentralWidget(self.centralwidget)

        # menu setup
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1225, 31))
        self.menubar.setObjectName("menubar")
        exportAction = QtWidgets.QAction('&Export BN', self.MainWindow)  # action pulling up a help menu
        exportAction.setShortcut('Ctrl+E')
        exportAction.triggered.connect(lambda: self.save_BN(self.menubar))
        importAction = QtWidgets.QAction('&Import BN', self.MainWindow)  # action pulling up a help menu
        importAction.setShortcut('Ctrl+I')
        importAction.triggered.connect(lambda: self.load_BN(self.menubar))
        helpAction = QtWidgets.QAction('&Open Help', self.MainWindow)  # action pulling up a help menu
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip('application help')
        helpAction.triggered.connect(lambda: webbrowser.open("BayesianEditorHelp.pdf"))  # open help file
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("File")
        self.menu.addAction(exportAction)
        self.menu.addAction(importAction)
        self.menu.addAction(helpAction)
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.retranslateUi(self.MainWindow)  # call retranslateUi function
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.button_setup()

    def button_setup(self):
        # connect the MainWindows init_control_panel function to button
        self.control_panel_btn.clicked.connect(lambda: self.MainWindow.init_control_pane())

        # connect update_data function to signal 
        self.scene.data_updater.signal.connect(lambda: self.update_data())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        # complete setup of labels and buttons by adding text
        MainWindow.setWindowTitle(_translate("MainWindow", "Network"))
        self.graph_info_lab.setText(_translate("MainWindow", "-NETWORK INFO-"))
        self.node_count_lab.setText(_translate("MainWindow", "Node Count:"))
        self.edge_count_lab.setText(_translate("MainWindow", "Arc  Count:"))
        self.num_nodes_val.setText(_translate("MainWindow", "0"))
        self.num_edges_val.setText(_translate("MainWindow", "0"))
        self.control_panel_btn.setText(_translate("MainWindow", "CONTROL PANEL"))

        self.menu.setTitle(_translate("MainWindow", "File"))

    @QtCore.pyqtSlot()
    def update_data(self):
        # function is called when signel is sent indicating the graph has been updated 
        _translate = QtCore.QCoreApplication.translate

        # show the current number of edges and nodes in graph
        self.num_nodes_val.setText(_translate("MainWindow", str(len(self.scene.nodes))))
        self.num_edges_val.setText(_translate("MainWindow", str(len(self.scene.edges))))

    def save_BN(self, menu):
        path, __ = QFileDialog.getSaveFileName(menu, 'Export BN', "BN.bif", "BIF (*.bif)")
        if path:  # Procedo all'export solo se è stato selezionato un percorso
            self.scene.bn.saveBIF(path)
            self.scene.saveNodesLocation(path)

    def load_BN(self, menu):
        file, __ = QFileDialog.getOpenFileName(menu, 'Import BN', "BN.bif", "BIF (*.bif)")
        if file:
            self.scene.importBN(file)


class SceneConnectedComboBox(QtWidgets.QComboBox):

    def __init__(self, widget, graph_scene):
        super().__init__(widget)  # initialize a combo box as part of input widget
        self.scene = graph_scene  # include a graph scene reference in combobox

    def keyPressEvent(self, event):
        self.scene.keyPressEvent(event)  # if the combobox is selected and a key is pressed send event to graph scene


class MainGraphWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # initialize the main window of the GUI
        super().__init__()

        self.graph_scene = GraphScene()  # initialize it with a graph scene

        self.app = QtWidgets.QApplication([])
        self.screen_resolution = app.desktop().screenGeometry()
        self.width = self.screen_resolution.width()
        self.height = self.screen_resolution.height()

        self.init_control_pane()  # also intitialize with a control panel

    def init_control_pane(self):
        self.setGeometry(self.width / 4 + 5, 40, 3 * self.width / 4,
                         self.height - 100)  # main window take up 3/4 of the total width of the screen
        self.GraphControlWindow = QtWidgets.QWidget()  # create an new control panel window
        ui = GraphControlPanel()
        ui.setupUi(self.GraphControlWindow, self.graph_scene)
        self.GraphControlWindow.setGeometry(0, 40, self.width / 4,
                                            self.height - 100)  # control panel takes 1/4 of the total width of the screen
        self.GraphControlWindow.show()  # display control panel

    def closeEvent(self, event):
        self.GraphControlWindow.close()  # when the main window is closed the control panel must also close


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainGraphWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
