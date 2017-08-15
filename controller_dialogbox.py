# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PID_properties.ui'
#
# Created: Tue Jul 04 15:26:55 2017
#      by: PyQt4 UI code generator 4.10.2

# Installed Libs
import re

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.ticker import FormatStrFormatter

# Local Libs
from dynamic_diagrams import DynamicGraphic
from control import *
from global_data import *

#global values
global Enable_cursor
global flag_Mv_selector
global flag_Mv_selector2
global one_time
global one_reload
global Mv_selection
global id_time
global SP

Mv_selection="--Variable a controlar--"
Enable_cursor=False
flag_Mv_selector=1
flag_Mv_selector2=1
one_time=1
one_reload=1
id_time=0
SP=0.0

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

##Function for update window when closing
def update_window():
	global P
	global I
	global D
	global SP
	global one_reload
	global one_time

	Num_window=re.sub('([a-zA-Z]+)', "", nameDialog)

	fields="Ans_type,KP,KI,KD,SP,MV_type,Control_type,Control_type_value"
	result=db.read_data("Controllers",fields,"Name","PID"+Num_window)
	controller_data=[]
	if len(result)>0:
		for data in result:
			for values in data:
				controller_data.append(str(values))

		index = selector_answer_type.findText(controller_data[0], QtCore.Qt.MatchFixedString)
		if index >= 0:
			selector_answer_type.setCurrentIndex(index)
		
		index = Mv_selector.findText(controller_data[5], QtCore.Qt.MatchFixedString)
		if index >= 0:
			Mv_selector.setCurrentIndex(index)

		P=float(controller_data[1])
		I=float(controller_data[2])
		D=float(controller_data[3])
		SP=float(controller_data[4])

		info_Mv.setText(str(item_controller.labelMV.toPlainText()))
		info_Pv.setText(str(item_controller.labelPV.toPlainText()))
		info_SP.setText(str(item_controller.labelSP.toPlainText()))

		Control_type=controller_data[6]
		Control_type_value=float(controller_data[7])

		P_value.setText(str(P))
		I_value.setText(str(I))
		D_value.setText(str(D))
		SP_value.setText(str(SP))

		index = signal_control_selector.findText(Control_type, QtCore.Qt.MatchFixedString)
		if index >= 0:
			signal_control_selector.setCurrentIndex(index)

		if signal_control_selector.currentText()=="Automatico":
			label_Spinbox.setText("Setpoint:")
			SpinBox_signal_control.setSingleStep(1)
			SpinBox_signal_control.setMinimum(0)
			SpinBox_signal_control.setMaximum(10000)
			SpinBox_signal_control.setValue(Control_type_value)

		else:
			label_Spinbox.setText("Variable manipulada:")
			SpinBox_signal_control.setSingleStep(10)
			SpinBox_signal_control.setMinimum(10)
			SpinBox_signal_control.setMaximum(100)
			SpinBox_signal_control.setValue(Control_type_value)

	if hasattr(Db_data, 'time'):
		
		if Db_data.time!="stop":
			Enable_cursor=False
		else:
			Enable_cursor=True

		one_time=1
		one_reload=0

## Get data base info for the device connected
def adquire_data_device_connected(device_connected):

	if (re.sub("\d+", "", device_connected))=="Calentador":
		Pv_array=[]

		id_heater=0
		result=db.read_data("Heaters","id","Name","Ht"+re.sub('([a-zA-Z]+)', "", device_connected))
		if len(result)>0:
			for data in result:
				id_heater=data[0]
			
			
			
			fields="Heaters_id,Out_fluid_temperature,Out_fluid_brix,Out_fluid_flow,Out_fluid_pH,Out_fluid_pressure"
			result=db.read_data("Outputs_heater",fields,"LAST","Heaters_id")
			if len(result)>0:	
				for data in result:
					for i,values in enumerate(data):
						if  str(data[0])==str(id_heater):
							if i>0:
								Pv_array.append(values)

	return Pv_array

