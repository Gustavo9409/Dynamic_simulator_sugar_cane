# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Heater_properties.ui'
#
# Created: Thu Apr 27 15:14:40 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

# from PyQt4 import QtCore, QtGui
#from Run_heater_model import Simulation
from matplotlib.backends import qt_compat
# use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
# if use_pyside:
# 	from PySide import QtGui, QtCore
# else:
# 	from PyQt4 import QtGui, QtCore
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from numpy import arange, sin, pi
from decimal import Decimal
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
from physicochemical_properties import liquor_properties
from heat_transfer import htc_shell_tube

import random
import threading
import re
import math

global time_1
global outout_1
global ts
global time_exec
global model_value
global Heater_type
global liquor
global Ht
global SnT
Heater_type="Carcaza y tubos"
time_exec=[]
model_value=[]
ts=0.0
time_1=0.0
outout_1=0.0
SnT=1.0

liquor=liquor_properties()
Ht=htc_shell_tube()

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

class Validator(object):
	def NumValidator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,100000,2,LineEdit))

class calculated_properties():

	def Juice_velocity(self,Fj,Tj,Bj,Zj):
		pjin=liquor.density(Tj,Bj,Zj)
		Np=float(Pipe_x_Step.text())
		Disp=float(Ext_Pipe_Diameter.text())-(2*(float(Pipe_Thickness.text())/25.4));

		vj=(4*((Fj*pjin)))/(Np*pjin*math.pi*((0.0254*Disp)**2));
		return vj
	def Heat_area(self):
		Dosp=float(Ext_Pipe_Diameter.text())
		Np=float(Pipe_x_Step.text())
		Lp=float(Lenght_Pipe.text())
		Nst=float(N_steps.text())

		Ac=0.0254*math.pi*Dosp*Np*Lp*Nst;
		return Ac
	def Scalling_r(self,Fj,Tj,Bj,Zj):
		vj=self.Juice_velocity(Fj,Tj,Bj,Zj)
		Hrop=float(Time_Op.text())
		B=float(Scalling_Coeff.text())

		Ri=((3.5*10**-6)*(Hrop**B))*(1+(10.73/(vj**3)))
		return Ri

global heat_properties
heat_properties=calculated_properties()

def Update_data():
	input_heat = open('Blocks_data.txt', 'r+')
	data=input_heat.readlines()
	vapor_data=[]
	juice_data=[]
	for i in data:
		info=(i.strip()).split("\t")
		if len(info)>1:
			flag=info[0]
			#print ("Flag "+flag+" "+flag[:2])
			if flag[:2]=="Fv":
				for k in range(1,len(info)):
					vapor_data.append(float(info[k]))
			elif flag[:2]=="Fj":
				for k in range(1,len(info)):
					juice_data.append(float(info[k]))
	input_heat.close()
	
	## Calculated heater properties
	Dosp=float(Ext_Pipe_Diameter.text())
	Disp=float(Ext_Pipe_Diameter.text())-(2*(float(Pipe_Thickness.text())/25.4))
	Np=float(Pipe_x_Step.text())
	Ep=float(Pipe_Rough.text())
	Lp=float(Lenght_Pipe.text())
	Nst=float(N_steps.text())
	Hrop=float(Time_Op.text())
	B=float(Scalling_Coeff.text())
	Aosc=heat_properties.Heat_area()
	Aisc=0.0254*math.pi*Disp*Np*Lp*Nst
	Tjc=(float(juice_data[3])+round(float(split_model_data_n1[1]),3))/2.0;
	Fj=(float(juice_data[0])/3.6)/float(juice_data[8])

	a=round(heat_properties.Juice_velocity(Fj,float(juice_data[3]),float(juice_data[1]),float(juice_data[2])),3)
	Juice_Velocity.setText(str(a))
	b=round(heat_properties.Heat_area(),3)
	Heat_Area.setText(str(b))
	f="{:.3E}".format(Decimal(heat_properties.Scalling_r(Fj,float(juice_data[3]),float(juice_data[1]),float(juice_data[2]))))
	Scalling_Resist.setText(str(f))
	c="{:.3E}".format(Decimal(Ht.overall_u(Fj,float(juice_data[1]),float(juice_data[2]),float(juice_data[3]),
		Tjc,float(vapor_data[3]),float(vapor_data[0]),Np,Aisc,Aosc,Disp,Dosp,Ep,Hrop,B)))
	Overall_U.setText(str(c))
	d="{:.3E}".format(Decimal(Ht.internal_u(Disp,Dosp,Np,Ep,Fj,float(juice_data[3]),float(juice_data[1]),float(juice_data[2]))))
	Inside_U.setText(str(d))
	e="{:.3E}".format(Decimal(Ht.external_u(Dosp,Tjc,float(vapor_data[3]),float(vapor_data[0]))))
	Outside_U.setText(str(e))


	##Process values 
	#Vapor
		#input
	InStm_Press.setText(str(round(vapor_data[0],1)))
	InStm_Flow.setText(str(vapor_data[1]))
	InStm_Temp.setText(str(round(vapor_data[3],2)))
		#output
	CondStm_Flow.setText(str(vapor_data[1]))
	CondStm_Temp.setText(str(round(vapor_data[3],2)))
	CondStm_Press.setText(str(round(vapor_data[0],1)))
	#Juice
		#input
	InFluid_Temp.setText(str(juice_data[3]))
	InFluid_Flow.setText(str(juice_data[0]))
	InFluid_pH.setText(str(juice_data[5]))
	InFluid_pressure.setText(str(round(juice_data[6],1)))
	InFluid_InsolubleSolids.setText(str(juice_data[4]))
	InFluid_Purity.setText(str(juice_data[2]))
	InFluid_Brix.setText(str(juice_data[1]))
		#output
	OutFluid_Temp.setText(str(round(float(split_model_data_n1[1]),3)))
	OutFluid_Brix.setText(str(juice_data[1]))
	OutFluid_Flow.setText(str(juice_data[0]))
	OutFluid_pH.setText(str(juice_data[5]))
	#OutFluid_pressure.setText(round(,1))
	OutFluid_InsolubleSolids.setText(str(juice_data[4]))
	OutFluid_Purity.setText(str(juice_data[2]))


