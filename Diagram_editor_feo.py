#!/usr/bin/python
import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#Import blocks
from EvaporatorBlock_feo import BlockItem_Evap
from Evapor_properties import Ui_Dialog
#
import sys
import os
dir_script=str(os.getcwd())
global puertosEvapIn
puertosEvapIn=None
global puertosEvapOut
puertosEvapOut=None

class Connection:
	"""
	 - fromPort
	 - toPort
	"""
	def __init__(self, fromPort, toPort):
		self.fromPort = fromPort
		self.pos1 = None
		self.pos2 = None
		if fromPort:
			self.pos1 = fromPort.scenePos()
			fromPort.posCallbacks.append(self.setBeginPos)
		self.toPort = toPort
		# Create arrow item:
		self.arrow = ArrowItem()
		editor.diagramScene.addItem(self.arrow)
	def setFromPort(self, fromPort):
		self.fromPort = fromPort
		if self.fromPort:
			self.pos1 = fromPort.scenePos()
			self.fromPort.posCallbacks.append(self.setBeginPos)
	def setToPort(self, toPort):
		self.toPort = toPort
		if self.toPort:
			self.pos2 = toPort.scenePos()
			self.toPort.posCallbacks.append(self.setEndPos)
	def setEndPos(self, endpos):
		self.pos2 = endpos
		self.arrow.setLine(QLineF(self.pos1, self.pos2))
	def setBeginPos(self, pos1):
		self.pos1 = pos1
		self.arrow.setLine(QLineF(self.pos1, self.pos2))
	def delete(self):
		editor.diagramScene.removeItem(self.arrow)
		# Remove position update callbacks:

class ParameterDialog(QDialog):
	def __init__(self, parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self.Resultado)
		self.Resultado.show()

class DeleteDialog(QDialog):
	def __init__(self, parent=None):
		super(DeleteDialog, self).__init__(parent)
		self.button = QPushButton('Ok', self)
		self.button2 = QPushButton('No', self)
		l = QVBoxLayout(self)
		l.addWidget(self.button)
		l.addWidget(self.button2)
		self.button.clicked.connect(self.OK)
		self.button2.clicked.connect(self.NO)
	def OK(self):
		self.close()
	def NO(self):
		self.close()

class PortItem(QGraphicsEllipseItem):
	""" Represents a port to a subsystem """
	def __init__(self, name,typ,edit, parent=None):
		self.edi=edit
		QGraphicsEllipseItem.__init__(self, QRectF(-6,-6,12.0,12.0), parent)
		self.setCursor(QCursor(QtCore.Qt.CrossCursor))
		# Properties:
		if typ=='out':
			self.setBrush(QBrush(Qt.green))
		elif typ=='in':
			self.setBrush(QBrush(Qt.blue))
		# Name:
		self.name = name
		self.posCallbacks = []
		self.setFlag(self.ItemSendsScenePositionChanges, True)
	def itemChange(self, change, value):
		if change == self.ItemScenePositionHasChanged:
			for cb in self.posCallbacks:
				cb(value)
			return value
		return super(PortItem, self).itemChange(change, value)
	def mousePressEvent(self, event):
		self.edi.startConnection(self)
	pass

class puertos():
	""" A handle that can be moved by the mouse """
	def __init__(self, parent=None):
		global puertosEvapIn
		global puertosEvapOut
		puertosEvapIn= []
		puertosEvapIn.append(PortItem('a','in',editor, self))
		puertosEvapIn.append(PortItem('b','in',editor, self))
		puertosEvapIn.append(PortItem('c','in',editor, self))
		puertosEvapIn.append(PortItem('d','in',editor, self))
		puertosEvapOut= []
		puertosEvapOut.append(PortItem('y','out',editor, self))

#Block part:
class HandleItem(QGraphicsEllipseItem):
	""" A handle that can be moved by the mouse """
	def __init__(self, parent=None):
		super(HandleItem, self).__init__(QRectF(-4.0,-4.0,8.0,8.0), parent)
		self.posChangeCallbacks = []
		self.setBrush(QtGui.QBrush(Qt.white))
		self.setFlag(self.ItemIsMovable, True)
		self.setFlag(self.ItemSendsScenePositionChanges, True)
		self.setCursor(QtGui.QCursor(Qt.SizeFDiagCursor))

	def itemChange(self, change, value):
		if change == self.ItemPositionChange:
			x, y = value.x(), value.y()
			# TODO: make this a signal?
			# This cannot be a signal because this is not a QObject
			for cb in self.posChangeCallbacks:
				res = cb(x, y)
				if res:
					x, y = res
					value = QPointF(x, y)
			return value
		# Call superclass method:
		return super(HandleItem, self).itemChange(change, value)

