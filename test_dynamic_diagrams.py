from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from matplotlib.ticker import FormatStrFormatter

from dynamic_diagrams import DynamicGraphic

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

class Ui_Dialog(object):
	def setupUi(self,Dialog):

		xs=0.5
		SS=[]

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(950, 670)
		self.verticalLayoutWidget = QtGui.QWidget(Dialog)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(15, 35, 900,600))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))


		dc = DynamicGraphic(Dialog,xs,True,True,True,self.verticalLayoutWidget,width=4, height=3, dpi=85)
		self.verticalLayoutWidget.setLayout(dc.dynamic_graph)
		t=[0.32,0.64,0.96,1.28,1.6,1.92,2.24,2.56,2.88,3.2]
		S0=[10, 20,20,20,20,20,7,5,5, 15]
		S0p=[21, 31,31,31,31,31,18,16,16,26]

		dc.default_principal_signal(S0,t,"Principal")
		dc.add_principal_signal_options(["principal","principal2"])
		dc.update_principal_signal_stop_mode([S0,S0p],t)
	

		S1=[5, 10,10,10,10,10,10,7, 2, 6]
		S2=[20, 40,40,40,40,40,30,27,10, 30]
		SS.append(S1)
		SS.append(S2)
		factors=[150,60]
		labels=["S1","S2"]
		groups=["tipo1","tipo2"]
		dc.add_table_signals(labels,groups)
		dc.update_table_signals_stop_mode(t,SS)
		dc.set_legends()

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