import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from evaporator_dialogbox import Ui_Dialog as evaporator_dialogbox
#Import blocks

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
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Evap, self).__init__(parent)
		self.editor=edit
		w = 140.0
		h = 235.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\Evap_Kstner.png"); 
		self.setBrush(QtGui.QBrush(Img))
		#self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
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
		self.inputs.append( PortItem('Jugo de entrada','in','juice',str(name_block),self.editor,None, self) )
		self.inputs.append( PortItem('Vapor vivo','in','vapor',str(name_block),self.editor,None, self) )
		self.outputs = []
		self.outputs.append( PortItem('Jugo de salida','out','juice',str(name_block),self.editor,None, self) )
		self.outputs.append( PortItem('Vapor vegetal','out','vapor',str(name_block),self.editor,None, self) )
		self.outputs.append( PortItem('Vapor condensado','out','condensed',str(name_block),self.editor,None, self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Evaporator(self.name_block,self.editor.Sim_time,self,self.editor.db,self.window())
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
		lx = ((w - lw) / 2)
		ly = ((h - lh) / 2)-20
		self.label.setPos(lx, ly)
		# Update port positions:
		
		self.inputs[0].setPos(0, (h-4))
		self.inputs[0].block_pos=[w,0,h,(h-4)]

		self.inputs[1].setPos(0, (h / 3)+73)
		self.inputs[1].block_pos=[w,0,h, (h / 3)+73]

		self.outputs[0].setPos(w, h-4)
		self.outputs[0].block_pos=[w,w,h, h-4]

		self.outputs[1].setPos((w/2), 0)
		self.outputs[1].block_pos=[w,(w/2),h, 0]

		self.outputs[2].setPos(w, (2*h/3)+23)
		self.outputs[2].block_pos=[w,w,h, (2*h/3)+23]

		return w, h

class ParameterDialog_Evaporator(QDialog):
	def __init__(self,dat,time,item,Data_base, parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = evaporator_dialogbox()
		self.ui.setupUi(dat,time,item,Data_base,self.Resultado)
		self.Resultado.exec_()