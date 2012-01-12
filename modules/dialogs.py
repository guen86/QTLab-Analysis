import sys
from PyQt4 import QtGui


class InputField(QtGui.QWidget):
    
    def __init__(self, inputtext):
        super(InputField, self).__init__()
        self._inputtext = inputtext
        self._value = None
        self.initUI()
        
    def initUI(self):      

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            self._inputtext)
        
        if ok:
            self._value = str(text)
        
def main():
    
    # app = QtGui.QApplication(sys.argv)
    ex = InputField()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()