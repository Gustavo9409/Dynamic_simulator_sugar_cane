# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'evaporator_dialogbox.ui'
#
# Created: Mon Jul 17 13:51:06 2017
#      by: PyQt4 UI code generator 4.10.2

# Installed Libs
import re

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.ticker import FormatStrFormatter
from dynamic_diagrams import DynamicGraphic
from collections import defaultdict

# Local Libs
from evaporators import *
from global_data import *
from streams import *

#global values
global Evaporator_type
global Enable_cursor
global Interest_variable
global flag_vapor_in
global flag_juice_in
global flag_vapor_out
global id_time
global one_time
global one_reload
global create_stream
global model_value
global label_graph
global label_y_axis

Evaporator_type="Evaporador Robert"
Interest_variable="Brix de jugo de salida"
Enable_cursor=False
flag_vapor_in=""
flag_juice_in=""
flag_vapor_out=""
id_time=0
one_time=1
one_reload=0
create_stream=0
model_value=[]
label_graph=""
label_y_axis=""

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
def write_outputs_evaporator():
	global juice_out
	global vapor_out
	global condensate_out
	global Evaporator

	db.insert_data("Outputs_evaporator","Evaporators_id,Out_juice_temperature,Out_juice_brix,Out_juice_flow,Out_juice_pH,Out_juice_pressure,Out_juice_insoluble_solids,Out_juice_purity"
				",Condensed_vapor_flow,Condensed_vapor_temperature,Condensed_vapor_pressure"
				",Out_vapor_flow,Out_vapor_temperature,Out_vapor_pressure"
				",Evaporator_level"
				",Time_exec_id",
				[id_evap,juice_out.Tj,juice_out.Bj,juice_out.Mj,juice_out.pHj,juice_out.Pj,juice_out.Ij,juice_out.Zj
				,condensate_out.Mw,condensate_out.Tw,condensate_out.Pw
				,vapor_out.Mv,vapor_out.Tv,vapor_out.Pv
				,Evaporator.Lje
				,id_time])

##Function for update process values
def write_process_values():
	global juice_in
	global juice_out
	global vapor_in
	global vapor_out
	global condensate_out

	InFluid_Flow.setText(str(round(juice_in.Mj*3.6,3)))
	InFluid_Temp.setText(str(round(juice_in.Tj,3)))
	InFluid_Brix.setText(str(round(juice_in.Bj*100.0,3)))
	InFluid_InsolubleSolids.setText(str(round(juice_in.Ij*100.0,3)))
	InFluid_Purity.setText(str(round(juice_in.Zj*100.0,3)))
	InFluid_Pressure.setText(str(round(juice_in.Pj/1000.0,3)))
	InFluid_pH.setText(str(round(juice_in.pHj,3)))

	OutFluid_Flow.setText(str(round(juice_out.Mj*3.6,3)))
	OutFluid_Temp.setText(str(round(juice_out.Tj,3)))
	OutFluid_Brix.setText(str(round(juice_out.Bj*100.0,3)))
	OutFluid_InsolubleSolids.setText(str(round(juice_out.Ij*100.0,3)))
	OutFluid_Purity.setText(str(round(juice_out.Zj*100.0,3)))
	OutFluid_Pressure.setText(str(round(juice_out.Pj/1000.0,3)))
	OutFluid_pH.setText(str(round(juice_out.pHj,3)))

	InStm_Flow.setText(str(round(vapor_in.Mv*3.6,3)))
	InStm_Press.setText(str(round(vapor_in.Pv/1000.0,3)))
	InStm_Temp.setText(str(round(vapor_in.Tv,3)))

	OutStm_Flow.setText(str(round(vapor_out.Mv*3.6,3)))
	OutStm_Press.setText(str(round(vapor_out.Pv/1000.0,3)))
	OutStm_Temp.setText(str(round(vapor_out.Tv,3)))

	CondStm_Flow.setText(str(round(condensate_out.Mw*3.6,3)))
	CondStm_Press.setText(str(round(condensate_out.Pw/1000.0,3)))
	CondStm_Temp.setText(str(round(condensate_out.Tw,3)))

##Evaluate devices connected in the evaporator inputs
def flag_inputs(device_connected,port_input,port_heater):
	flag=""
	
	flags={
	("Flujo","Jugo de entrada"):"Fj",
	("Flujo","Vapor vivo"):"Fv",

	("Valvula","Jugo de entrada"):"Vlv",
	("Valvula","Vapor vivo"):"Vlv",

	("Calentador","Jugo de entrada"):"Ht",
	("Calentador","Vapor vegetal"):"Ht",

	("Evaporador","Jugo de entrada"):"Evp"
	}

	flags = defaultdict(lambda: -1, flags)

	flag=flags[device_connected[:-1],port_input]

	if flag!=-1 and port_input==port_heater:
		flag=flag+device_connected[len(device_connected)-1:]
	else:
		flag=""

	return flag

## Timer for solve evaporator model and plot evaporator data
def update_figure():
	global Graph

	global tt
	global brix_model_value
	global flow_model_value
	global Le_model_value

	global model_value
	global label_graph
	global label_y_axis

	global id_time
	global id_evap
	global one_time
	global Enable_cursor
	global one_reload
	global create_stream

	global flag_juice_in
	global flag_vapor_in
	global flag_vapor_out	

	global juice_in
	global juice_out
	global vapor_in
	global vapor_out
	global vapor_use
	global condensate_out


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


					if flag_vapor_in=="":
						flag_vapor_in=flag_inputs(device_connected,"Vapor vivo",port_this_device)
					if flag_juice_in=="":
						flag_juice_in=flag_inputs(device_connected,"Jugo de entrada",port_this_device)
				if 	par_data[0]==nameDialog:
					device_connected=par_data[1]
					this_device=par_data[0]
					port_connected=par_data[3]
					port_this_device=par_data[2]

					if flag_vapor_out=="":
						flag_vapor_out=flag_inputs(device_connected,"Vapor vegetal",port_this_device)

		else:
			flag_juice_in=""
			flag_vapor_in=""
			flag_vapor_out=""

	if hasattr(Db_data, 'time_id'):

		new_id=False
		if int(Db_data.time_id)>int(id_time):
			new_id=True
		
		id_time=Db_data.time_id
		time=Db_data.time

		if time!="stop" and new_id==True:

			vapor_data=[]
			juice_data=[]
			vapor_use_data=[]

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

			fields="Evaporators_id,Out_vapor_flow"
			result=db.read_data("Outputs_evaporator",fields,"LAST","Evaporators_id")
			if len(result)>0:
				for data in result:
					for i,values in enumerate(data):
						if  str(data[0])==str(id_evap):
							if i>0:
								vapor_use_data.append(str(values))
							
			# if len(vapor_use_data)>0:
			# 	Mv_use=float(vapor_use_data[0])
			# 	Pv_use=float(vapor_use_data[6])
			# 	sat=float(vapor_use_data[7])


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
					juice_change=juice_in.comparation(juice_data)
					if juice_change==True:
						juice_in.update(Mjin,Pjin,Tjin,Bjin,Zjin,SolIn,pHjin)
					vapor_change=vapor_in.comparation(vapor_data)
					if vapor_change==True:
						if sat==1.0:
							vapor_in.update(Mvin,Pvin,None)
							# vapor_use.update(Mv_use,Pv_use,None)
					# if len(vapor_use_data)>0:
					# 	vapor_use.update(Mv_use,Pv_use,None)
				else:
					juice_in=juice(Mjin,Pjin,Tjin,Bjin,Zjin,SolIn,pHjin)
					juice_out=juice(Init_flow/3.6,Pjin,Tjin,Init_brix/100.0,Zjin,SolIn,pHjin-0.4)
					condensate_out=water(Mjin,Pjin,Tjin,pHjin)
					create_stream=1
					if sat==1.0:
						vapor_in=vapor(Mvin, Pvin, None)
						vapor_out=vapor(Mvin, Pvin, None)
						# if len(vapor_use_data)>0:
						# 	vapor_use=vapor(Mv_use,Pv_use,None)
						# else:
						vapor_use=vapor_out


				tt.append(time)

				Evaporator.in_out(juice_in, vapor_in, juice_out, vapor_out, vapor_use, condensate_out)
				juice_in, juice_out, vapor_in, vapor_out = Evaporator.solve([tt[-2],tt[-1]])
				brix_model_value.append(juice_out.Bj*100.0)
				Le_model_value.append(Evaporator.Lje*100.0)
				flow_model_value.append(juice_out.Mj)

				# print("Bx: " + str(juice_out.Bj) + "\tLv: " + str(Evaporator.Lje)+" Fjout: "+str(juice_out.Mj))
				# print("mve: " + str(Evaporator.mve0) + "\tPvv: " + str(vapor_out.Pv) + "\tTje: " + str(juice_out.Tj))
				
				if label_graph=="":
					model_value=brix_model_value
					label_graph="Brix"
					label_y_axis="Brix [%]"

				if len(tt)==len(brix_model_value):

					Graph.axes.cla()

					ax=Graph.figure.get_axes()

					ax[0].grid(True)
					gridlines = ax[0].get_xgridlines() + ax[0].get_ygridlines()
					for line in gridlines:
						line.set_linestyle('-.')
					ax[0].set_xlabel('Time (s)',fontsize=11)
					ax[0].set_ylabel(_translate("Dialog", label_y_axis, None),fontsize=11)

					ax[0].plot(tt,model_value,'r-',label=label_graph)
					Graph.set_legends()
					Graph.draw()

					
				
				if flag_vapor_in[:-1]=="Fv":
					field=["Flow"]
					value=[vapor_in.Mv]
					db.update_data("Flow_inputs",field,value,["Name"],[flag_vapor_in])

				write_process_values()
				write_outputs_evaporator()

				one_time=1
				

		elif one_time==1 and time=="stop":

			tt=[0.0]
			brix_model_value=[Init_brix]
			flow_model_value=[Init_flow/3.6]
			Le_model_value=[Init_Le]

			ids_in_device=[]
			output=db.read_data("Outputs_evaporator","Out_juice_brix,Out_juice_flow,Evaporator_level,Time_exec_id","Evaporators_id",id_evap)
			output=list(output)
			for data in output:
				brix_model_value.append(float(data[0])*100.0)
				flow_model_value.append(float(data[1]))
				Le_model_value.append(float(data[2])*100.0)
				ids_in_device.append(data[3])

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

			model_value=[]
			label_graph=""
			label_y_axis=""
			if Interest_variable=="Brix de jugo de salida":
				model_value=brix_model_value
				label_graph="Brix"
				label_y_axis="Brix [%]"
			elif Interest_variable=="Flujo de jugo de salida":
				model_value=flow_model_value
				label_graph="Flujo"
				label_y_axis="Flujo [kg/s]"
			elif Interest_variable=="Nivel en evaporador":
				model_value=Le_model_value
				label_graph="Nivel"
				label_y_axis="Nivel [%]"

			ax=Graph.figure.get_axes()
			if len(tt)==len(brix_model_value):

				Graph.axes.cla()

				ax[0].grid(True)
				gridlines = ax[0].get_xgridlines() + ax[0].get_ygridlines()
				for line in gridlines:
					line.set_linestyle('-.')
				ax[0].set_xlabel('Time (s)',fontsize=11)
				ax[0].set_ylabel(_translate("Dialog", label_y_axis, None),fontsize=11)

				ax[0].plot(tt,model_value,'r-',label=label_graph)
				Graph.set_legends()
				Graph.draw()
		

			write_process_values()

			Enable_cursor=True
			Graph.reload_toolbar(Enable_cursor)

			create_stream=0
			tt=[0.0]
			brix_model_value=[Init_brix]
			flow_model_value=[Init_flow/3.6]
			Le_model_value=[Init_Le]

			one_time=0
			one_reload=1

##Function for update window when closing
def update_window():
	global one_reload
	global one_time
	global Num_window

	global Init_brix
	global Init_flow
	global Init_Le

	Num_window=re.sub('([a-zA-Z]+)', "", nameDialog)

	fields=("_Type,Brix_init,Flow_init,Level_init,Heat_area,Pipe_length,N_pipes,Intl_pipe_diameter,Volumen,Downtake_diameter"
			+",Bottom_cone_heigth,N_effect,Operation_days,Heat_losses")
	result=db.read_data("Evaporators",fields,"Name","Evp"+Num_window)
	Evaporator_data=[]
	if len(result)>0:
		for data in result:
			for values in data:
				Evaporator_data.append(str(values))

		Evaporator_type=Evaporator_data[0]

		Init_brix=float(Evaporator_data[1])
		Init_flow=float(Evaporator_data[2])
		Init_Le=float(Evaporator_data[3])

		A=Evaporator_data[4]
		Lp=Evaporator_data[5]
		Np=Evaporator_data[6]
		Di=Evaporator_data[7]
		Vol=Evaporator_data[8]
		Dd=Evaporator_data[9]
		hc=Evaporator_data[10]
		Ne=Evaporator_data[11]
		Op=Evaporator_data[12]
		Ls=Evaporator_data[13]
		
		
		index = comBox_Selector_Type_Evap.findText(Evaporator_type, QtCore.Qt.MatchFixedString)
		comBox_Selector_Type_Evap.setCurrentIndex(index)

		index = Selector_effect.findText(str(Ne), QtCore.Qt.MatchFixedString)
		Selector_effect.setCurrentIndex(index)
		
		Volumen.setText(Vol)
		Bottom_Cone_Height.setText(hc)
		Heat_Area.setText(A)
		Pipe_Diameter.setText(Di)
		N_pipes.setText(Np)
		Pipe_Lenght.setText(Lp)
		Downtake_Diameter.setText(Dd)
		OperationsDays.setText(Op)
		HeatLosses.setText(Ls)

		Initial_Juice_Brix.setText(str(Init_brix))
		Initial_Juice_Flow.setText(str(Init_flow))
		Initial_Evaporator_Level.setText(str(Init_Le))
	
	if hasattr(Db_data, 'time'):
		write_process_values()
		if Db_data.time!="stop":
			Enable_cursor=False
		else:
			Enable_cursor=True

		one_time=1
		one_reload=0

##Function for confirm if exist initialization of evaporator
def exist_initialization(data):
	global id_evap
	flg=0
	result=db.read_data("Evaporators","id","Name",data)
	if len(result)>0:
		for data in result:
			id_evap=data[0]
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
		global id_evap
		global Evaporator
		global create_stream

		global brix_model_value
		global flow_model_value
		global Le_model_value

		global tt

		global Init_brix
		global Init_flow
		global Init_Le
		
		Vol=float(Volumen.text())
		hc=float(Bottom_Cone_Height.text())
		A=float(Heat_Area.text())
		Di=float(Pipe_Diameter.text())
		Np=float(N_pipes.text())
		Lp=float(Pipe_Lenght.text())
		Dd=float(Downtake_Diameter.text())
		Op=float(OperationsDays.text())
		Ls=float(HeatLosses.text())

		Init_brix=float(Initial_Juice_Brix.text())
		Init_flow=float(Initial_Juice_Flow.text())
		Init_Le=float(Initial_Evaporator_Level.text())

		Ne=int(float(Selector_effect.currentText()))

		Num_window=re.sub('([a-zA-Z]+)', "", nameDialog)

		if Evaporator_type=="Evaporador Robert":
			fields=("Name,_Type,Brix_init,Flow_init,Level_init,Heat_area,Pipe_length,N_pipes,Intl_pipe_diameter,Volumen,Downtake_diameter"
			+",Bottom_cone_heigth,N_effect,Operation_days,Heat_losses")
			values=["Evp"+Num_window,str(Evaporator_type),Init_brix,Init_flow,Init_Le,A,Lp,Np,Di,Vol,Dd,hc,Ne,Op,Ls]
		

		updt=exist_initialization("Evp"+Num_window)
		
		if updt==0:		
			db.insert_data("Evaporators",fields,values)

			result=db.read_data("Evaporators","id","Name","Evp"+Num_window)
			if len(result)>0:
				for data in result:
					id_evap=data[0]

			if Evaporator_type=="Evaporador Robert":
				create_stream=0
				Evaporator=evaporator_roberts(A, Lp, Np, Di*0.0254, Vol, Dd*0.0254, hc, Ne, Op, Ls, Init_Le/100.0)
				print(Evaporator.Dd)
				print(Evaporator.Di)

		else:
			if Evaporator_type=="Evaporador Robert":
				create_stream=0

				fields=["Name","_Type","Brix_init","Flow_init","Level_init","Heat_area","Pipe_length","N_pipes","Intl_pipe_diameter","Volumen","Downtake_diameter"
				,"Bottom_cone_heigth","N_effect","Operation_days","Heat_losses"]
				db.update_data("Evaporators",fields,values,["id"],[float(id_evap)])

				Evaporator.update(A, Lp, Np, Di*0.0254, Vol, Dd*0.0254, hc, Ne, Op, Ls, Init_Le/100.0)
				print(Evaporator.Dd)
				print(Evaporator.Di)
	
		tt=[0.0]
		brix_model_value=[Init_brix]
		flow_model_value=[Init_flow/3.6]
		Le_model_value=[Init_Le]

		self.close()
		Resultado=QtGui.QDialog()
		QtGui.QMessageBox.information(Resultado,'Ok',_translate("Dialog","Instanciación correcta de datos.",None),QtGui.QMessageBox.Ok)
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

		confirm= ( len(Volumen.text())>0 and len(Bottom_Cone_Height.text())>0 and len(Heat_Area.text())>0 and len(Pipe_Diameter.text())>0 
			and len(N_pipes.text())>0 and len(Pipe_Lenght.text())>0	and len(Downtake_Diameter.text())>0 and len(OperationsDays.text())>0 and len(HeatLosses.text())>0 
			and len(Initial_Juice_Brix.text())>0 and len(Initial_Juice_Flow.text())>0 and len(Initial_Evaporator_Level.text())>0 )

		if Evaporator_type!="--Seleccione tipo de evaporador--" and confirm==True:
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
	
	## Other global values
		global Graph

		global nameDialog
		global Dialog_window
		global title_name
		global Ts
		global db

		global comBox_Selector_Type_Evap
		global Selector_effect
		global comBox_InterestVariable

	##Inputs fields
		#Physical properties
		global Volumen
		global Bottom_Cone_Height
		global Heat_Area
		global Pipe_Diameter
		global N_pipes
		global Pipe_Lenght
		global Downtake_Diameter
		global OperationsDays
		global HeatLosses

		#Initial conditions
		global Initial_Juice_Brix
		global Initial_Juice_Flow
		global Initial_Evaporator_Level

	##Process values fields
		global InFluid_Flow
		global InFluid_Temp
		global InFluid_Brix
		global InFluid_InsolubleSolids
		global InFluid_Purity
		global InFluid_Pressure
		global InFluid_pH

		global OutFluid_Flow
		global OutFluid_Temp
		global OutFluid_Brix
		global OutFluid_InsolubleSolids
		global OutFluid_Purity
		global OutFluid_Pressure
		global OutFluid_pH

		global InStm_Flow
		global InStm_Press
		global InStm_Temp

		global CondStm_Flow
		global CondStm_Press
		global CondStm_Temp

		global OutStm_Flow
		global OutStm_Press
		global OutStm_Temp


		Ts=ts
		db=Data_Base

		Vali = Validator()
		nameDialog=name
		title_name=str(item.label.toPlainText())
		Dialog_window=Dialog

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(641, 468)

		self.verticalLayout = QtGui.QVBoxLayout(Dialog)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

	##----Selector of evaporator type----##		
		comBox_Selector_Type_Evap = QtGui.QComboBox(Dialog)
		comBox_Selector_Type_Evap.setObjectName(_fromUtf8("comBox_Selector_Type_Evap"))
		comBox_Selector_Type_Evap.addItem("--Seleccione tipo de evaporador--")
		comBox_Selector_Type_Evap.addItem("Evaporador Robert")
		comBox_Selector_Type_Evap.addItem("Evaporador Kestner")
		comBox_Selector_Type_Evap.addItem("Evaporador Falling Film")
		comBox_Selector_Type_Evap.setCurrentIndex(1)
		comBox_Selector_Type_Evap.activated.connect(self.selection_EvaporatorType)
		self.verticalLayout.addWidget(comBox_Selector_Type_Evap)
	
	##--Tab widget--##	
		self.tabWidget_Evap = QtGui.QTabWidget(Dialog)
		self.tabWidget_Evap.setObjectName(_fromUtf8("tabWidget_Evap"))
		
		self.Evap_tab_1 = QtGui.QWidget()
		self.Evap_tab_1.setObjectName(_fromUtf8("Evap_tab_1"))
		self.tabWidget_Evap.addTab(self.Evap_tab_1, _fromUtf8(""))

		self.Evap_tab_2 = QtGui.QWidget()
		self.Evap_tab_2.setObjectName(_fromUtf8("Evap_tab_2"))
		self.tabWidget_Evap.addTab(self.Evap_tab_2, _fromUtf8(""))

		self.Evap_tab_3 = QtGui.QWidget()
		self.Evap_tab_3.setObjectName(_fromUtf8("Evap_tab_3"))
		self.tabWidget_Evap.addTab(self.Evap_tab_3, _fromUtf8(""))


		self.gridLayout_2 = QtGui.QGridLayout(self.Evap_tab_1)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
	  

	##----Instantiation of elements for physical properties----## 
		self.Evapor_propert_GrBx = QtGui.QGroupBox(self.Evap_tab_1)
		self.Evapor_propert_GrBx.setObjectName(_fromUtf8("Evapor_propert_GrBx"))
		self.gridLayout = QtGui.QGridLayout(self.Evapor_propert_GrBx)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

		#Volumen
		self.label_Volumen = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Volumen.sizePolicy().hasHeightForWidth())
		self.label_Volumen.setSizePolicy(sizePolicy)
		self.label_Volumen.setObjectName(_fromUtf8("label_Volumen"))
		self.gridLayout.addWidget(self.label_Volumen, 0, 0, 1, 1)
		Volumen = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Volumen.sizePolicy().hasHeightForWidth())
		Volumen.setSizePolicy(sizePolicy)
		Volumen.setReadOnly(False)
		Volumen.setObjectName(_fromUtf8("Volumen"))
		Volumen.setText("20.0")
		self.gridLayout.addWidget(Volumen, 0, 1, 1, 1)
		
		##Bottom cone heigh
		self.label_Bottom_Cone_Height = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Bottom_Cone_Height.sizePolicy().hasHeightForWidth())
		self.label_Bottom_Cone_Height.setSizePolicy(sizePolicy)
		self.label_Bottom_Cone_Height.setObjectName(_fromUtf8("label_Bottom_Cone_Height"))
		self.gridLayout.addWidget(self.label_Bottom_Cone_Height, 1, 0, 1, 1)
		Bottom_Cone_Height = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Bottom_Cone_Height.sizePolicy().hasHeightForWidth())
		Bottom_Cone_Height.setSizePolicy(sizePolicy)
		Bottom_Cone_Height.setReadOnly(False)
		Bottom_Cone_Height.setObjectName(_fromUtf8("Bottom_Cone_Height"))
		Bottom_Cone_Height.setText("0.5")
		self.gridLayout.addWidget(Bottom_Cone_Height, 1, 1, 1, 1)

		##Heat area
		self.label_Heat_Area = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Heat_Area.sizePolicy().hasHeightForWidth())
		self.label_Heat_Area.setSizePolicy(sizePolicy)
		self.label_Heat_Area.setObjectName(_fromUtf8("label_Heat_Area"))
		self.gridLayout.addWidget(self.label_Heat_Area, 2, 0, 1, 1)
		Heat_Area = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Heat_Area.sizePolicy().hasHeightForWidth())
		Heat_Area.setSizePolicy(sizePolicy)
		Heat_Area.setReadOnly(False)
		Heat_Area.setObjectName(_fromUtf8("Heat_Area"))
		Heat_Area.setText("900.0")
		self.gridLayout.addWidget(Heat_Area, 2, 1, 1, 1)

		##Pipe diameter
		self.label_Pipe_Diameter = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Pipe_Diameter.sizePolicy().hasHeightForWidth())
		self.label_Pipe_Diameter.setSizePolicy(sizePolicy)
		self.label_Pipe_Diameter.setObjectName(_fromUtf8("label_Pipe_Diameter"))
		self.gridLayout.addWidget(self.label_Pipe_Diameter, 3, 0, 1, 1)
		Pipe_Diameter = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Pipe_Diameter.sizePolicy().hasHeightForWidth())
		Pipe_Diameter.setSizePolicy(sizePolicy)
		Pipe_Diameter.setReadOnly(False)
		Pipe_Diameter.setObjectName(_fromUtf8("Pipe_Diameter"))
		Pipe_Diameter.setText("2.0")
		self.gridLayout.addWidget(Pipe_Diameter, 3, 1, 1, 1)
		
		##Number of pipes
		self.label_N_pipes = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_N_pipes.sizePolicy().hasHeightForWidth())
		self.label_N_pipes.setSizePolicy(sizePolicy)
		self.label_N_pipes.setObjectName(_fromUtf8("label_N_pipes"))
		self.gridLayout.addWidget(self.label_N_pipes, 4, 0, 1, 1)
		N_pipes = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(N_pipes.sizePolicy().hasHeightForWidth())
		N_pipes.setSizePolicy(sizePolicy)
		N_pipes.setReadOnly(False)
		N_pipes.setObjectName(_fromUtf8("N_pipes"))
		N_pipes.setText("1500.0")
		self.gridLayout.addWidget(N_pipes, 4, 1, 1, 1)
		
		##Pipe lenght
		self.label_Pipe_Lenght = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Pipe_Lenght.sizePolicy().hasHeightForWidth())
		self.label_Pipe_Lenght.setSizePolicy(sizePolicy)
		self.label_Pipe_Lenght.setObjectName(_fromUtf8("label_Pipe_Lenght"))
		self.gridLayout.addWidget(self.label_Pipe_Lenght, 5, 0, 1, 1)
		Pipe_Lenght = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Pipe_Lenght.sizePolicy().hasHeightForWidth())
		Pipe_Lenght.setSizePolicy(sizePolicy)
		Pipe_Lenght.setReadOnly(False)
		Pipe_Lenght.setObjectName(_fromUtf8("Pipe_Lenght"))
		Pipe_Lenght.setText("2.0")
		self.gridLayout.addWidget(Pipe_Lenght, 5, 1, 1, 1)

		##Downtake diameter
		self.label_Downtake_Diameter = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Downtake_Diameter.sizePolicy().hasHeightForWidth())
		self.label_Downtake_Diameter.setSizePolicy(sizePolicy)
		self.label_Downtake_Diameter.setObjectName(_fromUtf8("label_Downtake_Diameter"))
		self.gridLayout.addWidget(self.label_Downtake_Diameter, 6, 0, 1, 1)
		Downtake_Diameter = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Downtake_Diameter.sizePolicy().hasHeightForWidth())
		Downtake_Diameter.setSizePolicy(sizePolicy)
		Downtake_Diameter.setReadOnly(False)
		Downtake_Diameter.setObjectName(_fromUtf8("Downtake_Diameter"))
		Downtake_Diameter.setText("15.748")
		self.gridLayout.addWidget(Downtake_Diameter, 6, 1, 1, 1)

		##Operation days
		self.label_OperationsDays = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OperationsDays.sizePolicy().hasHeightForWidth())
		self.label_OperationsDays.setSizePolicy(sizePolicy)
		self.label_OperationsDays.setObjectName(_fromUtf8("label_OperationsDays"))
		self.gridLayout.addWidget(self.label_OperationsDays, 7, 0, 1, 1)
		OperationsDays = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OperationsDays.sizePolicy().hasHeightForWidth())
		OperationsDays.setSizePolicy(sizePolicy)
		OperationsDays.setReadOnly(False)
		OperationsDays.setObjectName(_fromUtf8("OperationsDays"))
		OperationsDays.setText("0.0")
		self.gridLayout.addWidget(OperationsDays, 7, 1, 1, 1)

		##Heat losses
		self.label_HeatLosses = QtGui.QLabel(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_HeatLosses.sizePolicy().hasHeightForWidth())
		self.label_HeatLosses.setSizePolicy(sizePolicy)
		self.label_HeatLosses.setObjectName(_fromUtf8("label_HeatLosses"))
		self.gridLayout.addWidget(self.label_HeatLosses, 8, 0, 1, 1)
		HeatLosses = QtGui.QLineEdit(self.Evapor_propert_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(HeatLosses.sizePolicy().hasHeightForWidth())
		HeatLosses.setSizePolicy(sizePolicy)
		HeatLosses.setReadOnly(False)
		HeatLosses.setObjectName(_fromUtf8("HeatLosses"))
		HeatLosses.setText("0.0")
		self.gridLayout.addWidget(HeatLosses, 8, 1, 1, 1)

		##Number of effect
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.label_efectt = QtGui.QLabel(self.Evapor_propert_GrBx)
		self.label_efectt.setObjectName(_fromUtf8("label_efectt"))
		self.horizontalLayout.addWidget(self.label_efectt)
		Selector_effect = QtGui.QComboBox(self.Evapor_propert_GrBx)
		Selector_effect.setObjectName(_fromUtf8("Selector_effect"))
		Selector_effect.addItem("1")
		Selector_effect.addItem("2")
		Selector_effect.addItem("3")
		Selector_effect.addItem("4")
		Selector_effect.addItem("5")
		self.horizontalLayout.addWidget(Selector_effect)
		self.gridLayout.addLayout(self.horizontalLayout, 9, 0, 1, 1)

		self.gridLayout_2.addWidget(self.Evapor_propert_GrBx, 0, 0, 1, 1)

	##----Instantiation of elements for the initial condition----##
		self.Initial_Conditions_GrBx = QtGui.QGroupBox(self.Evap_tab_1)
		self.Initial_Conditions_GrBx.setObjectName(_fromUtf8("Initial_Conditions_GrBx"))
		self.gridLayout_3 = QtGui.QGridLayout(self.Initial_Conditions_GrBx)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))

		## Output juice brix 
		self.label_Output_Juice_Brix = QtGui.QLabel(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Output_Juice_Brix.sizePolicy().hasHeightForWidth())
		self.label_Output_Juice_Brix.setSizePolicy(sizePolicy)
		self.label_Output_Juice_Brix.setObjectName(_fromUtf8("label_Output_Juice_Brix"))
		self.gridLayout_3.addWidget(self.label_Output_Juice_Brix, 0, 0, 1, 1)
		Initial_Juice_Brix = QtGui.QLineEdit(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Initial_Juice_Brix.sizePolicy().hasHeightForWidth())
		Initial_Juice_Brix.setSizePolicy(sizePolicy)
		Initial_Juice_Brix.setObjectName(_fromUtf8("Output_Juice_Brix"))
		Initial_Juice_Brix.setText("19.0")
		self.gridLayout_3.addWidget(Initial_Juice_Brix, 0, 1, 1, 1)
		
		## Output juice flow
		self.label_Output_Juice_Flow = QtGui.QLabel(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Output_Juice_Flow.sizePolicy().hasHeightForWidth())
		self.label_Output_Juice_Flow.setSizePolicy(sizePolicy)
		self.label_Output_Juice_Flow.setObjectName(_fromUtf8("label_Output_Juice_Flow"))
		self.gridLayout_3.addWidget(self.label_Output_Juice_Flow, 1, 0, 1, 1)
		Initial_Juice_Flow = QtGui.QLineEdit(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Initial_Juice_Flow.sizePolicy().hasHeightForWidth())
		Initial_Juice_Flow.setSizePolicy(sizePolicy)
		Initial_Juice_Flow.setObjectName(_fromUtf8("Output_Juice_Flow"))
		Initial_Juice_Flow.setText("75.0")
		self.gridLayout_3.addWidget(Initial_Juice_Flow, 1, 1, 1, 1)

		## Output evaporator level
		self.label_Evaporator_Level = QtGui.QLabel(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Evaporator_Level.sizePolicy().hasHeightForWidth())
		self.label_Evaporator_Level.setSizePolicy(sizePolicy)
		self.label_Evaporator_Level.setObjectName(_fromUtf8("label_Evaporator_Level"))
		self.gridLayout_3.addWidget(self.label_Evaporator_Level, 2, 0, 1, 1)
		Initial_Evaporator_Level = QtGui.QLineEdit(self.Initial_Conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Initial_Evaporator_Level.sizePolicy().hasHeightForWidth())
		Initial_Evaporator_Level.setSizePolicy(sizePolicy)
		Initial_Evaporator_Level.setObjectName(_fromUtf8("Evaporator_Level"))
		Initial_Evaporator_Level.setText("35.0")
		self.gridLayout_3.addWidget(Initial_Evaporator_Level, 2, 1, 1, 1)

		self.gridLayout_2.addWidget(self.Initial_Conditions_GrBx, 0, 1, 1, 1)


	##--Instance button--##
		self.OKButton_Evap = QtGui.QPushButton(self.Evap_tab_1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OKButton_Evap.sizePolicy().hasHeightForWidth())
		self.OKButton_Evap.setSizePolicy(sizePolicy)
		self.OKButton_Evap.setObjectName(_fromUtf8("OKButton_Evap"))
		self.OKButton_Evap.clicked.connect(self.confirm_param)
		self.gridLayout_2.addWidget(self.OKButton_Evap, 2, 1, 1, 1)


	##----Instantiation of elements for input fluid----##

		self.gridLayout_4 = QtGui.QGridLayout(self.Evap_tab_2)
		self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
	   
		self.Input_fluid_GrBx = QtGui.QGroupBox(self.Evap_tab_2)
		self.Input_fluid_GrBx.setObjectName(_fromUtf8("Input_fluid_GrBx"))
		self.gridLayout_5 = QtGui.QGridLayout(self.Input_fluid_GrBx)
		self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
		
		## Flow
		self.label_InFluid_Flow = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Flow.setSizePolicy(sizePolicy)
		self.label_InFluid_Flow.setObjectName(_fromUtf8("label_InFluid_Flow"))
		self.gridLayout_5.addWidget(self.label_InFluid_Flow, 0, 0, 1, 1)
		InFluid_Flow = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Flow.sizePolicy().hasHeightForWidth())
		InFluid_Flow.setSizePolicy(sizePolicy)
		InFluid_Flow.setReadOnly(True)
		InFluid_Flow.setObjectName(_fromUtf8("InFluid_Flow"))
		self.gridLayout_5.addWidget(InFluid_Flow, 0, 1, 1, 1)

		## Temperature
		self.label_InFluid_Temp = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Temp.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Temp.setSizePolicy(sizePolicy)
		self.label_InFluid_Temp.setObjectName(_fromUtf8("label_InFluid_Temp"))
		self.gridLayout_5.addWidget(self.label_InFluid_Temp, 1, 0, 1, 1)
		InFluid_Temp = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Temp.sizePolicy().hasHeightForWidth())
		InFluid_Temp.setSizePolicy(sizePolicy)
		InFluid_Temp.setReadOnly(True)
		InFluid_Temp.setObjectName(_fromUtf8("InFluid_Temp"))
		self.gridLayout_5.addWidget(InFluid_Temp, 1, 1, 1, 1)
		
		## Brix
		self.label_InFluid_Brix = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Brix.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Brix.setSizePolicy(sizePolicy)
		self.label_InFluid_Brix.setObjectName(_fromUtf8("label_InFluid_Brix"))
		self.gridLayout_5.addWidget(self.label_InFluid_Brix, 2, 0, 1, 1)
		InFluid_Brix = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Brix.sizePolicy().hasHeightForWidth())
		InFluid_Brix.setSizePolicy(sizePolicy)
		InFluid_Brix.setReadOnly(True)
		InFluid_Brix.setObjectName(_fromUtf8("InFluid_Brix"))
		self.gridLayout_5.addWidget(InFluid_Brix, 2, 1, 1, 1)

		## Insoluble solids
		self.label_InFluid_InsolubleSolids = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.label_InFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		self.label_InFluid_InsolubleSolids.setObjectName(_fromUtf8("label_InFluid_InsolubleSolids"))
		self.gridLayout_5.addWidget(self.label_InFluid_InsolubleSolids, 3, 0, 1, 1)
		InFluid_InsolubleSolids = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		InFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		InFluid_InsolubleSolids.setReadOnly(True)
		InFluid_InsolubleSolids.setObjectName(_fromUtf8("InFluid_InsolubleSolids"))
		self.gridLayout_5.addWidget(InFluid_InsolubleSolids, 3, 1, 1, 1)

		## Purity
		self.label_InFluid_Purity = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Purity.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Purity.setSizePolicy(sizePolicy)
		self.label_InFluid_Purity.setObjectName(_fromUtf8("label_InFluid_Purity"))
		self.gridLayout_5.addWidget(self.label_InFluid_Purity, 4, 0, 1, 1)
		InFluid_Purity = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Purity.sizePolicy().hasHeightForWidth())
		InFluid_Purity.setSizePolicy(sizePolicy)
		InFluid_Purity.setReadOnly(True)
		InFluid_Purity.setObjectName(_fromUtf8("InFluid_Purity"))
		self.gridLayout_5.addWidget(InFluid_Purity, 4, 1, 1, 1)

		## Pressure
		self.label_InFluid_Pressure = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Pressure.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Pressure.setSizePolicy(sizePolicy)
		self.label_InFluid_Pressure.setObjectName(_fromUtf8("label_InFluid_Pressure"))
		self.gridLayout_5.addWidget(self.label_InFluid_Pressure, 5, 0, 1, 1)
		InFluid_Pressure = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_Pressure.sizePolicy().hasHeightForWidth())
		InFluid_Pressure.setSizePolicy(sizePolicy)
		InFluid_Pressure.setReadOnly(True)
		InFluid_Pressure.setObjectName(_fromUtf8("InFluid_Pressure"))
		self.gridLayout_5.addWidget(InFluid_Pressure, 5, 1, 1, 1)


		## pH
		self.label_InFluid_pH = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_pH.sizePolicy().hasHeightForWidth())
		self.label_InFluid_pH.setSizePolicy(sizePolicy)
		self.label_InFluid_pH.setObjectName(_fromUtf8("label_InFluid_pH"))
		self.gridLayout_5.addWidget(self.label_InFluid_pH, 6, 0, 1, 1)
		InFluid_pH = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InFluid_pH.sizePolicy().hasHeightForWidth())
		InFluid_pH.setSizePolicy(sizePolicy)
		InFluid_pH.setReadOnly(True)
		InFluid_pH.setObjectName(_fromUtf8("InFluid_pH"))
		self.gridLayout_5.addWidget(InFluid_pH, 6, 1, 1, 1)
		self.gridLayout_4.addWidget(self.Input_fluid_GrBx, 0, 0, 1, 1)
	   
	##----Instantiation of elements for output fluid----##

		self.Output_fluid_GrBx = QtGui.QGroupBox(self.Evap_tab_2)
		self.Output_fluid_GrBx.setObjectName(_fromUtf8("Output_fluid_GrBx"))
		self.gridLayout_6 = QtGui.QGridLayout(self.Output_fluid_GrBx)
		self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
		
		## Flow
		self.label_OutFluid_Flow = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Flow.setSizePolicy(sizePolicy)
		self.label_OutFluid_Flow.setObjectName(_fromUtf8("label_OutFluid_Flow"))
		self.gridLayout_6.addWidget(self.label_OutFluid_Flow, 0, 0, 1, 1)
		OutFluid_Flow = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Flow.sizePolicy().hasHeightForWidth())
		OutFluid_Flow.setSizePolicy(sizePolicy)
		OutFluid_Flow.setReadOnly(True)
		OutFluid_Flow.setObjectName(_fromUtf8("OutFluid_Flow"))
		self.gridLayout_6.addWidget(OutFluid_Flow, 0, 1, 1, 1)

		## Temperature		
		self.label_OutFluid_Temp = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Temp.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Temp.setSizePolicy(sizePolicy)
		self.label_OutFluid_Temp.setObjectName(_fromUtf8("label_OutFluid_Temp"))
		self.gridLayout_6.addWidget(self.label_OutFluid_Temp, 1, 0, 1, 1)
		OutFluid_Temp = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Temp.sizePolicy().hasHeightForWidth())
		OutFluid_Temp.setSizePolicy(sizePolicy)
		OutFluid_Temp.setReadOnly(True)
		OutFluid_Temp.setObjectName(_fromUtf8("OutFluid_Temp"))
		self.gridLayout_6.addWidget(OutFluid_Temp, 1, 1, 1, 1)
		
		## Brix
		self.label_OutFluid_Brix = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Brix.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Brix.setSizePolicy(sizePolicy)
		self.label_OutFluid_Brix.setObjectName(_fromUtf8("label_OutFluid_Brix"))
		self.gridLayout_6.addWidget(self.label_OutFluid_Brix, 2, 0, 1, 1)
		OutFluid_Brix = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Brix.sizePolicy().hasHeightForWidth())
		OutFluid_Brix.setSizePolicy(sizePolicy)
		OutFluid_Brix.setReadOnly(True)
		OutFluid_Brix.setObjectName(_fromUtf8("OutFluid_Brix"))
		self.gridLayout_6.addWidget(OutFluid_Brix, 2, 1, 1, 1)
		
		## Insoluble solids
		self.label_OutFluid_InsolubleSolids = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		self.label_OutFluid_InsolubleSolids.setObjectName(_fromUtf8("label_OutFluid_InsolubleSolids"))
		self.gridLayout_6.addWidget(self.label_OutFluid_InsolubleSolids, 3, 0, 1, 1)
		OutFluid_InsolubleSolids = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		OutFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		OutFluid_InsolubleSolids.setReadOnly(True)
		OutFluid_InsolubleSolids.setObjectName(_fromUtf8("OutFluid_InsolubleSolids"))
		self.gridLayout_6.addWidget(OutFluid_InsolubleSolids, 3, 1, 1, 1)
		
		## Purity
		self.label_OutFluid_Purity = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Purity.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Purity.setSizePolicy(sizePolicy)
		self.label_OutFluid_Purity.setObjectName(_fromUtf8("label_OutFluid_Purity"))
		self.gridLayout_6.addWidget(self.label_OutFluid_Purity, 4, 0, 1, 1)
		OutFluid_Purity = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Purity.sizePolicy().hasHeightForWidth())
		OutFluid_Purity.setSizePolicy(sizePolicy)
		OutFluid_Purity.setReadOnly(True)
		OutFluid_Purity.setObjectName(_fromUtf8("OutFluid_Purity"))
		self.gridLayout_6.addWidget(OutFluid_Purity, 4, 1, 1, 1)

		## Pressure
		self.label_OutFluid_Pressure = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Pressure.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Pressure.setSizePolicy(sizePolicy)
		self.label_OutFluid_Pressure.setObjectName(_fromUtf8("label_OutFluid_Pressure"))
		self.gridLayout_6.addWidget(self.label_OutFluid_Pressure, 5, 0, 1, 1)
		OutFluid_Pressure = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_Pressure.sizePolicy().hasHeightForWidth())
		OutFluid_Pressure.setSizePolicy(sizePolicy)
		OutFluid_Pressure.setReadOnly(True)
		OutFluid_Pressure.setObjectName(_fromUtf8("OutFluid_Pressure"))
		self.gridLayout_6.addWidget(OutFluid_Pressure, 5, 1, 1, 1)
		
		## pH
		self.label_OutFluid_pH = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_pH.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_pH.setSizePolicy(sizePolicy)
		self.label_OutFluid_pH.setObjectName(_fromUtf8("label_OutFluid_pH"))
		self.gridLayout_6.addWidget(self.label_OutFluid_pH, 6, 0, 1, 1)
		OutFluid_pH = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutFluid_pH.sizePolicy().hasHeightForWidth())
		OutFluid_pH.setSizePolicy(sizePolicy)
		OutFluid_pH.setReadOnly(True)
		OutFluid_pH.setObjectName(_fromUtf8("OutFluid_pH"))
		self.gridLayout_6.addWidget(OutFluid_pH, 6, 1, 1, 1)
		self.gridLayout_4.addWidget(self.Output_fluid_GrBx, 0, 1, 1, 1)

	##----Instantiation of elements for input steam----##
		self.Input_Steam_GrBx = QtGui.QGroupBox(self.Evap_tab_2)
		self.Input_Steam_GrBx.setObjectName(_fromUtf8("Input_Steam_GrBx"))
		self.gridLayout_7 = QtGui.QGridLayout(self.Input_Steam_GrBx)
		self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
		
		## Flow
		self.label_InStm_Flow = QtGui.QLabel(self.Input_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InStm_Flow.sizePolicy().hasHeightForWidth())
		self.label_InStm_Flow.setSizePolicy(sizePolicy)
		self.label_InStm_Flow.setObjectName(_fromUtf8("label_InStm_Flow"))
		self.gridLayout_7.addWidget(self.label_InStm_Flow, 0, 0, 1, 1)
		InStm_Flow = QtGui.QLineEdit(self.Input_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InStm_Flow.sizePolicy().hasHeightForWidth())
		InStm_Flow.setSizePolicy(sizePolicy)
		InStm_Flow.setReadOnly(True)
		InStm_Flow.setObjectName(_fromUtf8("InStm_Flow"))
		self.gridLayout_7.addWidget(InStm_Flow, 0, 1, 1, 1)
		
		## Pressure
		self.label_InStm_Press = QtGui.QLabel(self.Input_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InStm_Press.sizePolicy().hasHeightForWidth())
		self.label_InStm_Press.setSizePolicy(sizePolicy)
		self.label_InStm_Press.setObjectName(_fromUtf8("label_InStm_Press"))
		self.gridLayout_7.addWidget(self.label_InStm_Press, 1, 0, 1, 1)
		InStm_Press = QtGui.QLineEdit(self.Input_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InStm_Press.sizePolicy().hasHeightForWidth())
		InStm_Press.setSizePolicy(sizePolicy)
		InStm_Press.setReadOnly(True)
		InStm_Press.setObjectName(_fromUtf8("InStm_Press"))
		self.gridLayout_7.addWidget(InStm_Press, 1, 1, 1, 1)	

		## Temperature
		self.label_InStm_Temp = QtGui.QLabel(self.Input_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InStm_Temp.sizePolicy().hasHeightForWidth())
		self.label_InStm_Temp.setSizePolicy(sizePolicy)
		self.label_InStm_Temp.setObjectName(_fromUtf8("label_InStm_Temp"))
		self.gridLayout_7.addWidget(self.label_InStm_Temp, 2, 0, 1, 1)
		InStm_Temp = QtGui.QLineEdit(self.Input_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(InStm_Temp.sizePolicy().hasHeightForWidth())
		InStm_Temp.setSizePolicy(sizePolicy)
		InStm_Temp.setReadOnly(True)
		InStm_Temp.setObjectName(_fromUtf8("InStm_Temp"))
		self.gridLayout_7.addWidget(InStm_Temp, 2, 1, 1, 1)
		self.gridLayout_4.addWidget(self.Input_Steam_GrBx, 1, 0, 1, 1)

	##----Instantiation of elements for condensed steam----##
		self.Condensed_steam_GrBx = QtGui.QGroupBox(self.Evap_tab_2)
		self.Condensed_steam_GrBx.setObjectName(_fromUtf8("Condensed_steam_GrBx"))
		self.gridLayout_8 = QtGui.QGridLayout(self.Condensed_steam_GrBx)
		self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
		
		## Flow
		self.label_CondStm_Flow = QtGui.QLabel(self.Condensed_steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_CondStm_Flow.sizePolicy().hasHeightForWidth())
		self.label_CondStm_Flow.setSizePolicy(sizePolicy)
		self.label_CondStm_Flow.setObjectName(_fromUtf8("label_CondStm_Flow"))
		self.gridLayout_8.addWidget(self.label_CondStm_Flow, 0, 0, 1, 1)
		CondStm_Flow = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CondStm_Flow.sizePolicy().hasHeightForWidth())
		CondStm_Flow.setSizePolicy(sizePolicy)
		CondStm_Flow.setReadOnly(True)
		CondStm_Flow.setObjectName(_fromUtf8("CondStm_Flow"))
		self.gridLayout_8.addWidget(CondStm_Flow, 0, 1, 1, 1)
		
		## Pressure
		self.label_CondStm_Press = QtGui.QLabel(self.Condensed_steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_CondStm_Press.sizePolicy().hasHeightForWidth())
		self.label_CondStm_Press.setSizePolicy(sizePolicy)
		self.label_CondStm_Press.setObjectName(_fromUtf8("label_CondStm_Press"))
		self.gridLayout_8.addWidget(self.label_CondStm_Press, 1, 0, 1, 1)
		CondStm_Press = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CondStm_Press.sizePolicy().hasHeightForWidth())
		CondStm_Press.setSizePolicy(sizePolicy)
		CondStm_Press.setReadOnly(True)
		CondStm_Press.setObjectName(_fromUtf8("CondStm_Press"))
		self.gridLayout_8.addWidget(CondStm_Press, 1, 1, 1, 1)
		
		## Temperature
		self.label_CondStm_Temp = QtGui.QLabel(self.Condensed_steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_CondStm_Temp.sizePolicy().hasHeightForWidth())
		self.label_CondStm_Temp.setSizePolicy(sizePolicy)
		self.label_CondStm_Temp.setObjectName(_fromUtf8("label_CondStm_Temp"))
		self.gridLayout_8.addWidget(self.label_CondStm_Temp, 2, 0, 1, 1)
		CondStm_Temp = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CondStm_Temp.sizePolicy().hasHeightForWidth())
		CondStm_Temp.setSizePolicy(sizePolicy)
		CondStm_Temp.setReadOnly(True)
		CondStm_Temp.setObjectName(_fromUtf8("CondStm_Temp"))
		self.gridLayout_8.addWidget(CondStm_Temp, 2, 1, 1, 1)
		self.gridLayout_4.addWidget(self.Condensed_steam_GrBx, 1, 1, 1, 1)

	##----Instantiation of elements for output steam----##
		self.Output_Steam_GrBx = QtGui.QGroupBox(self.Evap_tab_2)
		self.Output_Steam_GrBx.setObjectName(_fromUtf8("Output_Steam_GrBx"))
		self.gridLayout_9 = QtGui.QGridLayout(self.Output_Steam_GrBx)
		self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
		
		## Flow
		self.label_OutStm_Flow = QtGui.QLabel(self.Output_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutStm_Flow.sizePolicy().hasHeightForWidth())
		self.label_OutStm_Flow.setSizePolicy(sizePolicy)
		self.label_OutStm_Flow.setObjectName(_fromUtf8("label_OutStm_Flow"))
		self.gridLayout_9.addWidget(self.label_OutStm_Flow, 0, 0, 1, 1)
		OutStm_Flow = QtGui.QLineEdit(self.Output_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutStm_Flow.sizePolicy().hasHeightForWidth())
		OutStm_Flow.setSizePolicy(sizePolicy)
		OutStm_Flow.setReadOnly(True)
		OutStm_Flow.setObjectName(_fromUtf8("OutStm_Flow"))
		self.gridLayout_9.addWidget(OutStm_Flow, 0, 1, 1, 1)
		
		## Temperature
		self.label_OutStm_Temp = QtGui.QLabel(self.Output_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutStm_Temp.sizePolicy().hasHeightForWidth())
		self.label_OutStm_Temp.setSizePolicy(sizePolicy)
		self.label_OutStm_Temp.setObjectName(_fromUtf8("label_OutStm_Temp"))
		self.gridLayout_9.addWidget(self.label_OutStm_Temp, 0, 2, 1, 1)
		OutStm_Temp = QtGui.QLineEdit(self.Output_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutStm_Temp.sizePolicy().hasHeightForWidth())
		OutStm_Temp.setSizePolicy(sizePolicy)
		OutStm_Temp.setReadOnly(True)
		OutStm_Temp.setObjectName(_fromUtf8("OutStm_Temp"))
		self.gridLayout_9.addWidget(OutStm_Temp, 0, 3, 1, 1)
		
		## Pressure
		self.label_OutStm_Press = QtGui.QLabel(self.Output_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutStm_Press.sizePolicy().hasHeightForWidth())
		self.label_OutStm_Press.setSizePolicy(sizePolicy)
		self.label_OutStm_Press.setObjectName(_fromUtf8("label_OutStm_Press"))
		self.gridLayout_9.addWidget(self.label_OutStm_Press, 1, 0, 1, 1)
		OutStm_Press = QtGui.QLineEdit(self.Output_Steam_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(OutStm_Press.sizePolicy().hasHeightForWidth())
		OutStm_Press.setSizePolicy(sizePolicy)
		OutStm_Press.setReadOnly(True)
		OutStm_Press.setObjectName(_fromUtf8("OutStm_Press"))
		self.gridLayout_9.addWidget(OutStm_Press, 1, 1, 1, 1)
		self.gridLayout_4.addWidget(self.Output_Steam_GrBx, 2, 0, 1, 2)
		

	##----Instantiation of elements for variable output---#
		self.verticalLayout_2 = QtGui.QVBoxLayout(self.Evap_tab_3)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		comBox_InterestVariable = QtGui.QComboBox(self.Evap_tab_3)
		comBox_InterestVariable.setObjectName(_fromUtf8("comBox_InterestVariable"))
		comBox_InterestVariable.addItem("Brix de jugo de salida")
		comBox_InterestVariable.addItem("Flujo de jugo de salida")
		comBox_InterestVariable.addItem("Nivel en evaporador")
		comBox_InterestVariable.activated.connect(self.selection_interest_variable)

	#--Dynamic Graph--##
		verticalLayoutWidget = QtGui.QWidget()
		verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 410, 260))
		verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

		Graph = DynamicGraphic(Dialog,Ts,Enable_cursor,False,False,self.Evap_tab_3, width=4, height=3, dpi=85)
		Graph.axes.set_xlabel('Time (s)',fontsize=11)
		Graph.axes.set_ylabel(_translate("Dialog", "Bjout [%]", None),fontsize=11)
		Graph.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		Graph.set_legends()
		verticalLayoutWidget.setLayout(Graph.dynamic_graph)

		self.Timer_graph()

		self.verticalLayout_2.addWidget(comBox_InterestVariable)
		self.verticalLayout_2.addWidget(verticalLayoutWidget)
		
		
		self.verticalLayout.addWidget(self.tabWidget_Evap)

		self.retranslateUi(Dialog)
		self.tabWidget_Evap.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		update_window()

	# Evaluate change in evaporator type
	def selection_EvaporatorType(self): 
		global Evaporator_type
		Evaporator_type=comBox_Selector_Type_Evap.currentText()

	# Evaluate change in interest variable
	def selection_interest_variable(self):
		global one_time

		global Interest_variable
		global model_value
		global label_graph
		global label_y_axis

		global brix_model_value
		global Le_model_value
		global flow_model_value

		Interest_variable=comBox_InterestVariable.currentText()

		model_value=[]
		label_graph=""
		label_y_axis=""
		if Interest_variable=="Brix de jugo de salida":
			model_value=brix_model_value
			label_graph="Brix"
			label_y_axis="Brix [%]"
		elif Interest_variable=="Flujo de jugo de salida":
			model_value=flow_model_value
			label_graph="Flujo"
			label_y_axis="Flujo [kg/s]"
		elif Interest_variable=="Nivel en evaporador":
			model_value=Le_model_value
			label_graph="Nivel"
			label_y_axis="Nivel [%]"

		if Db_data.time=="stop":
			one_time=1

	# Timer initialization
	def Timer_graph(self):
		# global timer
		self.timer = QtCore.QTimer(Dialog_window)
		self.timer.timeout.connect(update_figure)
		self.timer.start(Ts*100)#Ts*1000-300)
	
	## Labels set text
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Parametros "+title_name, None))
		self.Evapor_propert_GrBx.setTitle(_translate("Dialog", "Propiedades físicas", None))
		self.label_Volumen.setText(_translate("Dialog", "Volumen [m3]", None))
		self.label_Heat_Area.setText(_translate("Dialog", "Área de calentamiento [m2]", None))
		self.label_Pipe_Diameter.setText(_translate("Dialog", "Diámetro interno tubo de \n"
		"calandria [in]", None))
		self.label_Bottom_Cone_Height.setText(_translate("Dialog", "Longitud cono inferior [m]", None))
		self.label_N_pipes.setText(_translate("Dialog", "N° tubos de calandria", None))
		self.label_Pipe_Lenght.setText(_translate("Dialog", "Longitud tubo de calandria \n"
		"[m]", None))

		self.label_OperationsDays.setText(_translate("Dialog", "Días de operación", None))
		self.label_HeatLosses.setText(_translate("Dialog", "Perdidas de calor", None))

		self.label_Downtake_Diameter.setText(_translate("Dialog", "Diámetro downtake [in]", None))
		self.label_efectt.setText(_translate("Dialog", "Efecto", None))
		self.Initial_Conditions_GrBx.setTitle(_translate("Dialog", "Condiciones iniciales", None))
		self.label_Output_Juice_Brix.setText(_translate("Dialog", "Brix de jugo de salida [%]", None))
		self.label_Output_Juice_Flow.setText(_translate("Dialog", "Flujo másico de jugo de salida\n"
		"[t/h]", None))
		self.label_Evaporator_Level.setText(_translate("Dialog", "Nivel en evaporador [%]", None))
		self.OKButton_Evap.setText(_translate("Dialog", "Aceptar", None))
		self.tabWidget_Evap.setTabText(self.tabWidget_Evap.indexOf(self.Evap_tab_1), _translate("Dialog", "Propiedades físicas", None))
		self.Input_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de entrada", None))
		self.label_InFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_InFluid_Brix.setText(_translate("Dialog", "Brix [%]", None))
		self.label_InFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [%]", None))
		self.label_InFluid_Pressure.setText(_translate("Dialog", "Presión [kPa]", None))
		self.label_InFluid_Purity.setText(_translate("Dialog", "Pureza [%]", None))
		self.label_InFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.Output_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de salida", None))
		self.label_OutFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_OutFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_OutFluid_Brix.setText(_translate("Dialog", "Brix [%]", None))
		self.label_OutFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [%]", None))
		self.label_OutFluid_Purity.setText(_translate("Dialog", "Pureza [%]", None))
		self.label_OutFluid_Pressure.setText(_translate("Dialog", "Presión [kPa]", None))
		self.label_OutFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.Input_Steam_GrBx.setTitle(_translate("Dialog", "Vapor vivo", None))
		self.label_InStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InStm_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.label_InStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.Condensed_steam_GrBx.setTitle(_translate("Dialog", "Vapor condensado ", None))
		self.label_CondStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_CondStm_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.label_CondStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.Output_Steam_GrBx.setTitle(_translate("Dialog", "Vapor vegetal", None))
		self.label_OutStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_OutStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_OutStm_Press.setText(_translate("Dialog", "Presión [kPa]", None))
		self.tabWidget_Evap.setTabText(self.tabWidget_Evap.indexOf(self.Evap_tab_2), _translate("Dialog", "Variables de proceso", None))
		self.tabWidget_Evap.setTabText(self.tabWidget_Evap.indexOf(self.Evap_tab_3), _translate("Dialog", "Gráfica", None))