## Timer for solve controller model and plot controller data
def update_figure():
	global tt
	global Mv_value
	global Pv_value

	global flag_Mv_selector
	global flag_Mv_selector2
	global one_reload
	global PID
	global id_time
	global Graph
	global one_time
	global SP

	if hasattr(Devices, 'array_connections'):		
		if len(Devices.array_connections)>0:
			for k, par_data in enumerate(Devices.array_connections):
				
				if par_data[1]==nameDialog:
					device_connected=par_data[0]
					port_connected=par_data[2]
					for items in  Devices.panel_items:
						for outputs in items.outputs:
							if outputs.name_port==port_connected and  outputs.name_block==device_connected:
								port=outputs
								break

					if (port.typ=="juice" or port.typ=="none") and flag_Mv_selector==1:
						Mv_selector.addItem("Flujo")
						Mv_selector.addItem("Brix")
						Mv_selector.addItem("Temperatura")
						Mv_selector.addItem("Presion")
						Mv_selector.addItem("pH")
						update_window()
						flag_Mv_selector=0
					elif Mv_selector.count()<2:
						# print("Yes PID and not complete comboBox")
						flag_Mv_selector=1

				elif flag_Mv_selector2==1:
					# print("No PID and not delete comboBox")
					Mv_selector.clear()
					Mv_selector.addItem("--Variable a controlar--")
					flag_Mv_selector2=0
					flag_Mv_selector=1

		else:
			# print("No connections")
			Mv_selector.clear()
			Mv_selector.addItem("--Variable a controlar--")
			flag_Mv_selector=1
			flag_Mv_selector2=1

		
	
		if hasattr(Db_data, 'time_id') and Mv_selection!="--Variable a controlar--":

			new_id=False
			if int(Db_data.time_id)>int(id_time):
				new_id=True
			
			id_time=Db_data.time_id
			time=Db_data.time

			if time!="stop" and new_id==True:

				if one_reload==1:
					Graph.reload_toolbar(False)
					one_reload=0
				
				Pv_array=adquire_data_device_connected(device_connected)

				
				if len(Pv_array)>0:
					if Mv_selection=="Temperatura":
						Pv=float(Pv_array[0])

					if signal_control_selector.currentText()=="Automatico":	
						Mv=PID.solve(SP, Pv)					
					else:
						Mv=SpinBox_signal_control.value()
					# print("Mv: "+str(Mv)+" and PV= "+str(Pv))
					item_controller.labelMV.setPlainText("MV: "+str(round(Mv,3)))
					item_controller.labelPV.setPlainText("PV: "+str(round(Pv,3)))

					info_Mv.setText(str(item_controller.labelMV.toPlainText()))
					info_Pv.setText(str(item_controller.labelPV.toPlainText()))
					info_SP.setText(str(item_controller.labelSP.toPlainText()))

					tt.append(float(time))
					Mv_value.append(Mv)
					Pv_value.append(Pv)

					db.update_data("Controllers",["Mv","Pv","Control_type_value"],[Mv,Pv,SpinBox_signal_control.value()],["id"],[id_controller])

					if len(tt)==len(Mv_value):
						ax=Graph.figure.get_axes()
						ax[0].plot(tt,Mv_value,'r-',label="Mv")
						Graph.add_plot(tt,[Pv_value],["Pv"],[0.0],[1.0])
						Graph.set_legends()
						Graph.draw()

						# ax[0].legend_.remove()
						for x,line in enumerate(ax[0].lines): 
							del ax[0].lines[x]
						if len(ax)>1:
							for x,line in enumerate(ax[1].lines): 
								del ax[1].lines[x]

					one_time=1

			elif one_time==1 and time=="stop":
				tt=[0.0]
				Mv_value=[0.0]
				Pv_value=[SP]

				Control_type=str(signal_control_selector.currentText())
				if Control_type=="Automatico":
					SpinBox_signal_control.setValue(float(SP_value.text()))
					Control_type_value=float(SP_value.text())
				else:
					Control_type_value=float(SpinBox_signal_control.value())
					SpinBox_signal_control.setValue(Control_type_value)
				
				db.update_data("Controllers",["Mv","Pv","Control_type_value"],["None","None",SpinBox_signal_control.value()],["id"],[id_controller])

				Enable_cursor=True
				Graph.reload_toolbar(Enable_cursor)

				one_time=0
				one_reload=1

