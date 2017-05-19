# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python27\Scripts\GUI\Axis_options.ui'
#
# Created: Thu May 18 16:15:32 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
	def setupUi(self,axes, Dialog):
		global checkBox_x_stat
		global checkBox_x_din
		global checkBox_x_wind
		global tittle
		global x_min
		global label_x_min
		global x_max
		global label_x_max
		global y_min
		global label_y_min
		global y_max
		global label_y_max
		global x_label
		global label_x_label
		global y_label
		global label_y_label
		global label_window_range
		global window_range


		global axis
		global Dialog_window

		axis=axes

		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(366, 395)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Lib/site-packages/matplotlib/mpl-data/images/qt4_editor_options.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Dialog.setWindowIcon(icon)
		Dialog_window=Dialog

		self.horizontalLayout_10 = QtGui.QHBoxLayout(Dialog)
		self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
		self.widget = QtGui.QWidget(Dialog)
		self.widget.setObjectName(_fromUtf8("widget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

		self.tabWidget = QtGui.QTabWidget(self.widget)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.tab_axis = QtGui.QWidget()
		self.tab_axis.setObjectName(_fromUtf8("tab_axis"))

		self.gridLayout = QtGui.QGridLayout(self.tab_axis)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

		self.label_tittle = QtGui.QLabel(self.tab_axis)
		self.label_tittle.setObjectName(_fromUtf8("label_tittle"))
		self.gridLayout.addWidget(self.label_tittle, 0, 0, 1, 1)
		tittle = QtGui.QLineEdit(self.tab_axis)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(tittle.sizePolicy().hasHeightForWidth())
		tittle.setSizePolicy(sizePolicy)
		tittle.setObjectName(_fromUtf8("tittle"))
		self.gridLayout.addWidget(tittle, 0, 1, 1, 1)


		self.X_axis_GrBx = QtGui.QGroupBox(self.tab_axis)
		self.X_axis_GrBx.setObjectName(_fromUtf8("X_axis_GrBx"))
		self.verticalLayout_3 = QtGui.QVBoxLayout(self.X_axis_GrBx)
		self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))


		checkBox_x_stat = QtGui.QCheckBox(self.X_axis_GrBx)
		checkBox_x_stat.setObjectName(_fromUtf8("checkBox_x_stat"))
		self.buttonGroup = QtGui.QButtonGroup(Dialog)
		self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
		self.buttonGroup.addButton(checkBox_x_stat)
		self.horizontalLayout_2.addWidget(checkBox_x_stat)
		checkBox_x_din = QtGui.QCheckBox(self.X_axis_GrBx)
		checkBox_x_din.setObjectName(_fromUtf8("checkBox_x_din"))
		self.buttonGroup.addButton(checkBox_x_din)
		self.horizontalLayout_2.addWidget(checkBox_x_din)
		checkBox_x_wind = QtGui.QCheckBox(self.X_axis_GrBx)
		checkBox_x_wind.setObjectName(_fromUtf8("checkBox_x_wind"))
		self.buttonGroup.addButton(checkBox_x_wind)
		self.buttonGroup.buttonClicked['int'].connect(self.selection_check)


		self.horizontalLayout_2.addWidget(checkBox_x_wind)
		self.verticalLayout_2.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_5 = QtGui.QHBoxLayout()
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		label_x_min = QtGui.QLabel(self.X_axis_GrBx)
		label_x_min.setObjectName(_fromUtf8("label_x_min"))
		self.horizontalLayout_5.addWidget(label_x_min)
		x_min = QtGui.QLineEdit(self.X_axis_GrBx)
		x_min.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(x_min.sizePolicy().hasHeightForWidth())
		x_min.setSizePolicy(sizePolicy)
		x_min.setObjectName(_fromUtf8("x_min"))
		self.horizontalLayout_5.addWidget(x_min)
		self.verticalLayout_2.addLayout(self.horizontalLayout_5)

		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		label_x_max = QtGui.QLabel(self.X_axis_GrBx)
		label_x_max.setObjectName(_fromUtf8("label_x_max"))
		self.horizontalLayout_4.addWidget(label_x_max)
		x_max = QtGui.QLineEdit(self.X_axis_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(x_max.sizePolicy().hasHeightForWidth())
		x_max.setSizePolicy(sizePolicy)
		x_max.setObjectName(_fromUtf8("x_max"))
		self.horizontalLayout_4.addWidget(x_max)
		
		label_window_range = QtGui.QLabel(self.X_axis_GrBx)
		label_window_range.setObjectName(_fromUtf8("label_window_range"))
		self.horizontalLayout_4.addWidget(label_window_range)
		window_range = QtGui.QLineEdit(self.X_axis_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(window_range.sizePolicy().hasHeightForWidth())
		window_range.setSizePolicy(sizePolicy)
		window_range.setObjectName(_fromUtf8("window_range"))
		self.horizontalLayout_4.addWidget(window_range)
		label_window_range.hide()
		window_range.hide()

		self.verticalLayout_2.addLayout(self.horizontalLayout_4)


		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		label_x_label = QtGui.QLabel(self.X_axis_GrBx)
		label_x_label.setObjectName(_fromUtf8("label_x_label"))
		self.horizontalLayout_3.addWidget(label_x_label)
		x_label = QtGui.QLineEdit(self.X_axis_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(x_label.sizePolicy().hasHeightForWidth())
		x_label.setSizePolicy(sizePolicy)
		x_label.setObjectName(_fromUtf8("x_label"))
		self.horizontalLayout_3.addWidget(x_label)
		self.verticalLayout_2.addLayout(self.horizontalLayout_3)
		self.verticalLayout_3.addLayout(self.verticalLayout_2)
		self.gridLayout.addWidget(self.X_axis_GrBx, 1, 0, 1, 2)


		self.Y_axis_GrBx = QtGui.QGroupBox(self.tab_axis)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Y_axis_GrBx.sizePolicy().hasHeightForWidth())
		self.Y_axis_GrBx.setSizePolicy(sizePolicy)
		self.Y_axis_GrBx.setObjectName(_fromUtf8("Y_axis_GrBx"))
		self.verticalLayout_5 = QtGui.QVBoxLayout(self.Y_axis_GrBx)
		self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))


		self.horizontalLayout_6 = QtGui.QHBoxLayout()
		self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
		label_y_min = QtGui.QLabel(self.Y_axis_GrBx)
		label_y_min.setObjectName(_fromUtf8("label_y_min"))
		self.horizontalLayout_6.addWidget(label_y_min)
		y_min = QtGui.QLineEdit(self.Y_axis_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(y_min.sizePolicy().hasHeightForWidth())
		y_min.setSizePolicy(sizePolicy)
		y_min.setObjectName(_fromUtf8("y_min"))
		self.horizontalLayout_6.addWidget(y_min)
		self.verticalLayout_4.addLayout(self.horizontalLayout_6)


		self.horizontalLayout_7 = QtGui.QHBoxLayout()
		self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
		label_y_max = QtGui.QLabel(self.Y_axis_GrBx)
		label_y_max.setObjectName(_fromUtf8("label_y_max"))
		self.horizontalLayout_7.addWidget(label_y_max)
		y_max = QtGui.QLineEdit(self.Y_axis_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(y_max.sizePolicy().hasHeightForWidth())
		y_max.setSizePolicy(sizePolicy)
		y_max.setObjectName(_fromUtf8("y_max"))
		self.horizontalLayout_7.addWidget(y_max)
		self.verticalLayout_4.addLayout(self.horizontalLayout_7)


		self.horizontalLayout_8 = QtGui.QHBoxLayout()
		self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
		label_y_label = QtGui.QLabel(self.Y_axis_GrBx)
		label_y_label.setObjectName(_fromUtf8("label_y_label"))
		self.horizontalLayout_8.addWidget(label_y_label)
		y_label = QtGui.QLineEdit(self.Y_axis_GrBx)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(y_label.sizePolicy().hasHeightForWidth())
		y_label.setSizePolicy(sizePolicy)
		y_label.setObjectName(_fromUtf8("y_label"))
		self.horizontalLayout_8.addWidget(y_label)
		self.verticalLayout_4.addLayout(self.horizontalLayout_8)
		self.verticalLayout_5.addLayout(self.verticalLayout_4)
		self.gridLayout.addWidget(self.Y_axis_GrBx, 2, 0, 1, 2)
		#Vertical layout for buttons
		self.tabWidget.addTab(self.tab_axis, _fromUtf8(""))
		self.verticalLayout.addWidget(self.tabWidget)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		#Apply button
		self.Apply_btn = QtGui.QPushButton(self.widget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Apply_btn.sizePolicy().hasHeightForWidth())
		self.Apply_btn.setSizePolicy(sizePolicy)
		self.Apply_btn.setObjectName(_fromUtf8("Apply_btn"))
		self.horizontalLayout.addWidget(self.Apply_btn)
		self.Apply_btn.clicked.connect(self.apply_options)
		#Cancel button
		self.Cancel_btn = QtGui.QPushButton(self.widget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.Cancel_btn.sizePolicy().hasHeightForWidth())
		self.Cancel_btn.setSizePolicy(sizePolicy)
		self.Cancel_btn.setObjectName(_fromUtf8("Cancel_btn"))
		self.horizontalLayout.addWidget(self.Cancel_btn)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.horizontalLayout_10.addWidget(self.widget)

		self.retranslateUi(Dialog)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

		checkBox_x_stat.setChecked(True)
		title=axis.get_title()
		xmin, xmax = axis.get_xlim()
		ymin, ymax = axis.get_ylim()
		xlabel=axis.get_xlabel()
		ylabel=axis.get_ylabel()

		tittle.setText(str(title))
		x_min.setText(str(xmin))
		x_max.setText(str(xmax))
		y_min.setText(str(ymin))
		y_max.setText(str(ymax))
		x_label.setText(xlabel)
		y_label.setText(ylabel)

	def apply_options(self):
		if checkBox_x_stat.isChecked():
			axis.set_title(tittle.text())
			axis.set_xlim(float(x_min.text()), float(x_max.text()))
			axis.set_xlabel(x_label.text())
			axis.set_ylim(float(y_min.text()), float(y_max.text()))
			axis.set_ylabel(y_label.text())
			#Re-draw
			figure = axis.get_figure()
			figure.canvas.draw()
			#Close window
			Dialog_window.close()

	def selection_check(self):
		if checkBox_x_stat.isChecked():
			print "Stat"
			x_min.show()
			label_x_min.show()
			x_max.show()
			label_x_max.show()			
			x_label.show()
			label_x_label.show()

			label_window_range.hide()
			window_range.hide()


			x_min.setEnabled(1)
			label_x_min.setEnabled(1)
			x_max.setEnabled(1)
			label_x_max.setEnabled(1)
			x_label.setEnabled(1)
			label_x_label.setEnabled(1)
			
			title=axis.get_title()
			xmin, xmax = axis.get_xlim()
			ymin, ymax = axis.get_ylim()
			xlabel=axis.get_xlabel()
			ylabel=axis.get_ylabel()

			tittle.setText(str(title))
			x_min.setText(str(xmin))
			x_max.setText(str(xmax))
			y_min.setText(str(ymin))
			y_max.setText(str(ymax))
			x_label.setText(xlabel)
			y_label.setText(ylabel)

		elif checkBox_x_din.isChecked():
			print "Dinam"
			x_min.show()
			label_x_min.show()
			x_max.show()
			label_x_max.show()
			x_label.show()
			label_x_label.show()


			label_window_range.hide()
			window_range.hide()

			
			x_min.setDisabled(1)
			label_x_min.setDisabled(1)
			x_max.setDisabled(1)
			label_x_max.setDisabled(1)
			x_label.setDisabled(1)
			label_x_label.setDisabled(1)



		elif checkBox_x_wind.isChecked():
			print "Wind"
			x_min.hide()
			label_x_min.hide()
			x_max.hide()
			label_x_max.hide()
			x_label.hide()
			label_x_label.hide()

			label_window_range.show()
			window_range.show()



	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Opciones de eje", None))
		self.label_tittle.setText(_translate("Dialog", "Titulo", None))
		self.X_axis_GrBx.setTitle(_translate("Dialog", "Eje X", None))
		checkBox_x_stat.setText(_translate("Dialog", "Eje X fijo", None))
		checkBox_x_din.setText(_translate("Dialog", "Eje X dinámico", None))
		checkBox_x_wind.setText(_translate("Dialog", "Eje X por ventanas", None))
		label_x_min.setText(_translate("Dialog", "Min", None))
		label_x_max.setText(_translate("Dialog", "Max", None))
		label_window_range.setText(_translate("Dialog", "Ancho de ventana", None))
		label_x_label.setText(_translate("Dialog", "Etiqueta", None))
		self.Y_axis_GrBx.setTitle(_translate("Dialog", "Eje Y", None))
		label_y_min.setText(_translate("Dialog", "Min", None))
		label_y_max.setText(_translate("Dialog", "Max", None))
		label_y_label.setText(_translate("Dialog", "Etiqueta", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_axis), _translate("Dialog", "Ejes", None))
		self.Apply_btn.setText(_translate("Dialog", "Aplicar", None))
		self.Cancel_btn.setText(_translate("Dialog", "Cancelar", None))


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Dialog = QtGui.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	Dialog.show()
	sys.exit(app.exec_())

