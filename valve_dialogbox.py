# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'valve_dialogbox.ui'
#
# Created: Mon Jul 24 11:13:48 2017
#      by: PyQt4 UI code generator 4.10.2

# Installed Libs
import re

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.ticker import FormatStrFormatter

# Local Libs
from dynamic_diagrams import DynamicGraphic
from streams import *
from valves import *
from global_data import *

#global values
global Enable_cursor
global Valve_model_data
global Cv_or_Kv
global one_time
global one_reload
global id_time

Valve_model_data="Diametro"
Cv_or_Kv="Coeficientes Cv"
Enable_cursor=False
one_time=1
one_reload=1
id_time=0

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
		return QtGui.QApplication.translate(context, text, disambig)

## -- Text field number validator -- ##
class Validator(object):
	def NumValidator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,100000,2,LineEdit))

## Evaluate devices connected in the valve inputs
def adquire_data_device_connected(device_connected):
	stream_data=[]
	type_flow=""
	Fluid_in_name=""

	if device_connected[:-1]=="Flujo":
		fields="Name,_Type,Flow,Temperature,Brix,Purity,Insoluble_solids,pH,Pressure,Saturated_vapor"
		result=db.read_data("Flow_inputs",fields,"LAST","Name")
		if len(result)>0:	
			for data in result:
				for i,values in enumerate(data):
					if  str(data[0])=="Fj"+re.sub('([a-zA-Z]+)', "", device_connected) and str(data[1])=="Juice":
						type_flow=str(data[1])
						Fluid_in_name=str(data[0])
						if i>1:
							stream_data.append(str(values))
					elif str(data[0])=="Fv"+re.sub('([a-zA-Z]+)', "", device_connected) and str(data[1])=="Vapor":
						type_flow=str(data[1])
						Fluid_in_name=str(data[0])
						if i>1:
							stream_data.append(str(values))
	
	return stream_data,type_flow,Fluid_in_name

## Timer for solve valve model and plot valve data
def update_figure():
	global tt

	global Valve
	global id_time
	global one_reload
	global one_time

	global stream_in
	global stream_out

	global Coefficient_min
	global Coefficient_max

	global create_stream
	global init_M
	global init_P
	global pin_value
	global pout_value
	Controller_in=None
	Fluid_in=None
	
	controller_data=[]

	# print("LENTOOOO: ")

	if hasattr(Devices, 'array_connections'):		
		if len(Devices.array_connections)>0:
			for k, par_data in enumerate(Devices.array_connections):
				
				if par_data[1]==nameDialog:
					device_connected=par_data[0]
					port_connected=par_data[2]
					
					if par_data[3]=="Fluido de entrada":
						for items in  Devices.panel_items:
							for outputs in items.outputs:
								if outputs.name_port==port_connected and  outputs.name_block==device_connected:
									port=outputs
									break
									break

						item_valve.outputs[0].typ=port.typ
						item_valve.outputs[0].port_color=port.port_color
						item_valve.outputs[0].setBrush(QBrush(port.port_color))	
						Fluid_in=device_connected

					if par_data[3]=="Apertura de valvula":
						Controller_in="PID"+re.sub('([a-zA-Z]+)', "", device_connected)
						Manipulated_Valve_Opening.setDisabled(True)
		
		if hasattr(Db_data, 'time_id'):

			new_id=False
			if int(Db_data.time_id)>int(id_time):
				new_id=True
			
			id_time=Db_data.time_id
			time=Db_data.time

			if time!="stop" and new_id==True:

				if one_reload==1:
					Graph.reload_toolbar(False)
					one_reload=0
				
				

				stream_data,type_flow,Fluid_in_name=adquire_data_device_connected(Fluid_in)
				
				if Controller_in!=None:
					fields="SP,MV,PV"
					result=db.read_data("Controllers",fields,"Name",Controller_in)
					if len(result)>0:
						Manipulated_Valve_Opening.setSingleStep(1.1)
						for data in result:
							for i,values in enumerate(data):
								controller_data.append(str(values))
						if controller_data[1]!="None":
							Ap=float(controller_data[1])
							if Ap>100.0:
								Ap=100.0
							elif Ap<10.0:
								Ap=10.0
						else:
							Ap=Ap_initial

					else:
						Manipulated_Valve_Opening.setSingleStep(10)
						Ap=Manipulated_Valve_Opening.value()
				else:
					Manipulated_Valve_Opening.setSingleStep(10)
					Ap=Manipulated_Valve_Opening.value()
				
				item_valve.label_Ap.setPlainText("Ap:"+str(round(Ap,2))+"%")
				Manipulated_Valve_Opening.setValue(Ap)
				db.update_data("Valves",["Ap"],[Ap/100.0],["id"],[id_valve])	
				# print("juice")
				# print("vapor")
				
				if len(stream_data)>0:
					if type_flow=="Juice":
						Min=float(stream_data[0])	
						Tin=float(stream_data[1])
						Bin=float(stream_data[2])
						Zin=float(stream_data[3])
						SolIn=float(stream_data[4])
						pHin=float(stream_data[5])
						Pin=float(stream_data[6])
						sat=stream_data[7]
					else:
						Min=float(stream_data[0])
						Tin=float(stream_data[1])
						Pin=float(stream_data[6])
						sat=stream_data[7]

					Stream_exist=hasattr(Valve,'stream_in')
					Stream_change=(Min!=init_M or Pin!=init_P)

					if Type_valve=="Fluidos" and Stream_change==True:
						if create_stream==1:
							stream_in.update(Min,Pin,Tin,Bin,Zin,SolIn,pHin)
							stream_out.update(Min,Pin-400.0,Tin,Bin,Zin,SolIn,pHin)
						else:
							stream_in=juice(Min,Pin,Tin,Bin,Zin,SolIn,pHin)
							stream_out=juice(Min,Pin-400.0,Tin,Bin,Zin,SolIn,pHin)
							create_stream=1

						init_M=(stream_in.Mj)
						init_P=(stream_in.Pj)

					elif Type_valve=="Gases" and Stream_change==True:
						
						if create_stream==1:
							if sat=="1.0":
								stream_in.update(Min,Pin,None)
								stream_out.update(Min,Pin-400.0,None)
						else:
							if sat=="1.0":
								stream_in=vapor(Min,Pin,None)
								stream_out=vapor(Min,Pin-400.0,None)
							create_stream=1

						
						init_M=(stream_in.Mv)
						init_P=(stream_in.Pv)

					
					# print("Min: "+str(stream_in.Mj*3.6)+" Mout: "+str(stream_out.Mj*3.6))

					tt.append(float(time))

					# Ap=controller_data[1]
					# Ap=0.333
					# print("Aperture: "+str(Ap/100.0))
					# Ap=0.333

					Valve.in_out(stream_in, stream_out, Ap/100.0)
					strm_in, strm_out = Valve.solve([tt[-2],tt[-1]],Valve_model_data,Coefficient_min,Coefficient_max)

					stream_in = strm_in
					stream_out = strm_out						
					if Type_valve=="Fluidos":
						pin_value.append(strm_in.Pj)
						pout_value.append(strm_out.Pj)
					else:
						pin_value.append(strm_in.Pv)
						pout_value.append(strm_out.Pv)

					# print("len: "+str(len(tt))+" "+str(len(pout_value)))
					if len(tt)==len(pout_value):
						ax=Graph.figure.get_axes()
						ax[0].plot(tt,pout_value,'r-',label="Pout")
						Graph.add_plot(tt,[pin_value],["Pin"],[0.0],[1.0])
						Graph.set_legends()
						Graph.draw()

						# ax[0].legend_.remove()
						for x,line in enumerate(ax[0].lines): 
							del ax[0].lines[x]


					fields="In_flow"
					result=db.read_data("Valves",fields,"Name","Vlv"+Num_window)
					if len(result)>0:
						for data in result:
							Mv_consumed=str(data[0])
							# print("Mv consumde: "+Mv_consumed)
						db.update_data("Flow_inputs",["Flow"],[Mv_consumed],["Name"],[Fluid_in_name])
					
					fields="Time_exec_id,Valves_id,Out_flow,Out_temperature,Out_brix,Out_purity,Out_insoluble_solids,Out_pH,Out_pressure,Out_saturated_vapor"
					if Type_valve=="Fluidos":
						# print("Min: "+str(stream_in.Mj*3.6)+" Mout: "+str(stream_out.Mj*3.6))
						# print("Pin: "+str(stream_in.Pj)+" Pout: "+str(stream_out.Pj))

						InFluid_Flow.setText(str(round(stream_in.Mj*3.6,3)))
						InFluid_Press.setText(str(round(stream_in.Pj/1000.0,3)))
						OutFluid_Flow.setText(str(round(stream_out.Mj*3.6,3)))
						OutFluid_Press.setText(str(round(stream_out.Pj/1000.0,3)))

						values=[id_time,id_valve,stream_out.Mj,stream_out.Tj,stream_out.Bj,stream_out.Zj,stream_out.Ij,stream_out.pHj,stream_out.Pj,sat]
						db.insert_data("Outputs_valve",fields,values)
					else:
						# print("Mvin: "+str(stream_in.Mv*3.6)+" Mvout: "+str(stream_out.Mv*3.6))
						# print("Pvin: "+str(stream_in.Pv)+" Pvout: "+str(stream_out.Pv))

						InFluid_Flow.setText(str(round(stream_in.Mv*3.6,3)))
						InFluid_Press.setText(str(round(stream_in.Pv/1000.0,3)))
						OutFluid_Flow.setText(str(round(stream_out.Mv*3.6,3)))
						OutFluid_Press.setText(str(round(stream_out.Pv/1000.0,3)))

						values=[id_time,id_valve,stream_out.Mv,stream_out.Tv,"","","","",stream_out.Pv,sat]
						db.insert_data("Outputs_valve",fields,values)

					one_time=1

			elif one_time==1 and time=="stop":
				tt=[0.0]
				pout_value=[100000.0]
				pin_value=[100000.0]
				Manipulated_Valve_Opening.setValue(Ap_initial)
				db.update_data("Valves",["Ap","In_flow"],[Ap_initial/100.0,0.0],["id"],[id_valve])

				ax=Graph.figure.get_axes()
				for x,line in enumerate(ax[0].lines): 
					del ax[0].lines[x]
				for x,line in enumerate(ax[1].lines): 
					del ax[1].lines[x]

				Enable_cursor=True
				Graph.reload_toolbar(Enable_cursor)

				one_time=0
				one_reload=1

