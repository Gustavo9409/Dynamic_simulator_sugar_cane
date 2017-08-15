#!/usr/bin/python
# -*- coding: utf-8 -*-

# Installed Libs
import sys
import os
import re
import numpy as np
import psutil
import unicodedata

import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from collections import defaultdict

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignal

# Local Libs
from information_window import Ui_Dialog as information_window

from flow_symbol import BlockItem_Flow, ParameterDialog_Flow
from evaporator_symbol import BlockItem_Evap, ParameterDialog_Evaporator
from heater_symbol import BlockItem_Heat, ParameterDialog_Heater
from valve_symbol import BlockItem_Valve, ParameterDialog_Valve
from tank_symbol import BlockItem_Tank, ParameterDialog_Tank
from controller_symbol import BlockItem_Controller, ParameterDialog_Controller
from convergence_symbol import BlockItem_Convergence
from divergence_symbol import BlockItem_Divergence
from tag_input_symbol import BlockItem_tag_input
from tag_output_symbol import BlockItem_tag_output
from centrifuge_symbol import BlockItem_Centrifuge
from clarifier_symbol import BlockItem_Clarifier
from mel_clarifier_symbol import BlockItem_Mel_Clarifier
from condenser_symbol import BlockItem_Condenser
from cristalizer_symbol import BlockItem_Cristalizer
from electric_motor_symbol import BlockItem_Electric_Motor
from flash_tank_symbol import BlockItem_Flash_Tank
from mill_symbol import BlockItem_Mill
from donnelly_symbol import BlockItem_Donnelly
from mud_filter_symbol import BlockItem_Mud_Filter
from pump_symbol import BlockItem_Pump
from generator_symbol import BlockItem_Generator
from turbine_symbol import BlockItem_Turbine

from run_simulation import Simulation
from data_base import data_base_instance
from global_data import *
from import_export import OpenFile, SaveFile

#global values
global l
global dir_script
global run_flag
l=0
run_flag=0
dir_script=str(os.getcwd())

## Translate to utf format
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


## Class number validation
class Validator(object):
	def num_validator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,3,2,LineEdit))

