# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotwin.ui'
#
# Created: Wed Dec 07 16:18:32 2011
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
        QTLabAnalysis.resize(513, 105)
        QTLabAnalysis.setWindowTitle(QtGui.QApplication.translate("QTLabAnalysis", "QTLabAnalysis", None, QtGui.QApplication.UnicodeUTF8))
        # self.plot3d = ColorPlot(QTLabAnalysis)
        # self.plot3d.setGeometry(QtCore.QRect(9, 9, 495, 441))
        # self.plot3d.setObjectName(_fromUtf8("plot3d"))
        # self.plot2d = TracePlot(QTLabAnalysis)
        # self.plot2d.setGeometry(QtCore.QRect(9, 9, 495, 441))
        # self.plot2d.setObjectName(_fromUtf8("plot2d"))
        # self.plot.setFrameShape(QtGui.QFrame.StyledPanel)
        # self.plot.setFrameShadow(QtGui.QFrame.Raised)
        self.analysis_list = []
        
        ##############
        # COMBOBOXES #
        ##############
        self.x_combobox = QtGui.QComboBox(QTLabAnalysis)
        self.x_combobox.setGeometry(QtCore.QRect(30, 80, 111, 20))
        self.x_combobox.setObjectName(_fromUtf8("x_combobox"))
        
        self.y_combobox = QtGui.QComboBox(QTLabAnalysis)
        self.y_combobox.setGeometry(QtCore.QRect(170, 80, 111, 20))
        self.y_combobox.setObjectName(_fromUtf8("y_combobox"))
        
        self.z_combobox = QtGui.QComboBox(QTLabAnalysis)
        self.z_combobox.setGeometry(QtCore.QRect(310, 80, 111, 20))
        self.z_combobox.setObjectName(_fromUtf8("z_combobox"))
        
        self.choose_data = QtGui.QComboBox(QTLabAnalysis)
        self.choose_data.setGeometry(QtCore.QRect(90, 20, 191, 20))
        self.choose_data.setObjectName(_fromUtf8("choose_data"))
        
        self.choose_analysis = QtGui.QComboBox(QTLabAnalysis)
        self.choose_analysis.setGeometry(QtCore.QRect(90, 50, 191, 20))
        self.choose_analysis.setObjectName(_fromUtf8("choose_analysis"))
        
        ###########
        # BUTTONS #
        ###########
        self.browse_data_button = QtGui.QPushButton(QTLabAnalysis)
        self.browse_data_button.setGeometry(QtCore.QRect(290, 20, 75, 23))
        self.browse_data_button.setText(QtGui.QApplication.translate("QTLabAnalysis", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_data_button.setObjectName(_fromUtf8("browse_data_button"))
        
        self.run_button = QtGui.QPushButton(QTLabAnalysis)
        self.run_button.setGeometry(QtCore.QRect(430, 80, 75, 23))
        self.run_button.setText(QtGui.QApplication.translate("QTLabAnalysis", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.run_button.setObjectName(_fromUtf8("run_button"))
        
        self.browse_analysis_button = QtGui.QPushButton(QTLabAnalysis)
        self.browse_analysis_button.setGeometry(QtCore.QRect(290, 50, 75, 23))
        self.browse_analysis_button.setText(QtGui.QApplication.translate("QTLabAnalysis", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_analysis_button.setObjectName(_fromUtf8("browse_analysis_button"))

        ##############
        # CHECKBOXES #
        ##############
        self.live_checkBox = QtGui.QCheckBox(QTLabAnalysis)
        self.live_checkBox.setGeometry(QtCore.QRect(430, 60, 70, 17))
        self.live_checkBox.setText(QtGui.QApplication.translate("QTLabAnalysis", "Live plot", None, QtGui.QApplication.UnicodeUTF8))
        self.live_checkBox.setObjectName(_fromUtf8("live_checkBox"))
        
        self.holdon_checkBox = QtGui.QCheckBox(QTLabAnalysis)
        self.holdon_checkBox.setGeometry(QtCore.QRect(430, 30, 70, 17))
        self.holdon_checkBox.setText(QtGui.QApplication.translate("QTLabAnalysis", "Hold on", None, QtGui.QApplication.UnicodeUTF8))
        self.holdon_checkBox.setObjectName(_fromUtf8("holdon_checkBox"))
        
        ##########
        # LABELS #
        ##########
        self.x_label = QtGui.QLabel(QTLabAnalysis)
        self.x_label.setGeometry(QtCore.QRect(10, 80, 16, 16))
        self.x_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "x:", None, QtGui.QApplication.UnicodeUTF8))
        self.x_label.setObjectName(_fromUtf8("x_label"))
        
        self.y_label = QtGui.QLabel(QTLabAnalysis)
        self.y_label.setGeometry(QtCore.QRect(150, 80, 16, 16))
        self.y_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "y:", None, QtGui.QApplication.UnicodeUTF8))
        self.y_label.setObjectName(_fromUtf8("y_label"))
        
        self.z_label = QtGui.QLabel(QTLabAnalysis)
        self.z_label.setGeometry(QtCore.QRect(290, 80, 16, 16))
        self.z_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "z:", None, QtGui.QApplication.UnicodeUTF8))
        self.z_label.setObjectName(_fromUtf8("z_label"))
        
        self.choose_data_label = QtGui.QLabel(QTLabAnalysis)
        self.choose_data_label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.choose_data_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "Choose data:", None, QtGui.QApplication.UnicodeUTF8))
        self.choose_data_label.setObjectName(_fromUtf8("choose_data_label"))
        
        self.choose_analysis_label = QtGui.QLabel(QTLabAnalysis)
        self.choose_analysis_label.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.choose_analysis_label.setText(QtGui.QApplication.translate("QTLabAnalysis", "Analysis script:", None, QtGui.QApplication.UnicodeUTF8))
        self.choose_analysis_label.setObjectName(_fromUtf8("choose_analysis_label"))
        
        #############
        # CALLBACKS #
        #############
        
        self.holdon_checkBox.stateChanged.connect(QTLabAnalysis.holdon_cb)
        self.live_checkBox.stateChanged.connect(QTLabAnalysis.live_cb)

        self.retranslateUi(QTLabAnalysis)
        QtCore.QObject.connect(self.browse_data_button, QtCore.SIGNAL("clicked()"), QTLabAnalysis.browse_data_file)
        QtCore.QObject.connect(self.browse_analysis_button, QtCore.SIGNAL("clicked()"), QTLabAnalysis.browse_analysis_file)
        QtCore.QObject.connect(self.run_button, QtCore.SIGNAL("clicked()"), QTLabAnalysis.run)
        QtCore.QObject.connect(self.choose_data, QtCore.SIGNAL("activated(int)"), QTLabAnalysis.data_dropdown_changed)
        QtCore.QObject.connect(self.choose_data, QtCore.SIGNAL("highlighted(int)"), QTLabAnalysis.data_refresh)
        QtCore.QObject.connect(self.choose_analysis, QtCore.SIGNAL("activated(int)"), QTLabAnalysis.analysis_dropdown_changed)
        QtCore.QMetaObject.connectSlotsByName(QTLabAnalysis)

    def retranslateUi(self, QTLabAnalysis):
        pass
