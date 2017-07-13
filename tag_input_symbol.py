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

class BlockItem_tag_input(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled',edit=None, parent=None):
		super(BlockItem_tag_input, self).__init__(parent)
		self.editor=edit

		w = 48.0
		h = 46.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\wire_tag_input.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem("  TAG  ", self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		self.label.setTextInteractionFlags((QtCore.Qt.TextEditable))
		# Inputs and outputs of the block:
		from Dynamic_simulator import PortItem
		
		self.outputs = []
		self.outputs.append(PortItem('Salida','out','none',str(name_block),self.editor,None,self) )

		# Update size:
		self.changeSize(w, h)
	def deleteBlock(self):
		from Dynamic_simulator import DeleteDialog

		pd = DeleteDialog(self.editor,self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		dl.triggered.connect(self.deleteBlock)
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
		self.label.setPos(0, ly-5)
		# Update port positions:
		self.outputs[0].setPos(w+4, (h / 2)+1)
		self.outputs[0].block_pos=[w,w+4,h, (h / 2)+1]

		return w, h