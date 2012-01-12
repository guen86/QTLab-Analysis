# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\qtlabanalysis\source\designer\plotwin.ui'
#
# Created: Tue Jan 10 14:56:54 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_QTLabAnalysis(object):
    def setupUi(self, QTLabAnalysis):
        QTLabAnalysis.setObjectName(_fromUtf8("QTLabAnalysis"))
        QTLabAnalysis.resize(513, 99)
        QTLabAnalysis.setWindowTitle(QtGui.QApplication.translate("QTLabAnalysis", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.choose_data = QtGui.QComboBox(QTLabAnalysis)
        self.choose_data.setGeometry(QtCore.QRect(90, 10, 191, 20))
        self.choose_data.setObjectName(_fromUtf8("choose_data"))
        self.x_combobox = QtGui.QComboBox(QTLabAnalysis)
        self.x_combobox.setGeometry(QtCore.QRect(30, 70, 111, 20))
        self.x_combobox.setObjectName(_fromUtf8("x_combobox"))
        self.x_label = QtGui.QLabel(QTLabAnalysis)
        self.x_label.setGeometry(QtCore.QRect(10, 70, 16, 16))
        self.x_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "x:", None, QtGui.QApplication.UnicodeUTF8))
        self.x_label.setObjectName(_fromUtf8("x_label"))
        self.y_label = QtGui.QLabel(QTLabAnalysis)
        self.y_label.setGeometry(QtCore.QRect(150, 70, 16, 16))
        self.y_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "y:", None, QtGui.QApplication.UnicodeUTF8))
        self.y_label.setObjectName(_fromUtf8("y_label"))
        self.y_combobox = QtGui.QComboBox(QTLabAnalysis)
        self.y_combobox.setGeometry(QtCore.QRect(170, 70, 111, 20))
        self.y_combobox.setObjectName(_fromUtf8("y_combobox"))
        self.z_combobox = QtGui.QComboBox(QTLabAnalysis)
        self.z_combobox.setGeometry(QtCore.QRect(310, 70, 111, 20))
        self.z_combobox.setObjectName(_fromUtf8("z_combobox"))
        self.z_label = QtGui.QLabel(QTLabAnalysis)
        self.z_label.setGeometry(QtCore.QRect(290, 70, 16, 16))
        self.z_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "z:", None, QtGui.QApplication.UnicodeUTF8))
        self.z_label.setObjectName(_fromUtf8("z_label"))
        self.choose_data_label = QtGui.QLabel(QTLabAnalysis)
        self.choose_data_label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.choose_data_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "Choose data:", None, QtGui.QApplication.UnicodeUTF8))
        self.choose_data_label.setObjectName(_fromUtf8("choose_data_label"))
        self.browse_data_button = QtGui.QPushButton(QTLabAnalysis)
        self.browse_data_button.setGeometry(QtCore.QRect(290, 10, 75, 23))
        self.browse_data_button.setText(QtGui.QApplication.translate("QTLabAnalysis", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_data_button.setObjectName(_fromUtf8("browse_data_button"))
        self.plot_button = QtGui.QPushButton(QTLabAnalysis)
        self.plot_button.setGeometry(QtCore.QRect(430, 70, 75, 23))
        self.plot_button.setText(QtGui.QApplication.translate("QTLabAnalysis", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_button.setObjectName(_fromUtf8("plot_button"))
        self.newfig_checkBox = QtGui.QCheckBox(QTLabAnalysis)
        self.newfig_checkBox.setGeometry(QtCore.QRect(430, 50, 70, 17))
        self.newfig_checkBox.setText(QtGui.QApplication.translate("QTLabAnalysis", "Live plot", None, QtGui.QApplication.UnicodeUTF8))
        self.newfig_checkBox.setObjectName(_fromUtf8("newfig_checkBox"))
        self.browse_analysis_button = QtGui.QPushButton(QTLabAnalysis)
        self.browse_analysis_button.setGeometry(QtCore.QRect(290, 40, 75, 23))
        self.browse_analysis_button.setText(QtGui.QApplication.translate("QTLabAnalysis", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_analysis_button.setObjectName(_fromUtf8("browse_analysis_button"))
        self.choose_data_label_2 = QtGui.QLabel(QTLabAnalysis)
        self.choose_data_label_2.setGeometry(QtCore.QRect(10, 40, 81, 16))
        self.choose_data_label_2.setText(QtGui.QApplication.translate("QTLabAnalysis", "Analysis script:", None, QtGui.QApplication.UnicodeUTF8))
        self.choose_data_label_2.setObjectName(_fromUtf8("choose_data_label_2"))
        self.choose_data_2 = QtGui.QComboBox(QTLabAnalysis)
        self.choose_data_2.setGeometry(QtCore.QRect(90, 40, 191, 20))
        self.choose_data_2.setObjectName(_fromUtf8("choose_data_2"))
        self.holdon_checkBox = QtGui.QCheckBox(QTLabAnalysis)
        self.holdon_checkBox.setGeometry(QtCore.QRect(430, 30, 70, 17))
        self.holdon_checkBox.setText(QtGui.QApplication.translate("QTLabAnalysis", "Hold on", None, QtGui.QApplication.UnicodeUTF8))
        self.holdon_checkBox.setObjectName(_fromUtf8("holdon_checkBox"))

        self.retranslateUi(QTLabAnalysis)
        QtCore.QMetaObject.connectSlotsByName(QTLabAnalysis)

    def retranslateUi(self, QTLabAnalysis):
        pass

