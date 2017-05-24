# -*- coding: utf-8 -*-
import sys
import os
directory=str(os.getcwd())
sys.path.insert(0, directory+'\matplotlib_edit_package')
import matplotlib.pyplot as plt
import backend_qt5_DynamicSim as backend

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from backend_qt4agg_DynamicSim import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT )##as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter


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
			(None, None, None, None,None),
			('V_cursor', 'Cursores', 'haircross', 'V_cursor',None),
			(None, None, None, None,None),
			('Pan', _translate("Dialog", "Mover la gráfica (Click izquierdo) / Zoom (Click derecho)", None), 'move', 'pan',None),
			(None, None, None, None,None),
			('Edit axis',_translate("Dialog",'Modificación de ejes', None), 'qt4_editor_options','Edit_axis',[Ts,g_Widget]),
			(None, None, None, None,None),)
		NavigationToolbar2QT.__init__(self, canvas_, parent_)


class DynamicGraphic(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self,Widget,ts,parent=None, width=4, height=4, dpi=100):
		global Ts
		global g_Widget
		fig = Figure(figsize=[width, height], tight_layout = {'pad': 0}, dpi=dpi)
		self.axes = fig.add_subplot(111)
		self.current_timer=None
		# self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
		Ts=ts
		g_Widget=Widget
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


class Ui_Dialog(object):
	def setupUi(self,Dialog):
		# global model_data_txt
		# global data_label
		# model_data_txt=1
		# data_label="Tjout [°C]"
		xs=0.5

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(950, 670)
		self.verticalLayoutWidget = QtGui.QWidget(Dialog)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 900,600))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))


		dc = DynamicGraphic(Dialog,xs,self.verticalLayoutWidget,width=4, height=3, dpi=85)
		self.verticalLayoutWidget.setLayout(dc.dynamic_graph)
		t=[0, 1, 2, 3]
		dc.axes.plot(t, [1, 2, 0, 4], 'r')
		dc.axes.set_xlabel('Time (min)',fontsize=11)
		dc.axes.set_ylabel('Tjout (C)',fontsize=11)
		ax2 = dc.axes.twinx()
		ax2.plot(t, [10, 8, 2, 6], 'b')
		ax2.set_xlabel('Time (min)',fontsize=11)
		ax2.set_ylabel('Fjin (t/h)',fontsize=11)
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