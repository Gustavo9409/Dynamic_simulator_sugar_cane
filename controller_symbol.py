import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#
from controller_dialogbox import Ui_Dialog as controller_dialogbox

import sys
import os
dir_script=str(os.getcwd())


class BlockItem_Controller(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_Controller, self).__init__(parent)
		self.editor=edit

		w = 60.0
		h = 68.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(QtCore.Qt.black, 1))
		self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem("PID TAG", self)
		self.label.setFont(QtGui.QFont("TypeWriter",10,QtGui.QFont.Bold))
		self.label.setDefaultTextColor(QtGui.QColor('black'))
		self.label.setTextInteractionFlags((QtCore.Qt.TextEditable))

		self.separator = QGraphicsLineItem(0,20,w,20,self)
		self.separator.setPen(QtGui.QPen(QtCore.Qt.black,2))

		self.labelSP = QGraphicsTextItem("SP:", self)
		self.labelSP.setFont(QtGui.QFont("TypeWriter", 7))
		self.labelSP.setDefaultTextColor(QtGui.QColor('black'))
		self.separator = QGraphicsLineItem(0,35,w,35,self)
		self.separator.setPen(QtGui.QPen(QtCore.Qt.black,1))

		self.labelMV = QGraphicsTextItem("MV:", self)
		self.labelMV.setFont(QtGui.QFont("TypeWriter", 7))
		self.labelMV.setDefaultTextColor(QtGui.QColor('black'))
		self.separator = QGraphicsLineItem(0,51,w,51,self)
		self.separator.setPen(QtGui.QPen(QtCore.Qt.black,1))

		self.labelPV = QGraphicsTextItem("PV:", self)
		self.labelPV.setFont(QtGui.QFont("TypeWriter", 7))
		self.labelPV.setDefaultTextColor(QtGui.QColor('black'))
		

		# Inputs and outputs of the block:
		from Dynamic_simulator import PortItem
		
		self.inputs = []
		self.inputs.append(PortItem('Entrada realimentada','in','none',str(name_block),self.editor, self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida controlada','out','electric',str(name_block),self.editor, self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Controller(self.name_block,self.editor.Sim_time,self,self.window())
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
		self.setRect(0.0, 0.0, w, h)
		# center label:
		rect = self.label.boundingRect()
		lw, lh = rect.width(), rect.height()
		lx = (w - lw) / 2
		ly = (20 - lh)
		self.label.setPos(lx, ly)
		rect = self.labelSP.boundingRect()
		lw, lh = rect.width(), rect.height()
		ly = (37 - lh)
		self.labelSP.setPos(0, ly)
		rect = self.labelMV.boundingRect()
		lw, lh = rect.width(), rect.height()
		ly = (53 - lh)
		self.labelMV.setPos(0, ly)
		rect = self.labelPV.boundingRect()
		lw, lh = rect.width(), rect.height()
		ly = (68 - lh)
		self.labelPV.setPos(0, ly)
		# Update port positions:
		self.inputs[0].setPos(-2, h-32)
		self.inputs[0].block_pos=[w,-2,h,h-32]

		self.outputs[0].setPos(w+6, h-32)
		self.outputs[0].block_pos=[w,w+6,h,h-32]

		return w, h

class ParameterDialog_Controller(QDialog):
	def __init__(self,dat,time,item,parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = controller_dialogbox()
		self.ui.setupUi(dat,time,item,self.Resultado)
		self.Resultado.exec_()