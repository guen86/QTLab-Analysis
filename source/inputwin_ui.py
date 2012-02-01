# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\QTLab-Analysis\source\designer\inputwin.ui'
#
# Created: Mon Jan 30 13:31:43 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InputWin(object):
    def setupUi(self, Dialog, parameters):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Input parameters", "Input parameters", None, QtGui.QApplication.UnicodeUTF8))
        
        n = 0
        for parameter in parameters:
            setattr(self, 'lineEdit' + str(n), QtGui.QLineEdit(Dialog))
            getattr(self, 'lineEdit' + str(n)).setGeometry(QtCore.QRect(100, 20 + n*30, 100, 20))
            getattr(self, 'lineEdit' + str(n)).setObjectName(_fromUtf8("lineEdit"))
            
            setattr(self, 'label' + str(n), QtGui.QLabel(Dialog))
            getattr(self, 'label' + str(n)).setGeometry(QtCore.QRect(20, 20 + n*30, 60, 20))
            getattr(self, 'label' + str(n)).setText(QtGui.QApplication.translate("Input parameters", parameter, None, QtGui.QApplication.UnicodeUTF8))
            getattr(self, 'label' + str(n)).setObjectName(_fromUtf8(parameters[0]))
            
            n = n + 1

            
        Dialog.resize(230, 100 + n * 30)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 40 + n * 30, 160, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass