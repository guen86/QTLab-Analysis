# Input window class.
# For a pop-up window with variable input fields.
#
# Author: Guenevere Prawiroatmodjo <guen@vvtp.tudelft.nl>
#

import sys
from PyQt4 import QtCore, QtGui
QtCore.pyqtRemoveInputHook()
import inputwin_ui
reload(inputwin_ui)
from inputwin_ui import Ui_InputWin

import qtclient as qt
from data import Data
import os
import types
import traceback
from numpy import *

from lib.config import get_config
config = get_config()

class InputWin(QtGui.QDialog, Ui_InputWin):
    def __init__(self, parameters, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self, parameters)
        self.parameters = parameters
        self.values = []

    def getParameters(self):
        return self.values

    def accept(self):
        for n in arange(len(self.parameters)):
            self.values.append(getattr(self, 'lineEdit' + str(n)).text())
        QtGui.QDialog.accept(self)

    def reject(self):
        self.parameters = []
        QtGui.QDialog.reject(self)