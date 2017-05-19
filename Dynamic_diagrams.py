# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.backends.backend_qt4agg_DynamicSim import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT )##as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import matplotlib.backends.backend_qt5_DynamicSim as backend

global time_exec
global model_value
model_value=[]
time_exec=[]


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

class NavigationToolbar(NavigationToolbar2QT):
	def __init__(self, canvas_, parent_):
		#backend.figureoptions = None  # Monkey patched to kill the figure options button on matplotlib toolbar
		##Images: C:\Python27\Lib\site-packages\matplotlib\mpl-data\images
		##Functions: C:\Python27\Lib\site-packages\matplotlib\backends\backend_qt5.py
		self.toolitems = (
			('Home', 'Regresar a la vista inicial', 'Home2', 'Home_edit'),
			('Back', 'Regresar a la vista anterior', 'Row2L', 'back'),
			('Forward', 'Dirigirse a la siguiente vista', 'Row2R', 'forward'),
			(None, None, None, None),
			('Pan', _translate("Dialog", "Mover la gráfica (Click izquierdo) / Zoom (Click derecho)", None), 'move', 'pan'),
			('Edit axis',_translate("Dialog",'Modificación de ejes', None), 'qt4_editor_options','Edit_axis'),
			(None, None, None, None),
			(None, None, None, None),)
		NavigationToolbar2QT.__init__(self, canvas_, parent_)


class DynamicGraphic(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self,Widget,parent=None, width=4, height=4, dpi=100):
		
		fig = Figure(figsize=[width, height], tight_layout = {'pad': 0}, dpi=dpi)
		self.axes = fig.add_subplot(111)

		# self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
		
		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		self.mpl_toolbar = NavigationToolbar(self,Widget)

		self.dynamic_graph = QtGui.QVBoxLayout(Widget)
		self.dynamic_graph.setObjectName(_fromUtf8("verticalLayout"))
		self.dynamic_graph.addWidget(self,3)
		self.dynamic_graph.addWidget(self.mpl_toolbar,1)

		#self.mpl_connect('key_press_event', self.on_key_press)
		#FigureCanvas.updateGeometry(self)

# class DynamicGraphic(MyMplCanvas):
# 	"""A canvas that updates itself every second with a new plot."""
# 	def __init__(self,Sim_time,model_data_txt,data_label,Temp_Output_variable,Wid,*args, **kwargs):
# 		global g_Wid
# 		global g_data_label
# 		global g_model_data_txt
# 		g_Wid=Wid
# 		g_model_data_txt=model_data_txt
# 		g_data_label=data_label
# 		self.Temp_Output_variable=Temp_Output_variable
# 		#MyMplCanvas.__init__(self,self.Wid,*args, **kwargs)
# 		#self.axes.yaxis.set_label_coords(0.0, 1.03)
# 		#self.axes.xaxis.set_label_coords(1.03, 0.0)
# 		timer = QtCore.QTimer(Wid)
# 		timer.timeout.connect(update_figure)
# 		timer.start(Sim_time*1000)


# 	def compute_initial_figure(self):
# 		pass
# 		#self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')


		# else:
		# 	print "No hay datos para leer"


# class Dynamic_graph(object):
# 	def graph(self,Widget,Sim_time,mdt,dl):
# 		global model_data_txt
# 		global data_label
# 		global time

# 		model_data_txt=mdt
# 		data_label=dl
# 		time=Sim_time

# 		self.generalayout = QtGui.QGridLayout(Widget)
# 		self.generalayout.setSpacing(0)
# 		self.generalayout.setContentsMargins(0,0,0,0)

# 		self.LayoutWidget=  QtGui.QWidget(Widget)
# 		self.LayoutWidget.setGeometry(QtCore.QRect(0, 30, 1002, 26))

# 		verticalLayout = QtGui.QVBoxLayout(self.LayoutWidget)
# 		verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
# 		dc = MyDynamicMplCanvas(Widget,self.LayoutWidget, width=4, height=3, dpi=85)
# 		verticalLayout.addWidget(dc,3)
# 		verticalLayout.addWidget(dc.mpl_toolbar,1)

# 		self.generalayout.addWidget(self.LayoutWidget,0,0)

def update_figure():
	print (g_model_data_txt)
	global time_exec
	global model_value
	global split_model_data_n1
	infile = open('time_exec.txt', 'r+')
	data=infile.readlines()
	if len(data)>1:
		if data[-1]!="stop" and data[-2]!="stop":
			model_data_n0=data[-2].strip()
			model_data_n1=data[-1].strip()

			split_model_data_n0=model_data_n0.split("\t")
			split_model_data_n1=model_data_n1.split("\t")

			time_exec.append(float(split_model_data_n0[0]))
			model_value.append(round(float(split_model_data_n0[g_model_data_txt]),3))

			time_exec.append(float(split_model_data_n1[0]))
			model_value.append(round(float(split_model_data_n1[g_model_data_txt]),3))
			
			plot_time=time_exec[len(time_exec)-2:len(time_exec)]
			plot_model=model_value[len(model_value)-2:len(model_value)]

			#print(str(plot_time)+" -*- "+str(plot_model))

			infile.close()
			self.axes.set_xlabel('Time (min)',fontsize=11)
			self.axes.set_ylabel(_translate("Dialog", g_data_label, None),fontsize=11)
			self.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
			self.axes.plot(plot_time,plot_model,'b-')
			self.Temp_Output_variable.setText(str(round(float(split_model_data_n1[g_model_data_txt]),3)))
			self.draw()
		else :
			time_exec=[]
			model_value=[]
			self.axes.cla()
			for values in data:
				if values!="stop":
					values.strip()
					split_model_data=values.split("\t")
					time_exec.append(float(split_model_data[0]))
					model_value.append(round(float(split_model_data[self.model_data_txt]),3))
			self.axes.set_xlabel('Time (min)',fontsize=11)
			self.axes.set_ylabel(_translate("Dialog", self.data_label, None),fontsize=11)
			self.axes.plot(time_exec,model_value,'b-')
			# Update_data()

class Ui_Dialog(object):
	def setupUi(self,Dialog):
		# global model_data_txt
		# global data_label
		# model_data_txt=1
		# data_label="Tjout [°C]"

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(950, 670)
		self.verticalLayoutWidget = QtGui.QWidget(Dialog)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 900,600))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))


		dc = DynamicGraphic(Dialog,self.verticalLayoutWidget,width=4, height=3, dpi=85)
		self.verticalLayoutWidget.setLayout(dc.dynamic_graph)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Prueba Diagramas", None))

if __name__ == "__main__":
	##TEST##
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QWidget()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	Dialog.show()
	sys.exit(app.exec_())