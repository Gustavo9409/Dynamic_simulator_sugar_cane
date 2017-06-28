# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python27\Scripts\GUI\Valve_properties.ui'
#
# Created: Mon Apr 24 09:03:13 2017
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
class Validator(object):
    def NumValidator(self,LineEdit):
        LineEdit.setValidator(QtGui.QDoubleValidator(0,100000,2,LineEdit))

class Ui_Dialog(object):
    def setupUi(self,name,time,item,Dialog):
        global nameDialog
        Vali = Validator()

        nameDialog=name
        title_name=str(item.label.toPlainText())
        
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(415, 308)
        self.Valve_tabWidget = QtGui.QTabWidget(Dialog)
        self.Valve_tabWidget.setGeometry(QtCore.QRect(3, 32, 411, 271))
        self.Valve_tabWidget.setObjectName(_fromUtf8("Valve_tabWidget"))
        self.Valve_tab_1 = QtGui.QWidget()
        self.Valve_tab_1.setObjectName(_fromUtf8("Valve_tab_1"))
        self.Phisycal_Properties_GrBx = QtGui.QGroupBox(self.Valve_tab_1)
        self.Phisycal_Properties_GrBx.setGeometry(QtCore.QRect(7, 19, 391, 131))
        self.Phisycal_Properties_GrBx.setObjectName(_fromUtf8("Phisycal_Properties_GrBx"))
        self.label_Valve_Diameter = QtGui.QLabel(self.Phisycal_Properties_GrBx)
        self.label_Valve_Diameter.setGeometry(QtCore.QRect(14, 61, 131, 16))
        self.label_Valve_Diameter.setObjectName(_fromUtf8("label_Valve_Diameter"))
        self.Valve_Diameter = QtGui.QLineEdit(self.Phisycal_Properties_GrBx)
        self.Valve_Diameter.setGeometry(QtCore.QRect(138, 60, 41, 20))
        self.Valve_Diameter.setObjectName(_fromUtf8("Valve_Diameter"))
        self.ComBox_Diameter_or_FlowCoeff = QtGui.QComboBox(self.Phisycal_Properties_GrBx)
        self.ComBox_Diameter_or_FlowCoeff.setGeometry(QtCore.QRect(10, 19, 171, 22))
        self.ComBox_Diameter_or_FlowCoeff.setObjectName(_fromUtf8("ComBox_Diameter_or_FlowCoeff"))
        self.ComBox_Diameter_or_FlowCoeff.addItem("--Seleccione dato--")
        self.ComBox_Diameter_or_FlowCoeff.addItem(_translate("Dialog", "Dato de Diámetro", None))
        self.ComBox_Diameter_or_FlowCoeff.addItem("Dato de coeficientes de flujo")
        self.label_Min_Coeff_Flow = QtGui.QLabel(self.Phisycal_Properties_GrBx)
        self.label_Min_Coeff_Flow.setGeometry(QtCore.QRect(199, 53, 131, 31))
        self.label_Min_Coeff_Flow.setObjectName(_fromUtf8("label_Min_Coeff_Flow"))
        self.Min_Coeff_Flow = QtGui.QLineEdit(self.Phisycal_Properties_GrBx)
        self.Min_Coeff_Flow.setGeometry(QtCore.QRect(339, 59, 41, 20))
        self.Min_Coeff_Flow.setObjectName(_fromUtf8("Min_Coeff_Flow"))
        self.Max_Coeff_Flow = QtGui.QLineEdit(self.Phisycal_Properties_GrBx)
        self.Max_Coeff_Flow.setGeometry(QtCore.QRect(339, 98, 41, 20))
        self.Max_Coeff_Flow.setObjectName(_fromUtf8("Max_Coeff_Flow"))
        self.label_Max_Coeff_Flowe = QtGui.QLabel(self.Phisycal_Properties_GrBx)
        self.label_Max_Coeff_Flowe.setGeometry(QtCore.QRect(199, 92, 141, 31))
        self.label_Max_Coeff_Flowe.setObjectName(_fromUtf8("label_Max_Coeff_Flowe"))
        self.ComBox_Cv_or_Kv = QtGui.QComboBox(self.Phisycal_Properties_GrBx)
        self.ComBox_Cv_or_Kv.setGeometry(QtCore.QRect(199, 19, 181, 22))
        self.ComBox_Cv_or_Kv.setObjectName(_fromUtf8("ComBox_Cv_or_Kv"))
        self.ComBox_Cv_or_Kv.addItem("Tipo de coeficiente")
        self.ComBox_Cv_or_Kv.addItem("Coeficientes Cv")
        self.ComBox_Cv_or_Kv.addItem("Coeficientes Kv")
        self.Initial_Conditions_GrBx = QtGui.QGroupBox(self.Valve_tab_1)
        self.Initial_Conditions_GrBx.setGeometry(QtCore.QRect(8, 161, 191, 61))
        self.Initial_Conditions_GrBx.setObjectName(_fromUtf8("Initial_Conditions_GrBx"))
        self.label_Initial_Valve_Opening = QtGui.QLabel(self.Initial_Conditions_GrBx)
        self.label_Initial_Valve_Opening.setGeometry(QtCore.QRect(10, 22, 131, 31))
        self.label_Initial_Valve_Opening.setObjectName(_fromUtf8("label_Initial_Valve_Opening"))
        self.Initial_Valve_Opening = QtGui.QLineEdit(self.Initial_Conditions_GrBx)
        self.Initial_Valve_Opening.setGeometry(QtCore.QRect(141, 28, 41, 20))
        self.Initial_Valve_Opening.setReadOnly(False)
        self.Initial_Valve_Opening.setObjectName(_fromUtf8("Initial_Valve_Opening"))
        self.OKButton_Valve = QtGui.QPushButton(self.Valve_tab_1)
        self.OKButton_Valve.setGeometry(QtCore.QRect(255, 210, 131, 23))
        self.OKButton_Valve.setObjectName(_fromUtf8("OKButton_Valve"))
        self.Valve_tabWidget.addTab(self.Valve_tab_1, _fromUtf8(""))
        self.Valve_tab_2 = QtGui.QWidget()
        self.Valve_tab_2.setObjectName(_fromUtf8("Valve_tab_2"))
        self.Input_fluid_GrBx = QtGui.QGroupBox(self.Valve_tab_2)
        self.Input_fluid_GrBx.setGeometry(QtCore.QRect(10, 30, 191, 71))
        self.Input_fluid_GrBx.setObjectName(_fromUtf8("Input_fluid_GrBx"))
        self.label_InFluid_Flow = QtGui.QLabel(self.Input_fluid_GrBx)
        self.label_InFluid_Flow.setGeometry(QtCore.QRect(10, 21, 131, 16))
        self.label_InFluid_Flow.setObjectName(_fromUtf8("label_InFluid_Flow"))
        self.label_InFluid_Press = QtGui.QLabel(self.Input_fluid_GrBx)
        self.label_InFluid_Press.setGeometry(QtCore.QRect(10, 43, 121, 16))
        self.label_InFluid_Press.setObjectName(_fromUtf8("label_InFluid_Press"))
        self.InFluid_Press = QtGui.QLineEdit(self.Input_fluid_GrBx)
        self.InFluid_Press.setGeometry(QtCore.QRect(140, 42, 41, 20))
        self.InFluid_Press.setReadOnly(True)
        self.InFluid_Press.setObjectName(_fromUtf8("InFluid_Press"))
        self.InFluid_Flow = QtGui.QLineEdit(self.Input_fluid_GrBx)
        self.InFluid_Flow.setGeometry(QtCore.QRect(140, 20, 41, 20))
        self.InFluid_Flow.setReadOnly(True)
        self.InFluid_Flow.setObjectName(_fromUtf8("InFluid_Flow"))
        self.Output_fluid_GrBx = QtGui.QGroupBox(self.Valve_tab_2)
        self.Output_fluid_GrBx.setGeometry(QtCore.QRect(210, 30, 191, 71))
        self.Output_fluid_GrBx.setObjectName(_fromUtf8("Output_fluid_GrBx"))
        self.label_OutFluid_Flow = QtGui.QLabel(self.Output_fluid_GrBx)
        self.label_OutFluid_Flow.setGeometry(QtCore.QRect(10, 27, 131, 16))
        self.label_OutFluid_Flow.setObjectName(_fromUtf8("label_OutFluid_Flow"))
        self.label_OutFluid_Press = QtGui.QLabel(self.Output_fluid_GrBx)
        self.label_OutFluid_Press.setGeometry(QtCore.QRect(10, 49, 121, 16))
        self.label_OutFluid_Press.setObjectName(_fromUtf8("label_OutFluid_Press"))
        self.OutFluid_Press = QtGui.QLineEdit(self.Output_fluid_GrBx)
        self.OutFluid_Press.setGeometry(QtCore.QRect(140, 48, 41, 20))
        self.OutFluid_Press.setReadOnly(True)
        self.OutFluid_Press.setObjectName(_fromUtf8("OutFluid_Press"))
        self.OutFluid_Flow = QtGui.QLineEdit(self.Output_fluid_GrBx)
        self.OutFluid_Flow.setGeometry(QtCore.QRect(140, 26, 41, 20))
        self.OutFluid_Flow.setReadOnly(True)
        self.OutFluid_Flow.setObjectName(_fromUtf8("OutFluid_Flow"))
        self.Valve_tabWidget.addTab(self.Valve_tab_2, _fromUtf8(""))
        self.Valve_tab_3 = QtGui.QWidget()
        self.Valve_tab_3.setObjectName(_fromUtf8("Valve_tab_3"))
        self.Manipulated_Valve_Opening = QtGui.QSpinBox(self.Valve_tab_3)
        self.Manipulated_Valve_Opening.setGeometry(QtCore.QRect(182, 10, 51, 22))
        self.Manipulated_Valve_Opening.setObjectName(_fromUtf8("Manipulated_Valve_Opening"))
        self.label_Valve_Opening = QtGui.QLabel(self.Valve_tab_3)
        self.label_Valve_Opening.setGeometry(QtCore.QRect(10, 13, 191, 16))
        self.label_Valve_Opening.setObjectName(_fromUtf8("label_Valve_Opening"))
        self.Valve_tabWidget.addTab(self.Valve_tab_3, _fromUtf8(""))
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(6, 6, 401, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_translate("Dialog", "--Seleccione tipo de válvula--",None))
        self.comboBox.addItem(_translate("Dialog", "Válvula de gases",None))
        self.comboBox.addItem(_translate("Dialog", "Válvula de líquidos",None))

        self.retranslateUi(Dialog)
        self.Valve_tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.Phisycal_Properties_GrBx.setTitle(_translate("Dialog", "Propiedades físicas", None))
        self.label_Valve_Diameter.setText(_translate("Dialog", "Diámetro[in]", None))
        self.label_Min_Coeff_Flow.setText(_translate("Dialog", "Coeficiente de flujo mínimo\n"
"[gpm/√psi]", None))
        self.label_Max_Coeff_Flowe.setText(_translate("Dialog", "Coeficiente de flujo máximo\n"
"[gpm/√psi]", None))
        self.Initial_Conditions_GrBx.setTitle(_translate("Dialog", "Condiciones iniciales", None))
        self.label_Initial_Valve_Opening.setText(_translate("Dialog", "Apertura de válvula [%]", None))
        self.OKButton_Valve.setText(_translate("Dialog", "Aceptar", None))
        self.Valve_tabWidget.setTabText(self.Valve_tabWidget.indexOf(self.Valve_tab_1), _translate("Dialog", "Propiedades físicas", None))
        self.Input_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de entrada", None))
        self.label_InFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
        self.label_InFluid_Press.setText(_translate("Dialog", "Presión [Pa]", None))
        self.Output_fluid_GrBx.setTitle(_translate("Dialog", "Fluido de salida", None))
        self.label_OutFluid_Flow.setText(_translate("Dialog", "Flujo másico [t/h]", None))
        self.label_OutFluid_Press.setText(_translate("Dialog", "Presión [Pa]", None))
        self.Valve_tabWidget.setTabText(self.Valve_tabWidget.indexOf(self.Valve_tab_2), _translate("Dialog", "Variables de proceso", None))
        self.label_Valve_Opening.setText(_translate("Dialog", "Porcentaje de apertura de válvula:", None))
        self.Valve_tabWidget.setTabText(self.Valve_tabWidget.indexOf(self.Valve_tab_3), _translate("Dialog", "Variable manipulada", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