## for connection items
class Connection:
	def __init__(self, fromPort, toPort,edit):
		self.editor=edit
		self.fromPort = fromPort
		self.type_fromPort=self.fromPort.in_out
		self.from_port_pos=self.fromPort.block_pos
		self.posi = None
		self.posf = None

		if fromPort:
			self.posi = fromPort.scenePos()
			fromPort.posCallbacks.append(self.setBeginPos)
		self.toPort = toPort

		# Create arrow item:
		self.arrow = ArrowItem(self.fromPort,self.toPort,self.editor)
		self.arrow2 = ArrowItem(self.fromPort,self.toPort,self.editor)
		self.arrow3 = ArrowItem(self.fromPort,self.toPort,self.editor)
		self.arrow4= ArrowItem(self.fromPort,self.toPort,self.editor)
		self.arrow5= ArrowItem(self.fromPort,self.toPort,self.editor)
		
		# Add arrow items to edition panel
		self.editor.diagramScene.addItem(self.arrow)
		self.editor.diagramScene.addItem(self.arrow2)
		self.editor.diagramScene.addItem(self.arrow3)
		self.editor.diagramScene.addItem(self.arrow4)
		self.editor.diagramScene.addItem(self.arrow5)
		
	def setFromPort(self, fromPort):
		self.fromPort = fromPort

		if self.fromPort:
			self.posi = fromPort.scenePos()
			self.fromPort.posCallbacks.append(self.setBeginPos)
		self.arrow.port1=self.fromPort
		
	def setToPort(self, toPort):
		
		self.toPort = toPort
		self.type_toPort=self.toPort.in_out
		if self.toPort:
			self.posf = toPort.scenePos()
			self.toPort.posCallbacks.append(self.setEndPos)
		self.arrow2.port2=self.toPort
		self.to_port_pos=self.toPort.block_pos
		# self.arrow3.port2=self.toPort
		self.arrows=[self.arrow,self.arrow2,self.arrow3,self.arrow4,self.arrow5]
		self.editor.array_arrows.append(self.arrows)
	
	def setEndPos(self, endpos):
		
		self.posf=endpos

	## Initial port is an input
	##When the initial port is in the lateral side
		if self.type_fromPort=="in" and self.from_port_pos[1]>-10 and self.from_port_pos[1]<10:
			# Input right to the output
			if float(self.posi.x())>float(self.posf.x()):
				#Default final port in lateral side
				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[1])-20),self.posi.y())
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y())
				self.pos4=QtCore.QPointF(self.pos2.x(),self.pos3.y())
				
				#If final port is know
				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos4=QtCore.QPointF(self.pos2.x()+(self.to_port_pos[1]+20),self.pos2.y())
						self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())
						
						if self.pos4.x()>self.pos1.x() and self.posf.y()>self.posi.y():
							self.pos4=self.pos2
							self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())
						
						if self.pos4.x()>self.pos1.x() and self.posf.y()<self.posi.y():
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()+(self.from_port_pos[3]+10))

					#if final port is in the low side
					if self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()+20)
						self.pos4=QtCore.QPointF(self.pos2.x()+(self.to_port_pos[1]+30),self.pos2.y())
						self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())

						if self.pos4.x()>self.pos1.x() and self.posf.y()<self.posi.y():
							self.pos4=self.pos2
							self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())
						if self.pos4.x()>self.pos1.x() and self.posf.y()>self.posi.y():
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()-((self.from_port_pos[2]-self.from_port_pos[3])+10))


				if self.pos4.x()>self.pos3.x():
					self.pos1=QtCore.QPointF(self.pos2.x(),self.posi.y())
					self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y())
					if self.pos3.x()>=self.posf.x():
						self.pos1=self.posi
						self.pos2=QtCore.QPointF(self.posi.x(),self.posf.y())
						self.pos3=self.posi
						self.pos4=self.posi


				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos4))
				self.arrow5.setLine(QLineF(self.pos1, self.pos3))

			#Input left to the output
			elif float(self.posi.x())<float(self.posf.x()):
				#Default final port in lateral side
				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[1])-20),self.posi.y())
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				if self.posf.y()>self.posi.y():
					
					self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()+((self.from_port_pos[2]-self.from_port_pos[3])+20))
				elif self.posf.y()<self.posi.y():
					self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()-(self.from_port_pos[3]+20))
				self.pos4=QtCore.QPointF(self.pos2.x(),self.pos3.y())

				#If final port is know
				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos4=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
						self.pos3=QtCore.QPointF(self.pos1.x(),self.pos4.y())

						if self.pos4.x()>self.pos1.x() and self.posf.y()>self.posi.y():
							self.pos4=self.pos2
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos4.y())

						if self.pos4.x()<self.pos3.x():
							self.pos4=QtCore.QPointF(self.pos3.x(),self.pos4.y())

						# if self.pos4.x()>self.pos1.x() and self.posf.y()<self.posi.y():
						# 	self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()+(self.from_port_pos[3]+30))
						

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos4))
				self.arrow5.setLine(QLineF(self.pos1, self.pos3))
	##When the initial port is in the hight side
		elif self.type_fromPort=="in" and self.from_port_pos[3]>-10 and self.from_port_pos[3]< 10:
			# print("YES2")
			if float(self.posi.x())>float(self.posf.x()):
				
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				# if self.toPort is None:
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				# else:
				# 	self.pos2=QtCore.QPointF(self.posf.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()-20,self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
				
				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos2.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.pos2.y())
						self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
						if self.pos4.x()>self.pos1.x():
							self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
							self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
					#if final port is in the right side or final port is in the low side
					elif (self.to_port_pos[1]>self.to_port_pos[0]-10 and self.to_port_pos[1]< self.to_port_pos[0]+10) or (self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10):
						self.pos2=QtCore.QPointF(self.posf.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.posf.y())
						self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
						if self.pos2.x()>self.pos4.x():
							self.pos4=QtCore.QPointF(self.pos2.x(),self.pos1.y())
				
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				# if self.toPort is None:
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				# else:
				# 	self.pos2=QtCore.QPointF(self.posf.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()+20,self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())

				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos2.x()-((self.to_port_pos[1])+20),self.pos2.y())
						self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
					#if final port is in the low side
					elif (self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10):
						self.pos2=QtCore.QPointF(self.posf.x()-((self.to_port_pos[1])+20),self.posf.y())
						self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
						if self.pos2.x()<self.pos4.x():
							self.pos4=QtCore.QPointF(self.pos2.x(),self.pos1.y())

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

	## Initial port is an output
	##When the initial port is in the lateral side
		if self.type_fromPort=="out" and self.from_port_pos[1]>self.from_port_pos[0]-10 and self.from_port_pos[1]<self.from_port_pos[0]+10:
			if float(self.posi.x())>float(self.posf.x()):

				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.posi.y())
				if self.toPort is not None:
					self.pos2=QtCore.QPointF(self.posf.x()-(self.to_port_pos[1]+20),self.posf.y())
				else:
					self.pos2=QtCore.QPointF(self.posf.x()-20,self.posf.y())
				self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()-(self.from_port_pos[3]))-10)

				#If final port is know
				if self.toPort is not None:
					#if final port is in the low side
					if self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()+20)
						self.pos3=QtCore.QPointF(self.pos1.x(),self.pos2.y())
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos1.x(),self.pos2.y())
					else:
						if float(self.posi.y())>float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()-(self.from_port_pos[3]))-10)
						elif float(self.posi.y())<float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()+(self.from_port_pos[2]-self.from_port_pos[3]))+10)
				else:
					if float(self.posi.y())>float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()-(self.from_port_pos[3]))-10)
					elif float(self.posi.y())<float(self.posf.y()):
						self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()+(self.from_port_pos[2]-self.from_port_pos[3]))+10)
				self.pos4=QtCore.QPointF(self.pos2.x(),self.pos3.y())


				
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos4))
				self.arrow5.setLine(QLineF(self.pos1, self.pos3))

			elif float(self.posi.x())<float(self.posf.x()):

				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.posi.y())
				if self.toPort is not None:
					self.pos2=QtCore.QPointF(self.posf.x()-(self.to_port_pos[1]+20),self.posf.y())
				else:
					self.pos2=QtCore.QPointF(self.posf.x()-20,self.posf.y())

				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos2.y())
				self.pos4=QtCore.QPointF(self.pos1.x(),self.pos3.y())

				if self.toPort is not None and self.pos4.x()<self.pos3.x():
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-10)
						if float(self.posi.y())>float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos2.y()))
						elif float(self.posi.y())<float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos2.y())

						self.pos4=QtCore.QPointF(self.pos1.x(),self.pos3.y())

				if self.pos4.x()>self.pos3.x():
					self.pos2=QtCore.QPointF(self.pos4.x(),self.posf.y())
					self.pos3=self.pos2
					if self.pos3.x()>=self.posf.x():

						self.pos1=QtCore.QPointF(self.posf.x(),self.posi.y())
						self.pos2=self.posf
						self.pos3=self.posf
						self.pos4=self.pos1

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))
	##When the initial port is in the low side

		elif self.type_fromPort=="out" and self.from_port_pos[3]>self.from_port_pos[2]-10 and self.from_port_pos[3]<self.from_port_pos[2]+10:
			
			if float(self.posi.x())>float(self.posf.x()):
				
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()+10)
				self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-10)
				if self.toPort is None:
					self.pos3=QtCore.QPointF(self.pos2.x()-20,self.pos2.y())
				else:
					self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
				self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()+10)
				self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-10)
				if self.toPort is None:
					self.pos3=QtCore.QPointF(self.pos2.x()-20,self.pos2.y())
				else:
					self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
				self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))
	##When the initial port is in the hight side
		elif self.type_fromPort=="out" and self.from_port_pos[3]>-10 and self.from_port_pos[3]< 10:
			# print("YES2")
			if float(self.posi.x())>float(self.posf.x()):
				
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				self.pos2=QtCore.QPointF(self.posf.x()-20,self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()-20,self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
				
				if self.toPort is not None:
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos2.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.pos2.y())
						self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
						if self.pos4.x()>self.pos1.x():
							self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
							self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
				
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				if self.toPort is None:
					self.pos2=QtCore.QPointF(self.posf.x()-(20),self.posf.y())
				else:
					self.pos2=QtCore.QPointF(self.posf.x()-(self.to_port_pos[1]+20),self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos4.y())

				if self.toPort is not None:
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						if self.pos2.y()<self.pos1.y():
							self.pos4=QtCore.QPointF(self.pos1.x(),self.pos2.y())
							self.pos3=QtCore.QPointF(self.pos2.x(),self.pos4.y())
						else:
							self.pos4=QtCore.QPointF(self.pos1.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.pos1.y())
							self.pos3=QtCore.QPointF(self.pos2.x(),self.pos4.y())


				if self.pos2.x()<self.pos4.x() :
					if self.posi.y()<self.posf.y():
						self.pos4=QtCore.QPointF(self.pos1.x()-(self.from_port_pos[1]+20),self.pos1.y())
						self.pos3=QtCore.QPointF(self.pos4.x(),self.pos4.y())
						self.pos2=QtCore.QPointF(self.pos4.x(),self.posf.y())
					elif self.posi.y()>self.posf.y():
						self.pos2=QtCore.QPointF(self.posi.x(),self.posf.y())
						self.pos4=self.pos2
						self.pos3=self.pos2

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))
	
	def setBeginPos(self, pos1):
		self.posi = pos1

	## Initial port is an input
	##When the initial port is in the lateral side
		if self.type_fromPort=="in" and self.from_port_pos[1]>-10 and self.from_port_pos[1]<10:
			# Input right to the output
			if float(self.posi.x())>float(self.posf.x()):
				#Default final port in lateral side
				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[1])-20),self.posi.y())
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y())
				self.pos4=QtCore.QPointF(self.pos2.x(),self.pos3.y())
				
				#If final port is know
				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos4=QtCore.QPointF(self.pos2.x()+(self.to_port_pos[1]+20),self.pos2.y())
						self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())
						
						if self.pos4.x()>self.pos1.x() and self.posf.y()>self.posi.y():
							self.pos4=self.pos2
							self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())
						
						if self.pos4.x()>self.pos1.x() and self.posf.y()<self.posi.y():
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()+(self.from_port_pos[3]+10))

					#if final port is in the low side
					if self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()+20)
						self.pos4=QtCore.QPointF(self.pos2.x()+(self.to_port_pos[1]+30),self.pos2.y())
						self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())

						if self.pos4.x()>self.pos1.x() and self.posf.y()<self.posi.y():
							self.pos4=self.pos2
							self.pos3=QtCore.QPointF(self.pos4.x(),self.pos1.y())
						if self.pos4.x()>self.pos1.x() and self.posf.y()>self.posi.y():
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()-((self.from_port_pos[2]-self.from_port_pos[3])+10))


				if self.pos4.x()>self.pos3.x():
					self.pos1=QtCore.QPointF(self.pos2.x(),self.posi.y())
					self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y())
					if self.pos3.x()>=self.posf.x():
						self.pos1=self.posi
						self.pos2=QtCore.QPointF(self.posi.x(),self.posf.y())
						self.pos3=self.posi
						self.pos4=self.posi


				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos4))
				self.arrow5.setLine(QLineF(self.pos1, self.pos3))

			#Input left to the output
			elif float(self.posi.x())<float(self.posf.x()):
				#Default final port in lateral side
				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[1])-20),self.posi.y())
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				if self.posf.y()>self.posi.y():
					
					self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()+((self.from_port_pos[2]-self.from_port_pos[3])+20))
				elif self.posf.y()<self.posi.y():
					self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()-(self.from_port_pos[3]+20))
				self.pos4=QtCore.QPointF(self.pos2.x(),self.pos3.y())

				#If final port is know
				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos4=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
						self.pos3=QtCore.QPointF(self.pos1.x(),self.pos4.y())

						if self.pos4.x()>self.pos1.x() and self.posf.y()>self.posi.y():
							self.pos4=self.pos2
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos4.y())

						if self.pos4.x()<self.pos3.x():
							self.pos4=QtCore.QPointF(self.pos3.x(),self.pos4.y())

						# if self.pos4.x()>self.pos1.x() and self.posf.y()<self.posi.y():
						# 	self.pos3=QtCore.QPointF(self.pos1.x(),self.pos1.y()+(self.from_port_pos[3]+30))
						

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos4))
				self.arrow5.setLine(QLineF(self.pos1, self.pos3))
	##When the initial port is in the hight side
		elif self.type_fromPort=="in" and self.from_port_pos[3]>-10 and self.from_port_pos[3]< 10:
			# print("YES2")
			if float(self.posi.x())>float(self.posf.x()):
				
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				# if self.toPort is None:
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				# else:
				# 	self.pos2=QtCore.QPointF(self.posf.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()-20,self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
				
				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos2.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.pos2.y())
						self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
						if self.pos4.x()>self.pos1.x():
							self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
							self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
					#if final port is in the right side or final port is in the low side
					elif (self.to_port_pos[1]>self.to_port_pos[0]-10 and self.to_port_pos[1]< self.to_port_pos[0]+10) or (self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10):
						self.pos2=QtCore.QPointF(self.posf.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.posf.y())
						self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
						if self.pos2.x()>self.pos4.x():
							self.pos4=QtCore.QPointF(self.pos2.x(),self.pos1.y())
				
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				# if self.toPort is None:
				self.pos2=QtCore.QPointF(self.posf.x()+20,self.posf.y())
				# else:
				# 	self.pos2=QtCore.QPointF(self.posf.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()+20,self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())

				if self.toPort is not None:
					#if final port is in the hight side
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos2.x()-((self.to_port_pos[1])+20),self.pos2.y())
						self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
					#if final port is in the low side
					elif (self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10):
						self.pos2=QtCore.QPointF(self.posf.x()-((self.to_port_pos[1])+20),self.posf.y())
						self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
						if self.pos2.x()<self.pos4.x():
							self.pos4=QtCore.QPointF(self.pos2.x(),self.pos1.y())

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

	## Initial port is an output
	##When the initial port is in the lateral side
		if self.type_fromPort=="out" and self.from_port_pos[1]>self.from_port_pos[0]-10 and self.from_port_pos[1]<self.from_port_pos[0]+10:
			if float(self.posi.x())>float(self.posf.x()):

				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.posi.y())
				if self.toPort is not None:
					self.pos2=QtCore.QPointF(self.posf.x()-(self.to_port_pos[1]+20),self.posf.y())
				else:
					self.pos2=QtCore.QPointF(self.posf.x()-20,self.posf.y())
				self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()-(self.from_port_pos[3]))-10)

				#If final port is know
				if self.toPort is not None:
					#if final port is in the low side
					if self.to_port_pos[3]>self.to_port_pos[2]-10 and self.to_port_pos[3]<self.to_port_pos[2]+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()+20)
						self.pos3=QtCore.QPointF(self.pos1.x(),self.pos2.y())
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos1.x(),self.pos2.y())
					else:
						if float(self.posi.y())>float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()-(self.from_port_pos[3]))-10)
						elif float(self.posi.y())<float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()+(self.from_port_pos[2]-self.from_port_pos[3]))+10)
				else:
					if float(self.posi.y())>float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()-(self.from_port_pos[3]))-10)
					elif float(self.posi.y())<float(self.posf.y()):
						self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos1.y()+(self.from_port_pos[2]-self.from_port_pos[3]))+10)
				self.pos4=QtCore.QPointF(self.pos2.x(),self.pos3.y())


				
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos4))
				self.arrow5.setLine(QLineF(self.pos1, self.pos3))

			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.posi.y())
				self.pos2=QtCore.QPointF(self.posf.x()-20,self.posf.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos2.y())
				self.pos4=QtCore.QPointF(self.pos1.x(),self.pos3.y())

				if self.toPort is not None and self.pos4.x()<self.pos3.x():
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]<+10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-10)
						if float(self.posi.y())>float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),(self.pos2.y()))
						elif float(self.posi.y())<float(self.posf.y()):
							self.pos3=QtCore.QPointF(self.pos1.x(),self.pos2.y())

						self.pos4=QtCore.QPointF(self.pos1.x(),self.pos3.y())

				if self.pos4.x()>self.pos3.x():
					self.pos2=QtCore.QPointF(self.pos4.x(),self.posf.y())
					self.pos3=self.pos2
					if self.pos3.x()>=self.posf.x():
						self.pos1=QtCore.QPointF(self.posf.x(),self.posi.y())
						self.pos2=self.posf
						self.pos3=self.posf
						self.pos4=self.pos1
					
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))
	##When the initial port is in the low side
		elif self.type_fromPort=="out" and self.from_port_pos[3]>self.from_port_pos[2]-10 and self.from_port_pos[3]<self.from_port_pos[2]+10:
			if float(self.posi.x())>float(self.posf.x()):
				
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()+10)
				self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-10)
				if self.toPort is not None:
					self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
				else:
					self.pos3=QtCore.QPointF(self.pos2.x()-(20),self.pos2.y())
				self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))
			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()+10)
				self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-10)
				if self.toPort is None:
					self.pos3=QtCore.QPointF(self.pos2.x()-20,self.pos2.y())
				else:
					self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
				self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())

				if self.pos1.x()>self.pos4.x():
					self.pos4=self.pos1
					self.pos3=QtCore.QPointF(self.pos4.x(),self.pos2.y())
					if self.pos3.x()>=self.posf.x():
						self.pos3=self.pos2

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))
	##When the initial port is in the hight side
		elif self.type_fromPort=="out" and self.from_port_pos[3]>-10 and self.from_port_pos[3]< 10:
			# print("YES2")
			if float(self.posi.x())>float(self.posf.x()):
				
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				self.pos2=QtCore.QPointF(self.posf.x()-20,self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()-20,self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos1.y())
				
				if self.toPort is not None:
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						self.pos3=QtCore.QPointF(self.pos2.x()+((self.to_port_pos[0]-self.to_port_pos[1])+20),self.pos2.y())
						self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
						if self.pos4.x()>self.pos1.x():
							self.pos3=QtCore.QPointF(self.pos2.x()-(self.to_port_pos[1]+20),self.pos2.y())
							self.pos4=QtCore.QPointF(self.pos3.x(),self.pos1.y())
				
				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

			elif float(self.posi.x())<float(self.posf.x()):
				self.pos1=QtCore.QPointF(self.posi.x(),self.posi.y()-10)
				if self.toPort is None:
					self.pos2=QtCore.QPointF(self.posf.x()-(20),self.posf.y())
				else:
					self.pos2=QtCore.QPointF(self.posf.x()-(self.to_port_pos[1]+20),self.posf.y())
				self.pos4=QtCore.QPointF(self.pos1.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.pos1.y())
				self.pos3=QtCore.QPointF(self.pos2.x(),self.pos4.y())

				if self.toPort is not None:
					if self.to_port_pos[3]>-10 and self.to_port_pos[3]< 10:
						self.pos2=QtCore.QPointF(self.posf.x(),self.posf.y()-20)
						if self.pos2.y()<self.pos1.y():
							self.pos4=QtCore.QPointF(self.pos1.x(),self.pos2.y())
							self.pos3=QtCore.QPointF(self.pos2.x(),self.pos4.y())
						else:
							self.pos4=QtCore.QPointF(self.pos1.x()+((self.from_port_pos[0]-self.from_port_pos[1])+20),self.pos1.y())
							self.pos3=QtCore.QPointF(self.pos2.x(),self.pos4.y())


				if self.pos2.x()<self.pos4.x() :
					if self.posi.y()<self.posf.y():
						self.pos4=QtCore.QPointF(self.pos1.x()-(self.from_port_pos[1]+20),self.pos1.y())
						self.pos3=QtCore.QPointF(self.pos4.x(),self.pos4.y())
						self.pos2=QtCore.QPointF(self.pos4.x(),self.posf.y())
					elif self.posi.y()>self.posf.y():
						self.pos2=QtCore.QPointF(self.posi.x(),self.posf.y())
						self.pos4=self.pos2
						self.pos3=self.pos2

				self.arrow.setLine(QLineF(self.posi, self.pos1))
				self.arrow2.setLine(QLineF(self.pos2, self.posf))
				self.arrow3.setLine(QLineF(self.pos3, self.pos4))
				self.arrow4.setLine(QLineF(self.pos2, self.pos3))
				self.arrow5.setLine(QLineF(self.pos1, self.pos4))

	
	def delete(self):
		if self.arrow.scene()==self.editor.diagramScene:
			self.editor.diagramScene.removeItem(self.arrow)
			self.editor.diagramScene.removeItem(self.arrow2)
			self.editor.diagramScene.removeItem(self.arrow3)
			self.editor.diagramScene.removeItem(self.arrow4)
			self.editor.diagramScene.removeItem(self.arrow5)

		# Remove position update callbacks:

