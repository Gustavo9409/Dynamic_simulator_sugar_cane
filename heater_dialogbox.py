# -*- coding: utf-8 -*- 

# Form implementation generated from reading ui file 'Heater_properties.ui'.
#
# Created: Thu Apr 27 15:14:40 2017
#      by: PyQt4 UI code generator 4.10.2

# Installed Libs
import random
import threading
import re
import math

from collections import defaultdict
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from numpy import arange, sin, pi
from decimal import Decimal
from matplotlib.ticker import FormatStrFormatter

# Local Libs
from heaters import *
from dynamic_diagrams import DynamicGraphic
from streams import *
from global_data import *

#global values
global time_1
global outout_1
global one_time
global one_reload
global ts
global time_exec
global model_value
global Heater_type
global SnT
global Enable_cursor
global split_model_data
global Flow_in_array
global flag_vapor_in
global flag_juice_in
global time
global id_time
global id_Heater
global juice_data
global vapor_data

juice_data=[]
vapor_data=[]
id_Heater=""
time=""
id_time=0
split_model_data_n1=None
Enable_cursor=False
Heater_type="Carcaza y tubos"
time_exec=[]
model_value=[]
Flow_in_array=[]
ts=0.0
time_1=0.0
outout_1=0.0
SnT=1.0
one_time=1
one_reload=0
flag_juice_in=""
flag_vapor_in=""

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

## Class number validation
class Validator(object):
	def NumValidator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,100000,2,LineEdit))

##Function for update database info 
def write_outputs_heater():
	global ht_model
	global flag_vapor_in

	global fluid_in
	global fluid_out
	global vapor_in
	global vapor_out

	global id_heater 
	global id_time

	if flag_vapor_in[:-1]=="Fv":
		field=["Flow"]
		db.update_data("Flow_inputs",field,[vapor_in.Mv],["Name"],[flag_vapor_in])
	
	elif flag_vapor_in[:-1]=="Vlv":
		field=["In_flow"]
		db.update_data("Valves",field,[vapor_in.Mv],["Name"],[flag_vapor_in])

	elif flag_vapor_in[:-1]=="Evp":
		field=["Out_vapor_flow"]
		db.update_data("Outputs_evaporator",field,[vapor_in.Mv],["Name","Time_exec_id"],[flag_vapor_in,id_time])


	db.insert_data("OUTPUTS_HEATER","Heaters_id,Out_fluid_temperature,Out_fluid_brix,Out_fluid_flow,Out_fluid_pH,Out_fluid_pressure"
	",Out_fluid_insoluble_solids,Out_fluid_purity,Condensed_vapor_flow,Condensed_vapor_temperature,Condensed_vapor_pressure,Time_exec_id",
	[id_Heater,fluid_out.Tj,fluid_out.Bj*100.0,fluid_out.Mj,fluid_out.pHj,fluid_out.Pj/1000.0,fluid_out.Ij*100.0,fluid_out.Zj,vapor_out.Mv,vapor_out.Tv,"",id_time])
	
	db.update_data("Physical_properties_heater",["Heat_area","Scalling_resistance","Juice_velocity","Inside_U","Outside_U","Overall_U"]
	,[ht_model.Aosc,ht_model.htc.Ri,ht_model.htc.vj,ht_model.htc.Ui,ht_model.htc.Uo,ht_model.U],["Heaters_id"],[id_Heater])

##Function for update process values
def write_process_values():
	global ht_model

	global fluid_in
	global fluid_out
	global vapor_in
	global vapor_out

	Temp_Output_variable.setText(str(round(fluid_out.Tj,3)))

	#Physical properties
	Juice_Velocity.setText(str(round(ht_model.htc.vj,3)))
	Heat_Area.setText(str(round(ht_model.Aosc,3)))
	Scalling_Resist.setText(str("{:.3E}".format(Decimal(ht_model.htc.Ri))))
	Overall_U.setText(str("{:.3E}".format(Decimal(ht_model.U))))
	Inside_U.setText(str("{:.3E}".format(Decimal(ht_model.htc.Ui))))
	Outside_U.setText(str("{:.3E}".format(Decimal(ht_model.htc.Uo))))
	
	#Vapor input
	InStm_Press.setText(str(round(vapor_in.Pv/1000.0,3)))
	InStm_Flow.setText(str(round(vapor_in.Mv*3.6,3)))
	InStm_Temp.setText(str(round(vapor_in.Tv,2)))
	#Vapor output
	CondStm_Flow.setText(str(round(float(vapor_out.Mv*3.6),3)))
	CondStm_Temp.setText(str(round(vapor_out.Tv,2)))
	#CondStm_Press.setText(str(round(Pvin/1000.0,1)))
	
	#Juice input
	InFluid_Temp.setText(str(fluid_in.Tj))
	InFluid_Flow.setText(str(float(fluid_in.Mj)*3.6))
	InFluid_pH.setText(str(fluid_in.pHj))
	InFluid_pressure.setText(str(round(fluid_in.Pj/1000.0,1)))
	InFluid_InsolubleSolids.setText(str(fluid_in.Ij*100.0))
	InFluid_Purity.setText(str(fluid_in.Zj*100.0))
	InFluid_Brix.setText(str(fluid_in.Bj*100.0))
	#Juice output
	OutFluid_Temp.setText(str(round(fluid_out.Tj,3)))
	OutFluid_Brix.setText(str(fluid_out.Bj*100.0))
	OutFluid_Flow.setText(str(float(fluid_out.Mj)*3.6))
	OutFluid_pH.setText(str(fluid_out.pHj))
	OutFluid_pressure.setText(str(round( (fluid_out.Pj/1000.0),3) ))
	OutFluid_InsolubleSolids.setText(str(fluid_out.Ij*100.0))
	OutFluid_Purity.setText(str(round(fluid_out.Zj*100.0,3)))
			
##Function for update window when closing
def Update_window():
	global num_window
	global heater_data
	global update
	global Enable_cursor
	global one_time
	global one_reload
	global id_Heater
	global Tjout_ini

	# id_Heater=""
	num_window=re.sub('([a-zA-Z]+)', "", nameDialog)
	
	heater_data2=[]
	
	type_heater=""
	Tjout_ini=""
	fields="Name,id,_Type,Tjout_init"
	result=db.read_data("Heaters",fields,None,None)
	if len(result)>0:
		for data in result:
			for i,values in enumerate(data):
				if  str(data[0])==("Ht"+str(num_window)):
					id_Heater=str(data[1])
					type_heater=str(data[2])
					Tjout_ini=str(data[3])

	fields="Pipe_x_Step,N_steps,Ext_pipe_diameter,Pipe_length,Pipe_thickness,Pipe_rough,Scalling_coeff,Operation_time"
	result=db.read_data("Physical_properties_heater",fields,"Heaters_id",id_Heater)
	if len(result)>0:
		for data in result:
			for values in data:
				heater_data2.append(str(values))
	heater_data2.append(Tjout_ini)

	if len(heater_data2)>0 and type_heater=="Carcaza y tubos":
		update=1
		Pipe_x_Step.setText(str(heater_data2[0]))
		N_steps.setText(str(heater_data2[1]))
		Ext_Pipe_Diameter.setText(str(heater_data2[2]))
		Length_Pipe.setText(str(heater_data2[3]))
		Pipe_Thickness.setText(str(heater_data2[4]))					
		Pipe_Rough.setText(str(heater_data2[5]))
		Scalling_Coeff.setText(str(heater_data2[6]))
		Time_Op.setText(str(heater_data2[7]))
		Initial_Out_Temp.setText(str(heater_data2[8]))
		##
		Selector_Heater_type.setCurrentIndex(1)
	
	elif len(heater_data2)>0 and type_heater=="Placas":
		Selector_Heater_type.setCurrentIndex(2)

	else:
		update=0
		print "no datos"

	if hasattr(Db_data, 'time'):
		write_process_values()
		if Db_data.time!="stop":
			Enable_cursor=False
		else:
			Enable_cursor=True

		one_time=1
		one_reload=0

##Function for confirm if exist initialization of heater
def exist_initialization(data):
	flg=0
	dats=[]

	result=db.read_data("Heaters","id","Name",data)
	if len(result)>0:
		for data in result:
			id_heater=data[0]
		flg=1

	return flg

##Evaluate devices connected in the heater inputs
def flag_inputs(device_connected,port_input,port_heater):
	flag=""
	
	flags={
	("Flujo","Fluido de entrada"):"Fj",
	("Flujo","Vapor de entrada"):"Fv",

	("Valvula","Fluido de entrada"):"Vlv",
	("Valvula","Vapor de entrada"):"Vlv",

	("Calentador","Fluido de entrada"):"Ht",
	("Evaporador","Vapor de entrada"):"Evp"
	}

	flags = defaultdict(lambda: -1, flags)

	flag=flags[device_connected[:-1],port_input]

	if flag!=-1 and port_input==port_heater:
		flag=flag+device_connected[len(device_connected)-1:]
	else:
		flag=""

	return flag