##Function for update window when closing
def update_window():
	global one_reload
	global one_time
	global Num_window
	global Ap
	global Ap_initial

	global Type_valve

	Num_window=re.sub('([a-zA-Z]+)', "", nameDialog)

	fields="_Type,Ap_init,Diameter,Coeff_type,Coeff_min,Coeff_max,Ap"
	result=db.read_data("Valves",fields,"Name","Vlv"+Num_window)
	valve_data=[]
	if len(result)>0:
		for data in result:
			for values in data:
				valve_data.append(str(values))

		Type_valve=valve_data[0]	
		Ap_initial=float(valve_data[1])
		Diameter=valve_data[2]
		Coeff_type=valve_data[3]
		Coefficient_min=valve_data[4]
		Coefficient_max=valve_data[5]
		Ap=float(valve_data[6])*100.0


		Manipulated_Valve_Opening.setValue(Ap)
		index = ComBox_Valve_Type.findText(Type_valve, QtCore.Qt.MatchFixedString)
		ComBox_Valve_Type.setCurrentIndex(index)
		
		if Coeff_type=="None":
			index = ComBox_Diameter_or_FlowCoeff.findText("Diametro", QtCore.Qt.MatchFixedString)
			Valve_Diameter.setText(Diameter)

			Valve_Diameter.setEnabled(True)
			label_Valve_Diameter.setEnabled(True)
			ComBox_Cv_or_Kv.setDisabled(True)
			label_Max_Coeff_Flow.setDisabled(True)
			Max_Coeff_Flow.setDisabled(True)
			label_Min_Coeff_Flow.setDisabled(True)
			Min_Coeff_Flow.setDisabled(True)

		else:
			index = ComBox_Diameter_or_FlowCoeff.findText("Coeficientes de flujo", QtCore.Qt.MatchFixedString)
			Min_Coeff_Flow.setText(Coefficient_min)
			Max_Coeff_Flow.setText(Coefficient_max)

			label_Valve_Diameter.setDisabled(True)
			Valve_Diameter.setDisabled(True)
			ComBox_Cv_or_Kv.setEnabled(True)
			label_Max_Coeff_Flow.setEnabled(True)
			Max_Coeff_Flow.setEnabled(True)
			label_Min_Coeff_Flow.setEnabled(True)
			Min_Coeff_Flow.setEnabled(True)


		ComBox_Diameter_or_FlowCoeff.setCurrentIndex(index)
		Initial_Valve_Opening.setText(str(Ap_initial))
	
	if hasattr(Db_data, 'time'):
		
		if Db_data.time!="stop":
			Enable_cursor=False
		else:
			Enable_cursor=True

		one_time=1
		one_reload=0

def exist_initialization(data):
	global id_valve
	flg=0
	result=db.read_data("Valves","id","Name",data)
	if len(result)>0:
		for data in result:
			id_valve=data[0]
		flg=1
		

	return flg
