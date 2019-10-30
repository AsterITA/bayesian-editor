from PyQt5 import QtCore, QtGui, QtWidgets

''' Graph GUI 
  
    Author: Sharif Shaker
    Date: 4/29/2017
    
    Modified: 5/11/2017
    Changes made: allowed control panel to run bellman ford algorithm 

    Description:
        This file contains various classes and functions for displaying a graphical panel for controling various functions to 
        be run on a GraphScene object.  The control panel design was done using QtDesigner

'''


class Ui_GraphControlWindow(object):

    def setupUi(self, GraphControlWindow, graph_scene):
        self.scene = graph_scene  # get a GraphScene object from parameter

        # set up layouts, labels, text editors, and buttons
        GraphControlWindow.setObjectName("GraphControlWindow")
        GraphControlWindow.resize(483, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(GraphControlWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.add_edge_lab = QtWidgets.QLabel(GraphControlWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.add_edge_lab.setFont(font)
        self.add_edge_lab.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.add_edge_lab.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.add_edge_lab.setObjectName("add_edge_lab")
        self.verticalLayout_2.addWidget(self.add_edge_lab)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(GraphControlWindow)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.add_edge1_lab = QtWidgets.QLabel(GraphControlWindow)
        self.add_edge1_lab.setObjectName("add_edge1_lab")
        self.horizontalLayout.addWidget(self.add_edge1_lab)
        self.add_edge1_edit = QtWidgets.QLineEdit(GraphControlWindow)
        self.add_edge1_edit.setObjectName("add_edge1_edit")
        self.horizontalLayout.addWidget(self.add_edge1_edit)
        self.add_edge2_lab = QtWidgets.QLabel(GraphControlWindow)
        self.add_edge2_lab.setObjectName("add_edge2_lab")
        self.horizontalLayout.addWidget(self.add_edge2_lab)
        self.add_edge2_edit = QtWidgets.QLineEdit(GraphControlWindow)
        self.add_edge2_edit.setObjectName("add_edge2_edit")
        self.horizontalLayout.addWidget(self.add_edge2_edit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.add_edge_btn = QtWidgets.QPushButton(GraphControlWindow)
        self.add_edge_btn.setObjectName("add_edge_btn")
        self.verticalLayout_2.addWidget(self.add_edge_btn)
        self.remove_edge_lab = QtWidgets.QLabel(GraphControlWindow)
        self.remove_edge_lab.setFont(font)
        self.remove_edge_lab.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.remove_edge_lab.setObjectName("remove_edge_lab")
        self.verticalLayout_2.addWidget(self.remove_edge_lab)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.remove_edge1_lab = QtWidgets.QLabel(GraphControlWindow)
        self.remove_edge1_lab.setObjectName("remove_edge1_lab")
        self.horizontalLayout_2.addWidget(self.remove_edge1_lab)
        self.remove_edge1_edit = QtWidgets.QLineEdit(GraphControlWindow)
        self.remove_edge1_edit.setObjectName("remove_edge1_edit")
        self.horizontalLayout_2.addWidget(self.remove_edge1_edit)
        self.remove_edge2_lab = QtWidgets.QLabel(GraphControlWindow)
        self.remove_edge2_lab.setObjectName("remove_edge2_lab")
        self.horizontalLayout_2.addWidget(self.remove_edge2_lab)
        self.remove_edge2_edit = QtWidgets.QLineEdit(GraphControlWindow)
        self.remove_edge2_edit.setObjectName("remove_edge2_edit")
        self.horizontalLayout_2.addWidget(self.remove_edge2_edit)
        # spacerItem = QtWidgets.QSpacerItem(240, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.remove_edge_btn = QtWidgets.QPushButton(GraphControlWindow)
        self.remove_edge_btn.setObjectName("remove_edge_btn")
        self.verticalLayout_2.addWidget(self.remove_edge_btn)
        self.remove_node_lab_2 = QtWidgets.QLabel(GraphControlWindow)
        self.remove_node_lab_2.setFont(font)
        self.remove_node_lab_2.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.remove_node_lab_2.setObjectName("remove_node_lab_2")
        self.verticalLayout_2.addWidget(self.remove_node_lab_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.remove_node_lab = QtWidgets.QLabel(GraphControlWindow)
        self.remove_node_lab.setObjectName("remove_node_lab")
        self.horizontalLayout_3.addWidget(self.remove_node_lab)
        self.remove_node_edit = QtWidgets.QLineEdit(GraphControlWindow)
        self.remove_node_edit.setObjectName("remove_node_edit")
        self.horizontalLayout_3.addWidget(self.remove_node_edit)
        # spacerItem1 = QtWidgets.QSpacerItem(430, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.remove_node_btn = QtWidgets.QPushButton(GraphControlWindow)
        self.remove_node_btn.setObjectName("remove_node_btn")
        self.verticalLayout_2.addWidget(self.remove_node_btn)
        self.edit_CPT_header = QtWidgets.QLabel(GraphControlWindow)
        self.edit_CPT_header.setFont(font)
        self.edit_CPT_header.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.edit_CPT_header.setObjectName("edit_CPT_header")
        self.verticalLayout_2.addWidget(self.edit_CPT_header)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cpt_node_lab = QtWidgets.QLabel(GraphControlWindow)
        self.cpt_node_lab.setObjectName("cpt_node_lab")
        self.horizontalLayout_4.addWidget(self.cpt_node_lab)
        self.cpt_node_edit = QtWidgets.QLineEdit(GraphControlWindow)
        self.cpt_node_edit.setObjectName("cpt_node_edit")
        self.horizontalLayout_4.addWidget(self.cpt_node_edit)
        # spacerItem2 = QtWidgets.QSpacerItem(230, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.open_CPT_btn = QtWidgets.QPushButton(GraphControlWindow)
        self.open_CPT_btn.setObjectName("open_CPT_btn")
        self.verticalLayout_2.addWidget(self.open_CPT_btn)

        self.retranslateUi(GraphControlWindow)

        QtCore.QMetaObject.connectSlotsByName(GraphControlWindow)
        self.init_buttons()

    def init_buttons(self):
        # connect buttons and text edit values to various GraphScene functions
        # add edge
        self.add_edge_btn.clicked.connect(lambda: self.scene.add_edge(self.add_edge1_edit.text(),
                                                                      self.add_edge2_edit.text()))
        # remove edge
        self.remove_edge_btn.clicked.connect(lambda: self.scene.remove_edge(self.remove_edge1_edit.text(),
                                                                            self.remove_edge2_edit.text()))
        # remove node
        self.remove_node_btn.clicked.connect(
            lambda: self.scene.remove_node(self.remove_node_edit.text()))

        # open CPT
        self.open_CPT_btn.clicked.connect(lambda: self.scene.open_CPT(self.cpt_node_edit.text()))

        # Make inference
        # self.inference_btn.clicked.connect(lambda: self.scene.makeInference(self.inferenceMode.currentIndex()))

    def retranslateUi(self, GraphControlWindow):
        _translate = QtCore.QCoreApplication.translate

        # complete setup by adding text labels
        GraphControlWindow.setWindowTitle(_translate("GraphControlWindow", "Network Control WIndow"))
        self.add_edge_lab.setText(_translate("GraphControlWindow", "-Add Arc-"))
        self.add_edge1_lab.setText(_translate("GraphControlWindow", "Node 1:"))
        self.add_edge2_lab.setText(_translate("GraphControlWindow", "Node 2:"))
        self.add_edge_btn.setText(_translate("GraphControlWindow", "ADD ARC"))
        self.remove_edge_lab.setText(_translate("GraphControlWindow", "-Delete Arc-"))
        self.remove_edge1_lab.setText(_translate("GraphControlWindow", "Node 1:"))
        self.remove_edge2_lab.setText(_translate("GraphControlWindow", "Node 2:"))
        self.remove_edge_btn.setText(_translate("GraphControlWindow", "REMOVE ARC"))
        self.remove_node_lab_2.setText(_translate("GraphControlWindow", "-Delete Node-"))
        self.remove_node_lab.setText(_translate("GraphControlWindow", "Node:"))
        self.remove_node_btn.setText(_translate("GraphControlWindow", "REMOVE NODE"))
        self.edit_CPT_header.setText(_translate("GraphControlWindow", "-Conditional Probability Table-"))
        self.cpt_node_lab.setText(_translate("GraphControlWindow", "Node:"))
        self.open_CPT_btn.setText(_translate("GraphControlWindow", "OPEN CPT"))
