import math

import pyAgrum as gum
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QDialog

from NodeCPTGui import Ui_CPTWindow

''' Graph GUI Classes
  
    Author: Sharif Shaker
    Date: 4/29/2017
    
    Modified: 5/11/2017
    Changes made:  Included functionality for directed graph edges that include arrow heads to indicate direction. Functionality
    for running Bellman Ford algorithm added. 

    Description:
        This file contains objects for graphically displaying nodes and edges of a graph as well as the results of graph traversals.

'''


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.grid = QtWidgets.QGridLayout()
        self.setWindowTitle("Select range of the variable")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label = QtWidgets.QLabel()
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText("Minimum:")
        self.grid.addWidget(label, 0, 0)
        label = QtWidgets.QLabel()
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText("Maximum:")
        self.grid.addWidget(label, 0, 1)
        self.spinBoxes = [QtWidgets.QSpinBox(), QtWidgets.QSpinBox()]
        self.spinBoxes[0].setMaximum(1000)
        self.spinBoxes[1].setMaximum(1000)
        self.grid.addWidget(self.spinBoxes[0], 1, 0)
        self.grid.addWidget(self.spinBoxes[1], 1, 1)
        button = QtWidgets.QPushButton('OK', self)
        button.clicked.connect(self.closeWindow)
        self.grid.addWidget(button, 2, 0, 1, 2)
        self.setLayout(self.grid)

        # set up message box for displaying invalid input alerts
        self.InvalidInMsg = QtWidgets.QMessageBox()
        self.InvalidInMsg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.InvalidInMsg.setWindowTitle('Invalid input alert!')

    def closeWindow(self):
        if self.spinBoxes[0].value() <= self.spinBoxes[1].value():
            self.close()
        else:
            self.InvalidInMsg.setText("The minimum value must be lower or equal the maximum value")
            self.InvalidInMsg.exec_()


class Node(QtWidgets.QGraphicsItem):
    def __init__(self, x, y, val):

        super().__init__()

        self.x = x  # set x coordinate of node
        self.y = y  # set y coordinate of node
        self.val = val  # set node value
        self.parents = []  # name of parents
        self.children = []  # name of children
        self.highlighted = False
        self.selected = False

    def paint(self, painter, option, widget):

        if self.selected:
            # if the node is seleted paint it red
            painter.setPen(QtCore.Qt.green)
            painter.setBrush(QtGui.QColor(255, 50, 0, 255))
        elif self.highlighted:
            # if the node is highlighted paint it green
            painter.setPen(QtCore.Qt.green)
            painter.setBrush(QtGui.QColor(165, 255, 0, 255))
        else:
            # otehrwise paint it orange
            painter.setPen(QtCore.Qt.red)
            painter.setBrush(QtGui.QColor(255, 165, 0, 255))
        # paint the node to the scene
        painter.drawEllipse(QtCore.QRect(self.x, self.y, 40, 40))
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('Decorative', (10 / len(str(self.val)) + 5)))
        painter.drawText(QtCore.QRect(self.x, self.y, 40, 40), QtCore.Qt.AlignCenter, self.val)

    def boundingRect(self):
        return QtCore.QRectF(self.x, self.y, 37, 37)


