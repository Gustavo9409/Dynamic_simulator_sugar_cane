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

class BlockItem_Mud_Filter(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Mud_Filter, self).__init__(parent)
		self.editor=edit
		w = 155.0
		h = 113.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\Mud_filter.png"); 
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
		self.inputs.append(PortItem('Lodos de entrada','in','mud',str(name_block),self.editor,None, self) )
		self.inputs.append(PortItem('Agua de entrada','in','water',str(name_block),self.editor,None, self) )
		self.outputs = []
		self.outputs.append(PortItem('Jugo de salida','out','juice',str(name_block),self.editor,None, self) )
		self.outputs.append(PortItem('Cachaza de salida','none','',str(name_block),self.editor,None, self) )
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
		self.label.setPos(lx+45, ly)
		# Update port positions:
		
		self.inputs[0].setPos(0, (h/2)+4)
		self.inputs[0].block_pos=[w,0,h,(h/2)+4]

		self.inputs[1].setPos(30, 16)
		self.inputs[1].block_pos=[w,30,h, 16]

		self.outputs[0].setPos((w/2)+2, h+3)
		self.outputs[0].block_pos=[w,(w/2)+2,h, h+3]

		self.outputs[1].setPos(w,(h/2)+3)
		self.outputs[1].block_pos=[w,w,h,(h/2)+3]

		return w, h