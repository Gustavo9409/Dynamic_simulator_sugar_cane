#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import numpy as np
import psutil

import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignal
#Import blocks
from Evapor_properties import Ui_Dialog as Evap_properties
from Heater_properties import Ui_Dialog as Heat_properties
from Tank_properties import Ui_Dialog as Tank_properties
from Valve_properties import Ui_Dialog as Valve_properties
from Flow_properties import Ui_Dialog as Flow_properties
from PID_properties import Ui_Dialog as PID_properties
#Import simulation
from run_heater_model import Simulation_heat
#Instance Data Base
from Data_base import data_base_instance
#
from Devices_connections import *
global db
db=data_base_instance()
connection_db=db.connect()
db.clear_all()

#

dir_script=str(os.getcwd())

global Heater_juice_in
global Heater_vapor_in
global i_ev
global i_ht
global i_vl
global i_fl
global i_tk
global i_cnv
global i_dvg
global i_pid
global i_tgI
global i_tgO
global l
global run_flag
global Ts_value
global Sim_time
global array_connections
global array_arrows
global Tank_fluid_in
Heater_juice_in=""
Heater_vapor_in=""
Tank_fluid_in=""
Sim_time=0.5
l=0
i_ev=1
i_ht=1
i_vl=1
i_fl=1
i_tk=1
i_dvg=1
i_cnv=1
i_pid=1
i_tgI=1
i_tgO=1
run_flag=0
array_connections=[]
array_arrows=[]

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
		self.arrow = ArrowItem(self.fromPort,self.toPort)
		editor.diagramScene.addItem(self.arrow)
	def setFromPort(self, fromPort):
		self.fromPort = fromPort
		if self.fromPort:
			self.pos1 = fromPort.scenePos()
			self.fromPort.posCallbacks.append(self.setBeginPos)
		self.arrow.port1=self.fromPort
	def setToPort(self, toPort):
		global array_arrows
		self.toPort = toPort
		if self.toPort:
			self.pos2 = toPort.scenePos()
			self.toPort.posCallbacks.append(self.setEndPos)
		self.arrow.port2=self.toPort
		array_arrows.append(self.arrow)
	def setEndPos(self, endpos):
		self.pos2 = endpos
		self.arrow.setLine(QLineF(self.pos1, self.pos2))
		
	def setBeginPos(self, pos1):
		self.pos1 = pos1
		self.arrow.setLine(QLineF(self.pos1, self.pos2))
	def delete(self):
		editor.diagramScene.removeItem(self.arrow)
		# Remove position update callbacks:

class ArrowItem(QGraphicsLineItem):
	def __init__(self,port1,port2):
		super(ArrowItem, self).__init__(None)
		self.setPen(QtGui.QPen(QtCore.Qt.red,3))
		self.setFlag(self.ItemIsSelectable, True)
		self.port1=port1
		self.port2=port2
	def x(self):
		pass
	def contextMenuEvent(self, event):
		menu = QMenu()
		self.type_line1=QIcon(dir_script+"\Images\_type3_arrow.png");
		self.type_line2=QIcon(dir_script+"\Images\_type2_arrow.png");
		self.type_line3=QIcon(dir_script+"\Images\_type1_arrow.png");
		dl = menu.addAction(self.type_line1,'Normal')
		pa = menu.addAction(self.type_line2,'Curvo')
		pa = menu.addAction(self.type_line3,'Recto')
		menu.exec_(event.screenPos())