## Arrow items
class ArrowItem(QGraphicsLineItem):
	def __init__(self,port1,port2,edit):
		self.editor=edit
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
	def mousePressEvent(self, event):
		cnt_arrow=0

		for j,arrows in enumerate(self.editor.array_arrows):
			for arrow in arrows:
				if self==arrow:
					cnt_arrow=j

		for arrow in self.editor.array_arrows[cnt_arrow]:
			arrow.setSelected(True)

## for Delete items in edition panels
class DeleteDialog(QDialog):
	def __init__(self,edit, parent=None):
		super(DeleteDialog, self).__init__(parent)
		self.editor=edit
		self.setWindowTitle("Eliminar")
		self.button = QPushButton('Aceptar', self)
		self.button2 = QPushButton('Cancelar', self)
		self.label_Message = QtGui.QLabel('Esta seguro que desea eliminar este bloque?',self)
		l = QVBoxLayout(self)
		l.addWidget(self.label_Message)
		l.addWidget(self.button)
		l.addWidget(self.button2)
		self.button.clicked.connect(self.ok)
		self.button2.clicked.connect(self.no)

	# If the item to be deleted has a connection
	def delete_connections(self,i,item):
		conn=[]
		arr=[]
		if self.aux2==item:			
			if len(self.editor.array_connections)>0:			
				for k,par_data in enumerate(self.editor.array_connections):
					if par_data[0][:-1]==item or par_data[1][:-1]==item:
						if str((self.editor.array_arrows[k])[0].port1.name_block)==self.aux or str((self.editor.array_arrows[k])[1].port2.name_block)==self.aux:
							conn.append(par_data)
							arr.append((self.editor.array_arrows[k]))
							for i in range(0,5):
								if (self.editor.array_arrows[k])[i].scene()==self.editor.diagramScene:
									self.editor.diagramScene.removeItem((self.editor.array_arrows[k])[i])
									

							
			if int(self.aux3)==(i-1):
				i=i-1

			if item=="Flujo":
				self.delete_flow("Flow_inputs","Fj"+str(self.aux3))
				self.delete_flow("Flow_inputs","Fv"+str(self.aux3))
				self.delete_flow("Flow_inputs","Fw"+str(self.aux3))
			else:
				self.delete_device(item)

		else:
			i=i

		for connection,arrow in zip(conn,arr):
			self.editor.array_connections.remove(connection)
			self.editor.array_arrows.remove(arrow)


		return i

	# Accepted delete item
	def ok(self):

		# Delete_item = editor.diagramScene.items(pos)
		Delete_item = self.editor.diagramScene.selectedItems()
		for item in Delete_item:
			if hasattr(item, 'name_block'):
				self.aux=str(item.name_block)
				self.aux2=re.sub("\d+", "", self.aux)
				self.aux3=re.sub('([a-zA-Z]+)', "", self.aux)
				self.aux3=re.sub('[(){}<>]', "", self.aux3)
				''
				
			# Evaluate type of item to be deleted
				self.editor.i_fw=self.delete_connections(self.editor.i_fw,"Flujo")

				self.editor.i_ev=self.delete_connections(self.editor.i_ev,"Evaporador")
				self.editor.i_ht=self.delete_connections(self.editor.i_ht,"Calentador")
				self.editor.i_ctg=self.delete_connections(self.editor.i_ctg,"Centrifuga")
				self.editor.i_clr=self.delete_connections(self.editor.i_clr,"Clarificador")
				self.editor.i_clrm=self.delete_connections(self.editor.i_clrm,"Clarificador de meladura")
				self.editor.i_tch=self.delete_connections(self.editor.i_tch,"Tacho")
				self.editor.i_tk=self.delete_connections(self.editor.i_tk,"Tanque")
				self.editor.i_tkf=self.delete_connections(self.editor.i_tkf,"Tanque Flash")
				self.editor.i_flt=self.delete_connections(self.editor.i_flt,"Filtro de lodo")
				self.editor.i_cnd=self.delete_connections(self.editor.i_cnd,"Condensador")

				self.editor.i_mll=self.delete_connections(self.editor.i_mll,"Molino")
				self.editor.i_dnl=self.delete_connections(self.editor.i_dnl,"Conductor Donnelly")

				self.editor.i_tbg=self.delete_connections(self.editor.i_tbg,"Turbo generador")
				self.editor.i_tbt=self.delete_connections(self.editor.i_tbt,"Turbo accionador")

				self.editor.i_mte=self.delete_connections(self.editor.i_mte,"Motor electrico")
				self.editor.i_vl=self.delete_connections(self.editor.i_vl,"Valvula")
				self.editor.i_pmp=self.delete_connections(self.editor.i_pmp,"Bomba")
				
				self.editor.i_pid=self.delete_connections(self.editor.i_pid,"PID")
				
				self.editor.i_dvg=self.delete_connections(self.editor.i_dvg,"Divergencia")
				self.editor.i_cnv=self.delete_connections(self.editor.i_cnv,"Convergencia")
				self.editor.i_tgI=self.delete_connections(self.editor.i_tgI,"TAG(Entrada)")
				self.editor.i_tgO=self.delete_connections(self.editor.i_tgO,"TAG(Salida)")

			# Remove item to edition panel and global data
				self.editor.diagramScene.removeItem(item)
				self.editor.diagramScene.item_list.remove(item)
				Devices.panel_items=self.editor.diagramScene.item_list

		self.close()

	# Rejected delete item
	def no(self):
		self.close()

	# Evaluate delete info of data base for deleted item (Devices)
	def delete_device(self,item):

		tables = {"Calentador" : "Heaters",
		"Valvula": "Valves",
		"Evaporador": "Evaporators"
		}
		tables = defaultdict(lambda: -1, tables)
		
		flags= {"Calentador" : "Ht",
		"Valvula": "Vlv",
		"Evaporador": "Evp"
		}
		flags = defaultdict(lambda: -1, flags)
		
		table=tables[item]
		flag=flags[item]
	
		if table!=(-1) and flag!=(-1):
			name_device=flag+str(self.aux3)

			result=self.editor.db.read_data(table,"id","Name",name_device)
			if len(result)>0:
				for data in result:
					id_device=data[0]

				if table=="Heaters":
					self.editor.db.delete_data("Physical_properties_heater","Heaters_id",id_device)
					self.editor.db.delete_data("Outputs_heater","Heaters_id",id_device)
					self.editor.db.delete_data("Heaters","id",id_device)

				elif table=="Valves":
					self.editor.db.delete_data("Outputs_valve","Valves_id",id_device)
					self.editor.db.delete_data("Valves","id",id_device)

				elif table=="Evaporators":
					self.editor.db.delete_data("Outputs_evaporator","Evaporators_id",id_device)
					self.editor.db.delete_data("Evaporators","id",id_device)

	# Evaluate delete info of data base for deleted item (Flow input)
	def delete_flow(self,table,name_device):
		self.editor.db.delete_data(table,"Name",name_device)