def Update_window():
	global num_window
	global heater_data
	global update

	num_window=re.sub('([a-zA-Z]+)', "", nameDialog)
	input_heat = open('Blocks_data.txt', 'r+')
	data=input_heat.readlines()
	heater_data=[]
	if len(data)>0:
		for i in data:
			info=(i.strip()).split("\t")
			if len(info)>1:
				flag=info[0]
				#print ("Flag "+flag)
				if flag==("Ht"+str(num_window)):
					update=1
					for k in range(1,len(info)):
						heater_data.append(float(info[k]))
					if heater_data[9]==1.0: ##Shell and tubes
						Pipe_x_Step.setText(str(heater_data[0]))
						N_steps.setText(str(heater_data[1]))
						Lenght_Pipe.setText(str(heater_data[2]))
						Pipe_Thickness.setText(str(heater_data[3]))
						Ext_Pipe_Diameter.setText(str(heater_data[4]))
						Pipe_Rough.setText(str(heater_data[5]))
						Scalling_Coeff.setText(str(heater_data[6]))
						Time_Op.setText(str(heater_data[7]))
						Initial_Out_Temp.setText(str(heater_data[8]))
						##
						Selector_Heater_type.setCurrentIndex(1)
					else:	##Plates
						Selector_Heater_type.setCurrentIndex(2)
	else:
		update=0
		print "no datos"
	input_heat.close()