class ParameterDialog_Evaporator(QDialog):
	def __init__(self,dat,label, parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Evap_properties()
		self.ui.setupUi(dat,label,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Heater(QDialog):
	def __init__(self,dat,time,label,jui_port,vap_port,db, parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = Heat_properties()
		self.ui.setupUi(dat,time,label,jui_port,vap_port,db,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Tank(QDialog):
	def __init__(self,dat,time,label,fluid_port,parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Tank_properties()
		self.ui.setupUi(dat,time,label,fluid_port,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Valve(QDialog):
	def __init__(self,dat,time,item, parent=None):
		self.Resultado=QtGui.QDialog()
		self.ui = Valve_properties()
		self.ui.setupUi(dat,time,item,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Flow(QDialog):
	def __init__(self,dat,time,item,db,parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = Flow_properties()
		self.ui.setupUi(dat,time,item,db,self.Resultado)
		self.Resultado.exec_()

class ParameterDialog_Controller(QDialog):
	def __init__(self,dat,time,item,parent=None):
		self.Resultado=QtGui.QDialog()
		self.Resultado.setWindowModality(QtCore.Qt.WindowModal)
		self.ui = PID_properties()
		self.ui.setupUi(dat,time,item,self.Resultado)
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
		# Delete_item = editor.diagramScene.items(pos)
		Delete_item = editor.diagramScene.selectedItems()
		for item in Delete_item:
			if hasattr(item, 'name_block'):
				aux=str(item.name_block)
				aux2=re.sub("\d+", "", aux)
				aux3=re.sub('([a-zA-Z]+)', "", aux)
				editor.diagramScene.removeItem(item)
				if aux2=="Valvula":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Valvula" or par_data[1][:-1]=="Valvula":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
					if int(aux3)==(i_vl-1):
						i_vl=i_vl-1
				if aux2=="Tanque":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Tanque" or par_data[1][:-1]=="Tanque":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)=="Tanque" or str(arrows.port2.name_block)[:-1]=="Tanque":
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
					if int(aux3)==(i_tk-1):
						i_tk=i_tk-1
				if aux2=="Flujo":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Flujo" or par_data[1][:-1]=="Flujo":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(j)
										array_arrows.pop(j)
										print array_connections
										device_connections.array_connections=array_connections

					if int(aux3)==(i_fl-1):
						i_fl=i_fl-1

					self.delete_flow("Flow_inputs","Fj"+str(aux3))
					self.delete_flow("Flow_inputs","Fv"+str(aux3))
					self.delete_flow("Flow_inputs","Fw"+str(aux3))

				if aux2=="Evaporador":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Evaporador" or par_data[1][:-1]=="Evaporador":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
					if int(aux3)==(i_ev-1):
						i_ev=i_ev-1
				if aux2=="Calentador":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Calentador" or par_data[1][:-1]=="Calentador":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
					if int(aux3)==(i_ht-1):
						i_ht=i_ht-1

					self.delete_device("Heaters","Ht"+str(aux3))

				if aux2=="Divergencia":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Divergencia" or par_data[1][:-1]=="Divergencia":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
					if int(aux3)==(i_dvg-1):
						i_dvg=i_dvg-1
				if aux2=="Convergencia":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="Convergencia" or par_data[1][:-1]=="Convergencia":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
					if int(aux3)==(i_cnv-1):
						i_cnv=i_cnv-1
				if aux2=="PID":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="PID" or par_data[1][:-1]=="PID":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
										device_connections.array_connections=array_connections
					if int(aux3)==(i_cnv-1):
						i_pid=i_pid-1
				if aux2=="TAG (Entrada)":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="TAG (Entrada)" or par_data[1][:-1]=="TAG (Entrada)":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
										device_connections.array_connections=array_connections
					if int(aux3)==(i_cnv-1):
						i_tgI=i_tgI-1
				if aux2=="TAG (Salida)":
					if len(array_connections)>0:
						for k,par_data in enumerate(array_connections):
							if par_data[0][:-1]=="TAG (Salida)" or par_data[1][:-1]=="TAG (Salida)":
								for j,arrows in enumerate(array_arrows):
									if str(arrows.port1.name_block)==aux or str(arrows.port2.name_block)==aux:
										editor.diagramScene.removeItem(arrows)
										array_connections.pop(k)
										array_arrows.pop(j)
										device_connections.array_connections=array_connections
					if int(aux3)==(i_cnv-1):
						i_tgO=i_tgO-1
					
		self.close()
	def NO(self):
		self.close()

	def delete_device(self,table,name_device):
		result=db.read_data(table,"id","Name",name_device)
		if len(result)>0:
			for data in result:
				id_device=data[0]
			if table=="Heaters":
				db.delete_data("Physical_properties_heater","Heaters_id",id_device)
				db.delete_data("Outputs_heater","id_heater",id_device)
				db.delete_data("Heaters","id",id_device)

	def delete_flow(self,table,name_device):
		db.delete_data(table,"Name",name_device)
	

class PortItem(QGraphicsEllipseItem):
	""" Represents a port to a subsystem """
	def __init__(self, name,in_out,typ,block, parent=None):
		QGraphicsEllipseItem.__init__(self, QRectF(-6,-6,8.0,8.0), parent)
		self.setCursor(QCursor(QtCore.Qt.CrossCursor))
		# Properties:
		self.name_block=block
		self.label=block
		self.typ=typ
		self.in_out=in_out

		if self.typ=='juice':
			self.port_color=QColor(215, 125, 0)
			self.setBrush(QBrush(QColor(215, 125, 0)))
		elif self.typ=='vapor':
			self.port_color=Qt.green
			self.setBrush(QBrush(Qt.green))
		elif self.typ=='condensed' or self.typ=='water':
			self.port_color=Qt.blue
			self.setBrush(QBrush(Qt.blue))
		elif self.typ=='electric':
			self.port_color=Qt.gray
			self.setBrush(QBrush(Qt.gray))

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
		w = 179.0
		h = 240.0
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
		self.inputs = []
		self.inputs.append( PortItem('Jugo de entrada','in','juice',str(name_block), self) )
		self.inputs.append( PortItem('Vapor vivo','in','vapor',str(name_block), self) )
		self.outputs = []
		self.outputs.append( PortItem('Jugo de salida','out','juice',str(name_block), self) )
		self.outputs.append( PortItem('Vapor vegetal','out','vapor',str(name_block), self) )
		self.outputs.append( PortItem('Vapor condensado','out','condensed',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Evaporator(self.name_block,self,self.window())
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
		lx = ((w - lw) / 2)
		ly = ((h - lh) / 2)-20
		self.label.setPos(lx, ly)
		# Update port positions:
		
		self.inputs[0].setPos(0, (h-8))
		self.inputs[1].setPos(0, (h / 3)+50)
		self.outputs[0].setPos(w, h-8)
		self.outputs[1].setPos((w/2), 0)
		self.outputs[2].setPos(w, (2*h/3)+5)

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
		w = 165.0
		h = 161.0
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
		self.inputs = []
		self.inputs.append(PortItem('Fluido de entrada','in','juice',str(name_block), self) )
		self.inputs.append(PortItem('Vapor de entrada','in','vapor',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out','juice',str(name_block), self) )
		self.outputs.append(PortItem('Vapor condensado','out','condensed',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Heater(self.name_block,Sim_time,self,Heater_juice_in,Heater_vapor_in,db,self.window())
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
		lx = (w - 40)
		ly = (h -20) 
		self.label.setPos(lx, ly)
		# Update port positions:
		self.inputs[0].setPos(0, h/2 )
		self.inputs[1].setPos((w/2), 0)
		self.outputs[0].setPos(w+2, h/2)
		self.outputs[1].setPos((w/2)+1, h+2)

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
		self.outputs = []
		self.outputs.append(PortItem('Salida','out','none',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,Sim_time,self,db,self.window())
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
		w = 101.0
		h = 75.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\_valve.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem(self.name_block, self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		self.label.setTextInteractionFlags((QtCore.Qt.TextEditable))
		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Fluido de entrada','in','none',str(name_block), self) )
		self.inputs.append(PortItem('Apertura de valvula','in','electric',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out','none',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Valve(self.name_block,Sim_time,self,self.window())
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
		ly = (h-10)
		self.label.setPos(lx+2, ly)
		# Update port positions:
		
		self.inputs[0].setPos(0, h-24)
		self.inputs[1].setPos((w/2)+2, 0)
		self.outputs[0].setPos(w+4, h-24)

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
		Img= QtGui.QImage(dir_script+"\Images\Convergence.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem("", self)
		# self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Entrada 1','in','none',str(name_block), self) )
		self.inputs.append(PortItem('Entrada 2','in','none',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida','out','none',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,db,self.window())
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
		Img= QtGui.QImage(dir_script+"\Images\Divergence.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		# self.label = QGraphicsTextItem(self.name_block, self)
		# self.label.setDefaultTextColor(QtGui.QColor('red'))

		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Entrada','in','none',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida 1','out','none',str(name_block), self) )
		self.outputs.append(PortItem('Salida 2','out','none',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Flow(self.name_block,db,self.window())
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
		self.inputs = []
		self.inputs.append(PortItem('Fluido de entrada','in','juice',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Fluido de salida','out','juice',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Tank(self.name_block,Sim_time,self,Tank_fluid_in,self.window())
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
		lx = (w - lw) / 3
		ly = 2*(h - lh) / 3
		self.label.setPos(lx+13, ly-5)
		# Update port positions:
		self.inputs[0].setPos((w/2)-11, 0)
		self.outputs[0].setPos(w, h-12)
		return w, h


class BlockItem_Controller(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_Controller, self).__init__(parent)

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
		self.inputs = []
		self.inputs.append(PortItem('Entrada realimentada','in','none',str(name_block), self) )
		self.outputs = []
		self.outputs.append(PortItem('Salida controlada','out','electric',str(name_block), self) )
		# Update size:
		self.changeSize(w, h)
	def editParameters(self):
		pd = ParameterDialog_Controller(self.name_block,Sim_time,self,self.window())
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
		self.outputs[0].setPos(w+6, h-32)
		return w, h


class BlockItem_tag_input(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_tag_input, self).__init__(parent)

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
		self.outputs = []
		self.outputs.append(PortItem('Salida','out','none',str(name_block), self) )

		# Update size:
		self.changeSize(w, h)
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		dl.triggered.connect(self.DeleteBlock)
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

		return w, h

class BlockItem_tag_output(QGraphicsRectItem):
	""" 
	Represents a block in the diagram
	Has an x and y and width and height
	width and height can only be adjusted with a tip in the lower right corner.

	- in and output ports
	- parameters
	- description
	"""
	def __init__(self, name_block='Untitled', parent=None):
		super(BlockItem_tag_output, self).__init__(parent)

		w = 48.0
		h = 46.0
		# Properties of the rectangle:
		self.setPen(QtGui.QPen(Qt.NoPen)) 
		Img= QtGui.QImage(dir_script+"\Images\wire_tag_output.png"); 
		self.setBrush(QtGui.QBrush(Img))
		self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
		self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		# Label:
		self.name_block=name_block
		self.label = QGraphicsTextItem("  TAG  ", self)
		self.label.setDefaultTextColor(QtGui.QColor('red'))
		self.label.setTextInteractionFlags((QtCore.Qt.TextEditable))
		# Inputs and outputs of the block:
		self.inputs = []
		self.inputs.append(PortItem('Entrada','in','none',str(name_block), self) )

		# Update size:
		self.changeSize(w, h)
	def DeleteBlock(self):
		pd = DeleteDialog(self.window())
		pd.exec_()
	def contextMenuEvent(self, event):
		menu = QMenu()
		dl = menu.addAction('Eliminar')
		dl.triggered.connect(self.DeleteBlock)
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
		self.label.setPos(w-lw, ly-5)
		# Update port positions:
		self.inputs[0].setPos(0, (h / 2)+1)

		return w, h
	  
class EditorGraphicsView(QGraphicsView): #Edition panel, drop, drag and connect devices
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
			global i_pid 
			global i_tgI
			global i_tgO
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
			elif namex==str("PID"):
				b1 = BlockItem_Controller(name+str(i_pid))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_pid=i_pid+1
			elif namex==str("TAG(Entrada)"):
				b1 = BlockItem_tag_input(name+str(i_tgI))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_tgI=i_tgI+1
			elif namex==str("TAG(Salida)"):
				b1 = BlockItem_tag_output(name+str(i_tgO))
				b1.setPos(self.mapToScene(event.pos()))
				self.scene().addItem(b1)
				i_tgO=i_tgO+1
			# elif namex==str(Valvula):
			else:
				b1 = BlockItem_Valve("Valvula"+str(i_vl))
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
	itemSelected = QtCore.pyqtSignal(QtGui.QGraphicsItem)
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

		self.generalayout = QtGui.QGridLayout(self) #General Panel. Entire GUI
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

		self.buttonsHorizontalLayout = QtGui.QHBoxLayout(self.buttonsLayoutWidget) #Simulation Buttons Panel
		self.buttonsHorizontalLayout.setGeometry(QtCore.QRect(0, 30,970, 26))

		self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget) #Selection Panel. Tools and elements to be added to the edition panel
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
		self.iconEvaporator=QIcon(dir_script+"\Images\Evap_Kstner-icon.png");
		self.iconHeater=QIcon(dir_script+"\Images\Heater_SnT.png");
		self.iconFlow=QIcon(dir_script+"\Images\_flow_none.png");
		self.iconValve=QIcon(dir_script+"\Images\_valve.png");   
		self.iconTank=QIcon(dir_script+"\Images\_Tank.png");
		self.icon_divergence=QIcon(dir_script+"\Images\Divergence.png")  
		self.icon_convergence=QIcon(dir_script+"\Images\Convergence.png")  
		self.iconPID=QIcon(dir_script+"\Images\PID-icon.png");
		self.iconTagIn=QIcon(dir_script+"\Images\wire_tag_input.png");
		self.iconTagOut=QIcon(dir_script+"\Images\wire_tag_output.png");


		self.EvaporItem=QtGui.QStandardItem(self.iconEvaporator, 'Evaporador');
		self.HeaterItem=QtGui.QStandardItem(self.iconHeater, 'Calentador') ;
		self.Flow=QtGui.QStandardItem(self.iconFlow, 'Flujo') ;
		self.Valve=QtGui.QStandardItem(self.iconValve,_translate("Dialog","Válvula", None)) ;
		self.Tank=QtGui.QStandardItem(self.iconTank, 'Tanque') 
		self.Divergence=QtGui.QStandardItem(self.icon_divergence, 'Divergencia') 
		self.Convergence=QtGui.QStandardItem(self.icon_convergence, 'Convergencia') 
		self.PID_controller=QtGui.QStandardItem(self.iconPID, 'PID') 
		self.Tag_input=QtGui.QStandardItem(self.iconTagIn, 'TAG(Entrada)') 
		self.Tag_output=QtGui.QStandardItem(self.iconTagOut, 'TAG(Salida)') 

		self.libItems.append(self.EvaporItem)
		self.libItems.append(self.HeaterItem)
		self.libItems.append(self.Valve)
		self.libItems.append(self.Tank)
		self.libItems.append(self.Flow)
		self.libItems.append(self.Divergence)
		self.libItems.append(self.Convergence)
		self.libItems.append(self.PID_controller)
		self.libItems.append(self.Tag_input)
		self.libItems.append(self.Tag_output)

		for items in self.libItems:
		   items.setEditable(0)

		####
		self.libraryBrowserView_TREE = QtGui.QTreeView(self)
		self.libraryBrowserView_TREE.setIconSize(QtCore.QSize(60,60))
		self.libraryBrowserView_TREE.setModel(self.libraryModel)

		parent1 = QStandardItem('Entradas')
		parent1.setEditable(0)
		parent1.setSelectable(0)
		parent1.appendRow(self.libItems[4])
		self.libraryModel.appendRow(parent1)

		parent2 = QStandardItem('Equipos')
		parent2.setEditable(0)
		parent2.setSelectable(0)
		parent2.appendRow(self.libItems[0])
		parent2.appendRow(self.libItems[1])
		parent2.appendRow(self.libItems[2])
		parent2.appendRow(self.libItems[3])
		self.libraryModel.appendRow(parent2)
		
		parent3 = QStandardItem('Controladores')
		parent3.setEditable(0)
		parent3.setSelectable(0)
		parent3.appendRow(self.libItems[7])
		self.libraryModel.appendRow(parent3)	

		parent4 = QStandardItem('Conexiones')
		parent4.setEditable(0)
		parent4.setSelectable(0)
		parent4.appendRow(self.libItems[5])
		parent4.appendRow(self.libItems[6])
		parent4.appendRow(self.libItems[8])
		parent4.appendRow(self.libItems[9])
		self.libraryModel.appendRow(parent4)	



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
		global Heater_juice_in
		global Heater_vapor_in

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
								if par_data[3]=="Fluido de entrada":
									FLow_flag.append("Fj"+par_data[0][len(par_data[0])-1:])
								else:	
									FLow_flag.append("Fv"+par_data[0][len(par_data[0])-1:])
								b_ht=b_ht+1
						elif par_data[1][:-1]=="Tanque":
							Tank_flag.append("Tk"+par_data[1][len(par_data[1])-1:])
							if par_data[0][:-1]=="Flujo":
								if par_data[3]=="Fluido de entrada":
									FLow_flag.append("Fj"+par_data[0][len(par_data[0])-1:])
									
					if b_ht==2:
						print "cantidad de entradas bien en calentador"
						print Heater_flag
						print FLow_flag
					else:
						print "faltan entradas a calentador"

					heat_param2=[]
					result=db.read_data("Heaters","id,Tjout_init","Name",Heater_flag[0])
					if len(result)>0:
						for data in result:
							id_heater=data[0]
							Tjout_ini=data[1]
						print (Tjout_ini)
						fields="Pipe_x_Step,N_steps,Ext_pipe_diameter,Pipe_lenght,Pipe_thickness,Pipe_rough,Scalling_coeff,Operation_time"
						result=db.read_data("Physical_properties_heater",fields,"Heaters_id",id_heater)
						for data in result:
							for values in data:
								heat_param2.append(float(values))
						heat_param2.append(float(Tjout_ini))

					juice_data2=[]
					vapor_data2=[]
					for flag in FLow_flag:
						fields="_Type,Flow,Temperature,Brix,Purity,Insoluble_solids,pH,Pressure,Saturated_vapor"
						result=db.read_data("Flow_inputs",fields,"Name",flag)
						if len(result)>0:
							for data in result:
								for i,values in enumerate(data):
									if str(data[0])=="Juice":
										if i>0:
											juice_data2.append(str(values))
									elif str(data[0])=="Vapor":
										if i>0:
											vapor_data2.append(str(values))
					print "#-#-#-"
					print vapor_data2
					print juice_data2
					print "#-#-#-"

					file_heat = open('Blocks_data.txt', 'r+')
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
										Heater_vapor_in=dat
										for k in range(1,len(info)):
											vapor_data.append(info[k])
									elif flag[:2]=="Fj" and flag==dat:
										print "fue jugo "+dat
										Heater_juice_in=dat
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
						sim=Simulation_heat("_",sim_heat_data,Sim_time,db)
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
				db.insert_data("TIME_EXEC","TIME",["stop"])
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
		global port_item1
		prt1=""
		prt2=""
		itemname1=""
		itemname2=""
		prt1=str(port.in_out)
		port_item1=port
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
					pd = ParameterDialog_Valve(aux,Sim_time,item,self.window())
				if str(aux2)==str("Flujo"):
					pd = ParameterDialog_Flow(aux,Sim_time,item,db,self.window())
				if str(aux2)==str("Evaporador"):
					pd = ParameterDialog_Evaporator(aux,item,self.window())
				if str(aux2)==str("Calentador"):	
					pd = ParameterDialog_Heater(aux,Sim_time,item,Heater_juice_in,Heater_vapor_in,db,self.window())
				if str(aux2)==str("Tanque"):
					pd = ParameterDialog_Tank(aux,Sim_time,item,Tank_fluid_in,self.window())
				if str(aux2)==str("PID"):
					pd = ParameterDialog_Controller(aux,Sim_time,item,self.window())
		if self.startedConnection:
			for item in items:
				if type(item) is PortItem:
					prt2=str(item.in_out)
					port_item2=item
					itemname2=str(item.name_block)
					if prt2!=prt1 and itemname2!=itemname1:
						if prt1=="out" and prt2=='in':
							self.startedConnection.setToPort(item)
							connections=[itemname1, itemname2,str(port_item1.name),str(port_item2.name)]
							array_connections.append(connections)
							device_connections.array_connections=array_connections
														
							if port_item1.typ!="none" and port_item2.typ=="none":
								self.startedConnection.arrow.setPen(QtGui.QPen(port_item1.port_color,3))
								if port_item1.typ=="juice":
									port_item2.setBrush(QBrush(QColor(215, 125, 0)))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QColor(215, 125, 0),3))
								elif port_item1.typ=="vapor":
									port_item2.setBrush(QBrush(Qt.green))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QtCore.Qt.green,3))
								elif port_item1.typ=="condensed" or port_item1.typ=="water":
									port_item2.setBrush(QBrush(Qt.blue))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QtCore.Qt.blue,3))
								elif port_item1.typ=="electric":
									port_item2.setBrush(QBrush(Qt.gray))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QtCore.Qt.gray,3))
							
							elif port_item2.typ!="none" and port_item1.typ=="none":
								self.startedConnection.arrow.setPen(QtGui.QPen(port_item2.port_color,3))
								if port_item2.typ=="juice":
									port_item1.setBrush(QBrush(QColor(215, 125, 0)))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QColor(215, 125, 0),3))
								elif port_item2.typ=="vapor":
									port_item1.setBrush(QBrush(Qt.green))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QtCore.Qt.green,3))
								elif port_item2.typ=="condensed" or port_item2.typ=="water":
									port_item1.setBrush(QBrush(Qt.blue))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QtCore.Qt.blue,3))
								elif port_item2.typ=="electric":
									port_item1.setBrush(QBrush(Qt.gray))
									# self.startedConnection.arrow.setPen(QtGui.QPen(QtCore.Qt.gray,3))

							elif port_item2.typ!="none" and port_item1.typ!="none":
								self.startedConnection.arrow.setPen(QtGui.QPen(port_item1.port_color,3))

							print array_connections
						elif prt1=="in" and prt2=='out':
							self.startedConnection.setToPort(item)
							connections=[itemname2,itemname1,str(port_item2.name),str(port_item1.name)]
							array_connections.append(connections)
							device_connections.array_connections=array_connections

							if port_item2.typ!="none" and port_item1.typ=="none":
								self.startedConnection.arrow.setPen(QtGui.QPen(port_item2.port_color,3))
								if port_item2.typ=="juice":
									port_item1.setBrush(QBrush(QColor(215, 125, 0)))
								elif port_item2.typ=="vapor":
									port_item1.setBrush(QBrush(Qt.green))
								elif port_item2.typ=="condensed" or port_item1.typ=="water":
									port_item1.setBrush(QBrush(Qt.blue))
								elif port_item2.typ=="electric":
									port_item1.setBrush(QBrush(Qt.gray))

							elif port_item1.typ!="none" and port_item2.typ=="none":
								self.startedConnection.arrow.setPen(QtGui.QPen(port_item1.port_color,3))
								if port_item1.typ=="juice":
									port_item2.setBrush(QBrush(QColor(215, 125, 0)))
								elif port_item1.typ=="vapor":
									port_item2.setBrush(QBrush(Qt.green))
								elif port_item1.typ=="condensed" or port_item1.typ=="water":
									port_item2.setBrush(QBrush(Qt.blue))
								elif port_item1.typ=="electric":
									port_item2.setBrush(QBrush(Qt.gray))

							elif port_item1.typ!="none" and port_item2.typ!="none":
							 	self.startedConnection.arrow.setPen(QtGui.QPen(port_item2.port_color,3))

							print array_connections
					# else:
						#self.startedConnection.delete()
			if self.startedConnection.toPort == None:
				self.startedConnection.delete()
			self.startedConnection = None
	def keyPressEvent(self, kevent):
		#items = self.diagramScene.items(pos)
		items = self.diagramScene.selectedItems()
		for item in items:
			if item.isSelected()==True:
				key = kevent.key()
				if key == QtCore.Qt.Key_Delete :
					if hasattr(item, 'port1'): ##If is an ArrowItem()
						editor.diagramScene.removeItem(item)
						for j,arrows in enumerate(array_arrows):
							if arrows==item:
								array_arrows.pop(j)
						for k, par_data in enumerate(array_connections):
							if ((str(par_data[0])==str(item.port1.name_block) and str(par_data[1])==str(item.port2.name_block))
								or (str(par_data[0])==str(item.port2.name_block) and str(par_data[1])==str(item.port1.name_block))):
								array_connections.pop(k)
					else: ## If is a BlockItem()
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