## Ports of items	
class PortItem(QGraphicsEllipseItem):
	def __init__(self, name,in_out,typ,block,edit,block_pos, parent=None):
		self.editor=edit
		QGraphicsEllipseItem.__init__(self, QRectF(-6,-6,8.0,8.0), parent)
		self.setCursor(QCursor(QtCore.Qt.CrossCursor))
		# Properties:
		self.name_block=block
		self.label=block
		self.typ=typ
		self.in_out=in_out
		self.block_pos=block_pos

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
			self.port_color=QColor(249, 196, 66)
			self.setBrush(QBrush(QColor(249, 196, 66)))
		elif self.typ=='mecanic':
			self.port_color=Qt.gray
			self.setBrush(QBrush(Qt.gray))
		elif self.typ=='mud':
			self.port_color=QColor(93, 67, 41)
			self.setBrush(QBrush(QColor(93, 67, 41)))

		# Name:
		self.name_port = name
		self.posCallbacks = []
		self.setFlag(self.ItemSendsScenePositionChanges, True)

	def itemChange(self, change, value):
		if change == self.ItemScenePositionHasChanged:
			for cb in self.posCallbacks:
				cb(value)
			return value
		return super(PortItem, self).itemChange(change, value)

	def mousePressEvent(self, event):
		self.editor.startConnection(self)

