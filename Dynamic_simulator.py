#!/usr/bin/python
# -*- coding: utf-8 -*-
import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#Import blocks
from Evapor_properties import Ui_Dialog as Evap_properties
from Heater_properties import Ui_Dialog as Heat_properties
from Tank_properties import Ui_Dialog as Tank_properties
from Valve_properties import Ui_Dialog as Valve_properties
from Flow_properties import Ui_Dialog as Flow_properties
#Import simulation
from Run_heater_model import Simulation_heat
#
import sys
import os
import re
import numpy as np
import psutil
dir_script=str(os.getcwd())

global i_ev
global i_ht
global i_vl
global i_fl
global i_tk
global i_cnv
global i_dvg
global l
global run_flag
global Ts_value
global Sim_time
global array_connections
Sim_time=1.0
l=0
i_ev=1
i_ht=1
i_vl=1
i_fl=1
i_tk=1
i_dvg=1
i_cnv=1
run_flag=0
array_connections=[]

outfile=open('time_exec.txt', 'w')
outfile.close()
outfile=open('Blocks_data.txt', 'w')
outfile.close()

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s
try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(text, disambig)

def Thread_time():
	global l
	while True:
		l = [random.randint(0, 20) for i in range(4)]

class Validator(object):
	def NumValidator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,3,2,LineEdit))

class Connection:
	"""
	 - fromPort
	 - toPort
	"""
	def __init__(self, fromPort, toPort):
		self.fromPort = fromPort
		self.pos1 = None
		self.pos2 = None
		if fromPort:
			self.pos1 = fromPort.scenePos()
			fromPort.posCallbacks.append(self.setBeginPos)
		self.toPort = toPort
		# Create arrow item:
		self.arrow = ArrowItem()
		editor.diagramScene.addItem(self.arrow)
	def setFromPort(self, fromPort):
		self.fromPort = fromPort
		if self.fromPort:
			self.pos1 = fromPort.scenePos()
			self.fromPort.posCallbacks.append(self.setBeginPos)
	def setToPort(self, toPort):
		self.toPort = toPort
		if self.toPort:
			self.pos2 = toPort.scenePos()
			self.toPort.posCallbacks.append(self.setEndPos)
	def setEndPos(self, endpos):
		self.pos2 = endpos
		self.arrow.setLine(QLineF(self.pos1, self.pos2))
	def setBeginPos(self, pos1):
		self.pos1 = pos1
		self.arrow.setLine(QLineF(self.pos1, self.pos2))
	def delete(self):
		editor.diagramScene.removeItem(self.arrow)
		# Remove position update callbacks:

