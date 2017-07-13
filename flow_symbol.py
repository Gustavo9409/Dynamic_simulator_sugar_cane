import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from flow_dialogbox import Ui_Dialog as flow_dialogbox
#Import blocks

#
import sys
import os
dir_script=str(os.getcwd())


class BlockItem_Flow(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Flow, self).__init__(parent)
		self.editor=edit
		w = 47.0
		h = 45.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		self.icon= QtGui.QImage();
		self.icon.load(dir_script+"\Images\_flow_none.png")

		self.setBrush(QtGui.QBrush(self.icon))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem(self.name_block, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		self.label.setTextInteractionFlags((QtCore.Qt.TextEditable))
		# Output of the block:
		from Dynamic_simulator import PortItem
		
		self.outputs = []
		self.outputs.append(PortItem('Salida','out','none',str(name_block),self.editor,None,self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,self.editor.Sim_time,self,self.editor.db,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		from Dynamic_simulator import DeleteDialog

		pd = DeleteDialog(self.editor,self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		pa = menu.addAction('Propiedades')
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
	
		self.outputs[0].setPos(w+4, (h / 2)+1)
		self.outputs[0].block_pos=[w,w+4,h, (h / 2)+1]
		
		return w, h 

class ParameterDialog_Flow(QDialog):
	def __init__(self,dat,time,item,db,parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = flow_dialogbox()
		self.ui.setupUi(dat,time,item,db,self.Resultado)
		self.Resultado.exec_()