# class BlockItem_Evap(QGraphicsRectItem):
	# """ 
	# Represents a block in the diagram
	# Has an x and y and width and height
	# width and height can only be adjusted with a tip in the lower right corner.

	# - in and output ports
	# - parameters
	# - description
	# """
	# def __init__(self, name='Untitled', parent=None):
		# super(BlockItem_Evap, self).__init__(parent)
		# w = 198.0
		# h = 404.0
		# # Properties of the rectangle:
		# #self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
		# Img= QtGui.QImage(dir_script+"\Images\Evap_Kstner.png"); 
		# self.setBrush(QtGui.QBrush(Img))
		# #self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
		# self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		# self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# # Label:
		# self.label = QGraphicsTextItem(name, self)
		# self.label.setDefaultTextColor(QtGui.QColor('red'))
		# # Create corner for resize:
		# self.sizer = HandleItem(self)
		# self.sizer.setPos(w, h)
		# self.sizer.posChangeCallbacks.append(self.changeSize) # Connect the callback
		# self.sizer.setVisible(False)
		# self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

		# # Inputs and outputs of the block:
		# self.inputs = []
		# self.inputs.append( PortItem('a','in', self) )
		# self.inputs.append( PortItem('b','in', self) )
		# self.inputs.append( PortItem('c','in', self) )
		# self.inputs.append( PortItem('d','in', self) )
		# self.outputs = []
		# self.outputs.append( PortItem('y','out', self) )
		# # Update size:
		# self.changeSize(w, h)
	# def editParameters(self):
		# pd = ParameterDialog(self.window())
		# pd.exec_()
	# def DeleteBlock(self):
		# pd = DeleteDialog(self.window())
		# pd.exec_()
	# def contextMenuEvent(self, event):
		# menu = QMenu()
		# dl = menu.addAction('Delete')
		# pa = menu.addAction('Parameters')
		# dl.triggered.connect(self.DeleteBlock)
		# pa.triggered.connect(self.editParameters)
		# menu.exec_(event.screenPos())
	# def changeSize(self, w, h):
		# """ Resize block function """
		# # Limit the block size:
		# if h < 20:
			# h = 20
		# if w < 40:
			# w = 40
		# self.setRect(0.0, 0.0, w, h)
		# # center label:
		# rect = self.label.boundingRect()
		# lw, lh = rect.width(), rect.height()
		# lx = (w - lw) / 2
		# ly = (h - lh) / 2
		# self.label.setPos(lx, ly)
		# # Update port positions:
		# if len(self.inputs) == 1:
			# self.inputs[0].setPos(-4, h / 2)
		# elif len(self.inputs) > 1:
			# y = 5
			# dy = (h - 10) / (len(self.inputs) - 1)
			# for inp in self.inputs:
				# inp.setPos(-4, y)
				# y += dy
		# if len(self.outputs) == 1:
			# self.outputs[0].setPos(w+4, h / 2)
		# elif len(self.outputs) > 1:
			# y = 5
			# dy = (h - 10) / (len(self.outputs) + 0)
			# for outp in self.outputs:
				# outp.setPos(w+4, y)
				# y += dy
		# return w, h