##Function for confirm if exist initialization of controller
def exist_initialization(data):
	global id_controller
	flg=0
	result=db.read_data("Controllers","id","Name",data)
	if len(result)>0:
		for data in result:
			id_controller=data[0]
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
		global tt
		global Mv_value
		global Pv_value

		global pid
		global PID
		global P
		global I
		global D
		global SP
		global id_controller

		Num_window=re.sub('([a-zA-Z]+)', "", nameDialog)

		P=float(P_value.text())
		I=float(I_value.text())
		D=float(D_value.text())
		SP=float(SP_value.text())

		Ans_type=str(selector_answer_type.currentText())
		Control_type=str(signal_control_selector.currentText())


		if Control_type=="Automatico":
			SpinBox_signal_control.setValue(SP)
			Control_type_value=SP
		else:
			Control_type_value=float(SpinBox_signal_control.value())
			SpinBox_signal_control.setValue(Control_type_value)
			

		item_controller.labelSP.setPlainText("SP: "+str(SP))
		info_SP.setText("SP: "+str(SP))
		fields="Time_exec_id,Name,Ans_type,KP,KI,KD,SP,MV_type,Control_type,Control_type_value"
		
		updt=exist_initialization("PID"+Num_window)
		values=[1,"PID"+Num_window,Ans_type,P,I,D,SP,str(Mv_selection),str(Control_type),Control_type_value]
		if updt==0:		
			db.insert_data("Controllers",fields,values)
			if selector_answer_type.currentText()=="Directa":
				PID=pid(Ts,P,I,D)
			else:
				PID=pid(Ts,-P,-I,-D)
			
			result=db.read_data("Controllers","id","Name","PID"+Num_window)
			if len(result)>0:
				for data in result:
					id_controller=data[0]
		else:
			fields=["Time_exec_id","Name","Ans_type","KP","KI","KD","SP","MV_type","Control_type","Control_type_value"]
			db.update_data("Controllers",fields,values,["id"],[float(id_controller)])
			if selector_answer_type.currentText()=="Directa":
				PID.update(Ts,P,I,D)
			else:
				PID.update(Ts,-P,-I,-D)

		
		tt=[0.0]
		Mv_value=[0.0]
		Pv_value=[SP]

		self.close()
		Resultado=QtGui.QDialog()
		QtGui.QMessageBox.information(Resultado,'Ok',_translate("Dialog","Instanciación correcta de datos.",None),QtGui.QMessageBox.Ok)
		# Dialog_window.close()

	
	def NO(self):
		self.close()

