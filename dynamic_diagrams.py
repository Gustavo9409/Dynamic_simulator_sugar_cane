# -*- coding: utf-8 -*-

# Installed Libs
import sys
import os
directory=str(os.getcwd())
images_directory=directory+"\Images"
sys.path.insert(0, directory+'\matplotlib_edit_package')
import matplotlib.pyplot as plt
import backend_qt5_DynamicSim as backend
import matplotlib.patches as patches

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from backend_qt4agg_DynamicSim import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT )##as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches

#global values
global time_exec
global model_value
model_value=[]
time_exec=[]



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

## Toolbar functions
class NavigationToolbar(NavigationToolbar2QT):
	def __init__(self, Enable,canvas_, parent_):
		#backend.figureoptions = None  # Monkey patched to kill the figure options button on matplotlib toolbar
		##Images: C:\Python27\Lib\site-packages\matplotlib\mpl-data\images
		##Functions: C:\Python27\Lib\site-packages\matplotlib\backends\backend_qt5.py
		self.toolitems = (
			(None, None, None, None,None),
			('V_cursor', 'Cursores', images_directory+'\haircross','V_cursor',Enable),
			(None, None, None, None,None),
			('Pan', _translate("Dialog", "Mover la gráfica (Click izquierdo) / Zoom (Click derecho)", None), images_directory+'\move', 'pan',None),
			(None, None, None, None,None),
			('Edit axis',_translate("Dialog",'Modificación de ejes', None), images_directory+'\qt4_editor_options','Edit_axis',[Ts,g_Widget]),
			('Save',_translate("Dialog",'Guardar gráfica', None), images_directory+'\_filesave','save_figure',None),
			)
		NavigationToolbar2QT.__init__(self, canvas_, parent_)