## Timer for solve heater model and plot heater data
def update_figure():
	global Graph
	global create_stream

	global timer
	global time_exec
	global model_value
	global split_model_data_n1
	global one_time
	global Enable_cursor
	global one_reload
	global Flow_in_array
	global yb_l
	global tt
	global u
	global ht_model
	global flag_juice_in
	global flag_vapor_in
	global id_time

	global vapor_data
	global juice_data

	global Vapor_input

	global fluid_in
	global fluid_out
	global vapor_in
	global vapor_out


	if hasattr(Devices, 'array_connections'):

		flag_juice_in=""
		flag_vapor_in=""
		
		if len(Devices.array_connections)>0:
			for k, par_data in enumerate(Devices.array_connections):
				if par_data[1]==nameDialog:
					device_connected=par_data[0]
					this_device=par_data[1]
					port_connected=par_data[2]
					port_this_device=par_data[3]

					for items in  Devices.panel_items:
						for outputs in items.outputs:
							if outputs.name_port==port_connected and outputs.name_block==device_connected :
								port=outputs
								if port_this_device=="Fluido de entrada":
									if hasattr(port,"port_color"):
										item_heater.outputs[0].typ=port.typ
										item_heater.outputs[0].port_color=port.port_color
										item_heater.outputs[0].setBrush(QBrush(port.port_color))
									break
					
					if flag_vapor_in=="":
						flag_vapor_in=flag_inputs(device_connected,"Vapor de entrada",port_this_device)
					if flag_juice_in=="":
						flag_juice_in=flag_inputs(device_connected,"Fluido de entrada",port_this_device)

		else:
			flag_juice_in=""
			flag_vapor_in=""

	
	if hasattr(Db_data, 'time_id'):

		new_id=False
		if int(Db_data.time_id)>int(id_time):
			new_id=True
		
		id_time=Db_data.time_id
		time=Db_data.time

		if time!="stop" and new_id==True:

			vapor_data=[]
			juice_data=[]

			# print (str(id_time)+" *---* "+time)

			if one_reload==1:
				Graph.reload_toolbar(False)
				one_reload=0

			fields="Name,_Type,Flow,Temperature,Brix,Purity,Insoluble_solids,pH,Pressure,Saturated_vapor"
			result=db.read_data("Flow_inputs",fields,"LAST","Name")
			if len(result)>0:	
				for data in result:
					for i,values in enumerate(data):
						if  str(data[0])==flag_juice_in and str(data[1])=="Juice":
							if i>1:
								juice_data.append(str(values))
						elif str(data[0])==flag_vapor_in and str(data[1])=="Vapor":
							if i>1:
								vapor_data.append(str(values))

			id_valve=0
			result=db.read_data("Valves","id","Name",flag_vapor_in)
			if len(result)>0:
				for data in result:
					id_valve=data[0]
				fields="Valves_id,Out_flow,Out_temperature,Out_brix,Out_purity,Out_insoluble_solids,Out_pH,Out_pressure,Out_saturated_vapor"
				result=db.read_data("Outputs_valve",fields,"LAST","Valves_id")
				if len(result)>0:	
					for data in result:
						for i,values in enumerate(data):
							if  str(data[0])==str(id_valve):
								if i>0:
									vapor_data.append(str(values))

			if len(juice_data)>0 and len(vapor_data)>0:
				Mjin=float(juice_data[0])	
				Tjin=float(juice_data[1])
				Bjin=float(juice_data[2])
				Zjin=float(juice_data[3])
				SolIn=float(juice_data[4])
				pHjin=float(juice_data[5])
				Pjin=float(juice_data[6])

				
				Mvin=float(vapor_data[0])
				Tvin=float(vapor_data[1])
				Pvin=float(vapor_data[6])
				sat=float(vapor_data[7])

				if create_stream==1:
					#Fluid					
					fluid_change=fluid_in.comparation(juice_data)
					if fluid_change==True:
						# print("cambio jugo")
						fluid_out.update(Mjin,Pjin,Tjin,Bjin,Zjin,SolIn,pHjin)
						fluid_in.update(Mjin,Pjin,Tjin,Bjin,Zjin,SolIn,pHjin)

					#Vapor
					vapor_change=vapor_in.comparation(vapor_data)
					if vapor_change==True:
						# print("cambio vapor"+str(Mvin))
						if sat==1.0:
							vapor_in.update(Mvin,Pvin,None)
							vapor_out.update(Mvin,Pvin,None)

				else:
					#Fluid
					fluid_in=juice(Mjin,Pjin,Tjin,Bjin,Zjin,SolIn,pHjin)
					fluid_out=juice(Mjin,Pjin,Tjin,Bjin,Zjin,SolIn,pHjin)
					#Vapor
					if sat==1.0:
						vapor_in=vapor(Mvin,Pvin,None)
						vapor_out=vapor(Mvin,Pvin,None)
					create_stream=1
				
				tt.append(float(time))
				
				ht_model.in_out(fluid_in, fluid_out, vapor_in, vapor_out)
				fluid_in, fluid_out, vapor_in, vapor_out = ht_model.solve([tt[-2],tt[-1]])
				model_value.append(fluid_out.Tj)
				
				split_model_data_n1=[tt[-1],model_value[-1]]

				write_process_values()
				write_outputs_heater()
				# print("len: "+str(len(tt))+" "+str(len(model_value)))
				if len(tt)==len(model_value):
					Graph.draw()
					ax=Graph.figure.get_axes()

					for x,line in enumerate(ax[0].lines): 
						del ax[0].lines[x]

					
					ax[0].plot(tt,model_value,'r-',label="Tjout")
					Graph.set_legends()
					Graph.draw()
					
				one_time=1


		elif one_time==1 and time=="stop":
			# time_exec=[]
			tt=[0.0]
			model_value=[Tjout_ini]
			
			ids_in_device=[]
			output=db.read_data("OUTPUTS_HEATER","Out_fluid_temperature,Time_exec_id","Heaters_id",id_Heater)
			Tout=list(output)
			for data in Tout:
				model_value.append(float(data[0]))
				ids_in_device.append(data[1])

			result=db.read_data("TIME_EXEC","id,TIME",None,None)
			result=list(result)
			ids_result=[]
			for k in range(0,len(result)):
				ids_result.append(result[k][0])
				result[k]=str(result[k][1])

			for ids in ids_in_device:
				for dato,id_result in zip(result,ids_result):
					if ids==id_result and dato!="stop":
						tt.append(float(dato))


			ax=Graph.figure.get_axes()
			if len(tt)==len(model_value):						
				for x,line in enumerate(ax[0].lines): 
						del ax[0].lines[x]

				ax[0].plot(tt,model_value,'r-',label="Tjout")
				Graph.set_legends()
				Graph.draw()

			Enable_cursor=True
			Graph.reload_toolbar(Enable_cursor)
			write_process_values()
			
			time_exec=[]
			model_value=[float(Tjout_ini)]
			tt=[0.0]
			ht_model.Tjout=float(Tjout_ini)

			Flow_in_array=[]
			one_time=0
			one_reload=1
			create_stream=0

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
			global create_stream

			global fluid_in
			global fluid_out
			global vapor_in
			global vapor_out


			global yb_l
			global yt
			global tt
			global u_mod
			global ht_model
			global model_value
			global id_Heater
			global Tjout_ini

			Np=Pipe_x_Step.text()
			Nst=N_steps.text()
			Lp=Length_Pipe.text()
			Ip=Pipe_Thickness.text()
			Dosp=Ext_Pipe_Diameter.text()
			Ep=Pipe_Rough.text()
			Gf=Scalling_Coeff.text()
			Op=Time_Op.text()
			Tjout_ini=Initial_Out_Temp.text()

			flag=re.sub('([a-zA-Z]+)', "", nameDialog)

			upd =exist_initialization("Ht"+flag)
			fields="Heaters_id,Pipe_x_Step,N_steps,Ext_pipe_diameter,Pipe_length,Pipe_thickness,Pipe_rough,Scalling_coeff,Operation_time"
			
			if upd==0:
				outfile = open('Blocks_data.txt', 'a')
				outfile.write("\n"+"Ht"+flag+"\t"+Np+"\t"+Nst+"\t"+Dosp+"\t"+Lp+"\t"+Ip+"\t"+Ep+"\t"+Gf+"\t"+Op+"\t"+Tjout_ini+"\t"+str(SnT))
				outfile.close()			
				
				db.insert_data("Heaters","Name,_Type,Tjout_init",["Ht"+flag,str(Heater_type),float(Tjout_ini)])
				result=db.read_data("Heaters","id","Name","Ht"+flag)
				if len(result)>0:
					for data in result:
						id_Heater=data[0]
				values=[float(id_Heater),float(Np),float(Nst),float(Dosp),float(Lp),float(Ip),float(Ep),float(Gf),float(Op)]
				db.insert_data("Physical_properties_heater",fields,values)
			else:

				result=db.read_data("Heaters","id","Name","Ht"+flag)
				if len(result)>0:
					for data in result:
						id_Heater=data[0]

				db.update_data("Heaters",["_Type","Tjout_init"],[str(Heater_type),float(Tjout_ini)],["id"],[float(id_Heater)])

				values=[float(id_Heater),float(Np),float(Nst),float(Dosp),float(Lp),float(Ip),float(Ep),float(Gf),float(Op)]
				fields=["Heaters_id","Pipe_x_Step","N_steps","Ext_pipe_diameter","Pipe_length","Pipe_thickness","Pipe_rough","Scalling_coeff","Operation_time"]
				db.update_data("Physical_properties_heater",fields,values,["Heaters_id"],[float(id_Heater)])

			
			yb_l=[float(Tjout_ini)]
			yt=[0.0,float(Tjout_ini)]
			tt=[0.0]
			end_tt=[0.0,Ts]

			ht_model=heater_shell_tube(float(Np), float(Nst), float(Dosp), float(Lp), float(Ip), float(Ep), float(Gf), float(Op),float(Tjout_ini))
			model_value.append(float(Tjout_ini))

			create_stream=0
			self.close()
			Resultado=QtGui.QDialog()
			QtGui.QMessageBox.information(Resultado, 
			'Ok',
			_translate("Dialog","Instanciación correcta de datos.",None),QtGui.QMessageBox.Ok)
			Dialog_window.close()
		def NO(self):
			self.close()

