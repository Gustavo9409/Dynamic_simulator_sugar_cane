# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tank_properties.ui'
#
# Created: Tue Jun 06 13:53:54 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!
import re

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Dynamic_diagrams import DynamicGraphic
from matplotlib.ticker import FormatStrFormatter

global Enable_cursor
Enable_cursor=False

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


##Function for update window when closing
def Update_window():
	global num_window
	global tank_data
	global update
	global Enable_cursor

	num_window=re.sub('([a-zA-Z]+)', "", nameDialog)
	input_tank = open('Blocks_data.txt', 'r+')
	data=input_tank.readlines()
	input_tank.close()
	tank_data=[]
	if len(data)>0:
		for i in data:
			info=(i.strip()).split("\t")
			if len(info)>1:
				flag=info[0]
				#print ("Flag "+flag)
				
				if flag==("Tk"+str(num_window)):
					update=1
					for k in range(1,len(info)):
						tank_data.append(float(info[k]))	
					Volumen.setText(str(tank_data[0]))
					Cross_Sectional_Area.setText(str(tank_data[1]))
					Initial_Level.setText(str(tank_data[2]))

	else:
		update=0
		print "no datos"

	infile = open('time_exec.txt', 'r+')
	data=infile.readlines()
	if len(data)>1:
		for values in data:
			info=(values.strip()).split("\t")
			if values!="stop":
				Enable_cursor=True
			else:
				Enable_cursor=False
	infile.close()

def replace(path, pattern, subst):
	flags=0
	with open(path, "r+" ) as filex:
		fileContents = filex.read()
		textPattern = re.compile( re.escape( pattern ), flags )
		fileContents = textPattern.sub( subst, fileContents )
		filex.seek( 0 )
		filex.truncate()
		filex.write(fileContents) 

##Function for update Blocks_data.txt for new parameters confirmation 
def update_data_txt(data):
	flg=0
	dats=""
	input_tank = open('Blocks_data.txt', 'r+')
	file_data=input_tank.readlines()
	input_tank.close()
	for i in file_data:
		info=(i.strip()).split("\t")
		if info[0]==data:
			flg=1
			dats=(i.strip())
	return flg, dats	
	

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
		V=Volumen.text()
		A=Cross_Sectional_Area.text()
		Ltk_init=Initial_Level.text()

		flag=re.sub('([a-zA-Z]+)', "", nameDialog)

		upd, chang=update_data_txt("Tk"+flag)
		if upd==0:
			outfile = open('Blocks_data.txt', 'a')
			outfile.write("\n"+"Tk"+flag+"\t"+V+"\t"+A+"\t"+Ltk_init)
			outfile.close()
		else:
			replace("Blocks_data.txt",chang,"Tk"+flag+"\t"+V+"\t"+A+"\t"+Ltk_init)
		print "OK PARAMETERS"
		self.close()
		Resultado=QtGui.QDialog()
		QtGui.QMessageBox.information(Resultado, 
		'Ok',
		_translate("Dialog","Instanciación correcta de datos.",None),QtGui.QMessageBox.Ok)
		Dialog_window.close()
	def NO(self):
		self.close()


