import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from heater_dialogbox import Ui_Dialog as heat_dialogbox
#Import blocks

#
import sys
import os
dir_script=str(os.getcwd())

class BlockItem_Heat(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Heat, self).__init__(parent)
		self.editor=edit
		w = 145.0
		h = 141.0
		# Properties of the rectangle:
		#self.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
		Img= QtGui.QImage(dir_script+"\Images\Heater_SnT.png");
		self.setPen(QtGui.QPen(Qt.NoPen)) 
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
		self.inputs.append(PortItem('Vapor de entrada','in','vapor',str(name_block),self.editor,None, self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out','none',str(name_block),self.editor,None, self) )
		self.outputs.append(PortItem('Vapor condensado','out','condensed',str(name_block),self.editor,None, self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Heater(self.name_block,self.editor.Sim_time,self,self.editor.db,self.window())
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
		lx = (w - 65)
		ly = (h -35) 
		self.label.setPos(lx, ly)
		# Update port positions:
		self.inputs[0].setPos(0, h/2 )
		self.inputs[0].block_pos=[w,0,h,h/2]

		self.inputs[1].setPos((w/2)-1, 0)
		self.inputs[1].block_pos=[w,(w/2)-1,h,0]

		self.outputs[0].setPos(w+2, h/2)
		self.outputs[0].block_pos=[w,w+2,h,h/2]

		self.outputs[1].setPos((w/2)-1, h+2)
		self.outputs[1].block_pos=[w,(w/2)-1,h,h+2]

		return w, h

class ParameterDialog_Heater(QDialog):
	def __init__(self,dat,time,item,db, parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = heat_dialogbox()
		self.ui.setupUi(dat,time,item,db,self.Resultado)
		self.Resultado.exec_()