import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from tank_dialogbox import Ui_Dialog as tank_dialogbox
#Import blocks

#
import sys
import os
dir_script=str(os.getcwd())


class BlockItem_Tank(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Tank, self).__init__(parent)
		self.editor=edit
		
		w = 201.0
		h = 146.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\_Tank.png"); 
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
		self.inputs.append(PortItem('Fluido de entrada','in','none',str(name_block),self.editor,None, self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out','none',str(name_block),self.editor,None, self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Tank(self.name_block,self.editor.Sim_time,self,self.window())
		#pd.exec_()
	def deleteBlock(self):
		from Dynamic_simulator import DeleteDialog

		pd = DeleteDialog(self.editor,self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		pa = menu.addAction('Propiedades')
		dl.triggered.connect(self.deleteBlock)
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
		lx = (w - lw) / 3
		ly = 2*(h - lh) / 3
		self.label.setPos(lx+13, ly-5)
		# Update port positions:
		self.inputs[0].setPos((w/2)-11, 0)
		self.inputs[0].block_pos=[w,(w/2)-11,h,0]

		self.outputs[0].setPos(w, h-12)
		self.outputs[0].block_pos=[w,w,h, h-12]
		
		return w, h

class ParameterDialog_Tank(QDialog):
	def __init__(self,dat,time,label,fluid_port,parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = tank_dialogbox()
		self.ui.setupUi(dat,time,label,fluid_port,self.Resultado)
		self.Resultado.exec_()