class Edge(QtWidgets.QGraphicsItem):
    def __init__(self, node1, node2):

        super().__init__()
        self.node1 = node1  # set node at one end of edge
        self.node2 = node2  # set node at other end of edge
        self.x1 = node1.x + 20  # set x coordinate of one end of edge
        self.y1 = node1.y + 20  # set y coordinate of one end of edge
        self.x2 = node2.x + 20  # set x coordinate of other end of edge
        self.y2 = node2.y + 20  # set y coordinate of other end of edge

        self.highlighted = False

    def get_directed_arrow_points(self, x1, y1, x2, y2, d):

        # get point for head of arrow--
        v1 = x1 - x2  # x cooridinate for vector between points
        v2 = y1 - y2  # y coordinate for vicot between points

        # to get unit vector requires: u = v/|v|
        dom = math.sqrt(math.pow(v1, 2) + math.pow(v2, 2))  # = |v|

        new_x = v1 / dom  # unit vector x component
        new_y = v2 / dom  # unit vecotr y componenet

        point1 = (
            x2 + new_x * d, y2 + new_y * d)  # given node radius d, we want to multiply the unit vector by d to get a
        # vector length d in the direction of the original vector.  Add x2 and y2
        # so that the point is located on the actual edge

        # get point of another vertex of the triangle-- 
        p1x = x2 + new_x * d * 2  # get x value of a point along the edge that is twice as far along the edge as the given node radius d
        p1y = y2 + new_y * d * 2  # get y value of point

        # because we now want a unit vector perpendicular to the original edge
        v2 = x1 - p1x  # switch x and y vector values
        v1 = -(y1 - p1y)  # and negate a vector component

        # to get unit vector requires: u = v/|v|
        dom = math.sqrt(math.pow(v1, 2) + math.pow(v2, 2))  # = |v|

        new_x = v1 / dom  # get unit vector components
        new_y = v2 / dom

        point2 = (p1x + new_x * d / 2.0, p1y + new_y * d / 2.0)  # length from this point to edge is 1/2 radius of node

        # get point of final vertex of triangle--
        # because we want the other unit vector perpendicular to the original edge
        v1 = y1 - p1y  # switch x and y vector values
        v2 = -(x1 - p1x)  # negate the other vector component this time

        # to get unit vector requires: u = v/|v|
        dom = math.sqrt(math.pow(v1, 2) + math.pow(v2, 2))  # = |v|

        new_x = v1 / dom  # get unit vector
        new_y = v2 / dom

        point3 = (p1x + new_x * d / 2.0, p1y + new_y * d / 2.0)  # length from this point to edge is 1/2 radius of node

        return ([point1, point2, point3])  # return a list of the three points

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(3)
        if self.highlighted:
            # if edge is highlighted paint it green
            pen.setColor(QtGui.QColor(50, 175, 50, 200))
        else:
            # otherwise paint it red
            pen.setColor(QtGui.QColor(250, 100, 100, 255))
        # paint line to represent edge
        painter.setPen(pen)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)  # draw line to represent edge

        if self.highlighted:
            # if edge is highlighted paint arrow green
            # pen.setColor(QtCore.Qt.green)
            painter.setBrush(QtGui.QColor(165, 255, 0, 255))
        else:
            # otherwise paint it red
            pen.setColor(QtCore.Qt.red)
            painter.setBrush(QtGui.QColor(250, 100, 100, 255))
            painter.setPen(pen)
            point_array = self.get_directed_arrow_points(self.x1, self.y1, self.x2, self.y2,
                                                         20)  # get coordinates of arrow vertices
            points = [QtCore.QPointF(point_array[0][0], point_array[0][1]),
                      QtCore.QPointF(point_array[1][0], point_array[1][1]),
                      QtCore.QPointF(point_array[2][0], point_array[2][1])]  # create a list of QPointF
            arrow = QtGui.QPolygonF(points)  # create a triangle with the given points
            painter.drawPolygon(arrow)  # draw arrow

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 2500, 2500)


class GraphScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.movingNode = None
        self.importing = False
        self.setSceneRect(0, 0, 2500, 2500)  # set size of graphical scene
        self.nodes = {}  # node dictionary
        self.edges = {}  # edge dictionary
        self.importNames = []
        self.bn = gum.BayesNet('Bayesian Net')

        self.data_updater = UpdateData()  # create a data updater to send out a signal anytime data about the graph is changed

        # set up message box for displaying invalid input alerts 
        self.InvalidInMsg = QtWidgets.QMessageBox()
        self.InvalidInMsg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.InvalidInMsg.setWindowTitle('Invalid input alert!')

        self.selected = []

    def check_selected(self, requiredNum):

        if len(self.selected) != requiredNum:  # if nodes arent selected print message and cancel
            return False

        return True

    def deselect_nodes(self):
        for node in self.selected:
            node.selected = False
        self.selected = []

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:  # if right button pressed
            self.select_node(event)  # call selectd node function
            return

        QtWidgets.QGraphicsScene.mousePressEvent(self, event)  # call original function to maintain functionality

    def mouseReleaseEvent(self, event):
        if not self.movingNode:
            if event.button() == QtCore.Qt.LeftButton:  # if right button pressed
                self.add_node(event)  # otherwise call add node function
                return
        else:
            self.movingNode = None
        QtWidgets.QGraphicsScene.mouseReleaseEvent(self, event)  # call original function to maintain functionality

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:  # if left button pressed
            if self.movingNode is None:
                node = self.itemAt(event.scenePos(),
                                   QtGui.QTransform())  # get item clicked on at this position in scene
                if type(node) is Node:  # if item is a node
                    self.movingNode = node
            else:
                # Update node position
                self.movingNode.x = event.scenePos().x()
                self.movingNode.y = event.scenePos().y()
                # Updates arcs
                for edgeNode in self.movingNode.parents + self.movingNode.children:
                    try:
                        edge = self.edges[(self.movingNode.val, edgeNode)]
                        edge.x1 = edge.node1.x + 20
                        edge.y1 = edge.node1.y + 20
                    except KeyError:
                        edge = self.edges[(edgeNode, self.movingNode.val)]
                        edge.x2 = edge.node2.x + 20
                        edge.y2 = edge.node2.y + 20
                self.update()

        QtWidgets.QGraphicsScene.mouseMoveEvent(self, event)  # call original function to maintain functionality

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Return:  # if enter is pressed
            self.add_edge_selected()  # try to connect selected nodes with an edge
        elif event.key() == QtCore.Qt.Key_Backspace:  # if backspace pressed
            self.delete_nodes_selected()
        elif event.key() == QtCore.Qt.Key_Up:  # if up arrow pressed
            self.open_CPT_selected()
        elif event.key() == QtCore.Qt.Key_Delete:  # if delete pressed
            self.delete_edge_selected()  # remove edge between selected nodes

        self.update()

    def open_CPT_selected(self):
        if self.check_selected(1):
            self.open_CPT(self.selected[0].val)
            self.deselect_nodes()
        else:
            self.InvalidInMsg.setText('Must select only 1 node to open its CPT')
            self.InvalidInMsg.exec_()

    def open_CPT(self, nodeName):
        if nodeName not in self.nodes:  # if node1_val not in nodes dictionary
            self.InvalidInMsg.setText('"' + str(nodeName) + '" is not in network')
            self.InvalidInMsg.exec_()  # print message and exit
            return
        self.CPTWindow = Ui_CPTWindow(self, nodeName)
        self.CPTWindow.show()

    def makeInference(self, nodeName, index):
        if index == 0:  # Lazy Propagation
            ie = gum.LazyPropagation(self.bn)
        elif index == 1:  # Shafer Shenoy
            ie = gum.ShaferShenoyInference(self.bn)
        else:  # Variable Elimination
            ie = gum.VariableElimination(self.bn)
        ie.makeInference()
        try:
            self.CPTWindow.close()
            self.inferenceWindow = Ui_CPTWindow(self, nodeName, ie.posterior(nodeName))
            self.inferenceWindow.show()
        except Exception as e:
            self.InvalidInMsg.setText(e.__str__())
            self.InvalidInMsg.exec_()  # print message and exit

    def delete_edge_selected(self):

        if self.check_selected(2):  # if nodes selected
            self.remove_edge(self.selected[0].val, self.selected[1].val)  # delete edge between them
            self.deselect_nodes()  # deselect nodes
        else:  # else print error message
            self.InvalidInMsg.setText('Must select 2 nodes to delete edge')
            self.InvalidInMsg.exec_()

    def add_edge_selected(self):
        # check that 2 nodes selected
        if self.check_selected(2):  # if nodes selected
            if self.add_edge(self.selected[0].val, self.selected[1].val):  # add edge between selected nodes
                self.deselect_nodes()  # deselect nodes
        else:  # if invalid selection p rint error
            self.InvalidInMsg.setText('Must select 2 nodes to add edge')
            self.InvalidInMsg.exec_()

    def delete_nodes_selected(self):
        for node in self.selected:  # for each of the selected nodes
            self.remove_node(node.val)  # remove it from the graph

        self.selected = []

    def select_node(self, event):
        node = self.itemAt(event.scenePos(), QtGui.QTransform())  # get item clicked on at this position in scene

        if type(node) is Node:  # if item is a node
            node.selected = not node.selected  # set selected to True
            if node.selected:
                self.selected.append(node)
            else:
                self.selected.remove(node)
        self.update()

    def saveNodesLocation(self, path):
        file = open(path.replace('.bif', '_LOC.txt'), "w")
        for var in self.nodes.values():
            file.write(var.val)
            file.write(" ")
            file.write(str(var.x))
            file.write(" ")
            file.write(str(var.y))
            file.write("\n")
        file.close()

    def importBN(self, file):
        try:
            self.bn = gum.loadBN(file)
            self.importing = True
            self.nodes = {}
            self.edges = {}
            self.clear()
            node_LOC = file.replace(".bif", "_LOC.txt")
            try:  # Try to import nodes from file _LOC
                with open(node_LOC, "r") as loc:
                    nodes = loc.readlines()
                for node in nodes:
                    self.add_node(None, node.split())
                self.importArcs()
            except FileNotFoundError:  # Import only names, user will choose the positions of nodes
                for var in self.bn.names():
                    self.importNames.append(var)
                self.importNames.reverse()  # Reversing the list in order to start importing from the first node
                self.InvalidInMsg.setText("Click the point where to draw the node '" + self.importNames[-1] + "'")
                self.InvalidInMsg.exec_()  # print message and exit
        except gum.IOError:
            self.InvalidInMsg.setText("File not found")
            self.InvalidInMsg.exec_()  # print message and exit
        except gum.FatalError as e:
            self.InvalidInMsg.setText("File is not valid:\n{}".format(e))
            self.InvalidInMsg.exec_()  # print message and exit

    def importArcs(self):
        for arc in self.bn.arcs():
            self.add_edge(self.bn.variable(int(arc[0])).name(), self.bn.variable(int(arc[1])).name())
        self.importing = False

    def add_node(self, event, import_node=None):
        if import_node is None:
            x = event.scenePos().x()  # get x position of mouse
            y = event.scenePos().y()  # get y position of mouse
        else:  # Import positions from file _LOC
            x = float(import_node[1])
            y = float(import_node[2])
        if not self.importing:
            node_val, ok = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), 'Input Dialog',
                                                          'Enter node name:')  # use dialog to get node value to be added
            if node_val:  # In case user didn't want to create a node, he can just not type the name
                if node_val not in self.nodes:
                    variable_type, ok = QInputDialog.getItem(QtWidgets.QWidget(), "Select node type",
                                                             "Type:", ["LabelizedVariable", "RangeVariable"], 0, False)
                    if variable_type == "RangeVariable":
                        inputter = InputDialog()
                        inputter.exec_()
                        minVal = inputter.spinBoxes[0].value()
                        maxVal = inputter.spinBoxes[1].value()
                else:
                    self.InvalidInMsg.setText('Node already present')
                    self.InvalidInMsg.exec_()
                    return
        elif import_node is not None:  # Import the name from the file
            node_val = import_node[0]
        else:  # Import name from previous populated list
            node_val = self.importNames.pop()
        if node_val:  # dialog value was input
            if 10 > len(str(node_val)) > 0:  # if input was between 1 and 10 characters
                node = Node(x - 20, y - 20, str(node_val))  # create a new node at the given x and y coordinates
                self.addItem(node)  # add node to scene
                self.nodes[node.val] = node  # add node to node dictionary
                if not self.importing:
                    if variable_type == "RangeVariable":
                        var = gum.RangeVariable(node_val, "", minVal, maxVal)
                        potential = []
                        for i in range(var.domainSize()):
                            potential.append(0.5)
                    else:
                        var = gum.LabelizedVariable(node.val, "", 2)
                        potential = [0.5, 0.5]
                    self.bn.add(var)
                    self.bn.cpt(node.val).fillWith(potential)
            else:
                self.InvalidInMsg.setText(
                    'Node name must consist of between 1 and 10 characters')  # print message if invalid dialog input
                self.InvalidInMsg.exec_()
                return
            self.data_updater.signal.emit()  # emit a signal to notify that the graph was updated
            if self.importing and import_node is None:  # If importing without file
                if self.importNames:  # Import next node
                    self.InvalidInMsg.setText("Click the point where to draw the node '" + self.importNames[-1] + "'")
                    self.InvalidInMsg.exec_()  # print message and exit
                else:  # If nodes are imported, import arcs
                    self.importArcs()

    def add_edge(self, node1_val, node2_val):
        if node1_val not in self.nodes:  # ensure node value is in dictionary of nodes
            self.InvalidInMsg.setText('"' + str(node1_val) + '" is not in network')
            self.InvalidInMsg.exec_()
            return False
        if node2_val not in self.nodes:  # ensure node value is in dictionary of nodes
            self.InvalidInMsg.setText('"' + str(node2_val) + '" is not in network')
            self.InvalidInMsg.exec_()
            return False
        if node2_val == node1_val:  # ensure node values are unique
            self.InvalidInMsg.setText('Two unique node values required to create an arc')
            self.InvalidInMsg.exec_()
            return False
        # get nodes from dictionary
        node2 = self.nodes[node2_val]
        node1 = self.nodes[node1_val]
        if (node1_val, node2_val) in self.edges or ((node2_val,
                                                     node1_val) in self.edges):  # if edge already exists between given nodes
            self.InvalidInMsg.setText('Arc already present between the two nodes')
            self.InvalidInMsg.exec_()
            return False
        edge = Edge(node1, node2)  # create new edge
        self.addItem(edge)  # add edge to scene
        if not self.importing:
            self.bn.addArc(node1.val, node2.val)
        node1.children.append(node2_val)
        node2.parents.append(node1_val)
        # reset all nodes in graph so they are layered over the edges
        for val, node in self.nodes.items():
            self.removeItem(node)
            self.addItem(node)

        self.edges[(node1_val, node2_val)] = edge  # add new edge to list of edges
        self.data_updater.signal.emit()  # emit a signal to notify that the graph was updated
        return True  # return true if edge successfully added

    def remove_edge(self, node1_val, node2_val):

        if node1_val not in self.nodes:  # if node1_val not in nodes dictinary
            self.InvalidInMsg.setText('"' + str(node1_val) + '" is not in network')
            self.InvalidInMsg.exec_()  # print message and exit
            return

        if node2_val not in self.nodes:  # if node1_val not in nodes dictinary
            self.InvalidInMsg.setText('"' + str(node2_val) + '" is not in network')
            self.InvalidInMsg.exec_()  # print message and exit
            return

        if (node1_val, node2_val) not in self.edges:  # if edge from node1_val to node2_val not in edges dictionary
            self.InvalidInMsg.setText('No edge exists between nodes ' + str(node1_val) + ' and ' + str(node2_val))
            self.InvalidInMsg.exec_()  # print message and exit
            return
        else:
            edge = self.edges[(node1_val, node2_val)]  # otherwise represent edge from node1_val, node2_val

        self.removeItem(edge)  # remove edge from scene
        # self.graph.remove_edge(node1_val, node2_val)  # remove edge from underlaying graph
        self.bn.eraseArc(node1_val, node2_val)
        self.nodes[node1_val].children.remove(node2_val)
        self.nodes[node2_val].parents.remove(node1_val)
        del self.edges[(edge.node1.val, edge.node2.val)]  # delete edge from edges dictionary

        self.data_updater.signal.emit()  # emit a signal to notify that the graph was updated

    def remove_node(self, node_val):
        if node_val not in self.nodes:  # if node value not in dictionary
            self.InvalidInMsg.setText(str(node_val) + ' is not in graph')
            self.InvalidInMsg.exec_()  # print message and exit
            return
        connections = []
        for node_pair in self.edges.keys():  # for each edge in graph
            if node_pair[0] == node_val or node_pair[1] == node_val:  # if edge connects to this node
                connections.append(
                    (node_pair[0], node_pair[1]))  # save the connection in list
        for connection in connections:  # for all connections
            self.remove_edge(connection[0], connection[1])  # remove edges from graph
        self.removeItem(self.nodes[node_val])  # remove the node from the scene
        # self.graph.remove_node(node_val)  # remove the node from the underlaying graph
        self.bn.erase(node_val)
        del self.nodes[node_val]  # delete the node from the node dictionary

        self.data_updater.signal.emit()  # emit a signal to notify that the graph was updated
        return connections  # return the connections that were deleted

    def overlay_highlighted(self):
        for (from_node_val, to_node_val), edge in self.edges.items():
            if edge.highlighted:
                self.removeItem(edge)
                self.addItem(edge)  # layer highlighted edges over none highlighted edges

        for node_val, node in self.nodes.items():
            # layer all nodes over edges
            self.removeItem(node)
            self.addItem(node)


class UpdateData(QtCore.QObject):
    # class for signaling main window of updated data
    signal = QtCore.pyqtSignal()
