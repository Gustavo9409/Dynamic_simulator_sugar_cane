# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PID_properties.ui'
#
# Created: Tue Jul 04 15:26:55 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
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

## -- Text field number validator -- ##
class Validator(object):
	def NumValidator(self,LineEdit):
		LineEdit.setValidator(QtGui.QDoubleValidator(0,100000,2,LineEdit))

class Ui_Dialog(object):
	def setupUi(self,name,ts,item,Dialog):

		#Global others
		global Dialog_window
		global title_name
		global nameDialog
		global Ts
		global item_flow
		
		Vali = Validator()
		Ts=ts
		Dialog_window=Dialog
		nameDialog=name
		title_name=str(item.label.toPlainText())
		item_flow=item



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
		self.tabWidget = QtGui.QTabWidget(Dialog)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.Tab1 = QtGui.QWidget()
		self.Tab1.setObjectName(_fromUtf8("Tab1"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.Tab1)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.gridLayout = QtGui.QGridLayout()
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.label = QtGui.QLabel(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout.addWidget(self.label)
		self.comboBox = QtGui.QComboBox(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
		self.comboBox.setSizePolicy(sizePolicy)
		self.comboBox.setObjectName(_fromUtf8("comboBox"))
		self.horizontalLayout.addWidget(self.comboBox)
		self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
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
		self.P_value = QtGui.QLineEdit(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.P_value.sizePolicy().hasHeightForWidth())
		self.P_value.setSizePolicy(sizePolicy)
		self.P_value.setObjectName(_fromUtf8("P_value"))
		self.gridLayout_2.addWidget(self.P_value, 0, 1, 1, 1)
		self.label_I = QtGui.QLabel(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_I.sizePolicy().hasHeightForWidth())
		self.label_I.setSizePolicy(sizePolicy)
		self.label_I.setObjectName(_fromUtf8("label_I"))
		self.gridLayout_2.addWidget(self.label_I, 1, 0, 1, 1)
		self.I_value = QtGui.QLineEdit(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.I_value.sizePolicy().hasHeightForWidth())
		self.I_value.setSizePolicy(sizePolicy)
		self.I_value.setObjectName(_fromUtf8("I_value"))
		self.gridLayout_2.addWidget(self.I_value, 1, 1, 1, 1)
		self.label_D = QtGui.QLabel(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_D.sizePolicy().hasHeightForWidth())
		self.label_D.setSizePolicy(sizePolicy)
		self.label_D.setObjectName(_fromUtf8("label_D"))
		self.gridLayout_2.addWidget(self.label_D, 2, 0, 1, 1)
		self.D_value = QtGui.QLineEdit(self.Variables_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.D_value.sizePolicy().hasHeightForWidth())
		self.D_value.setSizePolicy(sizePolicy)
		self.D_value.setObjectName(_fromUtf8("D_value"))
		self.gridLayout_2.addWidget(self.D_value, 2, 1, 1, 1)
		self.gridLayout.addWidget(self.Variables_GrBx, 1, 0, 1, 1)
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
		self.SP_value = QtGui.QLineEdit(self.Set_point_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.SP_value.sizePolicy().hasHeightForWidth())
		self.SP_value.setSizePolicy(sizePolicy)
		self.SP_value.setObjectName(_fromUtf8("SP_value"))
		self.horizontalLayout_4.addWidget(self.SP_value)
		self.gridLayout.addWidget(self.Set_point_GrBx, 2, 0, 1, 1)
		self.horizontalLayout_2.addLayout(self.gridLayout)
		self.Ok_button = QtGui.QPushButton(self.Tab1)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Ok_button.sizePolicy().hasHeightForWidth())
		self.Ok_button.setSizePolicy(sizePolicy)
		self.Ok_button.setObjectName(_fromUtf8("Ok_button"))
		self.horizontalLayout_2.addWidget(self.Ok_button)
		self.tabWidget.addTab(self.Tab1, _fromUtf8(""))

		self.Tab2 = QtGui.QWidget()
		self.Tab2.setObjectName(_fromUtf8("Tab2"))
		self.tabWidget.addTab(self.Tab2, _fromUtf8(""))
		

		verticalLayoutWidget = QtGui.QWidget()
		verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 410, 260))
		verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

		Graph = DynamicGraphic(Dialog,Ts,Enable_cursor,False,False,self.Tab2, width=4, height=3, dpi=85)
		Graph.axes.set_xlabel('Time (min)',fontsize=11)
		Graph.axes.set_ylabel(_translate("Dialog", "Mv", None),fontsize=11)
		Graph.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		Graph.set_legends()

		self.V_layout_tab_2=QtGui.QVBoxLayout(self.Tab2)
		self.V_layout_tab_2.addWidget(verticalLayoutWidget)

		verticalLayoutWidget.setLayout(Graph.dynamic_graph)

		self.horizontalLayout_3.addWidget(self.tabWidget)
		self.retranslateUi(Dialog)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Datos "+title_name, None))
		self.label.setText(_translate("Dialog", "Variable a controlar:", None))
		self.Variables_GrBx.setTitle(_translate("Dialog", "PID", None))
		self.label_P.setText(_translate("Dialog", "Constante proporcional", None))
		self.label_I.setText(_translate("Dialog", "Constante  integral", None))
		self.label_D.setText(_translate("Dialog", "Constante  diferencial", None))
		self.Set_point_GrBx.setTitle(_translate("Dialog", "Ajuste", None))
		self.label_SP.setText(_translate("Dialog", "SP", None))
		self.Ok_button.setText(_translate("Dialog", "Aceptar", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("Dialog", "Entradas", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), _translate("Dialog", "Gráfico", None))

