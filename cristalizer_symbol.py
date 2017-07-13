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

class BlockItem_Cristalizer(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Cristalizer, self).__init__(parent)
		self.editor=edit
		w = 175.0
		h = 200.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\Cristallizer.png"); 
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
		self.inputs.append(PortItem('Semilla de entrada','in','seed',str(name_block),self.editor,None, self) )
		self.inputs.append(PortItem('Vapor de entrada','in','vapor',str(name_block),self.editor,None, self) )
		self.inputs.append(PortItem('Alimentacion de entrada','in','juice',str(name_block),self.editor,None, self) )
		self.outputs = []
		self.outputs.append(PortItem("Vapor de salida",'out','vapor',str(name_block),self.editor,None, self) )
		self.outputs.append(PortItem('Descarga','out','juice',str(name_block),self.editor,None, self) )
		self.outputs.append(PortItem("Vapor condensado",'out','condensed',str(name_block),self.editor,None, self) )
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
		ly = (h-20)
		self.label.setPos(lx+50, ly)
		# Update port positions:
		
		self.inputs[0].setPos(0, (h/2)+2)
		self.inputs[0].block_pos=[w,0,h,(h/2)+2]
		
		self.inputs[1].setPos(0, (h/2)+37)
		self.inputs[1].block_pos=[w,0,h,(h/2)+37]

		self.inputs[2].setPos(23, h-10)
		self.inputs[2].block_pos=[w,23,h, h-10]

		self.outputs[0].setPos(w-8, 12)
		self.outputs[0].block_pos=[w,w-8,h, 12]

		self.outputs[1].setPos(w/2, h)
		self.outputs[1].block_pos=[w,w/2,h,h]

		self.outputs[2].setPos(w, h-45)
		self.outputs[2].block_pos=[w,w,h,h-45]		

		return w, h