## Edition panel, drop and drag items
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
	def add_symbol(self,event,i,name,namex,condition):
		
		symbol={"Flujo":BlockItem_Flow,
		"Evaporador":BlockItem_Evap,
		"Calentador":BlockItem_Heat,
		"Centrifuga":BlockItem_Centrifuge,
		"Clarificador":BlockItem_Clarifier,
		"Clarificador de meladura":BlockItem_Mel_Clarifier,
		"Tacho":BlockItem_Cristalizer,
		"Tanque":BlockItem_Tank,
		"Tanque Flash":BlockItem_Flash_Tank,
		"Filtro de lodo":BlockItem_Mud_Filter,
		"Condensador":BlockItem_Condenser,
		"Molino":BlockItem_Mill,
		"Conductor Donnelly":BlockItem_Donnelly,
		"Generador":BlockItem_Generator,
		"Turbina":BlockItem_Turbine,
		"Motor electrico":BlockItem_Electric_Motor,
		"Valvula":BlockItem_Valve,
		"Bomba":BlockItem_Pump,
		"PID":BlockItem_Controller,
		"Convergencia":BlockItem_Convergence,
		"Divergencia":BlockItem_Divergence,
		"TAG(Entrada)":BlockItem_tag_input,
		"TAG(Salida)":BlockItem_tag_output		
		}

		if namex==str(condition):
			b1 = symbol[condition](name+str(i),editor)
			b1.setPos(self.mapToScene(event.pos()))
			editor.diagramScene.addItem(b1)
			editor.diagramScene.item_list.append(b1)
			Devices.panel_items=editor.diagramScene.item_list
			i=i+1
		else:
			i=i
		return i	

	def dropEvent(self, event):
		if event.mimeData().hasFormat('component/name'):
			global name

			name = str(event.mimeData().data('component/name'))

			editor.i_fw=self.add_symbol(event,editor.i_fw,name,namex,"Flujo")

			editor.i_ev=self.add_symbol(event,editor.i_ev,name,namex,"Evaporador")
			editor.i_ht=self.add_symbol(event,editor.i_ht,name,namex,"Calentador")
			editor.i_ctg=self.add_symbol(event,editor.i_ctg,name,namex,"Centrifuga")
			editor.i_clr=self.add_symbol(event,editor.i_clr,name,namex,"Clarificador")
			editor.i_clrm=self.add_symbol(event,editor.i_clrm,name,namex,"Clarificador de meladura")
			editor.i_tch=self.add_symbol(event,editor.i_tch,name,namex,"Tacho")
			editor.i_tk=self.add_symbol(event,editor.i_tk,name,namex,"Tanque")
			editor.i_tkf=self.add_symbol(event,editor.i_tkf,name,namex,"Tanque Flash")
			editor.i_flt=self.add_symbol(event,editor.i_tkf,name,namex,"Filtro de lodo")
			editor.i_cnd=self.add_symbol(event,editor.i_cnd,name,namex,"Condensador")

			editor.i_mll=self.add_symbol(event,editor.i_mll,name,namex,"Molino")
			editor.i_dnl=self.add_symbol(event,editor.i_dnl,name,namex,"Conductor Donnelly")

			editor.i_tbg=self.add_symbol(event,editor.i_tbg,name,namex,"Generador")
			editor.i_tbt=self.add_symbol(event,editor.i_tbt,name,namex,"Turbina")
			editor.i_mte=self.add_symbol(event,editor.i_mte,name,namex,"Motor electrico")

			editor.i_vl=self.add_symbol(event,editor.i_vl,name,namex,"Valvula")
			editor.i_pmp=self.add_symbol(event,editor.i_pmp,name,namex,"Bomba")

			editor.i_pid=self.add_symbol(event,editor.i_pid,name,namex,"PID")

			editor.i_cnv=self.add_symbol(event,editor.i_cnv,name,namex,"Convergencia")
			editor.i_dvg=self.add_symbol(event,editor.i_dvg,name,namex,"Divergencia")
			editor.i_tgI=self.add_symbol(event,editor.i_tgI,name,namex,"TAG(Entrada)")
			editor.i_tgO=self.add_symbol(event,editor.i_tgO,name,namex,"TAG(Salida)")			

## Model of list items
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
 #
class DiagramScene(QGraphicsScene):
	itemSelected = QtCore.pyqtSignal(QtGui.QGraphicsItem)
	
	def __init__(self, parent=None):
		super(DiagramScene, self).__init__(parent)
		self.item_list=[]
	def mouseMoveEvent(self, mouseEvent):
		editor.sceneMouseMoveEvent(mouseEvent)
		super(DiagramScene, self).mouseMoveEvent(mouseEvent)
	def mouseReleaseEvent(self, mouseEvent):
		editor.sceneMouseReleaseEvent(mouseEvent)
		super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
	pass