## Dialog box class
class Ui_Dialog(object):
	def confirm_param(self):
		global confirm
		global Resultado
		global pd

		confirm=((len(P_value.text())>0)and(len(I_value.text())>0)and(len(D_value.text())>0)and(len(SP_value.text())>0))
		
		if Mv_selection!="--Variable a controlar--" and confirm==True:
			Resultado=QtGui.QDialog()
			pd = window_confirm_param(Resultado.window())
			pd.exec_()
		else:
			self.Resultado=QtGui.QDialog()
			QtGui.QMessageBox.warning(self.Resultado, 
			'Advertencia',
			"Falta por ingresar algun dato.",QtGui.QMessageBox.Ok)

	def setupUi(self,name,ts,Data_Base,item,Dialog):

		#PID coefficients
		global P_value
		global I_value
		global D_value
		global SP_value

		# Info panel
		global info_Mv
		global info_Pv
		global info_SP

		#Normalized parameters
		global label_Mv_range
		global label_Mv_min
		global label_Mv_max
		global Mv_min_value
		global Mv_max_value
		global CheckBox_normalize

		#Selectors and spinbox
		global Mv_selector
		global signal_control_selector
		global selector_answer_type
		global SpinBox_signal_control
		global label_Spinbox

		#Global others
		global Dialog_window
		global title_name
		global nameDialog
		global Ts
		global item_controller
		global db
		global Graph

		
		Validation_text_field = Validator()
		Ts=ts
		Dialog_window=Dialog
		nameDialog=name
		title_name=str(item.label.toPlainText())
		item_controller=item
		db=Data_Base

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.setEnabled(True)
		Dialog.resize(480, 317)

		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
		Dialog.setSizePolicy(sizePolicy)

		self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

	##--Tab widget--##
		self.tabWidget = QtGui.QTabWidget(Dialog)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		
		self.Tab1 = QtGui.QWidget()
		self.Tab1.setObjectName(_fromUtf8("Tab1"))
		self.tabWidget.addTab(self.Tab1, _fromUtf8(""))

		self.Tab2 = QtGui.QWidget()
		self.Tab2.setObjectName(_fromUtf8("Tab2"))
		self.tabWidget.addTab(self.Tab2, _fromUtf8(""))

		self.gridLayout = QtGui.QGridLayout()
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

		self.Layout_tab1 = QtGui.QHBoxLayout(self.Tab1)
		self.Layout_tab1.setObjectName(_fromUtf8("horizontalLayout_2"))

		self.Layout_tab2 = QtGui.QVBoxLayout(self.Tab2)
		self.Layout_tab2.setObjectName(_fromUtf8("verticalLayout"))
	
	##-- Inputs --##
		
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		
		# Manipulated variable
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		
		self.label_Mv= QtGui.QLabel(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Mv.sizePolicy().hasHeightForWidth())
		self.label_Mv.setSizePolicy(sizePolicy)
		self.label_Mv.setObjectName(_fromUtf8("label_Mv"))
		self.horizontalLayout.addWidget(self.label_Mv)
		
		Mv_selector = QtGui.QComboBox(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Mv_selector.sizePolicy().hasHeightForWidth())
		Mv_selector.setSizePolicy(sizePolicy)
		Mv_selector.setObjectName(_fromUtf8("comboBox"))
		Mv_selector.addItem("--Variable a controlar--")
		self.horizontalLayout.addWidget(Mv_selector)
		Mv_selector.activated.connect(self.selection_MvType)
		self.verticalLayout_2.addLayout(self.horizontalLayout)
		
		# Answer type
		self.horizontalLayout_33 = QtGui.QHBoxLayout()
		self.horizontalLayout_33.setObjectName(_fromUtf8("horizontalLayout_33"))

		self.label_answer_type = QtGui.QLabel(self.Tab1)
		self.label_answer_type.setObjectName(_fromUtf8("label_answer_type"))
		self.horizontalLayout_33.addWidget(self.label_answer_type)
		selector_answer_type = QtGui.QComboBox(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(selector_answer_type.sizePolicy().hasHeightForWidth())
		
		selector_answer_type.setSizePolicy(sizePolicy)
		selector_answer_type.setObjectName(_fromUtf8("selector_answer_type"))
		selector_answer_type.addItem("Directa")
		selector_answer_type.addItem("Inversa")
		self.horizontalLayout_33.addWidget(selector_answer_type)
		self.verticalLayout_2.addLayout(self.horizontalLayout_33)

		self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
		
		# PID coefficients
		self.Variables_GrBx = QtGui.QGroupBox(self.Tab1)
		self.Variables_GrBx.setObjectName(_fromUtf8("Variables_GrBx"))
		self.gridLayout_2 = QtGui.QGridLayout(self.Variables_GrBx)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.label_P = QtGui.QLabel(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_P.sizePolicy().hasHeightForWidth())
		self.label_P.setSizePolicy(sizePolicy)
		self.label_P.setObjectName(_fromUtf8("label_P"))
		self.gridLayout_2.addWidget(self.label_P, 0, 0, 1, 1)
		
		P_value = QtGui.QLineEdit(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(P_value.sizePolicy().hasHeightForWidth())
		P_value.setSizePolicy(sizePolicy)
		P_value.setObjectName(_fromUtf8("P_value"))
		Validation_text_field.NumValidator(P_value)
		self.gridLayout_2.addWidget(P_value, 0, 1, 1, 1)

		self.label_I = QtGui.QLabel(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_I.sizePolicy().hasHeightForWidth())
		self.label_I.setSizePolicy(sizePolicy)
		self.label_I.setObjectName(_fromUtf8("label_I"))
		self.gridLayout_2.addWidget(self.label_I, 1, 0, 1, 1)
		
		I_value = QtGui.QLineEdit(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(I_value.sizePolicy().hasHeightForWidth())
		I_value.setSizePolicy(sizePolicy)
		I_value.setObjectName(_fromUtf8("I_value"))
		Validation_text_field.NumValidator(I_value)
		self.gridLayout_2.addWidget(I_value, 1, 1, 1, 1)

		self.label_D = QtGui.QLabel(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_D.sizePolicy().hasHeightForWidth())
		self.label_D.setSizePolicy(sizePolicy)
		self.label_D.setObjectName(_fromUtf8("label_D"))
		self.gridLayout_2.addWidget(self.label_D, 2, 0, 1, 1)
		
		D_value = QtGui.QLineEdit(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(D_value.sizePolicy().hasHeightForWidth())
		D_value.setSizePolicy(sizePolicy)
		D_value.setObjectName(_fromUtf8("D_value"))
		Validation_text_field.NumValidator(D_value)
		self.gridLayout_2.addWidget(D_value, 2, 1, 1, 1)

		self.gridLayout.addWidget(self.Variables_GrBx, 1, 0, 1, 1)

		#Set point
		self.Set_point_GrBx = QtGui.QGroupBox(self.Tab1)
		self.Set_point_GrBx.setObjectName(_fromUtf8("Set_point_GrBx"))
		self.horizontalLayout_4 = QtGui.QHBoxLayout(self.Set_point_GrBx)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.label_SP = QtGui.QLabel(self.Set_point_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_SP.sizePolicy().hasHeightForWidth())
		self.label_SP.setSizePolicy(sizePolicy)
		self.label_SP.setObjectName(_fromUtf8("label_SP"))
		self.horizontalLayout_4.addWidget(self.label_SP)
		
		SP_value = QtGui.QLineEdit(self.Set_point_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(SP_value.sizePolicy().hasHeightForWidth())
		SP_value.setSizePolicy(sizePolicy)
		SP_value.setObjectName(_fromUtf8("SP_value"))
		self.horizontalLayout_4.addWidget(SP_value)
		Validation_text_field.NumValidator(SP_value)
		self.gridLayout.addWidget(self.Set_point_GrBx, 2, 0, 1, 1)

	##-- Info panel --##
		self.groupBox_labels = QtGui.QGroupBox(self.Tab1)
		self.groupBox_labels.setTitle(_fromUtf8(""))
		self.groupBox_labels.setObjectName(_fromUtf8("groupBox_labels"))
		verticalLayout_info_labels = QtGui.QVBoxLayout(self.groupBox_labels)
		verticalLayout_info_labels.setObjectName(_fromUtf8("verticalLayout_info_labels"))
		info_SP = QtGui.QLabel(self.groupBox_labels)
		info_SP.setObjectName(_fromUtf8("info_SP"))
		verticalLayout_info_labels.addWidget(info_SP)
		info_Mv = QtGui.QLabel(self.groupBox_labels)
		info_Mv.setObjectName(_fromUtf8("info_Mv"))
		verticalLayout_info_labels.addWidget(info_Mv)
		info_Pv = QtGui.QLabel(self.groupBox_labels)
		info_Pv.setObjectName(_fromUtf8("info_Pv"))
		verticalLayout_info_labels.addWidget(info_Pv)	
		self.gridLayout.addWidget(self.groupBox_labels, 2, 1, 1, 1)

		self.Layout_tab1.addLayout(self.gridLayout)

	##--Instance button--##
		self.Ok_button = QtGui.QPushButton(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Ok_button.sizePolicy().hasHeightForWidth())
		self.Ok_button.setSizePolicy(sizePolicy)
		self.Ok_button.setObjectName(_fromUtf8("Ok_button"))
		self.gridLayout.addWidget(self.Ok_button, 4, 1, 1, 1)
		self.Ok_button.clicked.connect(self.confirm_param)
		self.verticalLayout_5 = QtGui.QVBoxLayout()
		self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
	
	##--Normalized parameters--##
		
		#Check box
		CheckBox_normalize = QtGui.QCheckBox(self.Tab1)
		CheckBox_normalize.setObjectName(_fromUtf8("checkBox_normalize"))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CheckBox_normalize.sizePolicy().hasHeightForWidth())
		CheckBox_normalize.setSizePolicy(sizePolicy)
		CheckBox_normalize.stateChanged.connect(self.normalize_parameters)
		
		#Mv range
		self.verticalLayout_5.addWidget(CheckBox_normalize)
		label_Mv_range = QtGui.QLabel(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(label_Mv_range.sizePolicy().hasHeightForWidth())
		label_Mv_range.setSizePolicy(sizePolicy)
		label_Mv_range.setObjectName(_fromUtf8("label_Mv_range"))
		label_Mv_range.setVisible(False)
		self.verticalLayout_5.addWidget(label_Mv_range)

		self.Layout_Mv_range = QtGui.QHBoxLayout()
		self.Layout_Mv_range.setObjectName(_fromUtf8("Layout_Mv_range"))
		
		label_Mv_min = QtGui.QLabel(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(label_Mv_min.sizePolicy().hasHeightForWidth())
		label_Mv_min.setSizePolicy(sizePolicy)
		label_Mv_min.setObjectName(_fromUtf8("label_Mv_min"))
		label_Mv_min.setVisible(False)
		self.Layout_Mv_range.addWidget(label_Mv_min)

		Mv_min_value = QtGui.QLineEdit(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Mv_min_value.sizePolicy().hasHeightForWidth())
		Mv_min_value.setSizePolicy(sizePolicy)
		Mv_min_value.setObjectName(_fromUtf8("Mv_min_value"))
		Mv_min_value.setVisible(False)
		self.Layout_Mv_range.addWidget(Mv_min_value)

		label_Mv_max = QtGui.QLabel(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(label_Mv_max.sizePolicy().hasHeightForWidth())
		label_Mv_max.setSizePolicy(sizePolicy)
		label_Mv_max.setObjectName(_fromUtf8("label_Mv_max"))
		label_Mv_max.setVisible(False)
		self.Layout_Mv_range.addWidget(label_Mv_max)

		Mv_max_value = QtGui.QLineEdit(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Mv_max_value.sizePolicy().hasHeightForWidth())
		Mv_max_value.setSizePolicy(sizePolicy)
		Mv_max_value.setObjectName(_fromUtf8("Mv_max_value"))
		Mv_max_value.setVisible(False)
		self.Layout_Mv_range.addWidget(Mv_max_value)

		self.verticalLayout_5.addLayout(self.Layout_Mv_range)
		self.gridLayout.addLayout(self.verticalLayout_5, 0, 1, 1, 1)
		
	##--Signal control--##
		self.horizontalLayout_5 = QtGui.QHBoxLayout()
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
	
		self.label_signal_control = QtGui.QLabel(self.Tab2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_signal_control.sizePolicy().hasHeightForWidth())
		self.label_signal_control.setSizePolicy(sizePolicy)
		self.label_signal_control.setObjectName(_fromUtf8("self.label_signal_control"))
		self.horizontalLayout_5.addWidget(self.label_signal_control)

		signal_control_selector = QtGui.QComboBox(self.Tab2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(signal_control_selector.sizePolicy().hasHeightForWidth())
		signal_control_selector.setSizePolicy(sizePolicy)
		signal_control_selector.setObjectName(_fromUtf8("signal_control_selector"))
		signal_control_selector.addItem("Automatico")
		signal_control_selector.addItem("Manual")
		signal_control_selector.activated.connect(self.selection_Type_control)
		self.horizontalLayout_5.addWidget(signal_control_selector)
		self.Layout_tab2.addLayout(self.horizontalLayout_5)

		self.horizontalLayout_6 = QtGui.QHBoxLayout()
		self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))

	##--Variable Mv or Sp--##
		label_Spinbox = QtGui.QLabel(self.Tab2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth( label_Spinbox.sizePolicy().hasHeightForWidth())
		label_Spinbox.setSizePolicy(sizePolicy)
		label_Spinbox.setObjectName(_fromUtf8("label_Spinbox"))
		self.horizontalLayout_6.addWidget(label_Spinbox)

		SpinBox_signal_control = QtGui.QDoubleSpinBox(self.Tab2)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(SpinBox_signal_control.sizePolicy().hasHeightForWidth())
		SpinBox_signal_control.setSizePolicy(sizePolicy)
		SpinBox_signal_control.setObjectName(_fromUtf8("SpinBox_signal_control"))
		self.horizontalLayout_6.addWidget(SpinBox_signal_control)
		self.Layout_tab2.addLayout(self.horizontalLayout_6)

		verticalLayoutWidget = QtGui.QWidget()
		verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 410, 260))
		verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

	#--Dynamic Graph--##
		Graph = DynamicGraphic(Dialog,Ts,Enable_cursor,False,False,self.Tab2, width=4, height=3, dpi=85)
		Graph.axes.set_xlabel('Time (s)',fontsize=11)
		Graph.axes.set_ylabel(_translate("Dialog", "Mv", None),fontsize=11)
		Graph.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		Graph.set_legends()
		self.Timer_graph()

		self.Layout_tab2.addLayout(Graph.dynamic_graph)

		self.horizontalLayout_3.addWidget(self.tabWidget)
		self.retranslateUi(Dialog)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)	

		update_window()

	# Timer initialization
	def Timer_graph(self):
		# global timer
		timer = QtCore.QTimer(Dialog_window)
		timer.timeout.connect(update_figure)
		timer.start(Ts*100)
		
	# Evaluate change in control type
	def selection_Type_control(self):
		Signal_control_selection=signal_control_selector.currentText()
		if Signal_control_selection=="Automatico":
			label_Spinbox.setText("Setpoint:")

		elif Signal_control_selection=="Manual":
			label_Spinbox.setText("Variable manipulada:")
	
	# Visible or not visible fields and labels for normalization parameters
	def normalize_parameters(self):
		if CheckBox_normalize.isChecked():
			label_Mv_range.setVisible(True)
			label_Mv_min.setVisible(True)
			Mv_min_value.setVisible(True)
			label_Mv_max.setVisible(True)
			Mv_max_value.setVisible(True)
		else:
			label_Mv_range.setVisible(False)
			label_Mv_min.setVisible(False)
			Mv_min_value.setVisible(False)
			label_Mv_max.setVisible(False)
			Mv_max_value.setVisible(False)

	# Evaluate change in manipulated variable type
	def selection_MvType(self):
		global Mv_selection
		Mv_selection=Mv_selector.currentText()
		
	## Labels set text
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Datos "+title_name, None))
		self.label_Mv.setText(_translate("Dialog", "Variable a controlar:", None))
		self.label_answer_type.setText(_translate("Dialog", "Tipo de respuesta:  ", None))
		self.Variables_GrBx.setTitle(_translate("Dialog", "PID", None))
		self.label_P.setText(_translate("Dialog", "Constante proporcional", None))
		self.label_I.setText(_translate("Dialog", "Constante  integral", None))
		self.label_D.setText(_translate("Dialog", "Constante  diferencial", None))
		self.Set_point_GrBx.setTitle(_translate("Dialog", "Ajuste", None))
		self.label_SP.setText(_translate("Dialog", "Setpoint", None))
		info_Mv.setText(_translate("Dialog", "MV:", None))
		info_Pv.setText(_translate("Dialog", "PV:", None))
		info_SP.setText(_translate("Dialog", "SP:", None))
		label_Mv_range.setText(_translate("Dialog", "Rango de control: ", None))
		label_Mv_min.setText(_translate("Dialog", "min:", None))
		label_Mv_max.setText(_translate("Dialog", "max:", None))
		self.label_signal_control.setText(_translate("Dialog", "Tipo de control:", None))
		label_Spinbox.setText(_translate("Dialog", "Setpoint:", None))
		self.Ok_button.setText(_translate("Dialog", "Aceptar", None))
		CheckBox_normalize.setText(_translate("Dialog", "Parametros\n"
		"normalizados", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("Dialog", "Entradas", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), _translate("Dialog", "Gráfico", None))

