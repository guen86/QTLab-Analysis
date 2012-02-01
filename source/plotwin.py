# Plot window class.
# For plotting data and running live analysis scripts.
#
# Author: Guenevere Prawiroatmodjo <guen@vvtp.tudelft.nl>
#

import sys
from PyQt4 import QtCore, QtGui
QtCore.pyqtRemoveInputHook()

from plotwin_ui import Ui_QTLabAnalysis

import qtclient as qt
from data import Data
import os
import types
import traceback

from lib.config import get_config
config = get_config()

class PlotWin(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_QTLabAnalysis()
        self.ui.setupUi(self)
        self.ui.choose_data.addItems(qt.data.get_items())
        self.ui.data_list = qt.data.get_items()
        self._data_obj = None
        self._analysis_mod = None
        self._hid = 0
        self._holdon = False
        self.data_dropdown_changed()
        self._old_colname_y = None
        
        # Connect new data object signal to updating data list
        #namedlist_data = qt.get_remote_proxy('namedlist_data')
        qt.data.connect('item-added', self.update_data_list)
        
        # Load all analysis modules in analysis_modules folder
        dirlist = os.listdir(config['qtlabanalysis_modules'])
        for file in dirlist:
            if (file[-3:] == '.py') & (file.find('__init__')<0):
                filename = file[:-3]
                fname = config['qtlabanalysis_modules'] + '\\' + file
                self.ui.analysis_list.append(fname)
                self.ui.choose_analysis.addItem(filename)
                self.analysis_dropdown_changed()
            # elif(file[-3:] != 'pyc') & (file.find('__init__')<0):
                # subdirlist = os.listdir(config['qtlabanalysis_modules'] + '\\' + file)
                # for subfile in subdirlist:
                    # if (subfile[-3:] == '.py') & (subfile.find('__init__')<0):
                        # filename = subfile[:-3]
                        # fname = config['qtlabanalysis_modules'] + '\\' + file + '\\' + subfile
                        # self.ui.analysis_list.append(fname)
                        # self.ui.choose_analysis.addItem(filename)
                        # self.analysis_dropdown_changed()
        
    def update_data_list(self, *args):
        '''
        Update data list
        '''
        data_list = qt.data.get_items()
        newdata = list(set(data_list)-set(self.ui.data_list))[0]
        self.ui.data_list.append(newdata)
        self.ui.choose_data.addItem(newdata)
        
    def browse_data_file(self):
        '''
        Open a browse window and browse for a data file.
        '''
        fname = QtGui.QFileDialog.getOpenFileName(directory=(config['qtlab_root'] + '\\data'))
        if fname not in self.ui.data_list:
            self.ui.data_list.append(fname)
            index = fname.find('/',30)
            filename = fname[index+1:-4]
            self.ui.choose_data.addItem(filename)
        self.ui.choose_data.setCurrentIndex(self.ui.data_list.index(fname))
        self.data_dropdown_changed()
    
    def browse_analysis_file(self):
        '''
        Open a browse window and browse for analysis file.
        Check if the object doesn't already exist.
        Set the index of the combobox to the added file.
        '''
        fname = str(QtGui.QFileDialog.getOpenFileName(directory=(config['qtlabanalysis_modules'])))
        fname = fname.replace('/','\\')
        fname = fname.lower()
        if fname not in self.ui.analysis_list:
            self.ui.analysis_list.append(fname)
            index = fname.find('\\',20)
            index2 = fname.find('\\',index)
            if(index2>-1):
                index = index2
            filename = fname[index+1:-3]
            self.ui.choose_analysis.addItem(filename)
        self.ui.choose_analysis.setCurrentIndex(self.ui.analysis_list.index(fname))
        self.analysis_dropdown_changed()
    
    def data_refresh(self):
        '''
        Refresh data list
        '''
        qt.data.get_items()
    
    def data_dropdown_changed(self):
        '''
        Callback for data dropdown list change
        First, get the data object from file or from proxy.
        Update x, y and z comboboxes.
        '''
        index = self.ui.choose_data.currentIndex()
        if(index > -1):
            fname = self.ui.data_list[index]
            if(fname.find('.dat') < 0):
                self._data_obj = qt.get_data_proxy(fname)
            else:
                self._data_obj = Data(str(fname))
            if type(self._data_obj) != types.NoneType:
                self.update_fields()

    def analysis_dropdown_changed(self):
        '''
        Callback for analysis dropdown list change
        '''
        index = self.ui.choose_analysis.currentIndex()
        if (index > -1):
            fname = self.ui.analysis_list[index]
            name = fname.replace(config['qtlabanalysis_root'] + '\\','')
            name = name.replace('\\','.')
            name = name.replace('.py','')
            try:
                __import__(name)
                self._analysis_mod = sys.modules[name]
                reload(self._analysis_mod)
            except Exception, e:
                print 'Error with analysis module' + name + 'import: ' + str(e)
    
    def update_fields(self):
        '''
        Update x, y and z
        '''
        dims = self._data_obj.get_dimensions()
        colnames = []
        for dim in dims:
            colnames.append(dim['name'])
        self.ui.x_combobox.clear()
        self.ui.y_combobox.clear()
        self.ui.z_combobox.clear()
        self.ui.x_combobox.addItems(colnames)
        self.ui.y_combobox.addItems(colnames)
        self.ui.z_combobox.addItems(colnames)
        # Automatically set the fields
        coords = self._data_obj.get_coordinates()
        vals = self._data_obj.get_values()
        if len(coords) == 1:
            self.ui.x_combobox.setCurrentIndex(0)
            self.ui.y_combobox.setCurrentIndex(1)
            self.ui.z_combobox.setCurrentIndex(0)
        if len(coords) > 1:
            self.ui.x_combobox.setCurrentIndex(0)
            self.ui.y_combobox.setCurrentIndex(1)
            self.ui.z_combobox.setCurrentIndex(len(coords))

    def live_cb(self, state):
        '''
        Callback for liveplot checkbox
        Disconnect when not active
        '''
        # Live plotting
        if state == QtCore.Qt.Checked:
            print "Liveplot checked"
            if self._hid == 0:
                self._hid = self._data_obj.connect('new-data-point', self.new_data_point)
        else:
            print "Liveplot unchecked"
            if self._hid != 0:
                self._data_obj.disconnect(self._hid)
                self._hid = 0
                
    def holdon_cb(self, state):
        '''
        Callback for hold on checkbox
        '''
        if state == QtCore.Qt.Checked:
            self._holdon = True
        else:
            self._holdon = False
            
    def accept():
        print 'accepted'

    def reject():
        print 'cancelled'
        
    
    def new_data_point(self, *args):
        '''
        New data point added
        '''
        print "New data point added"
        self._analysis_mod.new_data_point(self)

    def run(self):
        '''
        Run analysis
        '''
        if self._analysis_mod != None:
            try:
                self._analysis_mod.run(self)
            except Exception, e:
                traceback.print_exc()
                raise ValueError('Error in the analysis module: ' + str(e))