##-- Class for confirm parameters --## 
class window_confirm_param(QDialog):
	def __init__(self, parent=None):
		

		super(window_confirm_param, self).__init__(parent)
		self.setWindowTitle("Confirmar parametros")
		self.button = QPushButton('Aceptar', self)
		self.button2 = QPushButton('Cancelar', self)
		self.label_Message = QtGui.QLabel('Esta seguro que desea confirmar estos parametros?',self)
		l = QHBoxLayout(self)
		l.addWidget(self.label_Message)
		l.addWidget(self.button)
		l.addWidget(self.button2)
		self.button.clicked.connect(self.OK)
		self.button2.clicked.connect(self.NO)
	def OK(self):
		global id_valve

		global tt
		global stream_in
		global init_M
		global init_P
		global stream_out
		global Valve
		global Type_valve
		global Num_window

		global create_stream
		global pout_value
		global pin_value

		global Coefficient_min
		global Coefficient_max

		global Ap_initial

		Num_window=re.sub('([a-zA-Z]+)', "", nameDialog)

		Type_valve=str(ComBox_Valve_Type.currentText())
		Ap_initial=float(Initial_Valve_Opening.text())
		Manipulated_Valve_Opening.setValue(Ap_initial)
		Ap=Manipulated_Valve_Opening.value()/100.0
		Diameter=8.0
		Coefficient_min=None
		Coefficient_max=None
		init_M=0
		init_P=0

		item_valve.label_Ap.setPlainText("Ap:"+str(Ap*100.0)+"%")	

		if Valve_model_data=="Diametro":
			fields="Name,_Type,Ap_init,Diameter,In_flow,Ap"
			
			Diameter=float(Valve_Diameter.text())
			values=["Vlv"+Num_window,Type_valve,Ap_initial,Diameter,0.0,Ap]
		else:
			fields="Name,_Type,Ap_init,Coeff_type,Coeff_min,Coeff_max,In_flow,Ap"
			
			Coeff_type=str(Cv_or_Kv)
			Coefficient_min=float(Min_Coeff_Flow.text())
			Coefficient_max=float(Max_Coeff_Flow.text())
			values=["Vlv"+Num_window,Type_valve,Ap_initial,Coeff_type,Coefficient_min,Coefficient_max,0.0,Ap]
		

		updt=exist_initialization("Vlv"+Num_window)
		
		if updt==0:		
			db.insert_data("Valves",fields,values)

			result=db.read_data("Valves","id","Name","Vlv"+Num_window)
			if len(result)>0:
				for data in result:
					id_valve=data[0]

			if ComBox_Valve_Type.currentText()=="Fluidos":
				create_stream=0
				# stream_in=juice(100/3.6,200*(10**3),115, 0.15,0.85,0.00,7)
				# stream_out=juice(stream_in.Mj*0.9,stream_in.Pj-400.0,115, 0.15,0.87,0.00,7)
				# init_M=stream_in.Mj
				# init_P=stream_in.Pj
				Valve=valve_liquid(Diameter*0.0254,Ap_initial/100.0)
				print(Valve.Ap)
			else:
				create_stream=0
				# stream_in=vapor(100/3.6,134*(10**3),None)
				# stream_out=vapor(stream_in.Mv*0.9,stream_in.Pv-400.0,None)
				Valve=valve_vapor(Diameter*0.0254,Ap_initial/100.0)
		else:
			if Valve_model_data=="Diametro":
				fields=["Name","_Type","Ap_init","Diameter","In_flow","Ap"]
				db.update_data("Valves",fields,values,["id"],[float(id_valve)])
			else:
				fields=["Name","_Type","Ap_init","Coeff_type","Coeff_min","Coeff_max","In_flow","Ap"]
				db.update_data("Valves",fields,values,["id"],[float(id_valve)])

			if ComBox_Valve_Type.currentText()=="Fluidos":
				create_stream=0
				# stream_in.update(100/3.6,200*(10**3),115, 0.15,0.85,0.00,7)
				# stream_out.update(stream_in.Mj*0.9,stream_in.Pj-400.0,115, 0.15,0.87,0.00,7)
				# init_M=stream_in.Mj
				# init_P=stream_in.Pj
				Valve.update(Diameter*0.0254,Ap_initial/100.0)
				print(Valve.Ap)
			else:
				create_stream=0
				# stream_in.update(100/3.6,134*(10**3),None)
				# stream_out.update(stream_in.Mv*0.9,stream_in.Pv-400.0,None)
				Valve.update(Diameter*0.0254,Ap_initial/100.0)
		tt=[0.0]
		pout_value=[100000.0]
		pin_value=[100000.0]
		# Ui_Dialog.Timer_graph()
		self.close()
		Resultado=QtGui.QDialog()
		QtGui.QMessageBox.information(Resultado,'Ok',_translate("Dialog","Instanciación correcta de datos.",None),QtGui.QMessageBox.Ok)
		Dialog_window.close()
		

	
	def NO(self):
		self.close()

