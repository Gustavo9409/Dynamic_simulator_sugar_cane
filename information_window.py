# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'information_window.ui'
#
# Created: Fri Aug 11 09:34:36 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!
import os
directory=str(os.getcwd())
images_directory=directory+"\Images"

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

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
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(490, 503)

        ##Non-resizeable QDialog
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth());
        Dialog.setSizePolicy(sizePolicy);
        Dialog.setMinimumSize(QSize(490, 503));
        Dialog.setMaximumSize(QSize(490, 503));
        Dialog.setSizeGripEnabled(False);

        self.icon_cenicana = QtGui.QLabel(Dialog)
        self.icon_cenicana.setGeometry(QtCore.QRect(30, 30, 151, 141))
        self.icon_cenicana.setFrameShape(QtGui.QFrame.StyledPanel)
        self.icon_cenicana.setLineWidth(1)
        self.icon_cenicana.setText(_fromUtf8(""))
        self.icon_cenicana.setWordWrap(False)
        self.icon_cenicana.setMargin(0)
        self.icon_cenicana.setObjectName(_fromUtf8("icon_cenicana"))
        self.icon_cenicana.setPixmap(QtGui.QPixmap(images_directory + "/Cenicana_logo.jpg"))

        self.icon_dynamic_sim = QtGui.QLabel(Dialog)
        self.icon_dynamic_sim.setGeometry(QtCore.QRect(230, 10, 221, 188))
        self.icon_dynamic_sim.setFrameShape(QtGui.QFrame.StyledPanel)
        self.icon_dynamic_sim.setText(_fromUtf8(""))
        self.icon_dynamic_sim.setObjectName(_fromUtf8("icon_dynamic_sim"))
        self.icon_dynamic_sim.setPixmap(QtGui.QPixmap(images_directory + "/Simulador_dinamico_logo.jpg"))

        self.Dynamic_sim_tittle = QtGui.QLabel(Dialog)
        self.Dynamic_sim_tittle.setGeometry(QtCore.QRect(15, 186, 471, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Unicode MS"))
        font.setBold(True)
        font.setWeight(75)
        self.Dynamic_sim_tittle.setFont(font)
        self.Dynamic_sim_tittle.setAlignment(QtCore.Qt.AlignCenter)
        self.Dynamic_sim_tittle.setObjectName(_fromUtf8("Dynamic_sim_tittle"))
        self.Cenicana_tittle = QtGui.QLabel(Dialog)
        self.Cenicana_tittle.setGeometry(QtCore.QRect(9, 236, 471, 20))
        self.Cenicana_tittle.setAlignment(QtCore.Qt.AlignCenter)
        self.Cenicana_tittle.setObjectName(_fromUtf8("Cenicana_tittle"))
        self.cenican_tittle_2 = QtGui.QLabel(Dialog)
        self.cenican_tittle_2.setGeometry(QtCore.QRect(8, 255, 461, 20))
        self.cenican_tittle_2.setAlignment(QtCore.Qt.AlignCenter)
        self.cenican_tittle_2.setObjectName(_fromUtf8("cenican_tittle_2"))
        self.Version_label = QtGui.QLabel(Dialog)
        self.Version_label.setGeometry(QtCore.QRect(23, 439, 471, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Unicode MS"))
        font.setBold(True)
        font.setWeight(75)
        self.Version_label.setFont(font)
        self.Version_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Version_label.setObjectName(_fromUtf8("Version_label"))

        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(30, 280, 431, 181))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.setReadOnly(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Acerca del Simulador dinámico del proceso de producción de azucar", None))
        self.Dynamic_sim_tittle.setText(_translate("Dialog", "SIMULADOR DINÁMICO DEL PROCESO DE PRODUCCIÓN DE AZÚCAR ", None))
        self.Cenicana_tittle.setText(_translate("Dialog", "Centro de Investigación de la Caña de Ázucar de Colombia ", None))
        self.cenican_tittle_2.setText(_translate("Dialog", "Cenicaña", None))
        self.Version_label.setText(_translate("Dialog", "VERSIÓN: 1.0.0", None))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Desarrolladores:</span></p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">  Gustavo Adolfo Silva Alarcón</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">  Jose David Tascón Vidarte</span></p></body></html>", None))