class Ui_Dialog(object):
	def confirm_param(self):
		global confirm
		global Resultado
		global pd

		confirm=((len(Volumen.text())>0)and(len(Cross_Sectional_Area.text())>0)and(len(Initial_Level.text())>0))

		if confirm==True:
			print "AJAM"
			Resultado=QtGui.QDialog()
			pd = window_confirm_param(Resultado.window())
			pd.exec_()
		else:
			self.Resultado=QtGui.QDialog()
			QtGui.QMessageBox.warning(self.Resultado, 
			'Advertencia',
			"Falta por ingresar algun dato.",QtGui.QMessageBox.Ok)

	def setupUi(self,name,ts,fluid_in,Dialog):
		
		global nameDialog
		global Ts
		global Dialog_window
		global Objct_fluid_in

		global Volumen
		global Cross_Sectional_Area
		global Initial_Level

		Validation_text_field = Validator()

		nameDialog=name
		Ts=ts
		Dialog_window=Dialog
		Objct_fluid_in=fluid_in


		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(604, 350)

		self.gridLayout_Dialog = QtGui.QGridLayout(Dialog)
		self.gridLayout_Dialog.setObjectName(_fromUtf8("gridLayout"))
		
	##---Tab Widget---###
		self.Tank_tabWidget = QtGui.QTabWidget(Dialog)
		self.Tank_tabWidget.setObjectName(_fromUtf8("Tank_tabWidget"))
		
		self.Tank_tab_1 = QtGui.QWidget()
		self.Tank_tab_1.setObjectName(_fromUtf8("Tank_tab_1"))
		self.layout_tab_1 = QtGui.QGridLayout(self.Tank_tab_1)
		self.layout_tab_1.setObjectName(_fromUtf8("gridLayout_2"))

		self.Tank_tab_2 = QtGui.QWidget()
		self.Tank_tab_2.setObjectName(_fromUtf8("Tank_tab_2"))
		self.layout_tab_2 = QtGui.QGridLayout(self.Tank_tab_2)
		self.layout_tab_2.setObjectName(_fromUtf8("gridLayout_3"))

		self.Tank_tab_3 = QtGui.QWidget()
		self.Tank_tab_3.setObjectName(_fromUtf8("Tank_tab_3"))
		self.layout_tab_3 = QtGui.QVBoxLayout(self.Tank_tab_3)
		self.layout_tab_3.setObjectName(_fromUtf8("verticalLayout"))

	##--Instance button--##
		self.OKButton_Tank = QtGui.QPushButton(self.Tank_tab_1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OKButton_Tank.sizePolicy().hasHeightForWidth())
		self.OKButton_Tank.setSizePolicy(sizePolicy)
		self.OKButton_Tank.setObjectName(_fromUtf8("OKButton_Tank"))
		self.OKButton_Tank.clicked.connect(self.confirm_param)

	##----Instantiation of elements for physical properties----##
		self.Physical_properties_GrBx = QtGui.QGroupBox(self.Tank_tab_1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Physical_properties_GrBx.sizePolicy().hasHeightForWidth())
		self.Physical_properties_GrBx.setSizePolicy(sizePolicy)
		self.Physical_properties_GrBx.setObjectName(_fromUtf8("Physical_properties_GrBx"))
		self.gridLayout_Dialog_Physical_properties = QtGui.QGridLayout(self.Physical_properties_GrBx)
		self.gridLayout_Dialog_Physical_properties.setObjectName(_fromUtf8("gridLayout_4"))
		self.label_Volumen = QtGui.QLabel(self.Physical_properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Volumen.sizePolicy().hasHeightForWidth())
		self.label_Volumen.setSizePolicy(sizePolicy)
		self.label_Volumen.setObjectName(_fromUtf8("label_Volumen"))
		self.gridLayout_Dialog_Physical_properties.addWidget(self.label_Volumen, 0, 0, 1, 1)
		Volumen = QtGui.QLineEdit(self.Physical_properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Volumen.sizePolicy().hasHeightForWidth())
		Volumen.setSizePolicy(sizePolicy)
		Volumen.setObjectName(_fromUtf8("Volumen"))
		Validation_text_field.NumValidator(Volumen)

		self.gridLayout_Dialog_Physical_properties.addWidget(Volumen, 0, 1, 1, 1)
		self.label_Cross_Sectional_Area = QtGui.QLabel(self.Physical_properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Cross_Sectional_Area.sizePolicy().hasHeightForWidth())
		self.label_Cross_Sectional_Area.setSizePolicy(sizePolicy)
		self.label_Cross_Sectional_Area.setObjectName(_fromUtf8("label_Cross_Sectional_Area"))
		self.gridLayout_Dialog_Physical_properties.addWidget(self.label_Cross_Sectional_Area, 1, 0, 1, 1)
		Cross_Sectional_Area = QtGui.QLineEdit(self.Physical_properties_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Cross_Sectional_Area.sizePolicy().hasHeightForWidth())
		Cross_Sectional_Area.setSizePolicy(sizePolicy)
		Cross_Sectional_Area.setObjectName(_fromUtf8("Cross_Sectional_Area"))
		Validation_text_field.NumValidator(Cross_Sectional_Area)

		self.gridLayout_Dialog_Physical_properties.addWidget(Cross_Sectional_Area, 1, 1, 1, 1)
		self.layout_tab_1.addWidget(self.Physical_properties_GrBx, 0, 0, 1, 1)

	##----Instantiation of elements for the initial condition----##	
		self.Initial_conditions_GrBx = QtGui.QGroupBox(self.Tank_tab_1)
		self.Initial_conditions_GrBx.setObjectName(_fromUtf8("Initial_conditions_GrBx"))
		self.gridLayout_Dialog_Initial_conditions = QtGui.QGridLayout(self.Initial_conditions_GrBx)
		self.gridLayout_Dialog_Initial_conditions.setObjectName(_fromUtf8("gridLayout_5"))
		self.label_Initial_Level = QtGui.QLabel(self.Initial_conditions_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_Initial_Level.sizePolicy().hasHeightForWidth())
		self.label_Initial_Level.setSizePolicy(sizePolicy)
		self.label_Initial_Level.setObjectName(_fromUtf8("label_Initial_Level"))
		self.gridLayout_Dialog_Initial_conditions.addWidget(self.label_Initial_Level, 0, 0, 1, 1)
		Initial_Level = QtGui.QLineEdit(self.Initial_conditions_GrBx)
		Initial_Level.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Initial_Level.sizePolicy().hasHeightForWidth())
		Initial_Level.setSizePolicy(sizePolicy)
		Initial_Level.setReadOnly(False)
		Initial_Level.setObjectName(_fromUtf8("Initial_Level"))
		Validation_text_field.NumValidator(Initial_Level)

		self.gridLayout_Dialog_Initial_conditions.addWidget(Initial_Level, 0, 1, 1, 1)
		self.layout_tab_1.addWidget(self.Initial_conditions_GrBx, 0, 1, 1, 1)
		

		self.layout_tab_1.addWidget(self.OKButton_Tank, 1, 1, 1, 1)
		self.Tank_tabWidget.addTab(self.Tank_tab_1, _fromUtf8(""))
		
		
	##----Instantiation of elements for input fluid----##	
		self.Input_fluid_GrBx = QtGui.QGroupBox(self.Tank_tab_2)
		self.Input_fluid_GrBx.setObjectName(_fromUtf8("Input_fluid_GrBx"))
		self.gridLayout_Dialog_Input_fluid = QtGui.QGridLayout(self.Input_fluid_GrBx)
		self.gridLayout_Dialog_Input_fluid.setObjectName(_fromUtf8("gridLayout_6"))
		self.label_InFluid_Flow = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Flow.setSizePolicy(sizePolicy)
		self.label_InFluid_Flow.setObjectName(_fromUtf8("label_InFluid_Flow"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.label_InFluid_Flow, 0, 0, 1, 1)
		self.InFluid_Flow = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.InFluid_Flow.sizePolicy().hasHeightForWidth())
		self.InFluid_Flow.setSizePolicy(sizePolicy)
		self.InFluid_Flow.setReadOnly(True)
		self.InFluid_Flow.setObjectName(_fromUtf8("InFluid_Flow"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.InFluid_Flow, 0, 1, 1, 1)
		self.label_InFluid_Temp = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Temp.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Temp.setSizePolicy(sizePolicy)
		self.label_InFluid_Temp.setObjectName(_fromUtf8("label_InFluid_Temp"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.label_InFluid_Temp, 1, 0, 1, 1)
		self.InFluid_Temp = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.InFluid_Temp.sizePolicy().hasHeightForWidth())
		self.InFluid_Temp.setSizePolicy(sizePolicy)
		self.InFluid_Temp.setReadOnly(True)
		self.InFluid_Temp.setObjectName(_fromUtf8("InFluid_Temp"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.InFluid_Temp, 1, 1, 1, 1)
		self.label_InFluid_Brix = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Brix.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Brix.setSizePolicy(sizePolicy)
		self.label_InFluid_Brix.setObjectName(_fromUtf8("label_InFluid_Brix"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.label_InFluid_Brix, 2, 0, 1, 1)
		self.InFluid_Brix = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.InFluid_Brix.sizePolicy().hasHeightForWidth())
		self.InFluid_Brix.setSizePolicy(sizePolicy)
		self.InFluid_Brix.setReadOnly(True)
		self.InFluid_Brix.setObjectName(_fromUtf8("InFluid_Brix"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.InFluid_Brix, 2, 1, 1, 1)
		self.label_InFluid_InsolubleSolids = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.label_InFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		self.label_InFluid_InsolubleSolids.setObjectName(_fromUtf8("label_InFluid_InsolubleSolids"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.label_InFluid_InsolubleSolids, 3, 0, 1, 1)
		self.InFluid_InsolubleSolids_2 = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.InFluid_InsolubleSolids_2.sizePolicy().hasHeightForWidth())
		self.InFluid_InsolubleSolids_2.setSizePolicy(sizePolicy)
		self.InFluid_InsolubleSolids_2.setReadOnly(True)
		self.InFluid_InsolubleSolids_2.setObjectName(_fromUtf8("InFluid_InsolubleSolids_2"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.InFluid_InsolubleSolids_2, 3, 1, 1, 1)
		self.label_InFluid_Purity = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_Purity.sizePolicy().hasHeightForWidth())
		self.label_InFluid_Purity.setSizePolicy(sizePolicy)
		self.label_InFluid_Purity.setObjectName(_fromUtf8("label_InFluid_Purity"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.label_InFluid_Purity, 4, 0, 1, 1)
		self.InFluid_Purity = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.InFluid_Purity.sizePolicy().hasHeightForWidth())
		self.InFluid_Purity.setSizePolicy(sizePolicy)
		self.InFluid_Purity.setReadOnly(True)
		self.InFluid_Purity.setObjectName(_fromUtf8("InFluid_Purity"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.InFluid_Purity, 4, 1, 1, 1)
		self.label_InFluid_pH = QtGui.QLabel(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_InFluid_pH.sizePolicy().hasHeightForWidth())
		self.label_InFluid_pH.setSizePolicy(sizePolicy)
		self.label_InFluid_pH.setObjectName(_fromUtf8("label_InFluid_pH"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.label_InFluid_pH, 5, 0, 1, 1)
		self.InFluid_pH = QtGui.QLineEdit(self.Input_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.InFluid_pH.sizePolicy().hasHeightForWidth())
		self.InFluid_pH.setSizePolicy(sizePolicy)
		self.InFluid_pH.setReadOnly(True)
		self.InFluid_pH.setObjectName(_fromUtf8("InFluid_pH"))
		self.gridLayout_Dialog_Input_fluid.addWidget(self.InFluid_pH, 5, 1, 1, 1)
		self.layout_tab_2.addWidget(self.Input_fluid_GrBx, 0, 0, 1, 1)

	##----Instantiation of elements for output fluid----##
		self.Output_fluid_GrBx = QtGui.QGroupBox(self.Tank_tab_2)
		self.Output_fluid_GrBx.setObjectName(_fromUtf8("Output_fluid_GrBx"))
		self.gridLayout_Dialog_Output_fluid = QtGui.QGridLayout(self.Output_fluid_GrBx)
		self.gridLayout_Dialog_Output_fluid.setObjectName(_fromUtf8("gridLayout_7"))
		self.label_OutFluid_Flow = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Flow.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Flow.setSizePolicy(sizePolicy)
		self.label_OutFluid_Flow.setObjectName(_fromUtf8("label_OutFluid_Flow"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.label_OutFluid_Flow, 0, 0, 1, 1)
		self.OutFluid_Flow = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OutFluid_Flow.sizePolicy().hasHeightForWidth())
		self.OutFluid_Flow.setSizePolicy(sizePolicy)
		self.OutFluid_Flow.setReadOnly(True)
		self.OutFluid_Flow.setObjectName(_fromUtf8("OutFluid_Flow"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.OutFluid_Flow, 0, 1, 1, 1)
		self.label_OutFluid_Temp = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Temp.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Temp.setSizePolicy(sizePolicy)
		self.label_OutFluid_Temp.setObjectName(_fromUtf8("label_OutFluid_Temp"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.label_OutFluid_Temp, 1, 0, 1, 1)
		self.OutFluid_Temp = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OutFluid_Temp.sizePolicy().hasHeightForWidth())
		self.OutFluid_Temp.setSizePolicy(sizePolicy)
		self.OutFluid_Temp.setReadOnly(True)
		self.OutFluid_Temp.setObjectName(_fromUtf8("OutFluid_Temp"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.OutFluid_Temp, 1, 1, 1, 1)
		self.label_OutFluid_Brix = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Brix.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Brix.setSizePolicy(sizePolicy)
		self.label_OutFluid_Brix.setObjectName(_fromUtf8("label_OutFluid_Brix"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.label_OutFluid_Brix, 2, 0, 1, 1)
		self.OutFluid_Brix = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OutFluid_Brix.sizePolicy().hasHeightForWidth())
		self.OutFluid_Brix.setSizePolicy(sizePolicy)
		self.OutFluid_Brix.setReadOnly(True)
		self.OutFluid_Brix.setObjectName(_fromUtf8("OutFluid_Brix"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.OutFluid_Brix, 2, 1, 1, 1)
		self.label_OutFluid_InsolubleSolids = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		self.label_OutFluid_InsolubleSolids.setObjectName(_fromUtf8("label_OutFluid_InsolubleSolids"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.label_OutFluid_InsolubleSolids, 3, 0, 1, 1)
		self.OutFluid_InsolubleSolids = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OutFluid_InsolubleSolids.sizePolicy().hasHeightForWidth())
		self.OutFluid_InsolubleSolids.setSizePolicy(sizePolicy)
		self.OutFluid_InsolubleSolids.setReadOnly(True)
		self.OutFluid_InsolubleSolids.setObjectName(_fromUtf8("OutFluid_InsolubleSolids"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.OutFluid_InsolubleSolids, 3, 1, 1, 1)
		self.label_OutFluid_Purity = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_Purity.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_Purity.setSizePolicy(sizePolicy)
		self.label_OutFluid_Purity.setObjectName(_fromUtf8("label_OutFluid_Purity"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.label_OutFluid_Purity, 4, 0, 1, 1)
		self.OutFluid_Purity = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OutFluid_Purity.sizePolicy().hasHeightForWidth())
		self.OutFluid_Purity.setSizePolicy(sizePolicy)
		self.OutFluid_Purity.setReadOnly(True)
		self.OutFluid_Purity.setObjectName(_fromUtf8("OutFluid_Purity"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.OutFluid_Purity, 4, 1, 1, 1)
		self.label_OutFluid_pH = QtGui.QLabel(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_OutFluid_pH.sizePolicy().hasHeightForWidth())
		self.label_OutFluid_pH.setSizePolicy(sizePolicy)
		self.label_OutFluid_pH.setObjectName(_fromUtf8("label_OutFluid_pH"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.label_OutFluid_pH, 5, 0, 1, 1)
		self.OutFluid_pH = QtGui.QLineEdit(self.Output_fluid_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.OutFluid_pH.sizePolicy().hasHeightForWidth())
		self.OutFluid_pH.setSizePolicy(sizePolicy)
		self.OutFluid_pH.setReadOnly(True)
		self.OutFluid_pH.setObjectName(_fromUtf8("OutFluid_pH"))
		self.gridLayout_Dialog_Output_fluid.addWidget(self.OutFluid_pH, 5, 1, 1, 1)
		self.layout_tab_2.addWidget(self.Output_fluid_GrBx, 0, 1, 1, 1)
		self.Tank_tabWidget.addTab(self.Tank_tab_2, _fromUtf8(""))
		
	##----Instantiation of elements for variable output---#
		self.label_output_level = QtGui.QLabel(self.Tank_tab_3)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_output_level.sizePolicy().hasHeightForWidth())
		self.label_output_level.setSizePolicy(sizePolicy)
		self.label_output_level.setObjectName(_fromUtf8("label"))
		self.layout_tab_3.addWidget(self.label_output_level)

		verticalLayoutWidget = QtGui.QWidget()
		verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 410, 260))
		verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

		#Addition of grafics in window

		Graph = DynamicGraphic(Dialog,Ts,Enable_cursor,False,False,self.Tank_tab_3, width=4, height=3, dpi=85)
		Graph.axes.set_xlabel('Time (min)',fontsize=11)
		Graph.axes.set_ylabel(_translate("Dialog", "Nivel [m/m]", None),fontsize=11)
		Graph.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		Graph.set_legends()
		verticalLayoutWidget.setLayout(Graph.dynamic_graph)
		# self.Timer_graph()

		self.layout_tab_3.addWidget(verticalLayoutWidget)

		self.Tank_tabWidget.addTab(self.Tank_tab_3, _fromUtf8(""))
		self.gridLayout_Dialog.addWidget(self.Tank_tabWidget, 0, 0, 1, 1)

		self.retranslateUi(Dialog)
		self.Tank_tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		Update_window()

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.Physical_properties_GrBx.setTitle(_translate("Dialog", "Propiedades físicas", None))
		self.label_Volumen.setText(_translate("Dialog", "Volumen [m3]", None))
		self.label_Cross_Sectional_Area.setText(_translate("Dialog", "Área transversal [m2]", None))
		self.Initial_conditions_GrBx.setTitle(_translate("Dialog", "Condiciones iniciales", None))
		self.label_Initial_Level.setText(_translate("Dialog", "Nivel del tanque [%]", None))
		self.OKButton_Tank.setText(_translate("Dialog", "Aceptar", None))
		self.Tank_tabWidget.setTabText(self.Tank_tabWidget.indexOf(self.Tank_tab_1), _translate("Dialog", "Propiedades físicas", None))
		self.Input_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de entrada", None))
		self.label_InFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_InFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_InFluid_Brix.setText(_translate("Dialog", "Brix [kg/kg]", None))
		self.label_InFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [kg/kg]", None))
		self.label_InFluid_Purity.setText(_translate("Dialog", "Pureza [kg/kg]", None))
		self.label_InFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.Output_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de salida", None))
		self.label_OutFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
		self.label_OutFluid_Temp.setText(_translate("Dialog", "Temperatura [°C]", None))
		self.label_OutFluid_Brix.setText(_translate("Dialog", "Brix [kg/kg]", None))
		self.label_OutFluid_InsolubleSolids.setText(_translate("Dialog", "Sólidos insolubles [kg/kg]", None))
		self.label_OutFluid_Purity.setText(_translate("Dialog", "Pureza [kg/kg]", None))
		self.label_OutFluid_pH.setText(_translate("Dialog", "pH ", None))
		self.Tank_tabWidget.setTabText(self.Tank_tabWidget.indexOf(self.Tank_tab_2), _translate("Dialog", "Variables de proceso", None))
		self.label_output_level.setText(_translate("Dialog", "Nivel en tanque:", None))
		self.Tank_tabWidget.setTabText(self.Tank_tabWidget.indexOf(self.Tank_tab_3), _translate("Dialog", "Gráfica", None))

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QWidget()
	ui = Ui_Dialog()
	ui.setupUi("Tanque",0.5,"Fv1",Dialog)
	Dialog.show()
	sys.exit(app.exec_())