## Dialog box class
class Ui_Dialog(object):

	#Evaluate all data for correct heater initialization
	def confirm_param(self):
		global confirm
		global Resultado
		global pd

		confirm=((len(Pipe_x_Step.text())>0)and(len(N_steps.text())>0)and(len(Length_Pipe.text())>0)and(len(Pipe_Thickness.text())>0)
		and(len(Ext_Pipe_Diameter.text())>0)and(len(Pipe_Rough.text())>0)and(len(Scalling_Coeff.text())>0)and(len(Time_Op.text())>0)and(len(Initial_Out_Temp.text())>0))

		if Heater_type!="" and confirm==True:
			Resultado=QtGui.QDialog()
			pd = window_confirm_param(Resultado.window())
			pd.exec_()
		else:
			self.Resultado=QtGui.QDialog()
			QtGui.QMessageBox.warning(self.Resultado, 
			'Advertencia',
			"Falta por ingresar algun dato.",QtGui.QMessageBox.Ok)

	#Objects in dialog box
	def setupUi(self,name,ts,item,Data_Base,Dialog):
		##Heater properties
		#Physical properties
		global Pipe_x_Step
		global N_steps
		global Length_Pipe
		global Pipe_Thickness
		global Ext_Pipe_Diameter
		global Pipe_Rough
		global Scalling_Coeff
		global Time_Op
		global Initial_Out_Temp
		global nameDialog
		global Dialog_window
		global Ts
		global Temp_Output_variable
		global Selector_Heater_type
		#Calculated parameters
		global Scalling_Resist
		global Juice_Velocity
		global Inside_U
		global Outside_U
		global Overall_U
		global Heat_Area

		##Process values
		#Input fluid data
		global InFluid_Temp
		global InFluid_Flow
		global InFluid_pH
		global InFluid_pressure
		global InFluid_InsolubleSolids
		global InFluid_Purity
		global InFluid_Brix
		#Output fluid data
		global OutFluid_Temp
		global OutFluid_Brix
		global OutFluid_Flow
		global OutFluid_pH
		global OutFluid_pressure
		global OutFluid_InsolubleSolids
		global OutFluid_Purity
		#Input steam data
		global InStm_Press
		global InStm_Flow
		global InStm_Temp
		#Condensed Steam data
		global CondStm_Flow
		global CondStm_Temp
		global CondStm_Press
		global Graph

		global Heat_tab_3
		global verticalLayoutWidget
		global db
		global item_heater
		global title_name


		nameDialog=name
		Ts=ts
		Dialog_window=Dialog
		db=Data_Base
		item_heater=item
		title_name=str(item.label.toPlainText())


		Validation_text_field = Validator()
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(432, 355)

		self.Principal_layout = QtGui.QVBoxLayout(Dialog)
		self.Principal_layout.setObjectName(_fromUtf8("Principal_layout"))

		self.V_layout_principal = QtGui.QVBoxLayout()
		self.V_layout_principal.setObjectName(_fromUtf8("V_layout_principal"))

		
	##--Tab widget--##
		self.tabWidget_Heater = QtGui.QTabWidget(Dialog)
		self.tabWidget_Heater.setGeometry(QtCore.QRect(0, 30, 431, 360))
		self.tabWidget_Heater.setObjectName(_fromUtf8("tabWidget_Heater"))
		self.Heat_tab1 = QtGui.QWidget()
		self.Heat_tab1.setObjectName(_fromUtf8("Heat_tab1"))
		self.gridLayout_tab1 = QtGui.QGridLayout(self.Heat_tab1)
		self.gridLayout_tab1.setObjectName(_fromUtf8("gridLayout_tab1"))

		self.tabWidget_Heater.addTab(self.Heat_tab1, _fromUtf8(""))
		self.Heat_tab_2 = QtGui.QWidget()
		self.Heat_tab_2.setObjectName(_fromUtf8("Heat_tab_2"))
		self.gridLayout_tab2 = QtGui.QGridLayout(self.Heat_tab_2)
		self.gridLayout_tab2.setObjectName(_fromUtf8("gridLayout_tab2"))

		self.tabWidget_Heater.addTab(self.Heat_tab_2, _fromUtf8(""))
		Heat_tab_3 = QtGui.QWidget()
		Heat_tab_3.setObjectName(_fromUtf8("Heat_tab_3"))
		

	##--Instance button--##
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.OKButton_Heat = QtGui.QPushButton(self.Heat_tab1)
		self.OKButton_Heat.setGeometry(QtCore.QRect(280, 258, 131, 23))
		self.OKButton_Heat.setObjectName(_fromUtf8("OKButton_Heat"))
		self.OKButton_Heat.clicked.connect(self.confirm_param)

		sizePolicy.setHeightForWidth(self.OKButton_Heat.sizePolicy().hasHeightForWidth())
		self.OKButton_Heat.setSizePolicy(sizePolicy)



	##----Instantiation of elements for the initial condition----##
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		
		sizePolicy_label = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy_label.setHorizontalStretch(0)
		sizePolicy_label.setVerticalStretch(0)
		#Group box
		self.Initial_conditions_GrBx = QtGui.QGroupBox(self.Heat_tab1)
		self.Initial_conditions_GrBx.setGeometry(QtCore.QRect(213, 191, 201, 61))
		self.Initial_conditions_GrBx.setObjectName(_fromUtf8("Initial_conditions_GrBx"))
		#Line edit
		Initial_Out_Temp = QtGui.QLineEdit(self.Initial_conditions_GrBx)
		Initial_Out_Temp.setGeometry(QtCore.QRect(138, 27, 41, 20))
		Initial_Out_Temp.setReadOnly(False)
		Initial_Out_Temp.setObjectName(_fromUtf8("Initial_Out_Temp"))
		Initial_Out_Temp.setText("78.0")
		Validation_text_field.NumValidator(Initial_Out_Temp)
		sizePolicy.setHeightForWidth(Initial_Out_Temp.sizePolicy().hasHeightForWidth())
		Initial_Out_Temp.setSizePolicy(sizePolicy)
		#Label
		self.label_Initial_Out_Temp = QtGui.QLabel(self.Initial_conditions_GrBx)
		self.label_Initial_Out_Temp.setGeometry(QtCore.QRect(7, 21, 131, 31))
		self.label_Initial_Out_Temp.setObjectName(_fromUtf8("label_Initial_Out_Temp"))

		self.HLayout_Initial_conditions_GrBx = QtGui.QHBoxLayout(self.Initial_conditions_GrBx)
		self.HLayout_Initial_conditions_GrBx.setObjectName(_fromUtf8("HLayout_Initial_conditions_GrBx"))
		self.HLayout_Initial_conditions_GrBx2 = QtGui.QHBoxLayout()
		self.HLayout_Initial_conditions_GrBx2.setObjectName(_fromUtf8("HLayout_Initial_conditions_GrBx2"))

		self.HLayout_Initial_conditions_GrBx.addWidget(self.label_Initial_Out_Temp)
		self.HLayout_Initial_conditions_GrBx.addWidget(Initial_Out_Temp)

	##----Selector of material type----##
		self.horizontalLayout_tipo_material = QtGui.QHBoxLayout()
		self.horizontalLayout_tipo_material.setObjectName(_fromUtf8("horizontalLayout_tipo_material"))
		#Selectable list
		self.ComBox_Type_Material = QtGui.QComboBox(self.Heat_tab1)
		self.ComBox_Type_Material.setGeometry(QtCore.QRect(102, 228, 91, 22))
		self.ComBox_Type_Material.setObjectName(_fromUtf8("ComBox_Type_Material"))
		self.ComBox_Type_Material.addItem("Inoxidable")
		self.ComBox_Type_Material.addItem("Aluminio")

		#Label
		self.label_Type_Material = QtGui.QLabel(self.Heat_tab1)
		self.label_Type_Material.setGeometry(QtCore.QRect(14, 230, 81, 16))
		self.label_Type_Material.setObjectName(_fromUtf8("label_Type_Material"))


		self.horizontalLayout_tipo_material.addWidget(self.label_Type_Material)
		self.horizontalLayout_tipo_material.addWidget(self.ComBox_Type_Material)

	##----Instantiation of elements for calculated properties----##
		self.gridLayout_Calculated_properties = QtGui.QGridLayout()
		self.gridLayout_Calculated_properties.setObjectName(_fromUtf8("gridLayout_Calculated_properties"))
		#Group box
		self.Calculated_properties_GrBx = QtGui.QGroupBox(self.Heat_tab1)
		self.Calculated_properties_GrBx.setGeometry(QtCore.QRect(213, 6, 205, 181))
		self.Calculated_properties_GrBx.setObjectName(_fromUtf8("Calculated_properties_GrBx"))
		#Juice velocity
		self.label_Juice_Velocity = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Juice_Velocity.setGeometry(QtCore.QRect(10, 21, 131, 16))
		self.label_Juice_Velocity.setObjectName(_fromUtf8("label_Juice_Velocity"))
		sizePolicy_label.setHeightForWidth(self.label_Juice_Velocity.sizePolicy().hasHeightForWidth())
		self.label_Juice_Velocity.setSizePolicy(sizePolicy_label)
		Juice_Velocity = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Juice_Velocity.setGeometry(QtCore.QRect(145, 20, 55, 20))
		Juice_Velocity.setReadOnly(True)
		Juice_Velocity.setObjectName(_fromUtf8("Juice_Velocity"))
		sizePolicy.setHeightForWidth(Juice_Velocity.sizePolicy().hasHeightForWidth())
		Juice_Velocity.setSizePolicy(sizePolicy)

		#Scalling resistance
		self.label_Scalling_Resist = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Scalling_Resist.setGeometry(QtCore.QRect(10, 43, 151, 31))
		self.label_Scalling_Resist.setObjectName(_fromUtf8("label_Scalling_Resist"))
		sizePolicy_label.setHeightForWidth(self.label_Scalling_Resist.sizePolicy().hasHeightForWidth())
		self.label_Scalling_Resist.setSizePolicy(sizePolicy_label)
		Scalling_Resist = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Scalling_Resist.setGeometry(QtCore.QRect(145, 53, 55, 20))
		Scalling_Resist.setReadOnly(True)
		Scalling_Resist.setObjectName(_fromUtf8("Scalling_Resist"))
		sizePolicy.setHeightForWidth(Scalling_Resist.sizePolicy().hasHeightForWidth())
		Scalling_Resist.setSizePolicy(sizePolicy)
		#Outside heat transfer coeficcient
		self.label_Outside_U = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Outside_U.setGeometry(QtCore.QRect(10, 108, 121, 16))
		self.label_Outside_U.setObjectName(_fromUtf8("label_Outside_U"))
		sizePolicy_label.setHeightForWidth(self.label_Outside_U.sizePolicy().hasHeightForWidth())
		self.label_Outside_U.setSizePolicy(sizePolicy_label)
		Outside_U = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Outside_U.setGeometry(QtCore.QRect(145, 107, 55, 20))
		Outside_U.setReadOnly(True)
		Outside_U.setObjectName(_fromUtf8("Outside_U"))
		sizePolicy.setHeightForWidth(Outside_U.sizePolicy().hasHeightForWidth())
		Outside_U.setSizePolicy(sizePolicy)
		#Inside heat transfer coeficcient
		self.label_Inside_U = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Inside_U.setGeometry(QtCore.QRect(11, 130, 121, 16))
		self.label_Inside_U.setObjectName(_fromUtf8("label_Inside_U"))
		sizePolicy_label.setHeightForWidth(self.label_Inside_U.sizePolicy().hasHeightForWidth())
		self.label_Inside_U.setSizePolicy(sizePolicy_label)
		Inside_U = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Inside_U.setGeometry(QtCore.QRect(145, 130, 55, 20))
		Inside_U.setReadOnly(True)
		Inside_U.setObjectName(_fromUtf8("Inside_U"))
		sizePolicy.setHeightForWidth(Inside_U.sizePolicy().hasHeightForWidth())
		Inside_U.setSizePolicy(sizePolicy)
		#Overall heat transfer coeficcient
		self.label_Overall_U = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Overall_U.setGeometry(QtCore.QRect(11, 153, 121, 16))
		self.label_Overall_U.setObjectName(_fromUtf8("label_Overall_U"))
		sizePolicy_label.setHeightForWidth(self.label_Overall_U.sizePolicy().hasHeightForWidth())
		self.label_Overall_U.setSizePolicy(sizePolicy_label)
		Overall_U = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Overall_U.setGeometry(QtCore.QRect(145, 153, 55, 20))
		Overall_U.setReadOnly(True)
		Overall_U.setObjectName(_fromUtf8("Overall_U"))
		sizePolicy.setHeightForWidth(Overall_U.sizePolicy().hasHeightForWidth())
		Overall_U.setSizePolicy(sizePolicy)
		#Heat area
		self.label_Heat_Area = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Heat_Area.setGeometry(QtCore.QRect(10, 76, 121, 31))
		self.label_Heat_Area.setObjectName(_fromUtf8("label_Heat_Area"))
		sizePolicy_label.setHeightForWidth(self.label_Heat_Area.sizePolicy().hasHeightForWidth())
		self.label_Heat_Area.setSizePolicy(sizePolicy_label)
		Heat_Area = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Heat_Area.setGeometry(QtCore.QRect(145, 79, 55, 20))
		Heat_Area.setReadOnly(True)
		Heat_Area.setObjectName(_fromUtf8("Heat_Area"))
		sizePolicy.setHeightForWidth(Heat_Area.sizePolicy().hasHeightForWidth())
		Heat_Area.setSizePolicy(sizePolicy)

		self.Layout_GrBx_Calculated_properties = QtGui.QGridLayout(self.Calculated_properties_GrBx)
		self.Layout_GrBx_Calculated_properties.setObjectName(_fromUtf8("Layout_GrBx_Calculated_properties"))

		self.gridLayout_Calculated_properties.addWidget(self.label_Juice_Velocity, 0, 0, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(Juice_Velocity, 0, 1, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(self.label_Scalling_Resist, 1, 0, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(Scalling_Resist, 1, 1, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(self.label_Heat_Area, 2, 0, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(Heat_Area, 2, 1, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(self.label_Inside_U, 3, 0, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(Inside_U, 3, 1, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(self.label_Outside_U, 4, 0, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(Outside_U, 4, 1, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(self.label_Overall_U, 5, 0, 1, 1)
		self.gridLayout_Calculated_properties.addWidget(Overall_U, 5, 1, 1, 1)

		self.Layout_GrBx_Calculated_properties.addLayout(self.gridLayout_Calculated_properties,0, 0, 1, 1)

	##----Instantiation of elements for physical properties----##
		self.gridLayout_Physical_properties = QtGui.QGridLayout()
		self.gridLayout_Physical_properties.setObjectName(_fromUtf8("gridLayout_Physical_properties"))
		#Group box
		self.Physical_properties_GrBx = QtGui.QGroupBox(self.Heat_tab1)
		self.Physical_properties_GrBx.setGeometry(QtCore.QRect(10, 6, 191, 201))
		self.Physical_properties_GrBx.setObjectName(_fromUtf8("Physical_properties_GrBx"))
		#External pipe diameter
		self.label_Ext_Pipe_Diameter = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Ext_Pipe_Diameter.setGeometry(QtCore.QRect(7, 20, 131, 16))
		self.label_Ext_Pipe_Diameter.setObjectName(_fromUtf8("label_Ext_Pipe_Diameter"))
		sizePolicy_label.setHeightForWidth(self.label_Ext_Pipe_Diameter.sizePolicy().hasHeightForWidth())
		self.label_Ext_Pipe_Diameter.setSizePolicy(sizePolicy_label)
		Ext_Pipe_Diameter = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Ext_Pipe_Diameter.setGeometry(QtCore.QRect(143, 18, 41, 20))
		Ext_Pipe_Diameter.setObjectName(_fromUtf8("Ext_Pipe_Diameter"))
		Ext_Pipe_Diameter.setText("2.0")
		Validation_text_field.NumValidator(Ext_Pipe_Diameter)
		sizePolicy.setHeightForWidth(Ext_Pipe_Diameter.sizePolicy().hasHeightForWidth())
		Ext_Pipe_Diameter.setSizePolicy(sizePolicy)
		#Lenght of pipes
		self.label_Length_Pipe = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Length_Pipe.setGeometry(QtCore.QRect(7, 41, 121, 16))
		self.label_Length_Pipe.setObjectName(_fromUtf8("label_Length_Pipe"))
		sizePolicy_label.setHeightForWidth(self.label_Length_Pipe.sizePolicy().hasHeightForWidth())
		self.label_Length_Pipe.setSizePolicy(sizePolicy_label)
		Length_Pipe = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Length_Pipe.setGeometry(QtCore.QRect(143, 40, 41, 20))
		Length_Pipe.setObjectName(_fromUtf8("Length_Pipe"))
		Length_Pipe.setText("6.57")
		Validation_text_field.NumValidator(Length_Pipe)
		sizePolicy.setHeightForWidth(Length_Pipe.sizePolicy().hasHeightForWidth())
		Length_Pipe.setSizePolicy(sizePolicy)
		#Pipes for steps
		self.label_Pipe_x_Step = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Pipe_x_Step.setGeometry(QtCore.QRect(7, 108, 121, 16))
		self.label_Pipe_x_Step.setObjectName(_fromUtf8("label_Pipe_x_Step"))
		sizePolicy_label.setHeightForWidth(self.label_Pipe_x_Step.sizePolicy().hasHeightForWidth())
		self.label_Pipe_x_Step.setSizePolicy(sizePolicy_label)
		Pipe_x_Step = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Pipe_x_Step.setGeometry(QtCore.QRect(143, 106, 41, 20))
		Pipe_x_Step.setObjectName(_fromUtf8("self.Pipe_x_Step"))
		Pipe_x_Step.setText("6.0")
		Validation_text_field.NumValidator(Pipe_x_Step)
		sizePolicy.setHeightForWidth(Pipe_x_Step.sizePolicy().hasHeightForWidth())
		Pipe_x_Step.setSizePolicy(sizePolicy)
		#Number of steps
		self.label_N_steps = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_N_steps.setGeometry(QtCore.QRect(7, 130, 121, 16))
		self.label_N_steps.setObjectName(_fromUtf8("label_N_steps"))
		sizePolicy_label.setHeightForWidth(self.label_N_steps.sizePolicy().hasHeightForWidth())
		self.label_N_steps.setSizePolicy(sizePolicy_label)
		N_steps = QtGui.QLineEdit(self.Physical_properties_GrBx)
		N_steps.setGeometry(QtCore.QRect(143, 128, 41, 20))
		N_steps.setObjectName(_fromUtf8("N_steps"))
		N_steps.setText("2.0")
		Validation_text_field.NumValidator(N_steps)
		sizePolicy.setHeightForWidth(N_steps.sizePolicy().hasHeightForWidth())
		N_steps.setSizePolicy(sizePolicy)
		#Operation time
		self.label_Time_Op = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Time_Op.setGeometry(QtCore.QRect(7, 151, 121, 16))
		self.label_Time_Op.setObjectName(_fromUtf8("label_Time_Op"))
		sizePolicy_label.setHeightForWidth(self.label_Time_Op.sizePolicy().hasHeightForWidth())
		self.label_Time_Op.setSizePolicy(sizePolicy_label)
		Time_Op = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Time_Op.setGeometry(QtCore.QRect(143, 150, 41, 20))
		Time_Op.setObjectName(_fromUtf8("Time_Op"))
		Time_Op.setText("100.0")
		Validation_text_field.NumValidator(Time_Op)
		sizePolicy.setHeightForWidth(Time_Op.sizePolicy().hasHeightForWidth())
		Time_Op.setSizePolicy(sizePolicy)
		#Rough of pipes
		self.label_Pipe_Rough = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Pipe_Rough.setGeometry(QtCore.QRect(7, 85, 121, 16))
		self.label_Pipe_Rough.setObjectName(_fromUtf8("label_Pipe_Rough"))
		sizePolicy_label.setHeightForWidth(self.label_Pipe_Rough.sizePolicy().hasHeightForWidth())
		self.label_Pipe_Rough.setSizePolicy(sizePolicy_label)
		Pipe_Rough = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Pipe_Rough.setGeometry(QtCore.QRect(143, 84, 41, 20))
		Pipe_Rough.setObjectName(_fromUtf8("Pipe_Rough"))
		Pipe_Rough.setText("0.090")
		Validation_text_field.NumValidator(Pipe_Rough)
		sizePolicy.setHeightForWidth(Pipe_Rough.sizePolicy().hasHeightForWidth())
		Pipe_Rough.setSizePolicy(sizePolicy)
		#Scalling coefficient
		self.label_Scalling_Coeff = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Scalling_Coeff.setGeometry(QtCore.QRect(7, 166, 141, 31))
		self.label_Scalling_Coeff.setOpenExternalLinks(False)
		self.label_Scalling_Coeff.setObjectName(_fromUtf8("label_Scalling_Coeff"))
		sizePolicy_label.setHeightForWidth(self.label_Scalling_Coeff.sizePolicy().hasHeightForWidth())
		self.label_Scalling_Coeff.setSizePolicy(sizePolicy_label)
		Scalling_Coeff = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Scalling_Coeff.setGeometry(QtCore.QRect(143, 172, 41, 20))
		Scalling_Coeff.setObjectName(_fromUtf8("Scalling_Coeff"))
		Scalling_Coeff.setText("0.8")
		Validation_text_field.NumValidator(Scalling_Coeff)
		sizePolicy.setHeightForWidth(Scalling_Coeff.sizePolicy().hasHeightForWidth())
		Scalling_Coeff.setSizePolicy(sizePolicy)
		#Pipe thickness
		self.label_Pipe_Thickness = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Pipe_Thickness.setGeometry(QtCore.QRect(7, 64, 121, 16))
		self.label_Pipe_Thickness.setObjectName(_fromUtf8("label_Pipe_Thickness"))
		sizePolicy_label.setHeightForWidth(self.label_Pipe_Thickness.sizePolicy().hasHeightForWidth())
		self.label_Pipe_Thickness.setSizePolicy(sizePolicy_label)
		Pipe_Thickness = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Pipe_Thickness.setGeometry(QtCore.QRect(143, 62, 41, 20))
		Pipe_Thickness.setObjectName(_fromUtf8("Pipe_Thickness"))
		Pipe_Thickness.setText("1.2")
		Validation_text_field.NumValidator(Pipe_Thickness)
		sizePolicy.setHeightForWidth(Pipe_Thickness.sizePolicy().hasHeightForWidth())
		Pipe_Thickness.setSizePolicy(sizePolicy)


		self.Layout_GrBx_Physical_properties = QtGui.QGridLayout(self.Physical_properties_GrBx)
		self.Layout_GrBx_Physical_properties.setObjectName(_fromUtf8("Layout_GrBx_Physical_properties"))

		self.gridLayout_Physical_properties.addWidget(self.label_Ext_Pipe_Diameter, 0, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Ext_Pipe_Diameter, 0, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_Length_Pipe, 1, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Length_Pipe, 1, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_Pipe_Thickness, 2, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Pipe_Thickness, 2, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_Pipe_Rough, 3, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Pipe_Rough, 3, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_Pipe_x_Step, 4, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Pipe_x_Step, 4, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_N_steps, 5, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(N_steps, 5, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_Time_Op, 6, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Time_Op, 6, 1, 1, 1)
		self.gridLayout_Physical_properties.addWidget(self.label_Scalling_Coeff, 7, 0, 1, 1)
		self.gridLayout_Physical_properties.addWidget(Scalling_Coeff, 7, 1, 1, 1)

		self.Layout_GrBx_Physical_properties.addLayout(self.gridLayout_Physical_properties,0, 0, 1, 1)

		self.gridLayout_tab1.addWidget(self.Physical_properties_GrBx, 0, 0, 1, 1)
		self.gridLayout_tab1.addWidget(self.Calculated_properties_GrBx, 0, 1, 1, 1)
		self.gridLayout_tab1.addLayout(self.horizontalLayout_tipo_material, 1, 0, 1, 1)
		self.gridLayout_tab1.addWidget(self.Initial_conditions_GrBx, 1, 1, 1, 1)
		self.gridLayout_tab1.addWidget(self.OKButton_Heat, 2, 1, 1, 1)

	##----Instantiation of elements for output fluid----##
		self.gridLayout_Output_fluid = QtGui.QGridLayout()
		self.gridLayout_Output_fluid.setObjectName(_fromUtf8("gridLayout_Output_fluid"))	
		#Group box		
		self.Output_fluid_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Output_fluid_GrBx.setGeometry(QtCore.QRect(225, 10, 196, 176))
		self.Output_fluid_GrBx.setObjectName(_fromUtf8("Output_fluid_GrBx"))
		#Flow
		self.label_OutFluid_Flow = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Flow.setGeometry(QtCore.QRect(10, 21, 131, 16))
		self.label_OutFluid_Flow.setObjectName(_fromUtf8("label_OutFluid_Flow"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Flow.setSizePolicy(sizePolicy_label)
		OutFluid_Flow = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Flow.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_Flow.setReadOnly(True)
		OutFluid_Flow.setObjectName(_fromUtf8("OutFluid_Flow"))
		sizePolicy.setHeightForWidth(OutFluid_Flow.sizePolicy().hasHeightForWidth())
		OutFluid_Flow.setSizePolicy(sizePolicy)
		#Temperature
		self.label_OutFluid_Temp = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Temp.setGeometry(QtCore.QRect(10, 43, 121, 16))
		self.label_OutFluid_Temp.setObjectName(_fromUtf8("label_OutFluid_Temp"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_Temp.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Temp.setSizePolicy(sizePolicy_label)
		OutFluid_Temp = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Temp.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_Temp.setReadOnly(True)
		OutFluid_Temp.setObjectName(_fromUtf8("OutFluid_Temp"))
		sizePolicy.setHeightForWidth(OutFluid_Temp.sizePolicy().hasHeightForWidth())
		OutFluid_Temp.setSizePolicy(sizePolicy)
		#Brix
		self.label_OutFluid_Brix = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Brix.setGeometry(QtCore.QRect(10, 66, 121, 16))
		self.label_OutFluid_Brix.setObjectName(_fromUtf8("label_OutFluid_Brix"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_Brix.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Brix.setSizePolicy(sizePolicy_label)
		OutFluid_Brix = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Brix.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_Brix.setReadOnly(True)
		OutFluid_Brix.setObjectName(_fromUtf8("OutFluid_Brix"))
		sizePolicy.setHeightForWidth(OutFluid_Brix.sizePolicy().hasHeightForWidth())
		OutFluid_Brix.setSizePolicy(sizePolicy)
		#Purity
		self.label_OutFluid_Purity = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Purity.setGeometry(QtCore.QRect(10, 109, 121, 16))
		self.label_OutFluid_Purity.setObjectName(_fromUtf8("label_OutFluid_Purity"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_Purity.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Purity.setSizePolicy(sizePolicy_label)
		OutFluid_Purity = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Purity.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_Purity.setReadOnly(True)
		OutFluid_Purity.setObjectName(_fromUtf8("OutFluid_Purity"))
		sizePolicy.setHeightForWidth(OutFluid_Purity.sizePolicy().hasHeightForWidth())
		OutFluid_Purity.setSizePolicy(sizePolicy)
		#Pressure
		self.label_OutFluid_pressure = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_pressure.setGeometry(QtCore.QRect(10, 131, 121, 16))
		self.label_OutFluid_pressure.setObjectName(_fromUtf8("label_OutFluid_pressure"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_pressure.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_pressure.setSizePolicy(sizePolicy_label)
		OutFluid_pressure = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_pressure.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_pressure.setReadOnly(True)
		OutFluid_pressure.setObjectName(_fromUtf8("OutFluid_pressure"))
		sizePolicy.setHeightForWidth(OutFluid_pressure.sizePolicy().hasHeightForWidth())
		OutFluid_pressure.setSizePolicy(sizePolicy)
		#Insoluble solids
		self.label_OutFluid_InsolubleSolids = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_InsolubleSolids.setGeometry(QtCore.QRect(10, 87, 121, 16))
		self.label_OutFluid_InsolubleSolids.setObjectName(_fromUtf8("label_OutFluid_InsolubleSolids"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_InsolubleSolids.setSizePolicy(sizePolicy_label)
		OutFluid_InsolubleSolids = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_InsolubleSolids.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_InsolubleSolids.setReadOnly(True)
		OutFluid_InsolubleSolids.setObjectName(_fromUtf8("OutFluid_InsolubleSolids"))
		sizePolicy.setHeightForWidth(OutFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		OutFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		#pH
		self.label_OutFluid_pH = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_pH.setGeometry(QtCore.QRect(10, 153, 121, 16))
		self.label_OutFluid_pH.setObjectName(_fromUtf8("label_OutFluid_pH"))
		sizePolicy_label.setHeightForWidth(self.label_OutFluid_pH.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_pH.setSizePolicy(sizePolicy_label)
		OutFluid_pH = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_pH.setGeometry(QtCore.QRect(143, 62, 41, 20))
		OutFluid_pH.setReadOnly(True)
		OutFluid_pH.setObjectName(_fromUtf8("OutFluid_pH"))
		sizePolicy.setHeightForWidth(OutFluid_pH.sizePolicy().hasHeightForWidth())
		OutFluid_pH.setSizePolicy(sizePolicy)

		self.Layout_GrBx_Output_fluid = QtGui.QGridLayout(self.Output_fluid_GrBx)
		self.Layout_GrBx_Output_fluid.setObjectName(_fromUtf8("Layout_GrBx_Output_fluid"))

		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_Flow, 0, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_Flow, 0, 1, 1, 1)
		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_Temp, 1, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_Temp, 1, 1, 1, 1)
		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_Brix, 2, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_Brix, 2, 1, 1, 1)
		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_InsolubleSolids, 3, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_InsolubleSolids, 3, 1, 1, 1)
		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_Purity, 4, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_Purity, 4, 1, 1, 1)
		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_pressure, 5, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_pressure, 5, 1, 1, 1)
		self.gridLayout_Output_fluid.addWidget(self.label_OutFluid_pH, 6, 0, 1, 1)
		self.gridLayout_Output_fluid.addWidget(OutFluid_pH, 6, 1, 1, 1)

		self.Layout_GrBx_Output_fluid.addLayout(self.gridLayout_Output_fluid,0, 0, 1, 1)
	
	
	##----Instantiation of elements for input fluid----##	
		self.gridLayout_Input_fluid = QtGui.QGridLayout()
		self.gridLayout_Input_fluid.setObjectName(_fromUtf8("gridLayout_Input_fluid"))
		#Group box	
		self.Input_fluid_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Input_fluid_GrBx.setGeometry(QtCore.QRect(12, 10, 196, 176))
		self.Input_fluid_GrBx.setObjectName(_fromUtf8("Input_fluid_GrBx"))
		#Flow
		self.label_InFluid_Flow = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Flow.setGeometry(QtCore.QRect(10, 21, 131, 16))
		self.label_InFluid_Flow.setObjectName(_fromUtf8("label_InFluid_Flow"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Flow.setSizePolicy(sizePolicy_label)
		InFluid_Flow = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Flow.setGeometry(QtCore.QRect(139, 20, 52, 20))
		InFluid_Flow.setReadOnly(True)
		InFluid_Flow.setObjectName(_fromUtf8("InFluid_Flow"))
		sizePolicy.setHeightForWidth(InFluid_Flow.sizePolicy().hasHeightForWidth())
		InFluid_Flow.setSizePolicy(sizePolicy)
		#Temperature
		self.label_InFluid_Temp = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Temp.setGeometry(QtCore.QRect(10, 43, 121, 16))
		self.label_InFluid_Temp.setObjectName(_fromUtf8("label_InFluid_Temp"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_Temp.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Temp.setSizePolicy(sizePolicy_label)
		InFluid_Temp = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Temp.setGeometry(QtCore.QRect(139, 42, 52, 20))
		InFluid_Temp.setReadOnly(True)
		InFluid_Temp.setObjectName(_fromUtf8("InFluid_Temp"))
		sizePolicy.setHeightForWidth(InFluid_Temp.sizePolicy().hasHeightForWidth())
		InFluid_Temp.setSizePolicy(sizePolicy)
		#Brix
		self.label_InFluid_Brix = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Brix.setGeometry(QtCore.QRect(10, 66, 121, 16))
		self.label_InFluid_Brix.setObjectName(_fromUtf8("label_InFluid_Brix"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_Brix.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Brix.setSizePolicy(sizePolicy_label)
		InFluid_Brix = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Brix.setGeometry(QtCore.QRect(139, 64, 52, 20))
		InFluid_Brix.setReadOnly(True)
		InFluid_Brix.setObjectName(_fromUtf8("InFluid_Brix"))
		sizePolicy.setHeightForWidth(InFluid_Brix.sizePolicy().hasHeightForWidth())
		InFluid_Brix.setSizePolicy(sizePolicy)
		#Purity
		self.label_InFluid_Purity = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Purity.setGeometry(QtCore.QRect(10, 110, 121, 16))
		self.label_InFluid_Purity.setObjectName(_fromUtf8("label_InFluid_Purity"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_Purity.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Purity.setSizePolicy(sizePolicy_label)
		InFluid_Purity = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Purity.setGeometry(QtCore.QRect(139, 108, 52, 20))
		InFluid_Purity.setReadOnly(True)
		InFluid_Purity.setObjectName(_fromUtf8("InFluid_Purity"))
		sizePolicy.setHeightForWidth(InFluid_Purity.sizePolicy().hasHeightForWidth())
		InFluid_Purity.setSizePolicy(sizePolicy)
		#Pressure
		self.label_InFluid_pressure = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_pressure.setGeometry(QtCore.QRect(10, 132, 121, 16))
		self.label_InFluid_pressure.setObjectName(_fromUtf8("label_InFluid_pressure"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_pressure.sizePolicy().hasHeightForWidth())
		self.label_InFluid_pressure.setSizePolicy(sizePolicy_label)
		InFluid_pressure = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_pressure.setGeometry(QtCore.QRect(139, 130, 52, 20))
		InFluid_pressure.setReadOnly(True)
		InFluid_pressure.setObjectName(_fromUtf8("InFluid_pressure"))
		sizePolicy.setHeightForWidth(InFluid_pressure.sizePolicy().hasHeightForWidth())
		InFluid_pressure.setSizePolicy(sizePolicy)
		#Insoluble solids
		self.label_InFluid_InsolubleSolids = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_InsolubleSolids.setGeometry(QtCore.QRect(10, 88, 121, 16))
		self.label_InFluid_InsolubleSolids.setObjectName(_fromUtf8("label_InFluid_InsolubleSolids"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.label_InFluid_InsolubleSolids.setSizePolicy(sizePolicy_label)
		InFluid_InsolubleSolids = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_InsolubleSolids.setGeometry(QtCore.QRect(139, 86, 52, 20))
		InFluid_InsolubleSolids.setReadOnly(True)
		InFluid_InsolubleSolids.setObjectName(_fromUtf8("InFluid_InsolubleSolids_2"))
		sizePolicy.setHeightForWidth(InFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		InFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		#pH
		self.label_InFluid_pH = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_pH.setGeometry(QtCore.QRect(10, 153, 121, 16))
		self.label_InFluid_pH.setObjectName(_fromUtf8("label_InFluid_pH"))
		sizePolicy_label.setHeightForWidth(self.label_InFluid_pH.sizePolicy().hasHeightForWidth())
		self.label_InFluid_pH.setSizePolicy(sizePolicy_label)
		InFluid_pH = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_pH.setGeometry(QtCore.QRect(139, 152, 52, 20))
		InFluid_pH.setReadOnly(True)
		InFluid_pH.setObjectName(_fromUtf8("InFluid_pH"))
		sizePolicy.setHeightForWidth(InFluid_pH.sizePolicy().hasHeightForWidth())
		InFluid_pH.setSizePolicy(sizePolicy)

		self.Layout_GrBx_Input_fluid = QtGui.QGridLayout(self.Input_fluid_GrBx)
		self.Layout_GrBx_Input_fluid.setObjectName(_fromUtf8("Layout_GrBx_Input_fluid"))

		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_Flow, 0, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_Flow, 0, 1, 1, 1)
		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_Temp, 1, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_Temp, 1, 1, 1, 1)
		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_Brix, 2, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_Brix, 2, 1, 1, 1)
		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_InsolubleSolids, 3, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_InsolubleSolids, 3, 1, 1, 1)
		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_Purity, 4, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_Purity, 4, 1, 1, 1)
		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_pressure, 5, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_pressure, 5, 1, 1, 1)
		self.gridLayout_Input_fluid.addWidget(self.label_InFluid_pH, 6, 0, 1, 1)
		self.gridLayout_Input_fluid.addWidget(InFluid_pH, 6, 1, 1, 1)

		self.Layout_GrBx_Input_fluid.addLayout(self.gridLayout_Input_fluid,0, 0, 1, 1)

		
	##----Instantiation of elements for input steam----##	
		self.gridLayout_Input_Steam = QtGui.QGridLayout()
		self.gridLayout_Input_Steam.setObjectName(_fromUtf8("gridLayout_Input_Steam"))
		#Group box
		self.Input_Steam_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Input_Steam_GrBx.setGeometry(QtCore.QRect(12, 198, 196, 81))
		self.Input_Steam_GrBx.setObjectName(_fromUtf8("Input_Steam_GrBx"))
		#Flow
		self.label_InStm_Flow = QtGui.QLabel(self.Input_Steam_GrBx)
		self.label_InStm_Flow.setGeometry(QtCore.QRect(10, 18, 131, 16))
		self.label_InStm_Flow.setObjectName(_fromUtf8("label_InStm_Flow"))
		sizePolicy_label.setHeightForWidth(self.label_InStm_Flow.sizePolicy().hasHeightForWidth())
		self.label_InStm_Flow.setSizePolicy(sizePolicy_label)
		InStm_Flow = QtGui.QLineEdit(self.Input_Steam_GrBx)
		InStm_Flow.setGeometry(QtCore.QRect(139, 14, 52, 20))
		InStm_Flow.setReadOnly(True)
		InStm_Flow.setObjectName(_fromUtf8("InStm_Flow"))
		sizePolicy.setHeightForWidth(InStm_Flow.sizePolicy().hasHeightForWidth())
		InStm_Flow.setSizePolicy(sizePolicy)
		#Pressure
		self.label_InStm_Press = QtGui.QLabel(self.Input_Steam_GrBx)
		self.label_InStm_Press.setGeometry(QtCore.QRect(10, 38, 121, 16))
		self.label_InStm_Press.setObjectName(_fromUtf8("label_InStm_Press"))
		sizePolicy_label.setHeightForWidth(self.label_InStm_Press.sizePolicy().hasHeightForWidth())
		self.label_InStm_Press.setSizePolicy(sizePolicy_label)
		InStm_Press = QtGui.QLineEdit(self.Input_Steam_GrBx)
		InStm_Press.setGeometry(QtCore.QRect(139, 36, 52, 20))
		InStm_Press.setReadOnly(True)
		InStm_Press.setObjectName(_fromUtf8("InStm_Press"))
		sizePolicy.setHeightForWidth(InStm_Press.sizePolicy().hasHeightForWidth())
		InStm_Press.setSizePolicy(sizePolicy)
		#Temperature
		self.label_InStm_Temp = QtGui.QLabel(self.Input_Steam_GrBx)
		self.label_InStm_Temp.setGeometry(QtCore.QRect(10, 60, 131, 16))
		self.label_InStm_Temp.setObjectName(_fromUtf8("label_InStm_Temp"))
		sizePolicy_label.setHeightForWidth(self.label_InStm_Temp.sizePolicy().hasHeightForWidth())
		self.label_InStm_Temp.setSizePolicy(sizePolicy_label)
		InStm_Temp = QtGui.QLineEdit(self.Input_Steam_GrBx)
		InStm_Temp.setGeometry(QtCore.QRect(139, 58, 52, 20))
		InStm_Temp.setReadOnly(True)
		InStm_Temp.setObjectName(_fromUtf8("InStm_Temp"))
		sizePolicy.setHeightForWidth(InStm_Temp.sizePolicy().hasHeightForWidth())
		InStm_Temp.setSizePolicy(sizePolicy)

		self.Layout_GrBx_Input_Steam = QtGui.QGridLayout(self.Input_Steam_GrBx)
		self.Layout_GrBx_Input_Steam.setObjectName(_fromUtf8("Layout_GrBx_Input_Steam"))

		self.gridLayout_Input_Steam.addWidget(self.label_InStm_Flow, 0, 0, 1, 1)
		self.gridLayout_Input_Steam.addWidget(InStm_Flow, 0, 1, 1, 1)
		self.gridLayout_Input_Steam.addWidget(self.label_InStm_Press, 1, 0, 1, 1)
		self.gridLayout_Input_Steam.addWidget(InStm_Press, 1, 1, 1, 1)
		self.gridLayout_Input_Steam.addWidget(self.label_InStm_Temp, 2, 0, 1, 1)
		self.gridLayout_Input_Steam.addWidget(InStm_Temp, 2, 1, 1, 1)

		self.Layout_GrBx_Input_Steam.addLayout(self.gridLayout_Input_Steam,0, 0, 1, 1)
		
	##----Instantiation of elements for condensed steam----##
		self.gridLayout_Condensed_steam = QtGui.QGridLayout()
		self.gridLayout_Condensed_steam.setObjectName(_fromUtf8("gridLayout_Condensed_steam"))
		#Group box
		self.Condensed_steam_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Condensed_steam_GrBx.setGeometry(QtCore.QRect(225, 198, 196, 81))
		self.Condensed_steam_GrBx.setObjectName(_fromUtf8("Condensed_steam_GrBx"))
		#Flow
		self.label_CondStm_Flow = QtGui.QLabel(self.Condensed_steam_GrBx)
		self.label_CondStm_Flow.setGeometry(QtCore.QRect(16, 18, 121, 16))
		self.label_CondStm_Flow.setObjectName(_fromUtf8("label_CondStm_Flow"))
		sizePolicy_label.setHeightForWidth(self.label_CondStm_Flow.sizePolicy().hasHeightForWidth())
		self.label_CondStm_Flow.setSizePolicy(sizePolicy_label)
		CondStm_Flow = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		CondStm_Flow.setGeometry(QtCore.QRect(139, 16, 52, 20))
		CondStm_Flow.setReadOnly(True)
		CondStm_Flow.setObjectName(_fromUtf8("CondStm_Flow"))
		sizePolicy.setHeightForWidth(CondStm_Flow.sizePolicy().hasHeightForWidth())
		CondStm_Flow.setSizePolicy(sizePolicy)
		#Pressure
		self.label_CondStm_Press = QtGui.QLabel(self.Condensed_steam_GrBx)
		self.label_CondStm_Press.setGeometry(QtCore.QRect(16, 40, 131, 16))
		self.label_CondStm_Press.setObjectName(_fromUtf8("label_CondStm_Press"))
		sizePolicy_label.setHeightForWidth(self.label_CondStm_Press.sizePolicy().hasHeightForWidth())
		self.label_CondStm_Press.setSizePolicy(sizePolicy_label)
		CondStm_Press = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		CondStm_Press.setGeometry(QtCore.QRect(139, 38, 52, 20))
		CondStm_Press.setReadOnly(True)
		CondStm_Press.setObjectName(_fromUtf8("CondStm_Press"))
		sizePolicy.setHeightForWidth(CondStm_Press.sizePolicy().hasHeightForWidth())
		CondStm_Press.setSizePolicy(sizePolicy)
		#Temperature	
		self.label_CondStm_Temp = QtGui.QLabel(self.Condensed_steam_GrBx)
		self.label_CondStm_Temp.setGeometry(QtCore.QRect(16, 61, 121, 16))
		self.label_CondStm_Temp.setObjectName(_fromUtf8("label_CondStm_Temp"))
		sizePolicy_label.setHeightForWidth(self.label_CondStm_Temp.sizePolicy().hasHeightForWidth())
		self.label_CondStm_Temp.setSizePolicy(sizePolicy_label)
		CondStm_Temp = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		CondStm_Temp.setGeometry(QtCore.QRect(139, 60, 52, 20))
		CondStm_Temp.setReadOnly(True)
		CondStm_Temp.setObjectName(_fromUtf8("CondStm_Temp"))
		sizePolicy.setHeightForWidth(CondStm_Temp.sizePolicy().hasHeightForWidth())
		CondStm_Temp.setSizePolicy(sizePolicy)
				
		self.Layout_GrBx_Condensed_steam = QtGui.QGridLayout(self.Condensed_steam_GrBx)
		self.Layout_GrBx_Condensed_steam.setObjectName(_fromUtf8("Layout_GrBx_Condensed_steam"))

		self.gridLayout_Condensed_steam.addWidget(self.label_CondStm_Flow, 0, 0, 1, 1)
		self.gridLayout_Condensed_steam.addWidget(CondStm_Flow, 0, 1, 1, 1)
		self.gridLayout_Condensed_steam.addWidget(self.label_CondStm_Press, 1, 0, 1, 1)
		self.gridLayout_Condensed_steam.addWidget(CondStm_Press, 1, 1, 1, 1)
		self.gridLayout_Condensed_steam.addWidget(self.label_CondStm_Temp, 2, 0, 1, 1)
		self.gridLayout_Condensed_steam.addWidget(CondStm_Temp, 2, 1, 1, 1)

		self.Layout_GrBx_Condensed_steam.addLayout(self.gridLayout_Condensed_steam,0, 0, 1, 1)
		
		self.gridLayout_tab2.addWidget(self.Input_fluid_GrBx, 0, 0, 1, 1)
		self.gridLayout_tab2.addWidget(self.Output_fluid_GrBx, 0, 1, 1, 1)
		self.gridLayout_tab2.addWidget(self.Input_Steam_GrBx, 1, 0, 1, 1)
		self.gridLayout_tab2.addWidget(self.Condensed_steam_GrBx, 1, 1, 1, 1)	

	##----Instantiation of elements for variable output---#
		self.label_Temp_Output_variable = QtGui.QLabel(Heat_tab_3)
		self.label_Temp_Output_variable.setGeometry(QtCore.QRect(10, 10, 161, 16))
		self.label_Temp_Output_variable.setObjectName(_fromUtf8("label"))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		self.label_Temp_Output_variable.setSizePolicy(sizePolicy)
		Temp_Output_variable = QtGui.QLineEdit(Heat_tab_3)
		Temp_Output_variable.setGeometry(QtCore.QRect(180, 10, 51, 20))
		Temp_Output_variable.setReadOnly(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		Temp_Output_variable.setSizePolicy(sizePolicy)

		self.Widget_layout_Output_variable=QtGui.QWidget()
		self.H_layout_Output_variable=QtGui.QHBoxLayout()
		self.H_layout_Output_variable.addWidget(self.label_Temp_Output_variable)
		self.H_layout_Output_variable.addWidget(Temp_Output_variable)
		self.Widget_layout_Output_variable.setLayout(self.H_layout_Output_variable)



		verticalLayoutWidget = QtGui.QWidget()
		verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 410, 260))
		verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

		#Addition of grafics in window

		Graph = DynamicGraphic(Dialog,Ts,Enable_cursor,False,False,Heat_tab_3, width=4, height=3, dpi=85)
		Graph.axes.set_xlabel('Time (min)',fontsize=11)
		Graph.axes.set_ylabel(_translate("Dialog", "Tjout [°C]", None),fontsize=11)
		Graph.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		Graph.set_legends()
		extra_labels=['FlowIn']
		extra_groups=["Flujos"]
		Graph.add_table_signals(extra_labels,extra_groups)
		verticalLayoutWidget.setLayout(Graph.dynamic_graph)
		self.Timer_graph()
		
		self.V_layout_Heat_tab_3=QtGui.QVBoxLayout(Heat_tab_3)
		self.V_layout_Heat_tab_3.addWidget(self.Widget_layout_Output_variable)
		self.V_layout_Heat_tab_3.addWidget(verticalLayoutWidget)

		self.tabWidget_Heater.addTab(Heat_tab_3, _fromUtf8(""))
	
	##----Selector of Heat type----##
		#Selectable list
		Selector_Heater_type = QtGui.QComboBox(Dialog)
		Selector_Heater_type.setGeometry(QtCore.QRect(7, 6, 411, 22))
		Selector_Heater_type.setObjectName(_fromUtf8("Selector_Heater_type"))
		Selector_Heater_type.addItem("--Tipo de calentador--")
		Selector_Heater_type.addItem("Carcaza y tubos")
		Selector_Heater_type.addItem("Placas")
		Selector_Heater_type.activated.connect(self.selection_HeaterType)
		Selector_Heater_type.setCurrentIndex(1)

		self.V_layout_principal.addWidget(Selector_Heater_type)
		self.V_layout_principal.addWidget(self.tabWidget_Heater)
		self.Principal_layout.addLayout(self.V_layout_principal)

		self.retranslateUi(Dialog)
		self.tabWidget_Heater.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		Update_window()

	# Evaluate change in heater type
	def selection_HeaterType(self):
		global SnT
		global Heater_type
		Heater_type=Selector_Heater_type.currentText()
		if Heater_type=="--Tipo de calentador--":
			Heat_type=""
		elif Heater_type=="Carcaza y tubos":		
			SnT=1.0
		else:
			SnT=0.0

	# Timer initialization
	def Timer_graph(self):
		# global timer
		self.timer = QtCore.QTimer(Dialog_window)
		self.timer.timeout.connect(update_figure)
		self.timer.start(Ts*100)#Ts*1000-300)

	## Labels set text
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Parametros "+title_name, None))
		self.Initial_conditions_GrBx.setTitle(_translate("Dialog", "Condiciones iniciales", None))
		self.label_Initial_Out_Temp.setText(_translate("Dialog", "Temperatura del jugo \n"
		"de salida [°C]", None))
		self.label_Type_Material.setText(_translate("Dialog", "Tipo de material", None))
		self.OKButton_Heat.setText(_translate("Dialog", "Aceptar", None))
		self.Calculated_properties_GrBx.setTitle(_translate("Dialog", "Parametros calculados", None))
		self.label_Juice_Velocity.setText(_translate("Dialog", "Velocidad del jugo [m/s]", None))
		self.label_Scalling_Resist.setText(_translate("Dialog", "Resistencia incrustaciones \n"
		"[m2.°K/W]", None))
		self.label_Outside_U.setText(_translate("Dialog", "U interno  [W/(m2.°K)]", None))
		self.label_Inside_U.setText(_translate("Dialog", "U externo    [W/(m2.°K)]", None))
		self.label_Overall_U.setText(_translate("Dialog", "U global  [W/(m2.°K)]", None))
		self.label_Heat_Area.setText(_translate("Dialog", "Área de intercambio de \n"
		"calor [m2]", None))
		self.Physical_properties_GrBx.setTitle(_translate("Dialog", "Propiedades físicas", None))
		self.label_Ext_Pipe_Diameter.setText(_translate("Dialog", "Diámetro externo tubo[in]", None))
		self.label_Length_Pipe.setText(_translate("Dialog", "Longitud tubo [m]", None))
		self.label_Pipe_x_Step.setText(_translate("Dialog", "N° tubos por paso", None))
		self.label_N_steps.setText(_translate("Dialog", "N° pasos", None))
		self.label_Time_Op.setText(_translate("Dialog", "Tiempo operación [h]", None))
		self.label_Pipe_Rough.setText(_translate("Dialog", "Rugosidad tubo [mm]", None))
		self.label_Scalling_Coeff.setText(_translate("Dialog", "Coeficiente de incrustación", None))
		self.label_Pipe_Thickness.setText(_translate("Dialog", "Espesor tubo [mm]", None))
		self.tabWidget_Heater.setTabText(self.tabWidget_Heater.indexOf(self.Heat_tab1), _translate("Dialog", "Propiedades físicas", None))
		self.Output_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de salida", None))
		self.label_OutFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_OutFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_OutFluid_Brix.setText(_translate("Dialog", "Brix [%]", None))
		self.label_OutFluid_Purity.setText(_translate("Dialog", "Pureza [%]", None))
		self.label_OutFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [%]", None))
		self.label_OutFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.label_OutFluid_pressure.setText(_translate("Dialog", "Presión[kPa] ", None))
		self.label_InFluid_pressure.setText(_translate("Dialog", "Presión[kPa] ", None))

		self.Input_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de entrada", None))
		self.label_InFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_InFluid_Brix.setText(_translate("Dialog", "Brix [%]", None))
		self.label_InFluid_Purity.setText(_translate("Dialog", "Pureza [%]", None))
		self.label_InFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [%]", None))
		self.label_InFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.Input_Steam_GrBx.setTitle(_translate("Dialog", "Vapor de entrada", None))
		self.label_InStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InStm_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.label_InStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.Condensed_steam_GrBx.setTitle(_translate("Dialog", "Vapor condensado ", None))
		self.label_CondStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_CondStm_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.label_CondStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.tabWidget_Heater.setTabText(self.tabWidget_Heater.indexOf(self.Heat_tab_2), _translate("Dialog", "Variables de proceso", None))
		self.label_Temp_Output_variable.setText(_translate("Dialog", "Temperatura de jugo de salida:", None))
		self.tabWidget_Heater.setTabText(self.tabWidget_Heater.indexOf(Heat_tab_3), _translate("Dialog", "Gráfica", None))