#Dynamic graphic class
class DynamicGraphic(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self,Widget,ts,enable_cursor,Principal_signal_flag,multi_variable,parent=None, width=4, height=4, dpi=100):
		global Ts
		global Enable_flag
		global g_Widget
		global Vali

		Vali = Validator()
		self.ax2=None
		self.principal_signals=None
		self.signals_in_table=None
		self.time_in_table=None
		self.signals_table_checkboxs=None
		self.signals_min_factor=None
		self.signals_max_factor=None
		self.ids_connect=[]
		self.id_principal_selector_connect=[]

		self.fig = Figure(figsize=[width, height], tight_layout = {'pad': 0}, dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.current_timer=None

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		self.on_cursor_mode=None

		self.axes.spines['left'].set_color('red')
		self.axes.tick_params(axis='y', colors='red')
		self.axes.yaxis.label.set_color('red')

		self.axes.grid(True)
		gridlines = self.axes.get_xgridlines() + self.axes.get_ygridlines()
		for line in gridlines:
			line.set_linestyle('-.')

		self.signals_table = QtGui.QTableWidget()
		self.signals_table.setColumnCount(5)
		header = self.signals_table.horizontalHeader()
		self.signals_table.setHorizontalHeaderLabels(['', _translate("Dialog", "Nombre señal",None),"Grupo" ,_translate("Dialog", 
			"Valor mínimo de la señal ",None), _translate("Dialog", "Valor máximo de la señal",None)])
		
		header.setResizeMode(0,  QtGui.QHeaderView.ResizeToContents)
		header.setResizeMode(1,  QtGui.QHeaderView.Stretch)
		header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
		header.setResizeMode(3,  QtGui.QHeaderView.Stretch)
		header.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)

		self.principal_signal_selector = QtGui.QComboBox()
		self.principal_signal_selector.setGeometry(QtCore.QRect(7, 6, 411, 22))
		self.principal_signal_selector.setObjectName(_fromUtf8("Selector_principal_signal"))
		self.principal_signal_selector.addItem(_translate("Dialog","--Señal principal--",None))
		
		Ts=ts
		g_Widget=Widget
		Enable_flag=enable_cursor
		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		self.mpl_toolbar = NavigationToolbar(Enable_flag,self,Widget)

		self.dynamic_graph = QtGui.QGridLayout()

		if Principal_signal_flag==True:
			self.dynamic_graph.addWidget(self.principal_signal_selector, 0, 0)
			self.dynamic_graph.addWidget(self, 1, 0)
			self.dynamic_graph.setRowStretch(1, 4)
			self.dynamic_graph.addWidget(self.mpl_toolbar, 2, 0)
			self.dynamic_graph.setRowStretch(2, 1)
			if multi_variable==True:
				# self.dynamic_graph.addWidget(self.signals_table,1)
				self.dynamic_graph.addWidget(self.signals_table, 3, 0)
				self.dynamic_graph.setRowStretch(3, 1)
		else:
			self.dynamic_graph.addWidget(self, 0, 0)
			self.dynamic_graph.setRowStretch(0, 4)
			self.dynamic_graph.addWidget(self.mpl_toolbar, 1, 0)
			self.dynamic_graph.setRowStretch(1, 1)
			if multi_variable==True:
				self.dynamic_graph.addWidget(self.signals_table, 2, 0)
				self.dynamic_graph.setRowStretch(2, 1)
		

		self.colors=['b','g','c','y','m','k']
		
	## Set legends for signals plotting
	def set_legends(self):
		self.all_handles=[]
		self.all_labels=[]
		handles_principal, label_principal=self.axes.get_legend_handles_labels()

		for elmts in label_principal:
			self.all_labels.append(elmts)
		for elmts in handles_principal:
			self.all_handles.append(elmts)
		if self.ax2 is not None:
			handles_x2, label_x2=self.ax2.get_legend_handles_labels()
			for elmts in label_x2:
				self.all_labels.append(elmts)
			for elmts in handles_x2:
				self.all_handles.append(elmts)
		
		self.axes.legend(self.all_handles, self.all_labels)
		
	## Reload toolbar with disabled/enabled functions
	def reload_toolbar(self,enable_cursor_a):
		self.mpl_toolbar.setParent(None)
		self.mpl_toolbar = NavigationToolbar(enable_cursor_a,self,g_Widget)
		self.dynamic_graph.addWidget(self.mpl_toolbar, 1, 0)
		self.dynamic_graph.setRowStretch(1, 1)

	## Add principal signal to graph
	def add_principal_signal_options(self,label_signals):
		self.principal_labels=label_signals
		for label in label_signals:
			self.principal_signal_selector.addItem(_translate("Dialog",label,None))

	## Default principal signal to plot
	def default_principal_signal(self,signal,time,label):
		self.axes.plot(time,signal, color='r',label=label)
		self.axes.set_xlabel('Time (min)',fontsize=11)
		self.axes.set_ylabel(label,fontsize=11)
		self.draw()

	## Plot principal signal
	def principal_signal_plot(self):
		signal_selected=self.principal_signal_selector.currentText()
		for k,signals in enumerate(self.principal_signals):
			if signal_selected==self.principal_labels[k]:
				for ax_i,ax in enumerate(self.fig.get_axes()): 
					if ax_i==0:
						ax.cla()
						ax.plot(self.principal_time,signals, color='r',label=self.principal_labels[k])
						ax.set_xlabel('Time (min)',fontsize=11)
						ax.set_ylabel(self.principal_labels[k],fontsize=11)
						ax.grid(True)
						gridlines = ax.get_xgridlines() + ax.get_ygridlines()
						for line in gridlines:
							line.set_linestyle('-.')
						self.set_legends()
						self.draw()
						
	## Update values to principal signal
	def update_principal_signal(self,principal_signals,time):
		if len(self.id_principal_selector_connect)>0:
			self.principal_signal_selector.currentIndexChanged.disconnect()
			self.id_principal_selector_connect=[]
		signal_selected=self.principal_signal_selector.currentText()
		for k,signals in enumerate(principal_signals):
			if signal_selected==label_signals[k]:
				for ax_i,ax in enumerate(self.fig.get_axes()): 
					if ax_i==0:
						ax.cla()
						ax.plot(time,signals, color='r',label=self.principal_labels[k])
						ax.set_xlabel('Time (min)',fontsize=11)
						ax.set_ylabel(self.principal_labels[k],fontsize=11)
						ax.grid(True)
						gridlines = ax.get_xgridlines() + ax.get_ygridlines()
						for line in gridlines:
							line.set_linestyle('-.')
						self.set_legends()
						self.draw()

	## Stop mode for principal signal
	def update_principal_signal_stop_mode(self,signals,time):
		self.principal_signals=signals
		self.principal_time=time
		self.id_connect=self.principal_signal_selector.currentIndexChanged.connect(self.principal_signal_plot)
		self.id_principal_selector_connect.append(self.id_connect)

	## Add other signals to plot in other axis with scale factors
	def add_plot(self,time,signals,labels,min_factor,max_factor):
		if self.ax2 is not None:
			self.ax2.cla()
		else:
			self.ax2 = self.axes.twinx()
			
		left, width_r = .85, .13
		bottom, height_r = .88, .1
		right = left + width_r
		top = bottom + height_r
		space_w=0.0
		space_h=0.0
		ax2_patches=[]

		new_signals=[]
		self.maxims=[]
		self.max_factors=max_factor
		self.min_factors=min_factor
		if len(signals)>0:
			self.axes.spines['left'].set_color('red')
			self.axes.tick_params(axis='y', colors='red')
			self.ax2.set_ylabel(_translate("Dialog", "Otras señales", None),fontsize=11)
			for k,signal in enumerate(signals):
				new=[]
				# max_val=max(signal)
				# self.maxims.append(max_val)
				for data in signal:
					new.append((data-self.min_factors[k])/(self.max_factors[k]-self.min_factors[k]))
				new_signals.append(new)
			for k,signals in enumerate(new_signals):
				self.ax2.plot(time,signals,label=labels[k],color=self.colors[k])		
			# self.ax2.legend(loc = (0.875, 0.86))
			self.set_legends()
		else:
			self.ax2.remove()
			self.ax2=None
			self.set_legends()
		self.draw()
	
	# Add auxiliar signals to select in table 
	def add_table_signals(self,labels,groups):
		self.signals_table_checkboxs=[]
		self.signals_min_factor=[]
		self.signals_max_factor=[]
		
		self.labels_in_table=labels

		self.signals_table.setRowCount(0)
		for label,group in zip(labels,groups):
			rowPosition = self.signals_table.rowCount()
			self.signals_table.insertRow(rowPosition)
			checkBox = QtGui.QCheckBox(self.signals_table)
			LineEdit_min=QLineEdit(self.signals_table)

			Vali.NumValidator(LineEdit_min)
			LineEdit_min.setAlignment(QtCore.Qt.AlignHCenter)
			LineEdit_min.setFrame(False)
			LineEdit_min.setText("0.0")

			LineEdit_max=QLineEdit(self.signals_table)
			LineEdit_max.setAlignment(QtCore.Qt.AlignHCenter)
			Vali.NumValidator(LineEdit_max)
			LineEdit_max.setFrame(False)
			LineEdit_max.setText("10.0")

			self.signals_table_checkboxs.append(checkBox)
			self.signals_min_factor.append(LineEdit_min)
			self.signals_max_factor.append(LineEdit_max)
			
			self.signals_table.setCellWidget(rowPosition, 0, checkBox)

			self.signals_table.setItem(rowPosition, 1, QtGui.QTableWidgetItem(str(label)))
			self.signals_table.item(rowPosition, 1).setFlags(QtCore.Qt.ItemIsEnabled)
			self.signals_table.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignVCenter| QtCore.Qt.AlignHCenter)
			self.signals_table.setItem(rowPosition, 2, QtGui.QTableWidgetItem(str(group)))
			self.signals_table.item(rowPosition, 2).setFlags(QtCore.Qt.ItemIsEnabled)
			self.signals_table.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignVCenter| QtCore.Qt.AlignHCenter)

			self.signals_table.setCellWidget(rowPosition, 3, LineEdit_min)
			self.signals_table.setCellWidget(rowPosition, 4, LineEdit_max)

	## Update values of signals in table
	def update_table_signals(self,time,signals):
		if len(self.ids_connect)>0:
			for k,chkbox in enumerate(self.signals_table_checkboxs):
				chkbox.stateChanged.disconnect()
			self.ids_connect=[]

		self.signals_in_table=signals
		self.time_in_table=time
		signals_to_plot=[]
		labels_to_plot=[]
		max_factors_to_plot=[]
		min_factors_to_plot=[]
		cnt_checks=0
		some_check=True
		# if on_cursor_mode is None:
		for k,chkbox in enumerate(self.signals_table_checkboxs):
			if chkbox.isChecked():
				cnt_checks=cnt_checks+1
				signals_to_plot.append(self.signals_in_table[k])
				labels_to_plot.append(self.labels_in_table[k])
				max_factors_to_plot.append(float(self.signals_max_factor[k].text()))
				min_factors_to_plot.append(float(self.signals_min_factor[k].text()))
			else:
				self.signals_max_factor[k].setEnabled(True)
				self.signals_min_factor[k].setEnabled(True)
		if cnt_checks==0:
			some_check=False
		# if some_check==True:
		self.add_plot(self.time_in_table,signals_to_plot,labels_to_plot,min_factors_to_plot,max_factors_to_plot)

	## Stop mode to signals in table
	def update_table_signals_stop_mode(self,time,signals):
		self.signals_in_table=signals
		self.time_in_table=time
		self.ids_connect=[]
		for k,chkbox in enumerate(self.signals_table_checkboxs):
			id_connect=chkbox.stateChanged.connect(self.plot_select_signal)
			self.ids_connect.append(id_connect)
			# print (self.ids_connect)

	## Plot signals selected in table
	def plot_select_signal(self):
		if self.time_in_table is not None and self.signals_in_table is not None:
			signals_to_plot=[]
			labels_to_plot=[]
			max_factors_to_plot=[]
			min_factors_to_plot=[]
			cnt_checks=0
			some_check=True
			Empty_signal=False
			# if on_cursor_mode is None:
			for k,chkbox in enumerate(self.signals_table_checkboxs):
				if chkbox.isChecked():
					self.signals_max_factor[k].setDisabled(True)
					self.signals_min_factor[k].setDisabled(True)
					cnt_checks=cnt_checks+1
					signals_to_plot.append(self.signals_in_table[k])
					labels_to_plot.append(self.labels_in_table[k])
					if self.signals_max_factor[k].text()=='':
						self.signals_max_factor[k].setText("10.0")
					max_factors_to_plot.append(float(self.signals_max_factor[k].text()))
					if self.signals_min_factor[k].text()=='':
						self.signals_min_factor[k].setText("0.0")
					min_factors_to_plot.append(float(self.signals_min_factor[k].text()))
				else:
					self.signals_max_factor[k].setEnabled(True)
					self.signals_min_factor[k].setEnabled(True)
			if cnt_checks==0:
				some_check=False
			# if some_check==True:
			for signals in signals_to_plot:
				if len(signals)==0:
					Empty_signal=True
					print ("Empty_signal")
					break
				else:
					Empty_signal=False
			if Empty_signal==False:
				self.add_plot(self.time_in_table,signals_to_plot,labels_to_plot,min_factors_to_plot,max_factors_to_plot)



