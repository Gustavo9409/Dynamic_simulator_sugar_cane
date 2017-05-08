#!/usr/bin/python
import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#Import blocks
from Handle import HandleItem
#
import sys
import os
dir_script=str(os.getcwd())


class BlockItem_Evap(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name='Untitled',edit=None, parent=None):
		super(BlockItem_Evap, self).__init__(parent)
		self.edi=edit
		w = 198.0
		h = 404.0
		# Properties of the rectangle:
		#self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
		Img= QtGui.QImage(dir_script+"\Images\Evap_Kstner.png"); 
		self.setBrush(QtGui.QBrush(Img))
		#self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
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
		from Diagram_editor_feo import PortItem
		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('a','in',self.edi, self))
		self.inputs.append(PortItem('b','in',self.edi, self))
		self.inputs.append(PortItem('c','in',self.edi, self))
		self.inputs.append(PortItem('d','in',self.edi, self))
		self.outputs = []
		self.outputs.append(PortItem('y','out',self.edi, self))
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