## Dialog box class
class Ui_Dialog(object):

	#Evaluate all data for correct valve initialization
	def confirm_param(self):
		global confirm
		global Resultado
		global pd

		if Valve_model_data=="Diametro":
			confirm=( len(Valve_Diameter.text())>0 and len(Initial_Valve_Opening.text())>0 )
		elif Valve_model_data=="Coeficientes de flujo":
			confirm=( len(Min_Coeff_Flow.text())>0 and len(Max_Coeff_Flow.text())>0 and len(Initial_Valve_Opening.text())>0 )
		
		if ComBox_Valve_Type.currentText()!="--Tipo de valvula--" and confirm==True:
			Resultado=QtGui.QDialog()
			pd = window_confirm_param(Resultado.window())
			pd.exec_()
		else:
			self.Resultado=QtGui.QDialog()
			QtGui.QMessageBox.warning(self.Resultado, 
			'Advertencia',
			"Falta por ingresar algun dato.",QtGui.QMessageBox.Ok)

	#Objects in dialog box
	def setupUi(self,name,ts,Data_Base,item,Dialog):
		global Ts
		global title_name
		global nameDialog
		global db
		global Dialog_window
		global item_valve


		global ComBox_Valve_Type
		global ComBox_Diameter_or_FlowCoeff
		global ComBox_Cv_or_Kv
		global Manipulated_Valve_Opening

		global Valve_Diameter
		global label_Valve_Diameter
		global Initial_Valve_Opening
		global Max_Coeff_Flow
		global label_Max_Coeff_Flow
		global Min_Coeff_Flow
		global label_Min_Coeff_Flow

		global InFluid_Flow
		global InFluid_Press

		global OutFluid_Flow
		global OutFluid_Press

		global Graph


		Dialog_window=Dialog
		Ts=ts
		nameDialog=name
		db=Data_Base
		item_valve=item
		
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(542, 353)

		Validation_text_field = Validator()

		title_name=str(item.label.toPlainText())
		
		self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
		self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
		
	##----Selector of valve type----##	
		ComBox_Valve_Type = QtGui.QComboBox(Dialog)
		ComBox_Valve_Type.setObjectName(_fromUtf8("ComBox_Valve_Type"))
		ComBox_Valve_Type.addItem("--Tipo de valvula--")
		ComBox_Valve_Type.addItem("Fluidos")
		ComBox_Valve_Type.addItem("Gases")
		self.verticalLayout_3.addWidget(ComBox_Valve_Type)
		self.Valve_tabWidget = QtGui.QTabWidget(Dialog)
		self.Valve_tabWidget.setObjectName(_fromUtf8("Valve_tabWidget"))
		
	##--Tab widget--##
		self.Valve_tab_1 = QtGui.QWidget()
		self.Valve_tab_1.setObjectName(_fromUtf8("Valve_tab_1"))
		self.Valve_tabWidget.addTab(self.Valve_tab_1, _fromUtf8(""))
		
		self.Valve_tab_2 = QtGui.QWidget()
		self.Valve_tab_2.setObjectName(_fromUtf8("Valve_tab_2"))
		self.Valve_tabWidget.addTab(self.Valve_tab_2, _fromUtf8(""))
		
		self.Valve_tab_3 = QtGui.QWidget()
		self.Valve_tab_3.setObjectName(_fromUtf8("Valve_tab_3"))
		self.Valve_tabWidget.addTab(self.Valve_tab_3, _fromUtf8(""))


	##----Instantiation of elements for physical properties----##
		self.gridLayout_2 = QtGui.QGridLayout(self.Valve_tab_1)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))

		self.Phisycal_Properties_GrBx = QtGui.QGroupBox(self.Valve_tab_1)
		self.Phisycal_Properties_GrBx.setObjectName(_fromUtf8("Phisycal_Properties_GrBx"))
		self.verticalLayout = QtGui.QVBoxLayout(self.Phisycal_Properties_GrBx)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.label = QtGui.QLabel(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout.addWidget(self.label)

		#Selector Diameter or Flow coefficient
		ComBox_Diameter_or_FlowCoeff = QtGui.QComboBox(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(ComBox_Diameter_or_FlowCoeff.sizePolicy().hasHeightForWidth())
		ComBox_Diameter_or_FlowCoeff.setSizePolicy(sizePolicy)
		ComBox_Diameter_or_FlowCoeff.setObjectName(_fromUtf8("ComBox_Diameter_or_FlowCoeff"))
		ComBox_Diameter_or_FlowCoeff.addItem("Diametro")
		ComBox_Diameter_or_FlowCoeff.addItem("Coeficientes de flujo")
		ComBox_Diameter_or_FlowCoeff.activated.connect(self.selection_valve_data)
		self.horizontalLayout.addWidget(ComBox_Diameter_or_FlowCoeff)
		self.verticalLayout.addLayout(self.horizontalLayout)

		#Valve diameter
		self.gridLayout = QtGui.QGridLayout()
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		label_Valve_Diameter = QtGui.QLabel(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(label_Valve_Diameter.sizePolicy().hasHeightForWidth())
		label_Valve_Diameter.setSizePolicy(sizePolicy)
		label_Valve_Diameter.setObjectName(_fromUtf8("label_Valve_Diameter"))
		label_Valve_Diameter.setEnabled(True)
		self.gridLayout.addWidget(label_Valve_Diameter, 0, 0, 1, 1)
		
		Valve_Diameter = QtGui.QLineEdit(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Valve_Diameter.sizePolicy().hasHeightForWidth())
		Valve_Diameter.setSizePolicy(sizePolicy)
		Valve_Diameter.setObjectName(_fromUtf8("Valve_Diameter"))
		Valve_Diameter.setEnabled(True)
		Validation_text_field.NumValidator(Valve_Diameter)
		
		#Selector Cv or Kv coefficient
		self.gridLayout.addWidget(Valve_Diameter, 0, 1, 1, 1)
		ComBox_Cv_or_Kv = QtGui.QComboBox(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(ComBox_Cv_or_Kv.sizePolicy().hasHeightForWidth())
		ComBox_Cv_or_Kv.setSizePolicy(sizePolicy)
		ComBox_Cv_or_Kv.setObjectName(_fromUtf8("ComBox_Cv_or_Kv"))
		ComBox_Cv_or_Kv.addItem("Coeficientes Cv")
		ComBox_Cv_or_Kv.addItem("Coeficientes Kv")
		ComBox_Cv_or_Kv.activated.connect(self.selection_Cv_or_Kv)
		ComBox_Cv_or_Kv.setDisabled(True)
		self.gridLayout.addWidget(ComBox_Cv_or_Kv, 0, 2, 1, 2)
		
		#Min flow coefficient
		label_Min_Coeff_Flow = QtGui.QLabel(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(label_Min_Coeff_Flow.sizePolicy().hasHeightForWidth())
		label_Min_Coeff_Flow.setSizePolicy(sizePolicy)
		label_Min_Coeff_Flow.setObjectName(_fromUtf8("label_Min_Coeff_Flow"))
		label_Min_Coeff_Flow.setDisabled(True)
		self.gridLayout.addWidget(label_Min_Coeff_Flow, 1, 2, 1, 1)
		
		Min_Coeff_Flow = QtGui.QLineEdit(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Min_Coeff_Flow.sizePolicy().hasHeightForWidth())
		Min_Coeff_Flow.setSizePolicy(sizePolicy)
		Min_Coeff_Flow.setObjectName(_fromUtf8("Min_Coeff_Flow"))
		Min_Coeff_Flow.setDisabled(True)
		Validation_text_field.NumValidator(Min_Coeff_Flow)
		self.gridLayout.addWidget(Min_Coeff_Flow, 1, 3, 1, 1)

		#Max flow coefficient
		label_Max_Coeff_Flow = QtGui.QLabel(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(label_Max_Coeff_Flow.sizePolicy().hasHeightForWidth())
		label_Max_Coeff_Flow.setSizePolicy(sizePolicy)
		label_Max_Coeff_Flow.setObjectName(_fromUtf8("label_Max_Coeff_Flowe"))
		label_Max_Coeff_Flow.setDisabled(True)
		self.gridLayout.addWidget(label_Max_Coeff_Flow, 2, 2, 1, 1)
		
		Max_Coeff_Flow = QtGui.QLineEdit(self.Phisycal_Properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Max_Coeff_Flow.sizePolicy().hasHeightForWidth())
		Max_Coeff_Flow.setSizePolicy(sizePolicy)
		Max_Coeff_Flow.setObjectName(_fromUtf8("Max_Coeff_Flow"))
		Max_Coeff_Flow.setDisabled(True)
		Validation_text_field.NumValidator(Max_Coeff_Flow)
		self.gridLayout.addWidget(Max_Coeff_Flow, 2, 3, 1, 1)
		self.verticalLayout.addLayout(self.gridLayout)
		self.gridLayout_2.addWidget(self.Phisycal_Properties_GrBx, 0, 0, 1, 2)
		
	##----Instantiation of elements for the initial condition----##
		self.Initial_Conditions_GrBx = QtGui.QGroupBox(self.Valve_tab_1)
		self.Initial_Conditions_GrBx.setObjectName(_fromUtf8("Initial_Conditions_GrBx"))
		self.verticalLayout_2 = QtGui.QVBoxLayout(self.Initial_Conditions_GrBx)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

		#Initial valve openning
		self.label_Initial_Valve_Opening = QtGui.QLabel(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Initial_Valve_Opening.sizePolicy().hasHeightForWidth())
		self.label_Initial_Valve_Opening.setSizePolicy(sizePolicy)
		self.label_Initial_Valve_Opening.setObjectName(_fromUtf8("label_Initial_Valve_Opening"))
		self.horizontalLayout_2.addWidget(self.label_Initial_Valve_Opening)
		
		Initial_Valve_Opening = QtGui.QLineEdit(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Initial_Valve_Opening.sizePolicy().hasHeightForWidth())
		Initial_Valve_Opening.setSizePolicy(sizePolicy)
		Initial_Valve_Opening.setReadOnly(False)
		Initial_Valve_Opening.setObjectName(_fromUtf8("Initial_Valve_Opening"))
		Validation_text_field.NumValidator(Initial_Valve_Opening)
		self.horizontalLayout_2.addWidget(Initial_Valve_Opening)
		self.verticalLayout_2.addLayout(self.horizontalLayout_2)
		self.gridLayout_2.addWidget(self.Initial_Conditions_GrBx, 1, 0, 1, 1)
		
	##--Instance button--##
		self.OKButton_Valve = QtGui.QPushButton(self.Valve_tab_1)
		self.OKButton_Valve.setObjectName(_fromUtf8("OKButton_Valve"))
		self.OKButton_Valve.clicked.connect(self.confirm_param)
		self.gridLayout_2.addWidget(self.OKButton_Valve, 1, 1, 1, 1)
		
	##----Instantiation of elements for input fluid----##
		self.gridLayout_3 = QtGui.QGridLayout(self.Valve_tab_2)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
		self.Input_fluid_GrBx = QtGui.QGroupBox(self.Valve_tab_2)
		self.Input_fluid_GrBx.setObjectName(_fromUtf8("Input_fluid_GrBx"))
		self.gridLayout_4 = QtGui.QGridLayout(self.Input_fluid_GrBx)
		self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
		#Flow
		self.label_InFluid_Flow = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Flow.setSizePolicy(sizePolicy)
		self.label_InFluid_Flow.setObjectName(_fromUtf8("label_InFluid_Flow"))
		self.gridLayout_4.addWidget(self.label_InFluid_Flow, 0, 0, 1, 1)
		InFluid_Flow = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Flow.sizePolicy().hasHeightForWidth())
		InFluid_Flow.setSizePolicy(sizePolicy)
		InFluid_Flow.setReadOnly(True)
		InFluid_Flow.setObjectName(_fromUtf8("InFluid_Flow"))
		self.gridLayout_4.addWidget(InFluid_Flow, 0, 1, 1, 1)
		#Pressure
		self.label_InFluid_Press = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Press.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Press.setSizePolicy(sizePolicy)
		self.label_InFluid_Press.setObjectName(_fromUtf8("label_InFluid_Press"))
		self.gridLayout_4.addWidget(self.label_InFluid_Press, 1, 0, 1, 1)
		InFluid_Press = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Press.sizePolicy().hasHeightForWidth())
		InFluid_Press.setSizePolicy(sizePolicy)
		InFluid_Press.setReadOnly(True)
		InFluid_Press.setObjectName(_fromUtf8("InFluid_Press"))
		self.gridLayout_4.addWidget(InFluid_Press, 1, 1, 1, 1)
		self.gridLayout_3.addWidget(self.Input_fluid_GrBx, 0, 0, 1, 1)
		
	##----Instantiation of elements for output fluid----##
		self.Output_fluid_GrBx = QtGui.QGroupBox(self.Valve_tab_2)
		self.Output_fluid_GrBx.setObjectName(_fromUtf8("Output_fluid_GrBx"))
		self.gridLayout_5 = QtGui.QGridLayout(self.Output_fluid_GrBx)
		self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
		#Flow
		self.label_OutFluid_Flow = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Flow.setSizePolicy(sizePolicy)
		self.label_OutFluid_Flow.setObjectName(_fromUtf8("label_OutFluid_Flow"))
		self.gridLayout_5.addWidget(self.label_OutFluid_Flow, 0, 0, 1, 1)
		OutFluid_Flow = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Flow.sizePolicy().hasHeightForWidth())
		OutFluid_Flow.setSizePolicy(sizePolicy)
		OutFluid_Flow.setReadOnly(True)
		OutFluid_Flow.setObjectName(_fromUtf8("OutFluid_Flow"))
		self.gridLayout_5.addWidget(OutFluid_Flow, 0, 1, 1, 1)
		#Pressure
		self.label_OutFluid_Press = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Press.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Press.setSizePolicy(sizePolicy)
		self.label_OutFluid_Press.setObjectName(_fromUtf8("label_OutFluid_Press"))
		self.gridLayout_5.addWidget(self.label_OutFluid_Press, 1, 0, 1, 1)
		OutFluid_Press = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Press.sizePolicy().hasHeightForWidth())
		OutFluid_Press.setSizePolicy(sizePolicy)
		OutFluid_Press.setReadOnly(True)
		OutFluid_Press.setObjectName(_fromUtf8("OutFluid_Press"))
		self.gridLayout_5.addWidget(OutFluid_Press, 1, 1, 1, 1)
		self.gridLayout_3.addWidget(self.Output_fluid_GrBx, 0, 1, 1, 1)
	
	##----Instantiation of elements for variable output---#
		self.verticalLayout_4 = QtGui.QVBoxLayout(self.Valve_tab_3)
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		#Openning
		self.label_Valve_Opening = QtGui.QLabel(self.Valve_tab_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Valve_Opening.sizePolicy().hasHeightForWidth())
		self.label_Valve_Opening.setSizePolicy(sizePolicy)
		self.label_Valve_Opening.setObjectName(_fromUtf8("label_Valve_Opening"))
		self.horizontalLayout_3.addWidget(self.label_Valve_Opening)
		Manipulated_Valve_Opening = QtGui.QSpinBox(self.Valve_tab_3)
		Manipulated_Valve_Opening.setSuffix('%')
		Manipulated_Valve_Opening.setSingleStep(10)
		Manipulated_Valve_Opening.setMinimum(10)
		Manipulated_Valve_Opening.setMaximum(100)
		Manipulated_Valve_Opening.setValue(30)

		Manipulated_Valve_Opening.setObjectName(_fromUtf8("Manipulated_Valve_Opening"))
		self.horizontalLayout_3.addWidget(Manipulated_Valve_Opening)
		self.verticalLayout_4.addLayout(self.horizontalLayout_3)

		##--Dynamic Graph--##
		Graph = DynamicGraphic(Dialog,Ts,Enable_cursor,False,False,self.Valve_tab_3, width=4, height=3, dpi=85)
		Graph.axes.set_xlabel('Time (s)',fontsize=11)
		Graph.axes.set_ylabel(_translate("Dialog", "Pout", None),fontsize=11)
		Graph.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		Graph.set_legends()

		self.Timer_graph()

		self.verticalLayout_4.addLayout(Graph.dynamic_graph)

		self.verticalLayout_3.addWidget(self.Valve_tabWidget)

		update_window()

		self.retranslateUi(Dialog)
		self.Valve_tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	# Timer initialization
	def Timer_graph(self):
		# global timer
		timer = QtCore.QTimer(Dialog_window)
		timer.timeout.connect(update_figure)
		timer.start(Ts*100)

	# Evaluate change in selection to Cv or Kv coefficientd
	def selection_Cv_or_Kv(self):
		global Cv_or_Kv
		Cv_or_Kv=ComBox_Cv_or_Kv.currentText()
		if Cv_or_Kv=="Coeficientes Cv":
			label_Min_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo mínimo\n[gpm/√psi]", None))
			label_Max_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo máximo\n[gpm/√psi]", None))

		elif Cv_or_Kv=="Coeficientes Kv":
			label_Min_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo mínimo\n[(m3/h)/√bar]", None))
			label_Max_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo máximo\n[(m3/h)/√bar]", None))

	# Evaluate change in data type 
	def selection_valve_data(self):
		global Valve_model_data
		Valve_model_data=ComBox_Diameter_or_FlowCoeff.currentText()
		if Valve_model_data=="Diametro":
			Valve_Diameter.setEnabled(True)
			label_Valve_Diameter.setEnabled(True)
			ComBox_Cv_or_Kv.setDisabled(True)
			label_Max_Coeff_Flow.setDisabled(True)
			Max_Coeff_Flow.setDisabled(True)
			label_Min_Coeff_Flow.setDisabled(True)
			Min_Coeff_Flow.setDisabled(True)
		elif Valve_model_data=="Coeficientes de flujo":
			label_Valve_Diameter.setDisabled(True)
			Valve_Diameter.setDisabled(True)
			ComBox_Cv_or_Kv.setEnabled(True)
			label_Max_Coeff_Flow.setEnabled(True)
			Max_Coeff_Flow.setEnabled(True)
			label_Min_Coeff_Flow.setEnabled(True)
			Min_Coeff_Flow.setEnabled(True)

	## Labels set text
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Datos "+title_name, None))
		self.Phisycal_Properties_GrBx.setTitle(_translate("Dialog", "Propiedades físicas", None))
		self.label.setText(_translate("Dialog", "Modelo de valvula por:", None))
		label_Valve_Diameter.setText(_translate("Dialog", "Diámetro[in]", None))
		label_Min_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo mínimo\n"
		"[gpm/√psi]", None))
		label_Max_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo máximo\n"
		"[gpm/√psi]", None))
		self.Initial_Conditions_GrBx.setTitle(_translate("Dialog", "Condiciones iniciales", None))
		self.label_Initial_Valve_Opening.setText(_translate("Dialog", "Apertura de válvula [%]", None))
		self.OKButton_Valve.setText(_translate("Dialog", "Aceptar", None))
		self.Valve_tabWidget.setTabText(self.Valve_tabWidget.indexOf(self.Valve_tab_1), _translate("Dialog", "Propiedades físicas", None))
		self.Input_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de entrada", None))
		self.label_InFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InFluid_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.Output_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de salida", None))
		self.label_OutFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_OutFluid_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.Valve_tabWidget.setTabText(self.Valve_tabWidget.indexOf(self.Valve_tab_2), _translate("Dialog", "Variables de proceso", None))
		self.label_Valve_Opening.setText(_translate("Dialog", "Porcentaje de apertura de valvula", None))
		self.Valve_tabWidget.setTabText(self.Valve_tabWidget.indexOf(self.Valve_tab_3), _translate("Dialog", "Variable manipulada", None))

