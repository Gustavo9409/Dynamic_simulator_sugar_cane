
# Installed Libs
import re

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from collections import defaultdict

# Local Libs
from global_data import *

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

# Import Xml reader and writer
try:
	from PyQt4.QtCore import QXmlStreamWriter
	from PyQt4.QtCore import QXmlStreamReader
except:
	from PyQt4.QtXml import QXmlStreamWriter
	from PyQt4.QtCore import QXmlStreamReader

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

## Class to save dynamic simulator files
class SaveFile():
	def save(self,editor):
		filename, filter = QtGui.QFileDialog.getSaveFileNameAndFilter(editor, 'Guardar archivo', '', "*.xml")
		if filename:
			
			file=QFile (filename)
			if not (file.open(QIODevice.WriteOnly)):
				return
			
			xmlWriter = QXmlStreamWriter(file)
			xmlWriter.setAutoFormatting(True)
			xmlWriter.writeStartDocument()
			xmlWriter.writeStartElement("Dynamic_Simulator")
			xmlWriter.writeAttribute("version", "v1.0")
		
			xmlWriter.writeStartElement("ItemList")
			for items in editor.diagramScene.item_list:
				name=re.sub(" ", "_",items.name_block)
				xmlWriter.writeStartElement(str(name))
				xmlWriter.writeAttribute("Label", str(items.label.toPlainText()) )
				xmlWriter.writeAttribute("xCoord", str(items.x()))
				xmlWriter.writeAttribute("yCoord",str(items.y()))
				xmlWriter.writeEndElement() #end of each item
			xmlWriter.writeEndElement() #end of ItemList
			
			xmlWriter.writeStartElement("Connections")
			for connections in editor.array_connections:
				xmlWriter.writeStartElement("Connection")
				xmlWriter.writeAttribute("fromDevice", str(connections[0]) )
				xmlWriter.writeAttribute("toDevice",  str(connections[1]) )
				xmlWriter.writeAttribute("fromPort", str(connections[2]) )
				xmlWriter.writeAttribute("toPort",  str(connections[3]) )
				xmlWriter.writeEndElement() #end of each connection
			xmlWriter.writeEndElement() #end of Connections

			xmlWriter.writeEndElement() #end of Dynamic Simulator
			file.close()
			
			Resultado=QtGui.QDialog()
			QtGui.QMessageBox.information(Resultado,'Ok',_translate("Dialog","Archivo guardado correctamente.",None),QtGui.QMessageBox.Ok)