class ParameterDialog_Evaporator(QDialog):
	def __init__(self,dat, parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Evap_properties()
		self.ui.setupUi(dat,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Heater(QDialog):
	def __init__(self,dat,time, parent):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = Heat_properties()
		self.ui.setupUi(dat,time,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Tank(QDialog):
	def __init__(self,dat, parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Tank_properties()
		self.ui.setupUi(dat,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Valve(QDialog):
	def __init__(self,dat, parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Valve_properties()
		self.ui.setupUi(dat,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Flow(QDialog):
	def __init__(self,dat, parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = Flow_properties()
		self.ui.setupUi(dat,self.Resultado)
		self.Resultado.exec_()

class DeleteDialog(QDialog):
	def __init__(self, parent=None):
		super(DeleteDialog, self).__init__(parent)
		self.setWindowTitle("Eliminar")
		self.button = QPushButton('Aceptar', self)
		self.button2 = QPushButton('Cancelar', self)
		self.label_Message = QtGui.QLabel('Esta seguro que desea eliminar este bloque?',self)
		l = QVBoxLayout(self)
		l.addWidget(self.label_Message)
		l.addWidget(self.button)
		l.addWidget(self.button2)
		self.button.clicked.connect(self.OK)
		self.button2.clicked.connect(self.NO)
	def OK(self):
		global i_vl
		global i_fl
		global i_tk
		global i_ht
		global i_ev
		global i_dvg
		global i_cnv
		Delete_item = editor.diagramScene.items(pos)
		for item in Delete_item:
			if hasattr(item, 'name_block'):
				aux=str(item.name_block)
				aux2=re.sub("\d+", "", aux)
				aux3=re.sub('([a-zA-Z]+)', "", aux)
				editor.diagramScene.removeItem(item)
				if aux2=="Valvula":
					if int(aux3)==(i_vl-1):
						i_vl=i_vl-1
				if aux2=="Tanque":
					if int(aux3)==(i_tk-1):
						i_tk=i_tk-1
				if aux2=="Flujo":
					if int(aux3)==(i_fl-1):
						i_fl=i_fl-1

					input_flow = open('Blocks_data.txt', 'r+')
					data=input_flow.readlines()
					input_flow.close()
					heater_data=[]
					if len(data)>0:
						for i in data:
							info=(i.strip()).split("\t")
							if len(info)>1:
								flag=info[0]
								if flag==("Fj"+str(aux3)):
									self.replace("Blocks_data.txt",str(i.strip()),"")
								elif flag==("Fv"+str(aux3)):
									self.replace("Blocks_data.txt",str(i.strip()),"")
								elif flag==("Fw"+str(aux3)):
									self.replace("Blocks_data.txt",str(i.strip()),"")
				if aux2=="Evaporador":
					if int(aux3)==(i_ev-1):
						i_ev=i_ev-1
				if aux2=="Calentador":
					if int(aux3)==(i_ht-1):
						i_ht=i_ht-1

					input_heat = open('Blocks_data.txt', 'r+')
					data=input_heat.readlines()
					input_heat.close()
					heater_data=[]
					if len(data)>0:
						for i in data:
							info=(i.strip()).split("\t")
							if len(info)>1:
								flag=info[0]
								if flag==("Ht"+str(aux3)):
									self.replace("Blocks_data.txt",str(i.strip()),"")
				if aux2=="Divergencia":
					if int(aux3)==(i_dvg-1):
						i_dvg=i_dvg-1
				if aux2=="Convergencia":
					if int(aux3)==(i_cnv-1):
						i_cnv=i_cnv-1
					
		self.close()
	def NO(self):
		self.close()
	def replace(self,path, pattern, subst):
		flags=0
		with open(path, "r+" ) as filex:
			fileContents = filex.read()
			textPattern = re.compile( re.escape( pattern ), flags )
			fileContents = textPattern.sub( subst, fileContents )
			filex.seek( 0 )
			filex.truncate()
			filex.write(fileContents) 

class PortItem(QGraphicsEllipseItem):
	""" Represents a port to a subsystem """
	def __init__(self, name,typ,block, parent=None):
		QGraphicsEllipseItem.__init__(self, QRectF(-6,-6,8.0,8.0), parent)
		self.setCursor(QCursor(QtCore.Qt.CrossCursor))
		# Properties:
		self.name_block=block
		self.typ=typ
		if self.typ=='out':
			self.setBrush(QBrush(Qt.green))
		elif self.typ=='in':
			self.setBrush(QBrush(Qt.blue))
		# Name:
		self.name = name
		self.posCallbacks = []
		self.setFlag(self.ItemSendsScenePositionChanges, True)
	def itemChange(self, change, value):
		if change == self.ItemScenePositionHasChanged:
			for cb in self.posCallbacks:
				cb(value)
			return value
		return super(PortItem, self).itemChange(change, value)
	def mousePressEvent(self, event):
		editor.startConnection(self)


class BlockItem_Evap(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Evap, self).__init__(parent)
		w = 198.0
		h = 404.0
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

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append( PortItem('Jugo de entrada','in',str(name_block), self) )
		self.inputs.append( PortItem('Vapor vivo','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append( PortItem('Jugo de salida','out',str(name_block), self) )
		self.outputs.append( PortItem('Vapor vegetal','out',str(name_block), self) )
		self.outputs.append( PortItem('Vapor condensado','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Evaporator(self.name_block,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
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
		
		self.inputs[0].setPos(2, (h / 2)+16)
		self.inputs[1].setPos(w+2, (h / 2)+62)
		self.outputs[0].setPos(w, h-12)
		self.outputs[1].setPos((w/2)+28, 25)
		self.outputs[2].setPos((w/2)-2, h-5)

		return w, h

class BlockItem_Heat(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Heat, self).__init__(parent)
		w = 315.0
		h = 147.0
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

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Fluido de entrada','in',str(name_block), self) )
		self.inputs.append(PortItem('Vapor de entrada','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out',str(name_block), self) )
		self.outputs.append(PortItem('Vapor condensado','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Heater(self.name_block,Sim_time,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
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
		self.inputs[0].setPos(33, 0 )
		self.inputs[1].setPos(155, 5)
		self.outputs[0].setPos(33, h)
		self.outputs[1].setPos(w-43, h-4)

		return w, h

class BlockItem_Flow(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Flow, self).__init__(parent)
		w = 47.0
		h = 30.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\_arrow_flow2.jpg"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem(self.name_block, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Entrada','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
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
		self.inputs[0].setPos(-4, (h / 2)+1)
		
		self.outputs[0].setPos(w+4, (h / 2)+1)
		
		return w, h  

class BlockItem_Valve(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Valve, self).__init__(parent)
		w = 60.0
		h = 90.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\_valve.jpg"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem(self.name_block, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Fluido de entrada','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Valve(self.name_block,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
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
		
		self.inputs[0].setPos(0, h-17)
		self.outputs[0].setPos(w+4, h-17)

		return w, h

class BlockItem_Convergence(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Convergence, self).__init__(parent)
		w = 42.0
		h = 70.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\Convergence.jpg"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		# self.label = QGraphicsTextItem(self.name_block, self)
		# self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Entrada 1','in',str(name_block), self) )
		self.inputs.append(PortItem('Entrada 2','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		# pa = menu.addAction('Propiedades')
		dl.triggered.connect(self.DeleteBlock)
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
		# rect = self.label.boundingRect()
		# lw, lh = rect.width(), rect.height()
		# lx = (w - lw) / 2
		# ly = (h - lh) / 2
		# self.label.setPos(lx, ly)
		# Update port positions:
		self.inputs[0].setPos(-4, (h / 4)+3)
		self.inputs[1].setPos(-4, h-(h/4) )
		self.outputs[0].setPos(w+4, (h / 2)+1)
		
		return w, h 

class BlockItem_Divergence(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Divergence, self).__init__(parent)
		w = 45.0
		h = 70.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\Divergence.jpg"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		# self.label = QGraphicsTextItem(self.name_block, self)
		# self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Entrada','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida 1','out',str(name_block), self) )
		self.outputs.append(PortItem('Salida 2','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		# pa = menu.addAction('Propiedades')
		dl.triggered.connect(self.DeleteBlock)
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
		# rect = self.label.boundingRect()
		# lw, lh = rect.width(), rect.height()
		# lx = (w - lw) / 2
		# ly = (h - lh) / 2
		# self.label.setPos(lx, ly)
		# Update port positions:
		self.inputs[0].setPos(-2, (h / 2)+1)
		self.outputs[0].setPos(w+2, (h / 4)+3)
		self.outputs[1].setPos(w+2,  h-(h/4))
		
		return w, h 		



class BlockItem_Tank(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Tank, self).__init__(parent)

		w = 195.0
		h = 245.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\_Tank.jpg"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem(self.name_block, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Fluido de entrada','in',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Tank(self.name_block,self.window())
		#pd.exec_()
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
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
		self.inputs[0].setPos(0, h-32)
		self.outputs[0].setPos(w+4, h-32)
		return w, h

	  
class ArrowItem(QGraphicsLineItem):
	def __init__(self):
		super(ArrowItem, self).__init__(None)
		self.setPen(QtGui.QPen(QtCore.Qt.red,2))
		self.setFlag(self.ItemIsSelectable, True)
	def x(self):
		pass

class EditorGraphicsView(QGraphicsView):
	def __init__(self, scene, parent=None):
		QGraphicsView.__init__(self, scene, parent)
	def dragEnterEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			event.accept()
	def dragMoveEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			global namex
			namex = str(event.mimeData().data('component/name'))
			event.accept()
	def dropEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			global name
			global i_ev
			global i_ht 
			global i_vl 
			global i_tk 
			global i_fl
			global i_cnv
			global i_dvg  
			name = str(event.mimeData().data('component/name'))
			if namex==str("Flujo"):
				b1 = BlockItem_Flow(name+str(i_fl))
				b1.setPos(self.mapToScene(event.pos()))
				editor.diagramScene.addItem(b1)
				i_fl=i_fl+1
			elif namex==str("Evaporador"):
				b1 = BlockItem_Evap(name+str(i_ev))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_ev=i_ev+1
			elif namex==str("Calentador"):
				b1 = BlockItem_Heat(name+str(i_ht))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_ht=i_ht+1
			elif namex==str("Tanque"):
				b1 = BlockItem_Tank(name+str(i_tk))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_tk=i_tk+1
			elif namex==str("Convergencia"):
				b1 = BlockItem_Convergence(name+str(i_cnv))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_cnv=i_cnv+1
			elif namex==str("Divergencia"):
				b1 = BlockItem_Divergence(name+str(i_dvg))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_dvg=i_dvg+1
			# elif namex==str(Valvula):
			else:
				b1 = BlockItem_Valve(name+str(i_vl))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_vl=i_vl+1

class LibraryModel(QStandardItemModel):
	def __init__(self, parent=None):
		QStandardItemModel.__init__(self, parent)
	def mimeTypes(self):
		return ['component/name']
	def mimeData(self, idxs):
		mimedata = QMimeData()
		for idx in idxs:
			if idx.isValid():
				txt = self.data(idx, Qt.DisplayRole)
				mimedata.setData('component/name', txt)
		return mimedata

class DiagramScene(QGraphicsScene):
	def __init__(self, parent=None):
		super(DiagramScene, self).__init__(parent)
	def mouseMoveEvent(self, mouseEvent):
		editor.sceneMouseMoveEvent(mouseEvent)
		super(DiagramScene, self).mouseMoveEvent(mouseEvent)
	def mouseReleaseEvent(self, mouseEvent):
		editor.sceneMouseReleaseEvent(mouseEvent)
		super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
	pass

class DiagramEditor(QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		global indicator
		global label_indicator
		global Ts_value
		Vali = Validator()

		self.generalayout = QtGui.QGridLayout(self)
		self.generalayout.setSpacing(0)
		self.generalayout.setContentsMargins(0,0,0,0);

		self.resize(1000, 800)
		self.timer = QtCore.QTimer()
		self.timer.setInterval(500)
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.timeout)
		self.left_click_count = 0

		self.setWindowTitle(_translate("Dialog", "Simulador dinámico del proceso de producción de azúcar", None))

		# Widget layout and child widgets:

		self.horizontalLayoutWidget = QtGui.QWidget(self)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1002, 770))
		
		self.buttonsLayoutWidget=  QtGui.QWidget(self)
		self.buttonsLayoutWidget.setGeometry(QtCore.QRect(0, 30, 1002, 26))

		self.buttonsHorizontalLayout = QtGui.QHBoxLayout(self.buttonsLayoutWidget)
		self.buttonsHorizontalLayout.setGeometry(QtCore.QRect(0, 30,970, 26))

		self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setGeometry(QtCore.QRect(0, 0, 970, 800))
		self.buttonRun = QtGui.QPushButton(self)
		self.buttonRun.setGeometry(QtCore.QRect(940, 9, 24, 24))
		self.buttonRun.setIcon(QtGui.QIcon(dir_script+"\Images\play_icon.png"))
		self.buttonRun.setIconSize(QtCore.QSize(24,24))
		self.buttonRun.clicked.connect(self.run_emulation)
		self.buttonRun.setStyleSheet("border: none")

		self.buttonPause = QtGui.QPushButton(self)
		self.buttonPause.setGeometry(QtCore.QRect(965, 9, 24, 24))
		self.buttonPause.setIcon(QtGui.QIcon(dir_script+"\Images\stop_icon.png"))		
		self.buttonPause.setIconSize(QtCore.QSize(24,24))
		self.buttonPause.clicked.connect(self.stop_emulation)
		self.buttonPause.setStyleSheet("border: none")

		
		
		self.label_Ts=QtGui.QLabel(self)
		self.label_Ts.setGeometry(QtCore.QRect(747, 9, 127, 24))
		self.label_Ts.setText("Tiempo de muestreo (seg):")
		self.label_Ts.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		Ts_value=QtGui.QLineEdit(self)
		Ts_value.setGeometry(QtCore.QRect(876, 11, 33, 21))
		Ts_value.setText("0.5")
		Vali.NumValidator(Ts_value)



		indicator = QtGui.QPushButton(self)
		indicator.setGeometry(QtCore.QRect(15, 9, 24, 24))
		indicator.setIcon(QtGui.QIcon(dir_script+"\Images\led-black.png"))
		indicator.setIconSize(QtCore.QSize(24,24))
		indicator.setStyleSheet("border: none")
		label_indicator=QtGui.QLabel(self)
		label_indicator.setGeometry(QtCore.QRect(45, 9, 105, 24))
		label_indicator.setText(_translate("Dialog","Simulación: --", None))
		
		self.buttonsHorizontalLayout.addWidget(indicator)
		self.buttonsHorizontalLayout.addWidget(label_indicator,15)
		self.buttonsHorizontalLayout.addWidget(self.label_Ts,15)
		self.buttonsHorizontalLayout.addWidget(Ts_value,1)
		self.buttonsHorizontalLayout.addWidget(self.buttonRun)
		self.buttonsHorizontalLayout.addWidget(self.buttonPause)


		self.generalayout.addWidget(self.buttonsLayoutWidget,0,0)
		self.generalayout.addWidget(self.horizontalLayoutWidget,1,0)
		

		# self.libraryBrowserView = QtGui.QListView(self)
		# self.libraryBrowserView.setMovement(QListView.Static)
		# self.libraryBrowserView.setGridSize(QtCore.QSize(200,100))
		# self.libraryBrowserView.setIconSize(QtCore.QSize(60,60))
		self.libraryModel = LibraryModel(self)
		self.libraryModel.setColumnCount(1)
		self.libraryModel.setHeaderData(0, QtCore.Qt.Horizontal, _translate("Dialog", "Panel de selección", None));

		self.libItems = []
		self.iconEvaporator=QIcon(dir_script+"\Images\evapor-icon.png");
		self.iconHeater=QIcon(dir_script+"\Images\heater-icon.png");
		self.iconFlow=QIcon(dir_script+"\Images\_arrow_flow-icon.png");
		self.iconValve=QIcon(dir_script+"\Images\_valve_icon.png");   
		self.iconTank=QIcon(dir_script+"\Images\Tank-icon.png");
		self.icon_divergence=QIcon(dir_script+"\Images\Divergence.jpg")  
		self.icon_convergence=QIcon(dir_script+"\Images\Convergence.jpg")  
		self.EvaporItem=QtGui.QStandardItem(self.iconEvaporator, 'Evaporador');
		self.HeaterItem=QtGui.QStandardItem(self.iconHeater, 'Calentador') ;
		self.Flow=QtGui.QStandardItem(self.iconFlow, 'Flujo') ;
		self.Valve=QtGui.QStandardItem(self.iconValve,_translate("Dialog","Válvula", None)) ;
		self.Tank=QtGui.QStandardItem(self.iconTank, 'Tanque') 
		self.Divergence=QtGui.QStandardItem(self.icon_divergence, 'Divergencia') 
		self.Convergence=QtGui.QStandardItem(self.icon_convergence, 'Convergencia') 
		self.libItems.append(self.EvaporItem)
		self.libItems.append(self.HeaterItem)
		self.libItems.append(self.Valve)
		self.libItems.append(self.Tank)
		self.libItems.append(self.Flow)
		self.libItems.append(self.Divergence)
		self.libItems.append(self.Convergence)
		# for i in self.libItems:
		#    self.libraryModel.appendRow(i)

		####
		self.libraryBrowserView_TREE = QtGui.QTreeView(self)
		self.libraryBrowserView_TREE.setIconSize(QtCore.QSize(60,60))
		self.libraryBrowserView_TREE.setModel(self.libraryModel)
		parent1 = QStandardItem('Equipos')
		parent1.setEditable(0)
		parent1.setSelectable(0)
		parent1.appendRow(self.libItems[0])
		parent1.appendRow(self.libItems[1])
		parent1.appendRow(self.libItems[2])
		parent1.appendRow(self.libItems[3])
		self.libraryModel.appendRow(parent1)
		parent2 = QStandardItem('Entradas de flujo')
		parent2.setEditable(0)
		parent2.setSelectable(0)
		parent2.appendRow(self.libItems[4])
		self.libraryModel.appendRow(parent2)
		parent3 = QStandardItem('Otros')
		parent3.appendRow(self.libItems[5])
		parent3.appendRow(self.libItems[6])
		self.libraryModel.appendRow(parent3)		
		self.libraryBrowserView_TREE.setDragDropMode(self.libraryBrowserView_TREE.DragOnly)
		self.horizontalLayout.addWidget(self.libraryBrowserView_TREE,1)
		####

		#self.libraryBrowserView.setModel(self.libraryModel)
		#self.libraryBrowserView.setViewMode(self.libraryBrowserView.IconMode)
		# self.libraryBrowserView.setDragDropMode(self.libraryBrowserView.DragOnly)

		self.diagramScene = DiagramScene(self)
		self.diagramView = EditorGraphicsView(self.diagramScene, self)
		# self.horizontalLayout.addWidget(self.libraryBrowserView,1)
		self.horizontalLayout.addWidget(self.diagramView,3)

		self.startedConnection = None

	def read_time(self):
		global infile
		infile = open('time_exec.txt', 'r+')
		data=infile.readlines()
		if len(data)>0:
			model_data=data[-1].strip()
			split_model_data=model_data.split("\t")
			time_exec=split_model_data[0]
			model_value=split_model_data[1]
			print(time_exec+"--"+model_value)
			infile.close()
	def run_emulation(self):
		if len(Ts_value.text())>0:
			if float(Ts_value.text())>=0.5 and float(Ts_value.text())<=3.0 : 
				box = QtGui.QMessageBox()
				box.setIcon(QtGui.QMessageBox.Question)
				box.setWindowTitle('Simular')
				box.setText(_translate("MessBox","¿ Esta seguro que desea iniciar la simulación ?\nDebe tener todas las ventanas de los equipos cerradas.", None))
				box.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
				buttonY = box.button(QtGui.QMessageBox.Yes)
				buttonY.setText('Si')
				buttonN = box.button(QtGui.QMessageBox.No)
				buttonN.setText('No')
				box.exec_()
				if  box.clickedButton()==buttonY:
					global timer
					global run_flag
					global Sim_time
					Heater_flag=[]
					FLow_flag=[]
					b_ht=0
					for k, par_data in enumerate(array_connections):
						print par_data[0]+".."+par_data[1]
						if par_data[1][:-1]=="Calentador":
							if k%2==0:
								Heater_flag.append("Ht"+par_data[1][len(par_data[1])-1:])					
							if par_data[0][:-1]=="Flujo":
								if par_data[2]=="Fluido de entrada":
									FLow_flag.append("Fj"+par_data[0][len(par_data[0])-1:])
								else:	
									FLow_flag.append("Fv"+par_data[0][len(par_data[0])-1:])
								b_ht=b_ht+1
					if b_ht==2:
						print "cantidad de entradas bien en calentador"
						print Heater_flag
						print FLow_flag
					else:
						print "faltan entradas a calentador"



					file_heat = open('Blocks_data.txt', 'r+')
					Mjin=103.0
					Bjin=0.15
					Zjin=0.87
					Tjin=77.0
					Pvin=4.738
					data=file_heat.readlines()
					sim_heat_data=[]
					heat_param=[]
					vapor_data=[]
					juice_data=[]
					for i in data:
						info=(i.strip()).split("\t")
						if len(info)>1:
							flag=info[0]
							#print ("Flag "+flag+" "+flag[:2])
							if flag==Heater_flag[0]:
								for k in range(1,len(info)):
									heat_param.append(info[k])
							if flag[:1]=="F":
								for dat in FLow_flag:
									if flag[:2]=="Fv" and flag==dat:
										print "fue vapor "+dat
										for k in range(1,len(info)):
											vapor_data.append(info[k])
									elif flag[:2]=="Fj" and flag==dat:
										print "fue jugo "+dat
										for k in range(1,len(info)):
											juice_data.append(info[k])
					file_heat.close()

					if len(heat_param)>0 and len(vapor_data)>0 and len(juice_data)>0:
						indicator.setIcon(QtGui.QIcon(dir_script+"\Images\led-green.png"))
						label_indicator.setText(_translate("Dialog","Simulación: Corriendo", None))
						sim_heat_data=np.append(heat_param[0:9],juice_data[0:4])
						sim_heat_data=np.append(sim_heat_data,vapor_data[0])
						#print sim_heat_data
						Sim_time=float(Ts_value.text())
						sim=Simulation_heat("_",sim_heat_data,Sim_time)
						# timer = QtCore.QTimer(self)
						# timer.timeout.connect(self.read_time)
						# timer.start(float(sim.time_samp)*1000)
						run_flag=1
					else :
						QtGui.QMessageBox.warning(self, 
						'Advertencia',
						_translate("MessBox","No hay datos suficientes para poder iniciar la simulación.", None), 
						QtGui.QMessageBox.Ok)
			else:
				QtGui.QMessageBox.warning(self, 
				'Advertencia',
				_translate("MessBox", "El tiempo de simulación debe estar entre 0.5 y 3 seg", None), 
				QtGui.QMessageBox.Ok)
		else:
				QtGui.QMessageBox.warning(self, 
				'Advertencia',
				_translate("MessBox", "No ha ingresado un tiempo de simulación", None), 
				QtGui.QMessageBox.Ok)		
	def stop_emulation(self):
		global run_flag
		if run_flag==1:
			box = QtGui.QMessageBox()
			box.setIcon(QtGui.QMessageBox.Question)
			box.setWindowTitle(_translate("MessBox",'Detener', None))
			box.setText(_translate("MessBox","¿ Esta seguro que desea detener la simulación ?", None))
			box.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
			buttonY = box.button(QtGui.QMessageBox.Yes)
			buttonY.setText('Si')
			buttonN = box.button(QtGui.QMessageBox.No)
			buttonN.setText('No')
			box.exec_()
			if  box.clickedButton()==buttonY:
				indicator.setIcon(QtGui.QIcon(dir_script+"\Images\led-red.png"))
				label_indicator.setText(_translate("Dialog","Simulación: Detenida", None))
				outfile = open('time_exec.txt', 'a')
				outfile.write("stop")
				outfile.close()
				# timer.stop()
				run_flag=0
		else:
			QtGui.QMessageBox.warning(self, 
			'Advertencia',
			_translate("MessBox", "No ha iniciado ninguna simulación.", None), 
			QtGui.QMessageBox.Ok)


	def startConnection(self, port):
		global prt1
		global prt2
		global itemname1
		global itemname2
		prt1=""
		prt2=""
		itemname1=""
		itemname2=""
		prt1=str(port.typ)
		itemname1=str(port.name_block)
		self.startedConnection = Connection(port, None)
	def sceneMouseMoveEvent(self, event):
		global pos
		pos = event.scenePos()
		items = self.diagramScene.items(pos)
		for item in items:
			if hasattr(item, 'name'):
				item.setToolTip(item.name)
			# if type(item) is PortItem:
				# #print(item.name)
				# item.setToolTip(item.name)
		if self.startedConnection:
			pos = event.scenePos()
			self.startedConnection.setEndPos(pos)
	def sceneMouseReleaseEvent(self, event):
		global puerto2
		global itemname2
		global array_connections
		# Clear the actual connection:
		pos = event.scenePos()
		items = self.diagramScene.items(pos)
		for item in items:
			if (event.button()==1):
				if hasattr(item, 'name_block'):
					self.left_click_count += 1
					aux=str(item.name_block)
				if not self.timer.isActive():
					self.timer.start()
			if self.left_click_count>=3:
				aux2=re.sub("\d+", "", aux)
				if str(aux2)==str("Valvula"):
					pd = ParameterDialog_Valve(aux,self.window())
				if str(aux2)==str("Flujo"):
					pd = ParameterDialog_Flow(aux,self.window())
				if str(aux2)==str("Evaporador"):
					pd = ParameterDialog_Evaporator(aux,self.window())
				if str(aux2)==str("Calentador"):
					pd = ParameterDialog_Heater(aux,Sim_time,self.window())
				if str(aux2)==str("Tanque"):
					pd = ParameterDialog_Tank(aux,self.window())
		if self.startedConnection:
			for item in items:
				if type(item) is PortItem:
					prt2=str(item.typ)
					itemname2=str(item.name_block)
					if prt2!=prt1 and itemname2!=itemname1:
						self.startedConnection.setToPort(item)
						connections=[itemname1, itemname2,str(item.name)]
						array_connections.append(connections)
						print array_connections
					else:
						self.startedConnection.delete()
			if self.startedConnection.toPort == None:
				self.startedConnection.delete()
			self.startedConnection = None
	def keyPressEvent(self, kevent):
		items = self.diagramScene.items(pos)
		for item in items:
			if item.isSelected()==True:
				key = kevent.key()
				if key == QtCore.Qt.Key_Delete :
					pd = DeleteDialog(self.window())
					pd.exec_()
	def timeout(self):
		self.left_click_count = 0

	def closeEvent(self, event):
		box = QtGui.QMessageBox()
		box.setIcon(QtGui.QMessageBox.Question)
		box.setWindowTitle('Cerrar')
		box.setText(_translate("MessBox","¿ Esta seguro que desea cerrar el simulador ?", None))
		box.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
		buttonY = box.button(QtGui.QMessageBox.Yes)
		buttonY.setText('Si')
		buttonN = box.button(QtGui.QMessageBox.No)
		buttonN.setText('No')
		box.exec_()
		if  box.clickedButton()==buttonY:
			PROCNAME = "python.exe"
			for proc in psutil.process_iter():
				# check whether the process name matches
				if proc.name() == PROCNAME:
					proc.kill()
			if run_flag==1:
				try:
					start_thread()  
				except (KeyboardInterrupt, SystemExit):
					cleanup_stop_thread()
					sys.exit()
			event.accept()
		else:
			event.ignore()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	global editor
	editor = DiagramEditor()
	editor.show()
	app.exec_()