class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=4, height=4, dpi=100):
		fig = Figure(figsize=[width, height], tight_layout = {'pad': 0}, dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		#FigureCanvas.updateGeometry(self)

	def compute_initial_figure(self):
		pass


class MyDynamicMplCanvas(MyMplCanvas):
	"""A canvas that updates itself every second with a new plot."""
	def __init__(self, *args, **kwargs):
		MyMplCanvas.__init__(self, *args, **kwargs)
		self.axes.set_xlabel('Time (min)',fontsize=11)
		self.axes.set_ylabel(_translate("Dialog", "Tjout [°C]", None),fontsize=11)
		#self.axes.yaxis.set_label_coords(0.0, 1.03)
		#self.axes.xaxis.set_label_coords(1.03, 0.0)
		timer = QtCore.QTimer(self)
		timer.timeout.connect(self.update_figure)
		timer.start(Ts*1000)

	def compute_initial_figure(self):
		pass
		#self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

	def update_figure(self):
		global time_exec
		global model_value
		global split_model_data_n1
		# Build a list of 4 random integers between 0 and 10 (both inclusive)
		infile = open('time_exec.txt', 'r+')
		data=infile.readlines()
		if len(data)>1:
			if data[-1]!="stop" and data[-2]!="stop":
				model_data_n0=data[-2].strip()
				model_data_n1=data[-1].strip()

				split_model_data_n0=model_data_n0.split("\t")
				split_model_data_n1=model_data_n1.split("\t")

				time_exec.append(float(split_model_data_n0[0]))
				model_value.append(round(float(split_model_data_n0[1]),3))

				time_exec.append(float(split_model_data_n1[0]))
				model_value.append(round(float(split_model_data_n1[1]),3))
				
				plot_time=time_exec[len(time_exec)-2:len(time_exec)]
				plot_model=model_value[len(model_value)-2:len(model_value)]

				#print(str(plot_time)+" -*- "+str(plot_model))

				infile.close()
				l = [random.randint(0, 10) for i in range(4)]
				#self.axes.cla()
				#self.axes.plot([0, 1, 2, 3], l, 'r')
				self.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
				self.axes.plot(plot_time,plot_model,'b-')
				Temp_Output_variable.setText(str(round(float(split_model_data_n1[1]),3)))
				self.draw()
				Update_data()

			else :
				time_exec=[]
				model_value=[]
				self.axes.cla()
				for values in data:
					if values!="stop":
						values.strip()
						split_model_data=values.split("\t")
						time_exec.append(float(split_model_data[0]))
						model_value.append(round(float(split_model_data[1]),3))
				self.axes.set_xlabel('Time (min)',fontsize=11)
				self.axes.set_ylabel(_translate("Dialog", "Tjout [°C]", None),fontsize=11)
				self.axes.plot(time_exec,model_value,'b-')
				Update_data()
		# else:
		# 	print "No hay datos para leer"

		

	# Time_exec =threading.Thread(target = Thread_time, args=(time_1,outout_1))
	# #Time_exec.setDaemon(True)
	# Time_exec.start()

	
	# Time_exec =threading.Thread(target = Thread_time)
	# #Time_exec.setDaemon(True)
	# Time_exec.start()
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
			# timer = QtCore.QTimer(Dialog)
			# timer.timeout.connect(self.read_data)
			# timer.start(0.5*1000)
			Np=Pipe_x_Step.text()
			Nst=N_steps.text()
			Lp=Lenght_Pipe.text()
			dp=Pipe_Thickness.text()
			Dosp=Ext_Pipe_Diameter.text()
			Ep=Pipe_Rough.text()
			B=Scalling_Coeff.text()
			Hrop=Time_Op.text()
			Tjout_ini=Initial_Out_Temp.text()



			flag=re.sub('([a-zA-Z]+)', "", nameDialog)
			outfile = open('Blocks_data.txt', 'a')
			outfile.write("\n"+"Ht"+flag+"\t"+Np+"\t"+Nst+"\t"+Lp+"\t"+dp+"\t"+Dosp+"\t"+Ep+"\t"+B+"\t"+Hrop+"\t"+Tjout_ini+"\t"+str(SnT))
			outfile.close()
			print "OK PARAMETERS"
			self.close()
		def NO(self):
			self.close()

class Ui_Dialog(object):
	
	def confirm_param(self):
		global confirm
		global Resultado
		global pd

		confirm=((len(Pipe_x_Step.text())>0)and(len(N_steps.text())>0)and(len(Lenght_Pipe.text())>0)and(len(Pipe_Thickness.text())>0)
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

	def setupUi(self,name,ts,Dialog):
		##Heater properties
		global Pipe_x_Step
		global N_steps
		global Lenght_Pipe
		global Pipe_Thickness
		global Ext_Pipe_Diameter
		global Pipe_Rough
		global Scalling_Coeff
		global Time_Op
		global Initial_Out_Temp
		global nameDialog
		global Ts
		global Temp_Output_variable
		global Selector_Heater_type

		global Scalling_Resist
		global Juice_Velocity
		global Inside_U
		global Outside_U
		global Overall_U
		global Heat_Area

		##Process values
		global InFluid_Temp
		global InFluid_Flow
		global InFluid_pH
		global InFluid_pressure
		global InFluid_InsolubleSolids
		global InFluid_Purity
		global InFluid_Brix

		global OutFluid_Temp
		global OutFluid_Brix
		global OutFluid_Flow
		global OutFluid_pH
		global OutFluid_pressure
		global OutFluid_InsolubleSolids
		global OutFluid_Purity

		global InStm_Press
		global InStm_Flow
		global InStm_Temp

		global CondStm_Flow
		global CondStm_Temp
		global CondStm_Press

		nameDialog=name
		Ts=ts
		Vali = Validator()
		#print(dat)
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(432, 355)
		self.tabWidget_Heater = QtGui.QTabWidget(Dialog)
		self.tabWidget_Heater.setGeometry(QtCore.QRect(0, 30, 431, 360))
		self.tabWidget_Heater.setObjectName(_fromUtf8("tabWidget_Heater"))
		self.Heat_tab1 = QtGui.QWidget()
		self.Heat_tab1.setObjectName(_fromUtf8("Heat_tab1"))
		self.Initial_conditions_GrBx = QtGui.QGroupBox(self.Heat_tab1)
		self.Initial_conditions_GrBx.setGeometry(QtCore.QRect(213, 191, 201, 61))
		self.Initial_conditions_GrBx.setObjectName(_fromUtf8("Initial_conditions_GrBx"))
		Initial_Out_Temp = QtGui.QLineEdit(self.Initial_conditions_GrBx)
		Initial_Out_Temp.setGeometry(QtCore.QRect(138, 27, 41, 20))
		Initial_Out_Temp.setReadOnly(False)
		Initial_Out_Temp.setObjectName(_fromUtf8("Initial_Out_Temp"))
		Initial_Out_Temp.setText("78.0")
		Vali.NumValidator(Initial_Out_Temp)

		self.label_Initial_Out_Temp = QtGui.QLabel(self.Initial_conditions_GrBx)
		self.label_Initial_Out_Temp.setGeometry(QtCore.QRect(7, 21, 131, 31))
		self.label_Initial_Out_Temp.setObjectName(_fromUtf8("label_Initial_Out_Temp"))
		self.ComBox_Type_Material = QtGui.QComboBox(self.Heat_tab1)
		self.ComBox_Type_Material.setGeometry(QtCore.QRect(102, 228, 91, 22))
		self.ComBox_Type_Material.setObjectName(_fromUtf8("ComBox_Type_Material"))
		self.ComBox_Type_Material.addItem("Inoxidable")
		self.ComBox_Type_Material.addItem("Aluminio")

		self.label_Type_Material = QtGui.QLabel(self.Heat_tab1)
		self.label_Type_Material.setGeometry(QtCore.QRect(14, 230, 81, 16))
		self.label_Type_Material.setObjectName(_fromUtf8("label_Type_Material"))
		self.OKButton_Heat = QtGui.QPushButton(self.Heat_tab1)
		self.OKButton_Heat.setGeometry(QtCore.QRect(280, 258, 131, 23))
		self.OKButton_Heat.setObjectName(_fromUtf8("OKButton_Heat"))
		self.OKButton_Heat.clicked.connect(self.confirm_param)



		self.Calculated_properties_GrBx = QtGui.QGroupBox(self.Heat_tab1)
		self.Calculated_properties_GrBx.setGeometry(QtCore.QRect(213, 6, 205, 181))
		self.Calculated_properties_GrBx.setObjectName(_fromUtf8("Calculated_properties_GrBx"))
		self.label_Juice_Velocity = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Juice_Velocity.setGeometry(QtCore.QRect(10, 21, 131, 16))
		self.label_Juice_Velocity.setObjectName(_fromUtf8("label_Juice_Velocity"))
		self.label_Scalling_Resist = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Scalling_Resist.setGeometry(QtCore.QRect(10, 43, 151, 31))
		self.label_Scalling_Resist.setObjectName(_fromUtf8("label_Scalling_Resist"))
		self.label_Outside_U = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Outside_U.setGeometry(QtCore.QRect(10, 108, 121, 16))
		self.label_Outside_U.setObjectName(_fromUtf8("label_Outside_U"))
		self.label_Inside_U = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Inside_U.setGeometry(QtCore.QRect(11, 130, 121, 16))
		self.label_Inside_U.setObjectName(_fromUtf8("label_Inside_U"))
		self.label_Overall_U = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Overall_U.setGeometry(QtCore.QRect(11, 153, 121, 16))
		self.label_Overall_U.setObjectName(_fromUtf8("label_Overall_U"))
		self.label_Heat_Area = QtGui.QLabel(self.Calculated_properties_GrBx)
		self.label_Heat_Area.setGeometry(QtCore.QRect(10, 76, 121, 31))
		self.label_Heat_Area.setObjectName(_fromUtf8("label_Heat_Area"))

		Scalling_Resist = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Scalling_Resist.setGeometry(QtCore.QRect(145, 53, 55, 20))
		Scalling_Resist.setReadOnly(True)
		Scalling_Resist.setObjectName(_fromUtf8("Scalling_Resist"))

		Juice_Velocity = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Juice_Velocity.setGeometry(QtCore.QRect(145, 20, 55, 20))
		Juice_Velocity.setReadOnly(True)
		Juice_Velocity.setObjectName(_fromUtf8("Juice_Velocity"))

		Inside_U = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Inside_U.setGeometry(QtCore.QRect(145, 130, 55, 20))
		Inside_U.setReadOnly(True)
		Inside_U.setObjectName(_fromUtf8("Inside_U"))

		Outside_U = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Outside_U.setGeometry(QtCore.QRect(145, 107, 55, 20))
		Outside_U.setReadOnly(True)
		Outside_U.setObjectName(_fromUtf8("Outside_U"))

		Overall_U = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Overall_U.setGeometry(QtCore.QRect(145, 153, 55, 20))
		Overall_U.setReadOnly(True)
		Overall_U.setObjectName(_fromUtf8("Overall_U"))

		Heat_Area = QtGui.QLineEdit(self.Calculated_properties_GrBx)
		Heat_Area.setGeometry(QtCore.QRect(145, 79, 55, 20))
		Heat_Area.setReadOnly(True)
		Heat_Area.setObjectName(_fromUtf8("Heat_Area"))

		self.Physical_properties_GrBx = QtGui.QGroupBox(self.Heat_tab1)
		self.Physical_properties_GrBx.setGeometry(QtCore.QRect(10, 6, 191, 201))
		self.Physical_properties_GrBx.setObjectName(_fromUtf8("Physical_properties_GrBx"))
		self.label_Ext_Pipe_Diameter = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Ext_Pipe_Diameter.setGeometry(QtCore.QRect(7, 20, 131, 16))
		self.label_Ext_Pipe_Diameter.setObjectName(_fromUtf8("label_Ext_Pipe_Diameter"))
		self.label_Lenght_Pipe = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Lenght_Pipe.setGeometry(QtCore.QRect(7, 41, 121, 16))
		self.label_Lenght_Pipe.setObjectName(_fromUtf8("label_Lenght_Pipe"))
		self.label_Pipe_x_Step = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Pipe_x_Step.setGeometry(QtCore.QRect(7, 108, 121, 16))
		self.label_Pipe_x_Step.setObjectName(_fromUtf8("label_Pipe_x_Step"))
		self.label_N_steps = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_N_steps.setGeometry(QtCore.QRect(7, 130, 121, 16))
		self.label_N_steps.setObjectName(_fromUtf8("label_N_steps"))
		self.label_Time_Op = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Time_Op.setGeometry(QtCore.QRect(7, 151, 121, 16))
		self.label_Time_Op.setObjectName(_fromUtf8("label_Time_Op"))
		self.label_Pipe_Rough = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Pipe_Rough.setGeometry(QtCore.QRect(7, 85, 121, 16))
		self.label_Pipe_Rough.setObjectName(_fromUtf8("label_Pipe_Rough"))
		self.label_Scalling_Coeff = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Scalling_Coeff.setGeometry(QtCore.QRect(7, 166, 141, 31))
		self.label_Scalling_Coeff.setOpenExternalLinks(False)
		self.label_Scalling_Coeff.setObjectName(_fromUtf8("label_Scalling_Coeff"))
		self.label_Pipe_Thickness = QtGui.QLabel(self.Physical_properties_GrBx)
		self.label_Pipe_Thickness.setGeometry(QtCore.QRect(7, 64, 121, 16))
		self.label_Pipe_Thickness.setObjectName(_fromUtf8("label_Pipe_Thickness"))
		Ext_Pipe_Diameter = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Ext_Pipe_Diameter.setGeometry(QtCore.QRect(143, 18, 41, 20))
		Ext_Pipe_Diameter.setObjectName(_fromUtf8("Ext_Pipe_Diameter"))
		Ext_Pipe_Diameter.setText("2.0")
		Vali.NumValidator(Ext_Pipe_Diameter)


		Lenght_Pipe = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Lenght_Pipe.setGeometry(QtCore.QRect(143, 40, 41, 20))
		Lenght_Pipe.setObjectName(_fromUtf8("Lenght_Pipe"))
		Lenght_Pipe.setText("6.57")
		Vali.NumValidator(Lenght_Pipe)

		Pipe_Thickness = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Pipe_Thickness.setGeometry(QtCore.QRect(143, 62, 41, 20))
		Pipe_Thickness.setObjectName(_fromUtf8("Pipe_Thickness"))
		Pipe_Thickness.setText("1.2")
		Vali.NumValidator(Pipe_Thickness)

		Pipe_Rough = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Pipe_Rough.setGeometry(QtCore.QRect(143, 84, 41, 20))
		Pipe_Rough.setObjectName(_fromUtf8("Pipe_Rough"))
		Pipe_Rough.setText("0.090")
		Vali.NumValidator(Pipe_Rough)

		Time_Op = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Time_Op.setGeometry(QtCore.QRect(143, 150, 41, 20))
		Time_Op.setObjectName(_fromUtf8("Time_Op"))
		Time_Op.setText("100.0")
		Vali.NumValidator(Time_Op)

		N_steps = QtGui.QLineEdit(self.Physical_properties_GrBx)
		N_steps.setGeometry(QtCore.QRect(143, 128, 41, 20))
		N_steps.setObjectName(_fromUtf8("N_steps"))
		N_steps.setText("2.0")
		Vali.NumValidator(N_steps)

		Pipe_x_Step = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Pipe_x_Step.setGeometry(QtCore.QRect(143, 106, 41, 20))
		Pipe_x_Step.setObjectName(_fromUtf8("self.Pipe_x_Step"))
		Pipe_x_Step.setText("6.0")
		Vali.NumValidator(Pipe_x_Step)

		Scalling_Coeff = QtGui.QLineEdit(self.Physical_properties_GrBx)
		Scalling_Coeff.setGeometry(QtCore.QRect(143, 172, 41, 20))
		Scalling_Coeff.setObjectName(_fromUtf8("Scalling_Coeff"))
		Scalling_Coeff.setText("0.8")
		Vali.NumValidator(Scalling_Coeff)

		self.tabWidget_Heater.addTab(self.Heat_tab1, _fromUtf8(""))
		self.Heat_tab_2 = QtGui.QWidget()
		self.Heat_tab_2.setObjectName(_fromUtf8("Heat_tab_2"))
		self.Output_fluid_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Output_fluid_GrBx.setGeometry(QtCore.QRect(225, 10, 196, 176))
		self.Output_fluid_GrBx.setObjectName(_fromUtf8("Output_fluid_GrBx"))
		self.label_OutFluid_Flow = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Flow.setGeometry(QtCore.QRect(10, 21, 131, 16))
		self.label_OutFluid_Flow.setObjectName(_fromUtf8("label_OutFluid_Flow"))
		self.label_OutFluid_Temp = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Temp.setGeometry(QtCore.QRect(10, 43, 121, 16))
		self.label_OutFluid_Temp.setObjectName(_fromUtf8("label_OutFluid_Temp"))
		self.label_OutFluid_Brix = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Brix.setGeometry(QtCore.QRect(10, 66, 121, 16))
		self.label_OutFluid_Brix.setObjectName(_fromUtf8("label_OutFluid_Brix"))
		self.label_OutFluid_Purity = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_Purity.setGeometry(QtCore.QRect(10, 109, 121, 16))
		self.label_OutFluid_Purity.setObjectName(_fromUtf8("label_OutFluid_Purity"))
		self.label_OutFluid_pressure = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_pressure.setGeometry(QtCore.QRect(10, 131, 121, 16))
		self.label_OutFluid_pressure.setObjectName(_fromUtf8("label_OutFluid_pressure"))
		self.label_OutFluid_InsolubleSolids = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_InsolubleSolids.setGeometry(QtCore.QRect(10, 87, 121, 16))
		self.label_OutFluid_InsolubleSolids.setObjectName(_fromUtf8("label_OutFluid_InsolubleSolids"))
		self.label_OutFluid_pH = QtGui.QLabel(self.Output_fluid_GrBx)
		self.label_OutFluid_pH.setGeometry(QtCore.QRect(10, 153, 121, 16))
		self.label_OutFluid_pH.setObjectName(_fromUtf8("label_OutFluid_pH"))
	

		OutFluid_Temp = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Temp.setGeometry(QtCore.QRect(139, 42, 52, 20))
		OutFluid_Temp.setReadOnly(True)
		OutFluid_Temp.setObjectName(_fromUtf8("OutFluid_Temp"))

		OutFluid_Flow = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Flow.setGeometry(QtCore.QRect(139, 20, 52, 20))
		OutFluid_Flow.setReadOnly(True)
		OutFluid_Flow.setObjectName(_fromUtf8("OutFluid_Flow"))

		OutFluid_Brix = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Brix.setGeometry(QtCore.QRect(139, 64, 52, 20))
		OutFluid_Brix.setReadOnly(True)
		OutFluid_Brix.setObjectName(_fromUtf8("OutFluid_Brix"))

		OutFluid_pH = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_pH.setGeometry(QtCore.QRect(139, 151, 52, 20))
		OutFluid_pH.setReadOnly(True)
		OutFluid_pH.setObjectName(_fromUtf8("OutFluid_pH"))

		OutFluid_pressure = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_pressure.setGeometry(QtCore.QRect(139, 129, 52, 20))
		OutFluid_pressure.setReadOnly(True)
		OutFluid_pressure.setObjectName(_fromUtf8("OutFluid_pressure"))

		OutFluid_InsolubleSolids = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_InsolubleSolids.setGeometry(QtCore.QRect(139, 85, 52, 20))
		OutFluid_InsolubleSolids.setReadOnly(True)
		OutFluid_InsolubleSolids.setObjectName(_fromUtf8("OutFluid_InsolubleSolids"))

		OutFluid_Purity = QtGui.QLineEdit(self.Output_fluid_GrBx)
		OutFluid_Purity.setGeometry(QtCore.QRect(139, 107, 52, 20))
		OutFluid_Purity.setReadOnly(True)
		OutFluid_Purity.setObjectName(_fromUtf8("OutFluid_Purity"))

		self.Input_fluid_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Input_fluid_GrBx.setGeometry(QtCore.QRect(12, 10, 196, 176))
		self.Input_fluid_GrBx.setObjectName(_fromUtf8("Input_fluid_GrBx"))
		self.label_InFluid_Flow = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Flow.setGeometry(QtCore.QRect(10, 21, 131, 16))
		self.label_InFluid_Flow.setObjectName(_fromUtf8("label_InFluid_Flow"))
		self.label_InFluid_Temp = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Temp.setGeometry(QtCore.QRect(10, 43, 121, 16))
		self.label_InFluid_Temp.setObjectName(_fromUtf8("label_InFluid_Temp"))
		self.label_InFluid_Brix = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Brix.setGeometry(QtCore.QRect(10, 66, 121, 16))
		self.label_InFluid_Brix.setObjectName(_fromUtf8("label_InFluid_Brix"))
		self.label_InFluid_Purity = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_Purity.setGeometry(QtCore.QRect(10, 110, 121, 16))
		self.label_InFluid_Purity.setObjectName(_fromUtf8("label_InFluid_Purity"))
		self.label_InFluid_InsolubleSolids = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_InsolubleSolids.setGeometry(QtCore.QRect(10, 88, 121, 16))
		self.label_InFluid_InsolubleSolids.setObjectName(_fromUtf8("label_InFluid_InsolubleSolids"))
		self.label_InFluid_pH = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_pH.setGeometry(QtCore.QRect(10, 153, 121, 16))
		self.label_InFluid_pH.setObjectName(_fromUtf8("label_InFluid_pH"))
		self.label_InFluid_pressure = QtGui.QLabel(self.Input_fluid_GrBx)
		self.label_InFluid_pressure.setGeometry(QtCore.QRect(10, 132, 121, 16))
		self.label_InFluid_pressure.setObjectName(_fromUtf8("label_InFluid_pressure"))

		InFluid_Temp = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Temp.setGeometry(QtCore.QRect(139, 42, 52, 20))
		InFluid_Temp.setReadOnly(True)
		InFluid_Temp.setObjectName(_fromUtf8("InFluid_Temp"))

		InFluid_Flow = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Flow.setGeometry(QtCore.QRect(139, 20, 52, 20))
		InFluid_Flow.setReadOnly(True)
		InFluid_Flow.setObjectName(_fromUtf8("InFluid_Flow"))

		InFluid_pH = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_pH.setGeometry(QtCore.QRect(139, 152, 52, 20))
		InFluid_pH.setReadOnly(True)
		InFluid_pH.setObjectName(_fromUtf8("InFluid_pH"))

		InFluid_pressure = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_pressure.setGeometry(QtCore.QRect(139, 130, 52, 20))
		InFluid_pressure.setReadOnly(True)
		InFluid_pressure.setObjectName(_fromUtf8("InFluid_pressure"))

		InFluid_InsolubleSolids = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_InsolubleSolids.setGeometry(QtCore.QRect(139, 86, 52, 20))
		InFluid_InsolubleSolids.setReadOnly(True)
		InFluid_InsolubleSolids.setObjectName(_fromUtf8("InFluid_InsolubleSolids_2"))			

		InFluid_Purity = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Purity.setGeometry(QtCore.QRect(139, 108, 52, 20))
		InFluid_Purity.setReadOnly(True)
		InFluid_Purity.setObjectName(_fromUtf8("InFluid_Purity"))

		InFluid_Brix = QtGui.QLineEdit(self.Input_fluid_GrBx)
		InFluid_Brix.setGeometry(QtCore.QRect(139, 64, 52, 20))
		InFluid_Brix.setReadOnly(True)
		InFluid_Brix.setObjectName(_fromUtf8("InFluid_Brix"))


		self.Input_Steam_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Input_Steam_GrBx.setGeometry(QtCore.QRect(12, 198, 196, 81))
		self.Input_Steam_GrBx.setObjectName(_fromUtf8("Input_Steam_GrBx"))
		self.label_InStm_Flow = QtGui.QLabel(self.Input_Steam_GrBx)
		self.label_InStm_Flow.setGeometry(QtCore.QRect(10, 18, 131, 16))
		self.label_InStm_Flow.setObjectName(_fromUtf8("label_InStm_Flow"))
		self.label_InStm_Press = QtGui.QLabel(self.Input_Steam_GrBx)
		self.label_InStm_Press.setGeometry(QtCore.QRect(10, 38, 121, 16))
		self.label_InStm_Press.setObjectName(_fromUtf8("label_InStm_Press"))
		self.label_InStm_Temp = QtGui.QLabel(self.Input_Steam_GrBx)
		self.label_InStm_Temp.setGeometry(QtCore.QRect(10, 60, 131, 16))
		self.label_InStm_Temp.setObjectName(_fromUtf8("label_InStm_Temp"))

		InStm_Press = QtGui.QLineEdit(self.Input_Steam_GrBx)
		InStm_Press.setGeometry(QtCore.QRect(139, 36, 52, 20))
		InStm_Press.setReadOnly(True)
		InStm_Press.setObjectName(_fromUtf8("InStm_Press"))

		InStm_Flow = QtGui.QLineEdit(self.Input_Steam_GrBx)
		InStm_Flow.setGeometry(QtCore.QRect(139, 14, 52, 20))
		InStm_Flow.setReadOnly(True)
		InStm_Flow.setObjectName(_fromUtf8("InStm_Flow"))

		InStm_Temp = QtGui.QLineEdit(self.Input_Steam_GrBx)
		InStm_Temp.setGeometry(QtCore.QRect(139, 58, 52, 20))
		InStm_Temp.setReadOnly(True)
		InStm_Temp.setObjectName(_fromUtf8("InStm_Temp"))

		self.Condensed_steam_GrBx = QtGui.QGroupBox(self.Heat_tab_2)
		self.Condensed_steam_GrBx.setGeometry(QtCore.QRect(225, 198, 196, 81))
		self.Condensed_steam_GrBx.setObjectName(_fromUtf8("Condensed_steam_GrBx"))


		self.label_CondStm_Flow = QtGui.QLabel(self.Condensed_steam_GrBx)
		self.label_CondStm_Flow.setGeometry(QtCore.QRect(16, 18, 121, 16))
		self.label_CondStm_Flow.setObjectName(_fromUtf8("label_CondStm_Flow"))
		self.label_CondStm_Press = QtGui.QLabel(self.Condensed_steam_GrBx)
		self.label_CondStm_Press.setGeometry(QtCore.QRect(16, 40, 131, 16))
		self.label_CondStm_Press.setObjectName(_fromUtf8("label_CondStm_Press"))
		
		self.label_CondStm_Temp = QtGui.QLabel(self.Condensed_steam_GrBx)
		self.label_CondStm_Temp.setGeometry(QtCore.QRect(16, 61, 121, 16))
		self.label_CondStm_Temp.setObjectName(_fromUtf8("label_CondStm_Temp"))

		CondStm_Flow = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		CondStm_Flow.setGeometry(QtCore.QRect(139, 16, 52, 20))
		CondStm_Flow.setReadOnly(True)
		CondStm_Flow.setObjectName(_fromUtf8("CondStm_Flow"))

		CondStm_Temp = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		CondStm_Temp.setGeometry(QtCore.QRect(139, 60, 52, 20))
		CondStm_Temp.setReadOnly(True)
		CondStm_Temp.setObjectName(_fromUtf8("CondStm_Temp"))

		CondStm_Press = QtGui.QLineEdit(self.Condensed_steam_GrBx)
		CondStm_Press.setGeometry(QtCore.QRect(139, 38, 52, 20))
		CondStm_Press.setReadOnly(True)
		CondStm_Press.setObjectName(_fromUtf8("CondStm_Press"))

		self.tabWidget_Heater.addTab(self.Heat_tab_2, _fromUtf8(""))
		self.Heat_tab_3 = QtGui.QWidget()
		self.Heat_tab_3.setObjectName(_fromUtf8("Heat_tab_3"))
		self.label = QtGui.QLabel(self.Heat_tab_3)
		self.label.setGeometry(QtCore.QRect(10, 10, 161, 16))
		self.label.setObjectName(_fromUtf8("label"))
		Temp_Output_variable = QtGui.QLineEdit(self.Heat_tab_3)
		Temp_Output_variable.setGeometry(QtCore.QRect(180, 10, 51, 20))
		Temp_Output_variable.setReadOnly(True)

		self.verticalLayoutWidget = QtGui.QWidget(self.Heat_tab_3)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 410, 260))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setGeometry(QtCore.QRect(15, 0, 400, 300))
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

		dc = MyDynamicMplCanvas(Dialog, width=4, height=3, dpi=85)
		self.verticalLayout.addWidget(dc)


		self.tabWidget_Heater.addTab(self.Heat_tab_3, _fromUtf8(""))
		Selector_Heater_type = QtGui.QComboBox(Dialog)
		Selector_Heater_type.setGeometry(QtCore.QRect(7, 6, 411, 22))
		Selector_Heater_type.setObjectName(_fromUtf8("Selector_Heater_type"))
		Selector_Heater_type.addItem("--Tipo de calentador--")
		Selector_Heater_type.addItem("Carcaza y tubos")
		Selector_Heater_type.addItem("Placas")
		Selector_Heater_type.activated.connect(self.selection_HeaterType)
		Selector_Heater_type.setCurrentIndex(1)

		self.retranslateUi(Dialog)
		self.tabWidget_Heater.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		Update_window()

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


	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Parametros "+nameDialog, None))
		self.Initial_conditions_GrBx.setTitle(_translate("Dialog", "Condiciones iniciales", None))
		self.label_Initial_Out_Temp.setText(_translate("Dialog", "Temperatura del jugo \n"
"de salida [°C]", None))
		self.label_Type_Material.setText(_translate("Dialog", "Tipo de material", None))
		self.OKButton_Heat.setText(_translate("Dialog", "Aceptar", None))
		self.Calculated_properties_GrBx.setTitle(_translate("Dialog", "Propiedades físicas calculadas", None))
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
		self.label_Lenght_Pipe.setText(_translate("Dialog", "Longitud tubo [m]", None))
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
		self.label_OutFluid_Brix.setText(_translate("Dialog", "Brix [kg/kg]", None))
		self.label_OutFluid_Purity.setText(_translate("Dialog", "Pureza [kg/kg]", None))
		self.label_OutFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [kg/kg]", None))
		self.label_OutFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.label_OutFluid_pressure.setText(_translate("Dialog", "Presión[Pa] ", None))
		self.label_InFluid_pressure.setText(_translate("Dialog", "Presión[Pa] ", None))

		self.Input_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de entrada", None))
		self.label_InFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_InFluid_Brix.setText(_translate("Dialog", "Brix [kg/kg]", None))
		self.label_InFluid_Purity.setText(_translate("Dialog", "Pureza [kg/kg]", None))
		self.label_InFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [kg/kg]", None))
		self.label_InFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.Input_Steam_GrBx.setTitle(_translate("Dialog", "Vapor de entrada", None))
		self.label_InStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InStm_Press.setText(_translate("Dialog", "Presión [Pa]", None))
		self.label_InStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.Condensed_steam_GrBx.setTitle(_translate("Dialog", "Vapor condensado ", None))
		self.label_CondStm_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_CondStm_Press.setText(_translate("Dialog", "Presión [Pa]", None))
		self.label_CondStm_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.tabWidget_Heater.setTabText(self.tabWidget_Heater.indexOf(self.Heat_tab_2), _translate("Dialog", "Variables de proceso", None))
		self.label.setText(_translate("Dialog", "Temperatura de jugo de salida:", None))
		self.tabWidget_Heater.setTabText(self.tabWidget_Heater.indexOf(self.Heat_tab_3), _translate("Dialog", "Gráfica", None))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QWidget()
	ui = Ui_Dialog()
	ui.setupUi("Calentador",Dialog)
	Dialog.show()
	sys.exit(app.exec_())