## Principal window of Dynamic simulator
class DiagramEditor(QWidget): 
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
	
	# Initiation of variable
		global indicator
		global label_indicator
		global Ts_value

		self.Sim_time=0.5
		
		self.i_fw=1

		self.i_ev=1
		self.i_ht=1
		self.i_ctg=1
		self.i_clr=1
		self.i_clrm=1
		self.i_tch=1
		self.i_tk=1
		self.i_tkf=1
		self.i_flt=1
		self.i_cnd=1

		self.i_mll=1
		self.i_dnl=1

		self.i_tbg=1
		self.i_tbt=1
		self.i_mte=1

		self.i_vl=1
		self.i_pmp=1
		
		self.i_pid=1
		
		self.i_dvg=1
		self.i_cnv=1
		self.i_tgI=1
		self.i_tgO=1
		

		self.array_arrows=[]
		self.array_connections=[]

		self.db=data_base_instance()
		connection_db=self.db.connect()
		self.db.clear_all()

		Vali = Validator()

	#General Layout. Entire GUI
		self.generalayout = QtGui.QGridLayout(self) 
		self.generalayout.setSpacing(0)
		self.generalayout.setContentsMargins(0,0,0,0);

		self.resize(1000, 800)

	# Menu Bar 
		self.MenuBarLayoutWidget=  QtGui.QWidget(self) 
		self.MenuBar_layout=QVBoxLayout(self.MenuBarLayoutWidget)

		self.menu_bar = QMenuBar()
		
		self.file_menu = self.menu_bar.addMenu('Archivo')		
		self.open = QAction('Abrir', self)
		self.open.triggered.connect(self.open_files)
		self.save = QAction('Guardar', self)
		self.save.triggered.connect(self.save_files)		
		self.exit_action = QAction('Salir', self)
		self.exit_action.triggered.connect(self.closeEvent)
		
		self.file_menu.addAction(self.open)
		self.file_menu.addAction(self.save)
		self.file_menu.addAction(self.exit_action)

		self.analysis_menu=self.menu_bar.addMenu(_translate("Dialog",'Análisis', None))
		self.graphic= QAction(_translate("Dialog",'Gráfica', None), self)
		self.report= QAction('Informe', self)
		
		self.analysis_menu.addAction(self.graphic)
		self.analysis_menu.addAction(self.report)

		self.simulation_menu=self.menu_bar.addMenu(_translate("Dialog",'Simulación', None))
		self.simulation_options= QAction('Opciones', self)
		
		self.simulation_menu.addAction(self.simulation_options)

		self.help_menu = self.menu_bar.addMenu('Ayuda')
		self.about_us=QAction(_translate("Dialog",'Información', None), self)
		self.about_us.triggered.connect(self.information)
		
		self.help_menu.addAction(self.about_us)

		self.MenuBar_layout.addWidget(self.menu_bar)

	#Timer to count clicks in symbols
		self.timer = QtCore.QTimer()
		self.timer.setInterval(500)
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.timeout)
		self.left_click_count = 0

	# Window tittle
		self.setWindowTitle(_translate("Dialog", "Simulador dinámico del proceso de producción de azúcar", None))

	##Selection Panel. Tools and elements to be added to the edition panel
		self.horizontalLayoutWidget = QtGui.QWidget(self)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1002, 770))
		
		self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget) 
		self.horizontalLayout.setGeometry(QtCore.QRect(0, 0, 970, 800))

	## Simulation Buttons Panel
		#Layouts
		self.buttonsLayoutWidget=  QtGui.QWidget(self) 
		self.buttonsLayoutWidget.setGeometry(QtCore.QRect(0, 30, 1002, 26))

		self.buttonsHorizontalLayout = QtGui.QHBoxLayout(self.buttonsLayoutWidget) 
		self.buttonsHorizontalLayout.setGeometry(QtCore.QRect(0, 30,970, 26))

		#Buttons
		self.buttonRun = QtGui.QPushButton(self)
		self.buttonRun.setGeometry(QtCore.QRect(940, 9, 24, 24))
		self.buttonRun.setIcon(QtGui.QIcon(dir_script+"\Images\play_icon.png"))
		self.buttonRun.setIconSize(QtCore.QSize(24,24))
		self.buttonRun.clicked.connect(self.run_simulation)
		self.buttonRun.setStyleSheet("border: none")

		self.buttonPause = QtGui.QPushButton(self)
		self.buttonPause.setGeometry(QtCore.QRect(965, 9, 24, 24))
		self.buttonPause.setIcon(QtGui.QIcon(dir_script+"\Images\stop_icon.png"))		
		self.buttonPause.setIconSize(QtCore.QSize(24,24))
		self.buttonPause.clicked.connect(self.stop_simulation)
		self.buttonPause.setStyleSheet("border: none")

		#Sample time
		self.label_Ts=QtGui.QLabel(self)
		self.label_Ts.setGeometry(QtCore.QRect(747, 9, 127, 24))
		self.label_Ts.setText("Tiempo de muestreo (seg):")
		self.label_Ts.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		Ts_value=QtGui.QLineEdit(self)
		Ts_value.setGeometry(QtCore.QRect(876, 11, 33, 21))
		Ts_value.setText("0.5")
		Vali.num_validator(Ts_value)

		#Simulation indicators
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

		self.generalayout.addWidget(self.MenuBarLayoutWidget,0,0)
		self.generalayout.addWidget(self.buttonsLayoutWidget,1,0)
		self.generalayout.addWidget(self.horizontalLayoutWidget,2,0) 
		
	##Tree view inizalitation##
		self.libraryModel = LibraryModel(self)
		self.libraryModel.setColumnCount(1)
		self.libraryModel.setHeaderData(0, QtCore.Qt.Horizontal, _translate("Dialog", "Panel de selección", None));

		self.libItems = []

		self.libraryBrowserView_TREE = QtGui.QTreeView(self)
		self.libraryBrowserView_TREE.setIconSize(QtCore.QSize(60,60))
		self.libraryBrowserView_TREE.setModel(self.libraryModel)

	##Icons
		#-Inputs icons-#
		self.iconFlow=QIcon(dir_script+"\Images\_flow_none.png");

		#-Elaboration icons-#
		self.iconEvaporator=QIcon(dir_script+"\Images\Evap_Kstner-icon.png");
		self.iconHeater=QIcon(dir_script+"\Images\Heater_SnT.png");
		self.iconCentrifuge=QIcon(dir_script+"\Images\Centrifuge.png");	
		self.iconClarifier=QIcon(dir_script+"\Images\Clarifier.png");
		self.iconMelClarifier=QIcon(dir_script+"\Images\Mel_Clarifier.png");
		self.iconCrystalizer=QIcon(dir_script+"\Images\Cristallizer.png");
		self.iconTank=QIcon(dir_script+"\Images\_Tank.png");
		self.iconFlash_tank=QIcon(dir_script+"\Images\Flash.png");
		self.iconMud_filter=QIcon(dir_script+"\Images\Mud_filter.png");
		self.iconCondenser=QIcon(dir_script+"\Images\Condenser.png");
		# self.iconDryer=QIcon(dir_script+"\Images\Dryer.png");

		#-Preparation and grinding icons-#
		self.iconMill=QIcon(dir_script+"\Images\Mill.png");
		self.iconDonnelly=QIcon(dir_script+"\Images\Donnelly.png");

		#-Steam and electric power icons-#		
		self.iconTurbo_generator=QIcon(dir_script+"\Images\Generator.png");
		self.iconTurbo_trigger=QIcon(dir_script+"\Images\_Turbo_trigger.png");
		self.iconElectric_motor=QIcon(dir_script+"\Images\Electric_motor.png");
		# self.iconBoiler=QIcon(dir_script+"\Images\Boiler.png");
		
		#-Actuators icons-#
		self.iconValve=QIcon(dir_script+"\Images\_valve.png");  
		self.iconPump=QIcon(dir_script+"\Images\Pump.png");

		#-Controllers icons-#
		self.iconPID=QIcon(dir_script+"\Images\PID-icon.png");
		
		#-COnnections icons-#
		self.icon_divergence=QIcon(dir_script+"\Images\Divergence.png")  
		self.icon_convergence=QIcon(dir_script+"\Images\Convergence.png")  	
		self.iconTagIn=QIcon(dir_script+"\Images\wire_tag_input.png");
		self.iconTagOut=QIcon(dir_script+"\Images\wire_tag_output.png");
		
	##Items
		#-Inputs items-#
		self.Flow=QtGui.QStandardItem(self.iconFlow, 'Flujo') ;

		#-Elaboration items-#
		self.EvaporItem=QtGui.QStandardItem(self.iconEvaporator, 'Evaporador');
		self.HeaterItem=QtGui.QStandardItem(self.iconHeater, 'Calentador') ;
		self.Centrifuge=QtGui.QStandardItem(self.iconCentrifuge, 'Centrifuga')
		self.Clarifier=QtGui.QStandardItem(self.iconClarifier, 'Clarificador')
		self.Mel_Clarifier=QtGui.QStandardItem(self.iconMelClarifier, 'Clarificador de meladura')
		self.Cristallizer=QtGui.QStandardItem(self.iconCrystalizer, 'Tacho')
		self.Tank=QtGui.QStandardItem(self.iconTank, 'Tanque') 
		self.Flash_tank=QtGui.QStandardItem(self.iconFlash_tank, 'Tanque Flash')
		self.Mud_filter=QtGui.QStandardItem(self.iconMud_filter, 'Filtro de lodo')
		self.Condenser=QtGui.QStandardItem(self.iconCondenser, 'Condensador')
		# self.Dryer=QtGui.QStandardItem(self.iconDryer, 'Secadora')

		#-Preparation and grinding items-#
		self.Mill=QtGui.QStandardItem(self.iconMill, 'Molino')
		self.Donnelly=QtGui.QStandardItem(self.iconDonnelly, 'Conductor Donnelly')

		#-Steam and electric power items-#	
		self.Turbo_generator=QtGui.QStandardItem(self.iconTurbo_generator, 'Generador')
		self.Turbo_trigger=QtGui.QStandardItem(self.iconTurbo_trigger, 'Turbina')
		self.Electric_motor=QtGui.QStandardItem(self.iconElectric_motor, 'Motor electrico')
		# self.Boiler=QtGui.QStandardItem(self.iconBoiler, 'Caldera')

		#-Actuators items-#		
		self.Valve=QtGui.QStandardItem(self.iconValve,"Valvula") ;
		self.Pump=QtGui.QStandardItem(self.iconPump, 'Bomba')

		#-Controllers items-#
		self.PID_controller=QtGui.QStandardItem(self.iconPID, 'PID')

		#-Connections items-#		
		self.Divergence=QtGui.QStandardItem(self.icon_divergence, 'Divergencia') 
		self.Convergence=QtGui.QStandardItem(self.icon_convergence, 'Convergencia') 	
		self.Tag_input=QtGui.QStandardItem(self.iconTagIn, 'TAG(Entrada)') 
		self.Tag_output=QtGui.QStandardItem(self.iconTagOut, 'TAG(Salida)')

	
		self.libItems.append(self.Flow)

		self.libItems.append(self.EvaporItem)
		self.libItems.append(self.HeaterItem)
		self.libItems.append(self.Centrifuge)
		self.libItems.append(self.Clarifier)
		self.libItems.append(self.Mel_Clarifier)
		self.libItems.append(self.Cristallizer)
		self.libItems.append(self.Tank)
		self.libItems.append(self.Flash_tank)
		self.libItems.append(self.Mud_filter)
		self.libItems.append(self.Condenser)
		# self.libItems.append(self.Dryer)

		self.libItems.append(self.Mill)
		self.libItems.append(self.Donnelly)

		# self.libItems.append(self.Boiler)
		self.libItems.append(self.Turbo_generator)
		self.libItems.append(self.Turbo_trigger)
		self.libItems.append(self.Electric_motor)


		self.libItems.append(self.Valve)
		self.libItems.append(self.Pump)

		self.libItems.append(self.PID_controller)

		self.libItems.append(self.Divergence)
		self.libItems.append(self.Convergence)
		self.libItems.append(self.Tag_input)
		self.libItems.append(self.Tag_output)

		for items in self.libItems:
		   items.setEditable(0)

	##Division items		
		
		parent1 = QStandardItem('Entradas')
		parent1.setEditable(0)
		parent1.setSelectable(0)
		parent1.appendRow(self.libItems[0])
		self.libraryModel.appendRow(parent1)

		parent3 = QStandardItem(_translate("item",'Preparación y molienda', None))
		parent3.setEditable(0)
		parent3.setSelectable(0)
		parent3.appendRow(self.libItems[11])
		parent3.appendRow(self.libItems[12])
		self.libraryModel.appendRow(parent3)

		parent2 = QStandardItem(_translate("item",'Elaboración', None))
		parent2.setEditable(0)
		parent2.setSelectable(0)
		parent2.appendRow(self.libItems[1])
		parent2.appendRow(self.libItems[2])
		parent2.appendRow(self.libItems[3])
		parent2.appendRow(self.libItems[4])
		parent2.appendRow(self.libItems[5])
		parent2.appendRow(self.libItems[6])
		parent2.appendRow(self.libItems[7])
		parent2.appendRow(self.libItems[8])
		parent2.appendRow(self.libItems[9])
		parent2.appendRow(self.libItems[10])
		self.libraryModel.appendRow(parent2)


		parent4 = QStandardItem(_translate("item",'Vapor y energía eléctrica', None))
		parent4.setEditable(0)
		parent4.setSelectable(0)
		parent4.appendRow(self.libItems[13])
		parent4.appendRow(self.libItems[14])
		self.libraryModel.appendRow(parent4)

		parent5 = QStandardItem('Actuadores')
		parent5.setEditable(0)
		parent5.setSelectable(0)
		parent5.appendRow(self.libItems[15])
		parent5.appendRow(self.libItems[16])
		parent5.appendRow(self.libItems[17])
		self.libraryModel.appendRow(parent5)
		
		parent6 = QStandardItem('Controladores')
		parent6.setEditable(0)
		parent6.setSelectable(0)
		parent6.appendRow(self.libItems[18])
		self.libraryModel.appendRow(parent6)	

		parent7 = QStandardItem('Conexiones')
		parent7.setEditable(0)
		parent7.setSelectable(0)
		parent7.appendRow(self.libItems[19])
		parent7.appendRow(self.libItems[20])
		parent7.appendRow(self.libItems[21])
		parent7.appendRow(self.libItems[22])
		self.libraryModel.appendRow(parent7)	


	## Set tree view
		self.libraryBrowserView_TREE.setDragDropMode(self.libraryBrowserView_TREE.DragOnly)
		self.horizontalLayout.addWidget(self.libraryBrowserView_TREE,1)

	## Selection Panel. Tools and elements to be added to the edition panel INIZALITATION
		self.diagramScene = DiagramScene(self)
		self.diagramView = EditorGraphicsView(self.diagramScene, self)
		self.horizontalLayout.addWidget(self.diagramView,3)

		self.startedConnection = None

	# Action realized for About us option in menu bar
	def information(self):
		Resultado=QtGui.QDialog()
		ui = information_window()
		ui.setupUi(Resultado)
		Resultado.exec_()

	# Action realized for Save option in menu bar
	def save_files(self):
		SvFile=SaveFile()
		SvFile.save(self)

	# Action realized for Open option in menu bar
	def open_files(self):
		OpFile=OpenFile()
		OpFile.read(editor)

	# Action realized for play simulation
	def run_simulation(self):
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
					
						# if len(heat_param)>0 and len(vapor_data)>0 and len(juice_data)>0:
					if len(self.diagramScene.item_list)>0:
						indicator.setIcon(QtGui.QIcon(dir_script+"\Images\led-green.png"))
						label_indicator.setText(_translate("Dialog","Simulación: Corriendo", None))
						# sim_heat_data=np.append(heat_param[0:9],juice_data[0:4])
						# sim_heat_data=np.append(sim_heat_data,vapor_data[0])
						#print sim_heat_data

						self.Sim_time=float(Ts_value.text())
						# sim=Simulation("_",sim_heat_data,self.Sim_time,self.db)
						sim=Simulation("_",self.Sim_time,self.db)

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

	# Action realized for stop simulation	
	def stop_simulation(self):
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
				self.db.insert_data("TIME_EXEC","TIME",["stop"])
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

	# Start connection in edition panel
	def startConnection(self, port):
		global prt1
		global prt2
		global itemname1
		global itemname2
		global port_item1
		global type_prt1
		global type_prt2
		prt1=""
		prt2=""
		type_prt2=""
		itemname1=""
		itemname2=""
		prt1=str(port.in_out)
		type_prt1=str(port.typ)
		port_item1=port
		itemname1=str(port.name_block)
		self.startedConnection = Connection(port, None,editor)

	def sceneMouseMoveEvent(self, event):
		global pos
		pos = event.scenePos()
		items = self.diagramScene.items(pos)
		for item in items:
			if hasattr(item, 'name_port'):
				item.setToolTip(item.name_port)
			# if type(item) is PortItem:
				# #print(item.name)
				# item.setToolTip(item.name)
		if self.startedConnection:
			pos = event.scenePos()
			self.startedConnection.setEndPos(pos)

	def sceneMouseReleaseEvent(self, event):
		global puerto2
		global itemname2

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
					pd = ParameterDialog_Valve(aux,self.Sim_time,self.db,item,self.window())
				if str(aux2)==str("Flujo"):
					pd = ParameterDialog_Flow(aux,self.Sim_time,item,self.db,self.window())
				if str(aux2)==str("Evaporador"):
					pd = ParameterDialog_Evaporator(aux,self.Sim_time,item,self.db,self.window())
				if str(aux2)==str("Calentador"):	
					pd = ParameterDialog_Heater(aux,self.Sim_time,item,self.db,self.window())
				if str(aux2)==str("Tanque"):
					pd = ParameterDialog_Tank(aux,self.Sim_time,item,self.window())
				if str(aux2)==str("PID"):
					pd = ParameterDialog_Controller(aux,self.Sim_time,self.db,item,self.window())
		
		if self.startedConnection:
			for item in items:
				# print(type(item))
				if hasattr(item, 'name_port'):
				# if type(item) is PortItem:
					prt2=str(item.in_out)
					type_prt2=str(item.typ)
					port_item2=item
					itemname2=str(item.name_block)
					
					# Condition for star a connection
					type_condition=(type_prt1==type_prt2)or(type_prt1=="none" and type_prt2!="none")or(type_prt2=="none" and type_prt1!="none")

					if prt2!=prt1 and itemname2!=itemname1:
						if prt1=="out" and prt2=='in'and type_condition==True:
								
							self.startedConnection.setToPort(item)
							self.startedConnection.setEndPos(item.scenePos())
							connections=[itemname1, itemname2,str(port_item1.name_port),str(port_item2.name_port)]
							self.array_connections.append(connections)
							Devices.array_connections=self.array_connections
														
							self.connection_painter(self.startedConnection,port_item1,port_item2)			

						elif prt1=="in" and prt2=='out'and type_condition==True:

							self.startedConnection.setToPort(item)
							self.startedConnection.setEndPos(item.scenePos())
							connections=[itemname2,itemname1,str(port_item2.name_port),str(port_item1.name_port)]
							self.array_connections.append(connections)
							Devices.array_connections=self.array_connections

							self.connection_painter(self.startedConnection,port_item1,port_item2)
							
					else:
						self.startedConnection.delete()
			if self.startedConnection.toPort == None:
				self.startedConnection.delete()
			self.startedConnection = None

	def connection_painter(self,connection,port1,port2):

		prt1=str(port1.in_out)
		type_prt1=str(port1.typ)
		port_item1=port1
		itemname1=str(port1.name_block)

		item=port2
		prt2=str(port2.in_out)
		type_prt2=str(port2.typ)
		port_item2=port2
		itemname2=str(port2.name_block)
		
		if prt1=="out" and prt2=='in':
									
			if port_item1.typ!="none" and port_item2.typ=="none" and hasattr(port_item1, 'port_color'):

				connection.arrow.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow2.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow3.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow4.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow5.setPen(QtGui.QPen(port_item1.port_color,3))
				if port_item1.typ=="juice":
					port_item2.setBrush(QBrush(QColor(215, 125, 0)))
				elif port_item1.typ=="vapor":
					port_item2.setBrush(QBrush(Qt.green))
				elif port_item1.typ=="condensed" or port_item1.typ=="water":
					port_item2.setBrush(QBrush(Qt.blue))
				elif port_item1.typ=="electric":
					port_item2.setBrush(QBrush(QColor(249, 196, 66)))
				elif port_item1.typ=="mecanic":
					port_item2.setBrush(QBrush(Qt.gray))
				elif port_item1.typ=="mud":
					port_item2.setBrush(QBrush(QColor(93, 67, 41)))
					
			
			elif port_item2.typ!="none" and port_item1.typ=="none" and hasattr(port_item2, 'port_color'):
				connection.arrow.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow2.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow3.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow4.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow5.setPen(QtGui.QPen(port_item2.port_color,3))
				if port_item2.typ=="juice":
					port_item1.setBrush(QBrush(QColor(215, 125, 0)))
				elif port_item2.typ=="vapor":
					port_item1.setBrush(QBrush(Qt.green))
				elif port_item2.typ=="condensed" or port_item2.typ=="water":
					port_item1.setBrush(QBrush(Qt.blue))
				elif port_item2.typ=="electric":
					port_item1.setBrush(QBrush(QColor(249, 196, 66)))
				elif port_item2.typ=="mecanic":
					port_item1.setBrush(QBrush(Qt.gray))
				elif port_item2.typ=="mud":
					port_item1.setBrush(QBrush(QColor(93, 67, 41)))

			elif port_item2.typ!="none" and port_item1.typ!="none" and hasattr(port_item1, 'port_color'):
				connection.arrow.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow2.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow3.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow4.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow5.setPen(QtGui.QPen(port_item1.port_color,3))

			print self.array_connections
			

		elif prt1=="in" and prt2=='out':
						
			if port_item2.typ!="none" and port_item1.typ=="none" and hasattr(port_item2, 'port_color'):
				connection.arrow.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow2.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow3.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow4.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow5.setPen(QtGui.QPen(port_item2.port_color,3))
				if port_item2.typ=="juice":
					port_item1.setBrush(QBrush(QColor(215, 125, 0)))
				elif port_item2.typ=="vapor":
					port_item1.setBrush(QBrush(Qt.green))
				elif port_item2.typ=="condensed" or port_item2.typ=="water":
					port_item1.setBrush(QBrush(Qt.blue))
				elif port_item2.typ=="electric":
					port_item1.setBrush(QBrush(QColor(249, 196, 66)))
				elif port_item2.typ=="mecanic":
					port_item1.setBrush(QBrush(Qt.gray))
				elif port_item2.typ=="mud":
					port_item1.setBrush(QBrush(QColor(93, 67, 41)))

			elif port_item1.typ!="none" and port_item2.typ=="none" and hasattr(port_item1, 'port_color'):
				connection.arrow.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow2.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow3.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow4.setPen(QtGui.QPen(port_item1.port_color,3))
				connection.arrow5.setPen(QtGui.QPen(port_item1.port_color,3))
				if port_item1.typ=="juice":
					port_item2.setBrush(QBrush(QColor(215, 125, 0)))
				elif port_item1.typ=="vapor":
					port_item2.setBrush(QBrush(Qt.green))
				elif port_item1.typ=="condensed" or port_item1.typ=="water":
					port_item2.setBrush(QBrush(Qt.blue))
				elif port_item1.typ=="electric":
					port_item2.setBrush(QBrush(QColor(249, 196, 66)))
				elif port_item1.typ=="mecanic":
					port_item2.setBrush(QBrush(Qt.gray))
				elif port_item1.typ=="mud":
					port_item2.setBrush(QBrush(QColor(93, 67, 41)))

			elif port_item1.typ!="none" and port_item2.typ!="none" and hasattr(port_item2, 'port_color'):
				connection.arrow.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow2.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow3.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow4.setPen(QtGui.QPen(port_item2.port_color,3))
				connection.arrow5.setPen(QtGui.QPen(port_item2.port_color,3))

			print self.array_connections

	def keyPressEvent(self, kevent):

		items = self.diagramScene.selectedItems()
		for item in items:
			if item.isSelected()==True:
				key = kevent.key()

				# If press delete key about selected item
				if key == QtCore.Qt.Key_Delete :
					if hasattr(item, 'port1'): ##If is an ArrowItem()
						cnt_arrow=0
						for j,arrows in enumerate(self.array_arrows):
							for arrow in arrows:
								if item==arrow:
									cnt_arrow=j
			
						for k, par_data in enumerate(self.array_connections):
							if ((str(par_data[0])==str(self.array_arrows[cnt_arrow][0].port1.name_block) and str(par_data[1])==str(self.array_arrows[cnt_arrow][1].port2.name_block))
								or (str(par_data[0])==str(self.array_arrows[cnt_arrow][1].port2.name_block) and str(par_data[1])==str(self.array_arrows[cnt_arrow][0].port1.name_block))):
								self.array_connections.pop(k)
						
						for arrow in self.array_arrows[cnt_arrow]:
							editor.diagramScene.removeItem(arrow)
						self.array_arrows.pop(cnt_arrow)
						
					else: ## If is a BlockItem()
						pd = DeleteDialog(editor,self.window())
						pd.exec_()
	def timeout(self):
		self.left_click_count = 0

	## Close Dynamic simulator 
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

## Main Class
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	global editor
	editor = DiagramEditor()
	editor.show()
	Window_icon=QtGui.QIcon(dir_script+"\Images\Simulador_dinamico.png")
	
	from connections_devices import *

	app.setWindowIcon(Window_icon)
	app.exec_()