## Class to open dynamic simulator and ceniprof 2.0 files
class OpenFile():
	
	def port_convertion(self,device,id_port):
		ports={
		("Flujo",1):"Salida",

		("Evaporador",0):"Jugo de entrada",
		("Evaporador",1):"Vapor vivo",
		("Evaporador",2):"Jugo de salida",
		("Evaporador",3):"Vapor vegetal",
		("Evaporador",4):"Vapor condensado",
		
		("Calentador",0):"Fluido de entrada",
		("Calentador",1):"Fluido de salida",
		("Calentador",2):"Vapor de entrada",
		("Calentador",3):"Vapor condensado",

		("Centrifuga",0):"Masa cocida",
		("Centrifuga",1):"Agua de entrada",
		("Centrifuga",2):"Azucar",
		("Centrifuga",3):"Miel de salida",
		("Centrifuga",4):"Energia electrica de entrada",

		("Clarificador",0):"Jugo de entrada",
		("Clarificador",1):"Jugo de salida",
		("Clarificador",2):"Lodo de salida",

		("Tacho",0):"Alimentacion de entrada",
		("Tacho",1):"Semilla de entrada",
		("Tacho",2):"Vapor de salida",
		("Tacho",3):"Descarga",
		("Tacho",4):"Vapor de entrada",
		("Tacho",6):"Vapor condensado",

		("Tanque Flash",0):"Fluido de entrada",
		("Tanque Flash",1):"Fluido de salida",
		("Tanque Flash",2):"Vapor de salida",

		("Filtro de lodo",0):"Lodos de entrada",
		("Filtro de lodo",2):"Agua de entrada",
		("Filtro de lodo",3):"Jugo de salida",

		("Condensador",0):"Agua de entrada",
		("Condensador",1):"Vapor de entrada",
		("Condensador",2):"Agua+Condensado",

		("Molino",0):"Alimentacion",
		("Molino",2):"Bagazo de salida",
		("Molino",3):"Jugo de salida",

		("Generador",2):"Energia electrica",

		("Turbina",0):"Energia mecanica",
		("Turbina",1):"Vapor de entrada",
		("Turbina",2):"Vapor de salida",

		("Motor electrico",0):"Energia mecanica",
		("Motor electrico",1):"Energia electrica",

		("Divergencia",0):"Entrada",
		("Divergencia",1):"Salida 1",
		("Divergencia",2):"Salida 2",

		("Convergencia",0):"Entrada 1",
		("Convergencia",1):"Entrada 2",
		("Convergencia",3):"Salida",
		}
		ports = defaultdict(lambda: -1, ports)
		port=ports[device,id_port]

		if port!=-1:
			return port
		else:
			return None


	def name_convertion(self,condition):
		names={
		"Flujo":"Flujo",
		"Evaporador":"Evaporador",
		"Calentador":"Calentador",
		"Centrifuga":"Centrifuga",
		"Clarificador":"Clarificador",
		"Clarificador_Mel":"Clarificador de meladura",
		"Tacho":"Tacho",
		"TanqueFlash":"Tanque Flash",
		"Filtros":"Filtro de lodo",
		"Condensador":"Condensador",
		"Molino":"Molino",
		"Turbogeneradores":"Generador",
		"Turbo_Acc":"Turbina",
		"Motor_Elec":"Motor electrico",
		"SumFlow":"Convergencia",
		"DivFlow":"Divergencia",
		}
		names = defaultdict(lambda: -1, names)

		name=names[condition]

		if name!=-1:
			return name
		else:
			return None


	def load_symbol(self,pos,i,i_editor,name,namex,label_text,condition):
		
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
			b1 = symbol[condition](name+str(i),self.editor)
			b1.setPos(self.editor.diagramView.mapToScene(pos))
			self.editor.diagramScene.addItem(b1)
			b1.label.setPlainText(_translate("Dialog",label_text,None))
			self.editor.diagramScene.item_list.append(b1)
			Devices.panel_items=self.editor.diagramScene.item_list
			i=i+1
		else:
			i=i_editor
		return i	

	def load_items(self, name,i,pos,label):

		namex=name
	
		self.editor.i_fw=self.load_symbol(pos,i,self.editor.i_fw,name,namex,label,"Flujo")

		self.editor.i_ev=self.load_symbol(pos,i,self.editor.i_ev,name,namex,label,"Evaporador")
		self.editor.i_ht=self.load_symbol(pos,i,self.editor.i_ht,name,namex,label,"Calentador")
		self.editor.i_ctg=self.load_symbol(pos,i,self.editor.i_ctg,name,namex,label,"Centrifuga")
		self.editor.i_clr=self.load_symbol(pos,i,self.editor.i_clr,name,namex,label,"Clarificador")
		self.editor.i_clrm=self.load_symbol(pos,i,self.editor.i_clrm,name,namex,label,"Clarificador de meladura")
		self.editor.i_tch=self.load_symbol(pos,i,self.editor.i_tch,name,namex,label,"Tacho")
		self.editor.i_tk=self.load_symbol(pos,i,self.editor.i_tk,name,namex,label,"Tanque")
		self.editor.i_tkf=self.load_symbol(pos,i,self.editor.i_tkf,name,namex,label,"Tanque Flash")
		self.editor.i_tkf=self.load_symbol(pos,i,self.editor.i_tkf,name,namex,label,"TanqueFlash")
		self.editor.i_flt=self.load_symbol(pos,i,self.editor.i_flt,name,namex,label,"Filtro de lodo")
		self.editor.i_flt=self.load_symbol(pos,i,self.editor.i_flt,name,namex,label,"Filtros")
		self.editor.i_cnd=self.load_symbol(pos,i,self.editor.i_cnd,name,namex,label,"Condensador")

		self.editor.i_mll=self.load_symbol(pos,i,self.editor.i_mll,name,namex,label,"Molino")
		self.editor.i_dnl=self.load_symbol(pos,i,self.editor.i_dnl,name,namex,label,"Conductor Donnelly")

		self.editor.i_tbg=self.load_symbol(pos,i,self.editor.i_tbg,name,namex,label,"Generador")
		self.editor.i_tbt=self.load_symbol(pos,i,self.editor.i_tbt,name,namex,label,"Turbina")
		self.editor.i_mte=self.load_symbol(pos,i,self.editor.i_mte,name,namex,label,"Motor electrico")

		self.editor.i_vl=self.load_symbol(pos,i,self.editor.i_vl,name,namex,label,"Valvula")
		self.editor.i_pmp=self.load_symbol(pos,i,self.editor.i_pmp,name,namex,label,"Bomba")

		self.editor.i_pid=self.load_symbol(pos,i,self.editor.i_pid,name,namex,label,"PID")

		self.editor.i_cnv=self.load_symbol(pos,i,self.editor.i_cnv,name,namex,label,"Convergencia")
		self.editor.i_dvg=self.load_symbol(pos,i,self.editor.i_cnv,name,namex,label,"Divergencia")
		self.editor.i_tgI=self.load_symbol(pos,i,self.editor.i_tgI,name,namex,label,"TAG(Entrada)")
		self.editor.i_tgO=self.load_symbol(pos,i,self.editor.i_tgO,name,namex,label,"TAG(Salida)")
	
	def dynamic_sim_file(self,xmlReader):
		while not(xmlReader.atEnd()):
			if(xmlReader.isEndElement()):
				xmlReader.readNext()
				break
			elif(xmlReader.isStartElement()):
				if xmlReader.name()=="ItemList":
					xmlReader.readNext()
					while not(xmlReader.atEnd()):
						if(xmlReader.isEndElement()):
							xmlReader.readNext()
							break
						elif(xmlReader.isStartElement()):
							while not(xmlReader.atEnd()):
								if(xmlReader.isEndElement()):
									xmlReader.readNext()
									break
								elif(xmlReader.isStartElement()):
									print("Start:"+str(xmlReader.name()))
									attributes=xmlReader.attributes()
									x_coord=float(attributes.value("xCoord"))
									y_coord=float(attributes.value("yCoord"))
									label_text=str(attributes.value("Label"))
									
									aux=str(xmlReader.name())
									aux=re.sub("_", " ",aux)
									name=re.sub("\d+", "", aux)
									i=re.sub('([a-zA-Z]+)', "", aux)
									i=re.sub('[(){}<>]', "", i)
									i=int(i)
									pos=QtCore.QPoint(x_coord,y_coord)
									self.load_items(name,i,pos,label_text)
									xmlReader.readNext()

						else:
							xmlReader.readNext()

				elif xmlReader.name()=="Connections":
					xmlReader.readNext()
					while not(xmlReader.atEnd()):
						if(xmlReader.isEndElement()):
							xmlReader.readNext()
							break
						elif(xmlReader.isStartElement()):
							while not(xmlReader.atEnd()):
								if(xmlReader.isEndElement()):
									xmlReader.readNext()
									break
								elif(xmlReader.isStartElement()):
									print("Start:"+str(xmlReader.name()))
									attributes=xmlReader.attributes()
									print(attributes.value("fromPort"))
									for items in self.editor.diagramScene.item_list:
										if hasattr(items,"outputs"):
											for outputs in items.outputs:
												if outputs.name_port==str(attributes.value("fromPort")) and  outputs.name_block==str(attributes.value("fromDevice")):
													port1=outputs
										if hasattr(items,"inputs"):
											for inputs in items.inputs:
												if inputs.name_port==str(attributes.value("toPort")) and  inputs.name_block==str(attributes.value("toDevice")):
													port2=inputs
									self.startedConnection=Connection(port1, None,self.editor)
									self.startedConnection.setEndPos(port2.scenePos())
									self.startedConnection.setToPort(port2)
									connections=[port1.name_block, port2.name_block,port1.name_port,port2.name_port]
									self.editor.array_connections.append(connections)
									Devices.array_connections=self.editor.array_connections

									self.editor.connection_painter(self.startedConnection,port2,port1)

									xmlReader.readNext()

						else:
							xmlReader.readNext()
				else:
					xmlReader.readNext()

			else:
				xmlReader.readNext()




	def ceniprof_file(self,xmlReader):
		
		while not(xmlReader.atEnd()):			
			if(xmlReader.isEndElement()):
				xmlReader.readNext()
				break
			elif(xmlReader.isStartElement()):
				print("Start:"+str(xmlReader.name()))
				if xmlReader.name()=="activity":
					while not(xmlReader.atEnd()):
						if(xmlReader.isEndElement()):
							xmlReader.readNext()
							break
						elif(xmlReader.isStartElement()):
							print("EQUIPO")
							attributes=xmlReader.attributes()
							name=self.name_convertion(str(attributes.value("TipoControl")))
							label_text=attributes.value("label")
							xy=(attributes.value("xy")).split(" ")
							i=int(attributes.value("id"))
							
							pos=QtCore.QPoint(float(xy[0]),float(xy[1]))
							self.load_items(name,i,pos,label_text)
							xmlReader.readNext()
						else:
							xmlReader.readNext()
				elif xmlReader.name()=="flow":

					while not(xmlReader.atEnd()):
						if(xmlReader.isEndElement()):
							xmlReader.readNext()
							break
						elif(xmlReader.isStartElement()):
							print("COnnections")
							attributes=xmlReader.attributes()
							connector=["","","",""]
							for items in self.editor.diagramScene.item_list:
								name=re.sub("\d+", "", items.name_block)
								iD=re.sub('([a-zA-Z]+)', "", items.name_block)
								
								if int(attributes.value("to"))==int(iD):
									connector[1]=items.name_block
									toPort=self.port_convertion(name,int(attributes.value("IdpuertoTO")))
									connector[3]=toPort
									if hasattr(items,"inputs"):
										for inputs in items.inputs:
											if inputs.name_port==connector[3] and  inputs.name_block==connector[1]:
												port2=inputs
									if hasattr(items,"outputs"):
										for outputs in items.outputs:
											if outputs.name_port==connector[3] and  outputs.name_block==connector[1]:
												port2=outputs
									print(port2.name_port)
									
								if int(attributes.value("fromID"))==int(iD):
									connector[0]=items.name_block
									fromPort=self.port_convertion(name,int(attributes.value("Idpuertofrom")))
									connector[2]=fromPort
									if hasattr(items,"inputs"):
										for inputs in items.inputs:
											if inputs.name_port==connector[2] and  inputs.name_block==connector[0]:
												port1=inputs
									if hasattr(items,"outputs"):
										for outputs in items.outputs:
											if outputs.name_port==connector[2] and  outputs.name_block==connector[0]:
												port1=outputs

							self.startedConnection=Connection(port1, None,self.editor)
							self.startedConnection.setEndPos(port2.scenePos())
							self.startedConnection.setToPort(port2)
							connections=[port1.name_block, port2.name_block,port1.name_port,port2.name_port]
							self.editor.array_connections.append(connections)
							Devices.array_connections=self.editor.array_connections

							self.editor.connection_painter(self.startedConnection,port2,port1)

							xmlReader.readNext()
						else:
							xmlReader.readNext()
				else:
					xmlReader.readNext()
			else:
				xmlReader.readNext()
	
	def read(self,editor):
		global Connection
		from Dynamic_simulator import Connection

		self.editor=editor
		filename = QtGui.QFileDialog.getOpenFileName(self.editor, 'Exportar archivo','', "*.xml")
		if filename:
			
			file=QFile (filename)
			if not (file.open(QIODevice.ReadOnly)):
				return

			xmlReader =QXmlStreamReader(filename)
			xmlReader.setDevice(file);
			xmlReader.readNext();

			while not(xmlReader.atEnd()):

				if(xmlReader.isStartElement()):
					print("Init:"+str(xmlReader.name()))
					if xmlReader.name()=="Dynamic_Simulator":
						xmlReader.readNext()
						self.dynamic_sim_file(xmlReader)
					elif xmlReader.name()=="Ceniprof":
						xmlReader.readNext()
						self.ceniprof_file(xmlReader)
					else:
						xmlReader.readNext()
					
				else:
					xmlReader.readNext()

			file.close()
			Resultado=QtGui.QDialog()
			QtGui.QMessageBox.information(Resultado,'Ok',_translate("Dialog","Archivo abierto correctamente.",None),QtGui.QMessageBox.Ok)