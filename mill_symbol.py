import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#
import sys
import os
dir_script=str(os.getcwd())

class BlockItem_Mill(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Mill, self).__init__(parent)
		self.editor=edit
		w = 132.0
		h = 199.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\Mill.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem(self.name_block, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		self.label.setTextInteractionFlags((QtCore.Qt.TextEditable))
		# Inputs and outputs of the block:
		from Dynamic_simulator import PortItem
		
		self.inputs = []
		self.inputs.append(PortItem('Alimentacion','in','none',str(name_block),self.editor,None, self) )
		self.outputs = []
		self.outputs.append(PortItem('Jugo de salida','out','juice',str(name_block),self.editor,None, self) )
		self.outputs.append(PortItem('Bagazo de salida','out','none',str(name_block),self.editor,None, self) )
		# Update size:
		self.changeSize(w, h)
	# def editParameters(self):
	# 	pd = ParameterDialog_Valve(self.name_block,Sim_time,self,self.window())
		
	def deleteBlock(self):
		from Dynamic_simulator import DeleteDialog

		pd = DeleteDialog(self.editor,self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		# pa = menu.addAction('Propiedades')
		dl.triggered.connect(self.deleteBlock)
		# pa.triggered.connect(self.editParameters)
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
		ly = (h)
		self.label.setPos(lx+2, ly)
		# Update port positions:
		
		self.inputs[0].setPos(4, 25)
		self.inputs[0].block_pos=[w,4,h, 25]

		self.outputs[0].setPos((w/2)+3, h)
		self.outputs[0].block_pos=[w,(w/2)+3,h, h]

		self.outputs[1].setPos(w+3, h-66)
		self.outputs[1].block_pos=[w,w+3,h, h-66]

		return w, h