class BlockItem_Heat(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name='Untitled',edit=None,parent=None):
		super(BlockItem_Heat, self).__init__(parent)
		self.edi=edit
		w = 315.0
		h = 147.0
		# Properties of the rectangle:
		#self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
		Img= QtGui.QImage(dir_script+"\Images\Heater_SnT.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.label = QGraphicsTextItem(name, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		# Create corner for resize:
		self.sizer = HandleItem(self)
		self.sizer.setPos(w, h)
		self.sizer.posChangeCallbacks.append(self.changeSize) # Connect the callback
		self.sizer.setVisible(False)
		self.sizer.setFlag(self.sizer.ItemIsSelectable, True)
		puertoin1=PortItem('a','in',self.edi, self)
		puertoin2=PortItem('b','in',self.edi, self)
		puertoout1=PortItem('y','out',self.edi, self)
		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(puertoin1)
		self.inputs.append(puertoin2 )
		self.outputs = []
		self.outputs.append(puertoout1)
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog(self.window())
		pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Delete')
		pa = menu.addAction('Parameters')
		dl.triggered.connect(self.DeleteBlock)
		pa.triggered.connect(self.editParameters)
		menu.exec_(event.screenPos())
	def changeSize(self, w, h):
		""" Resize block function """
		# Limit the block size:
		if h < 20:
		 h = 20
		if w < 40:
		 w = 40
		self.setRect(0.0, 0.0, w, h)
		# center label:
		rect = self.label.boundingRect()
		lw, lh = rect.width(), rect.height()
		lx = (w - lw) / 2
		ly = (h - lh) / 2
		self.label.setPos(lx, ly)
		# Update port positions:
		if len(self.inputs) == 1:
		 self.inputs[0].setPos(-4, h / 2)
		elif len(self.inputs) > 1:
		 y = 5
		 dy = (h - 10) / (len(self.inputs) - 1)
		 for inp in self.inputs:
			inp.setPos(-4, y)
			y += dy
		if len(self.outputs) == 1:
		 self.outputs[0].setPos(w+4, h / 2)
		elif len(self.outputs) > 1:
		 y = 5
		 dy = (h - 10) / (len(self.outputs) + 0)
		 for outp in self.outputs:
			outp.setPos(w+4, y)
			y += dy
		return w, h

class BlockItem_Flow(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name='Untitled',edit=None, parent=None):
		super(BlockItem_Flow, self).__init__(parent)
		self.edi=edit
		w = 47.0
		h = 30.0
		# Properties of the rectangle:
		#self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
		Img= QtGui.QImage(dir_script+"\Images\_arrow_flow2.jpg"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.label = QGraphicsTextItem(name, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		# Create corner for resize:
		self.sizer = HandleItem(self)
		self.sizer.setPos(w, h)
		self.sizer.posChangeCallbacks.append(self.changeSize) # Connect the callback
		self.sizer.setVisible(False)
		self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('a','in',self.edi, self) )
		self.outputs = []
		self.outputs.append(PortItem('y','out',self.edi, self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog(self.window())
		pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Delete')
		pa = menu.addAction('Parameters')
		dl.triggered.connect(self.DeleteBlock)
		pa.triggered.connect(self.editParameters)
		menu.exec_(event.screenPos())
	def changeSize(self, w, h):
		""" Resize block function """
		# Limit the block size:
		if h < 20:
		 h = 20
		if w < 40:
		 w = 40
		self.setRect(0.0, 0.0, w, h)
		# center label:
		rect = self.label.boundingRect()
		lw, lh = rect.width(), rect.height()
		lx = (w - lw) / 2
		ly = (h - lh) / 2
		self.label.setPos(lx, ly)
		# Update port positions:
		if len(self.inputs) == 1:
		 self.inputs[0].setPos(-4, h / 2)
		elif len(self.inputs) > 1:
		 y = 5
		 dy = (h - 10) / (len(self.inputs) - 1)
		 for inp in self.inputs:
			inp.setPos(-4, y)
			y += dy
		if len(self.outputs) == 1:
		 self.outputs[0].setPos(w+4, h / 2)
		elif len(self.outputs) > 1:
		 y = 5
		 dy = (h - 10) / (len(self.outputs) + 0)
		 for outp in self.outputs:
			outp.setPos(w+4, y)
			y += dy
		return w, h  
	  
class ArrowItem(QGraphicsLineItem):
	def __init__(self):
		super(ArrowItem, self).__init__(None)
		self.setPen(QtGui.QPen(QtCore.Qt.red,2))
		self.setFlag(self.ItemIsSelectable, True)
	def x(self):
		pass

class EditorGraphicsView(QGraphicsView):
	def __init__(self, scene, parent=None):
		QGraphicsView.__init__(self, scene, parent)
	def dragEnterEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			event.accept()
	def dragMoveEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			global namex
			namex = str(event.mimeData().data('component/name'))
			event.accept()
	def dropEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			name = str(event.mimeData().data('component/name'))
			if namex==str("Flow"):
				b1 = BlockItem_Flow(name,editor)
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
			elif namex==str("Evaporator"):
				b1 = BlockItem_Evap(name,editor)
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
			elif namex==str("Heater Exchanger"):
				b1 = BlockItem_Heat(name,editor)
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)

class LibraryModel(QStandardItemModel):
	def __init__(self, parent=None):
		QStandardItemModel.__init__(self, parent)
	def mimeTypes(self):
		return ['component/name']
	def mimeData(self, idxs):
		mimedata = QMimeData()
		for idx in idxs:
			if idx.isValid():
				txt = self.data(idx, Qt.DisplayRole)
				mimedata.setData('component/name', txt)
		return mimedata

class DiagramScene(QGraphicsScene):
	def __init__(self, parent=None):
		super(DiagramScene, self).__init__(parent)
	def mouseMoveEvent(self, mouseEvent):
		editor.sceneMouseMoveEvent(mouseEvent)
		super(DiagramScene, self).mouseMoveEvent(mouseEvent)
	def mouseReleaseEvent(self, mouseEvent):
		editor.sceneMouseReleaseEvent(mouseEvent)
		super(DiagramScene, self).mouseReleaseEvent(mouseEvent)

class DiagramEditor(QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowTitle("Energy simulator of the process of the sugar cane")

		# Widget layout and child widgets:
		self.horizontalLayout = QtGui.QHBoxLayout(self)
		# self.libraryBrowserView = QtGui.QListView(self)
		# self.libraryBrowserView.setMovement(QListView.Static)
		# self.libraryBrowserView.setGridSize(QtCore.QSize(200,100))
		# self.libraryBrowserView.setIconSize(QtCore.QSize(60,60))
		self.libraryModel = LibraryModel(self)
		self.libraryModel.setColumnCount(1)
		self.libraryModel.setHeaderData(0, QtCore.Qt.Horizontal, "Selection panel");

		self.libItems = []
		self.iconEvaporator=QIcon(dir_script+"\Images\evapor.jpg");
		self.iconHeater=QIcon(dir_script+"\Images\heater.png");
		self.iconFlow=QIcon(dir_script+"\Images\_arrow_flow.jpg");     
		self.EvaporItem=QtGui.QStandardItem(self.iconEvaporator, 'Evaporator');
		self.HeaterItem=QtGui.QStandardItem(self.iconHeater, 'Heater Exchanger') ;
		self.Flow=QtGui.QStandardItem(self.iconFlow, 'Flow') ;
		self.libItems.append(self.EvaporItem)
		self.libItems.append(self.HeaterItem)
		self.libItems.append(self.Flow)
		# for i in self.libItems:
		#    self.libraryModel.appendRow(i)

		####
		self.libraryBrowserView_TREE = QtGui.QTreeView(self)
		self.libraryBrowserView_TREE.setIconSize(QtCore.QSize(60,60))
		self.libraryBrowserView_TREE.setModel(self.libraryModel)
		parent1 = QStandardItem('Devices')
		parent1.appendRow(self.libItems[0])
		parent1.appendRow(self.libItems[1])
		self.libraryModel.appendRow(parent1)
		parent2 = QStandardItem('Flow inputs')
		parent2.appendRow(self.libItems[2])
		self.libraryModel.appendRow(parent2)
		self.libraryBrowserView_TREE.setDragDropMode(self.libraryBrowserView_TREE.DragOnly)
		self.horizontalLayout.addWidget(self.libraryBrowserView_TREE,1)
		####

		#self.libraryBrowserView.setModel(self.libraryModel)
		#self.libraryBrowserView.setViewMode(self.libraryBrowserView.IconMode)
		# self.libraryBrowserView.setDragDropMode(self.libraryBrowserView.DragOnly)
		self.diagramScene = DiagramScene(self)
		self.diagramView = EditorGraphicsView(self.diagramScene, self)
		# self.horizontalLayout.addWidget(self.libraryBrowserView,1)
		self.horizontalLayout.addWidget(self.diagramView,3)

		self.startedConnection = None
	def startConnection(self, port):
		self.startedConnection = Connection(port, None)
	def sceneMouseMoveEvent(self, event):
		pos = event.scenePos()
		items = self.diagramScene.items(pos)
		for item in items:
			if hasattr(item, 'name'):
				item.setToolTip(item.name)
			# if type(item) is PortItem:
				# item.setToolTip(item.name)
		if self.startedConnection:
			pos = event.scenePos()
			self.startedConnection.setEndPos(pos)
	def sceneMouseReleaseEvent(self, event):
		# Clear the actual connection:
		if self.startedConnection:
			pos = event.scenePos()
			items = self.diagramScene.items(pos)
			for item in items:
				if hasattr(item, 'name'):
				#if type(item) is PortItem:
					self.startedConnection.setToPort(item)
			if self.startedConnection.toPort == None:
				self.startedConnection.delete()
			self.startedConnection = None

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	global editor
	editor = DiagramEditor()
	editor.show()
	editor.resize(1000, 800)
	app.exec_()