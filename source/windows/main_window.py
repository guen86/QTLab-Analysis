# main_window.py
# Main window for analysis client

import gtk
import sys
from gettext import gettext as _L
import logging

import lib.gui as gui
from lib.gui import dropdowns, qtwindow, stopbutton, orderedbox
from lib import databrowser

import qtclient as qt
from modules.analyse_general import *

import types
import time

# Load matplotlib and select the GTK Agg back-end
import matplotlib as mpl
mpl.use('gtkagg')

# Load pyplot wrappers and set interactive mode on
import matplotlib.pyplot as plt
from pylab import *

class MainWindow:
    def __init__(self):
        '''
        Initialization of main window
        '''
        # Default parameters
        self._nfig = 1
        self._hid = 0 # Proxy connect hid
        self._plottype = 'none'
        self._data_obj = None
        self._operations = ['None', 'Plot 2D', 'Plot 3D', 'Plot 2D Difference', 'Plot 3D - horizontal offset', 'Plot 3D - vertical offset', 'Plot 3D - horizontal difference', 'Plot 3D - vertical difference', 'Close all']
        self._cid = 0 # Connect ID for crosshair
        self._xdata = None
        self._ydata = None
        self._x = None
        self._y = None
        self._z = None
        self._offset = None
        
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        # Set title
        self.window.set_title("QTLab Analysis")
        
        # Handler for delete_event
        self.window.connect("delete_event", self._delete_event)
        
        # Border for the window
        self.window.set_border_width(10)
        
        # Button
        # self.plot2d_button = gtk.Button("Plot XY")
        # self.plot2d_button.connect("clicked", self._plot2d_cb)
        
        # self.plot3d_button = gtk.Button("Plot XYZ")
        # self.plot3d_button.connect("clicked", self._plot3d_cb)
        
        self.go_button = gtk.Button("Go")
        self.go_button.connect("clicked", self._go_cb)
        
        self._dir_entry = gtk.Entry()
        self._dir_entry.connect('activate', self._dir_activate_cb)
        
        self._dir_button = gtk.Button(_L('Browse'))
        self._dir_button.connect('clicked', self._dir_button_clicked_cb)
        
        self._dir_hbox = gui.pack_hbox(
                (gtk.Label('Choose filename (*.dat): '), self._dir_entry, self._dir_button),
                True, True)
        
        
        # Dropdowns
        self._data_dropdown = dropdowns.NamedListDropdown(qt.data)
        self._data_dropdown.connect('changed', self._data_dropdown_changed_cb)
        
        self._colnames_dropdown_x = dropdowns.StringListDropdown([])
        self._colnames_dropdown_y = dropdowns.StringListDropdown([])
        self._colnames_dropdown_z = dropdowns.StringListDropdown([])        
        self._operations_dropdown = dropdowns.StringListDropdown(self._operations)
        self._operations_dropdown.connect('changed', self._operations_dropdown_changed_cb)
        
        # Checkboxes
        self._hold_check = gtk.CheckButton('Hold on')
        self._hold_check.set_active(False)
        
        self._newfig_check = gtk.CheckButton('New figure')
        self._newfig_check.set_active(False)
        
        self._liveplot_check = gtk.CheckButton('Live plot')
        self._liveplot_check.set_active(False)
        self._liveplot_check.connect("clicked", self._liveplot_cb)
        
        # Pack vbox
        self.vbox = gui.pack_vbox([
            gui.pack_hbox([
                gtk.Label(_L('Choose data: ')),
                self._data_dropdown], True, True),
            self._dir_hbox,
            gui.pack_hbox([
                gtk.Label(_L('X: ')),
                self._colnames_dropdown_x], True, True),
            gui.pack_hbox([
                gtk.Label(_L('Y: ')),
                self._colnames_dropdown_y], True, True),
            gui.pack_hbox([
                gtk.Label(_L('Z: ')),
                self._colnames_dropdown_z], True, True),
            gui.pack_hbox([
                gtk.Label(_L('Operations: ')),
                self._operations_dropdown], True, True),
            self.go_button,
            gui.pack_hbox([self._hold_check,
            self._newfig_check,
            self._liveplot_check], True,True),
        ], False, False)
        self.window.add(self.vbox)
        
        self._data_dropdown.show()
        self._colnames_dropdown_x.show()
        self._colnames_dropdown_y.show()
        self._colnames_dropdown_z.show()
        self._operations_dropdown.show()
        self.go_button.show()
        self.vbox.show_all()
        self.window.show()

    #############
    # Functions #
    #############
    
    def on_info(self, message):
        md = gtk.MessageDialog(None, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()
    
    def _create_figure(self, xlabel, ylabel, title):
        '''
        Create figure, set x and y label and title
        '''        
        plt.ion()
        if self._newfig_check.get_active():
            self._nfig = self._nfig + 1
        plt.figure(self._nfig)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()
        plt.hold(self._hold_check.get_active())
    
    def update_plot(self, *args):
        '''
        Update plot
        '''
        print "New data point added."
        if self._plottype == '2d':
            self._plot2d_cb()
        if self._plottype == '3d':
            self._plot3d_cb()
    
    def _delete_event(self, widget, event):
        gtk.main_quit()
        return False
    
    ###################
    # Plot operations #
    ###################
    
    def _plot2d(self, difference = False):
        '''
        Plot 2D graph
        '''
        self._plottype = '2d'
        
        # Get x, y cols
        colname_x = self._colnames_dropdown_x.get_item()
        colname_y = self._colnames_dropdown_y.get_item()
        col_x = self._colnames_dropdown_x.get_active()
        col_y = self._colnames_dropdown_y.get_active()
        col_z = self._colnames_dropdown_z.get_active()
        
        # Get data
        data_obj = self._data_obj
        data = data_obj.get_data()
        dims = data_obj.get_dimensions()
        if (dims[col_x]['type'] == 'coordinate') & (dims[col_y]['type'] == 'value'):
            x = data[:,col_x]
            y = data[:,col_y]
        elif (dims[col_x]['type'] == 'coordinate') & (dims[col_z]['type'] == 'value'):
            # If z is a value, take that one to plot
            x = data[:,col_x]
            y = data[:,col_z]
            colname_y = self._colnames_dropdown_z.get_item()
        else:
            raise ValueError('Plot error: X should be coordinate and Y should be value!')
            
        if difference:
            y = smooth_data(y, 3)
            y = smoothListGaussian(y)
            y = absolute(diff(y))
            colname_y = 'Difference of ' + colname_y
        
        # Plot
        self._create_figure(colname_x, colname_y, data_obj.get_name())
        plt.plot(x[range(len(y))],y)
        
    def _plot3d(self, offset = 'none', difference = 'none'):
        '''
        Plot 3D graph
        '''
        self._plottype = '3d'
        
        # Get x, y, z cols
        colname_x = self._colnames_dropdown_x.get_item()
        colname_y = self._colnames_dropdown_y.get_item()
        colname_z = self._colnames_dropdown_z.get_item()
        col_x = self._colnames_dropdown_x.get_active()
        col_y = self._colnames_dropdown_y.get_active()
        col_z = self._colnames_dropdown_z.get_active()
        
        # Get data
        data_obj = self._data_obj
        dims = data_obj.get_dimensions()
        data = data_obj.get_data()
        
        if (dims[col_x]['type'] == 'coordinate') & (dims[col_y]['type'] == 'coordinate') & (dims[col_z]['type'] == 'value'):
            x = get_3d_data_coord(data[:,col_x])
            y = get_3d_data_coord(data[:,col_y])
            z = data[:,col_z]
            if len(z)%len(x) != 0:
                z = append(z, zeros(len(x)*len(y) - len(z)))
            z = reshape(z, (len(y), len(x)))
        else:
            raise ValueError('Plot error: X should be coordinate, Y should be coordinate and Z should be value!')
        
        # Plot
        self._create_figure(colname_x, colname_y, data_obj.get_name())
        pcolor(x,y,z)
        plt.colorbar()
        self._x = x
        self._y = y
        self._z = z
        if (offset ==  'horizontal') | (offset == 'vertical'):
            self._offset = offset
            self._sub_offset()
        show()
        
    def _sub_offset(self):
        '''
        Subtract offset
        '''
        self._cid = connect('button_press_event', self._sub_offset_press_call_first)
    
    #############
    # Callbacks #
    #############
    
    def _sub_offset_press_call_first(self, event, *args):
        '''
        Press call for first point
        '''
        print 'Click first on the left upper and second on the right lower corner of the square from which offset along X will be determined.'
        self._xdata = event.xdata
        self._ydata = event.ydata
        plt.figure(self._nfig)
        plt.hold(True)
        plt.plot(self._xdata, self._ydata, 'ro')
        disconnect(self._cid)
        self._cid = connect('button_press_event', self._sub_offset_press_call_second)
    
    def _sub_offset_press_call_second(self, event, *args):
        '''
        Press call for second point
        '''
        x0 = self._xdata
        y0 = self._ydata
        x1 = event.xdata
        y1 = event.ydata
        self._xdata = None
        self._ydata = None

        plt.figure(self._nfig)
        plt.hold(True)
        plt.plot(x1, y1, 'ro')
        disconnect(self._cid)
        
        xdata = self._x
        ydata = self._y
        zdata = self._z
        zdata_new = zeros((len(ydata), len(xdata)))
        if self._offset == 'horizontal':
            x_index_min = abs(xdata-x0).argmin()
            x_index_max = abs(xdata-x1).argmin()
            for i in arange(0,len(ydata)):
                offset = mean(zdata[i][arange(x_index_min,x_index_max)])
            for j in arange(0,len(xdata)):
                zdata_new[i][j]=zdata[i][j]-offset;
        if self._offset == 'vertical':
            y_index_min = abs(ydata-y0).argmin()
            y_index_max = abs(ydata-y1).argmin()
            for i in arange(0,len(ydata)):
                offset = mean(zdata[arange(y_index_min,y_index_max)][j])
            for j in arange(0,len(xdata)):
                zdata_new[i][j]=zdata[i][j]-offset;
        self._nfig = self._nfig + 1
        plt.figure(self._nfig)
        pcolor(xdata,ydata,zdata_new)
        plt.colorbar()
    
    def _go_cb(self, *args):
        '''
        GO button
        self._operations = ['None', 'Plot 2D', 'Plot 3D', 'Plot 2D Difference', 'Plot 3D - horizontal offset', 'Plot 3D - vertical offset', 'Plot 3D - horizontal difference', 'Plot 3D - vertical difference']
        '''
        # Plot 2D
        if self._operations_dropdown.get_item() == self._operations[1]:
            self._plot2d()
        if self._operations_dropdown.get_item() == self._operations[2]:
            self._plot3d()
        if self._operations_dropdown.get_item() == self._operations[3]:
            self._plot2d(difference = True)
        if self._operations_dropdown.get_item() == self._operations[4]:
            self._plot3d(offset = 'horizontal', difference = 'none')
        if self._operations_dropdown.get_item() == self._operations[5]:
            self._plot3d(offset = 'vertical', difference = 'none')
        if self._operations_dropdown.get_item() == self._operations[4]:
            self._plot3d(offset = 'none', difference = 'horizontal')
        if self._operations_dropdown.get_item() == self._operations[5]:
            self._plot3d(offset = 'none', difference = 'vertical')
        if self._operations_dropdown.get_item() == self._operations[6]:
            plt.close('all')
            self._nfig = 1
    
    def _data_dropdown_changed_cb(self, widget):
        '''
        Callback for data dropdown list
        '''
        self._liveplot_check.set_active(False)
        if self._hid != 0:
            self._data_obj.disconnect(self._hid)
        self._data_obj = self._data_dropdown.get_item()
        if type(self._data_obj) != types.NoneType:
            self._update_fields()
    
    def _operations_dropdown_changed_cb(self, widget):
        '''
        Callback for operation dropdown list
        '''
        # Make Z appear or disappear
        

    def _update_fields(self):
        '''
        Update dropdown menus
        '''
        dims = self._data_obj.get_dimensions()
        vals = self._data_obj.get_values()
        colnames = []
        for dim in dims:
            colnames.append(dim['name'])
            
        self._colnames_dropdown_x.set_items(colnames)
        self._colnames_dropdown_y.set_items(colnames)
        self._colnames_dropdown_z.set_items(colnames)
        
    def _liveplot_cb(self, widget):
        '''
        Callback for liveplot checkbox
        Disconnect when not active
        '''
        # Live plotting
        if self._liveplot_check.get_active():
            if self._hid == 0:
                self._hid = self._data_obj.connect('new-data-point', self.update_plot)
        else:
            if self._hid != 0:
                self._data_obj.disconnect(self._hid)
                self._hid = 0
                
    def _dir_button_clicked_cb(self, sender):
        chooser = gtk.FileChooserDialog(
                title=_L('Select data file'),
                action=gtk.FILE_CHOOSER_ACTION_OPEN,
                buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_current_folder('Q:/')
        ret = chooser.run()
        if ret == gtk.RESPONSE_OK:
            self._dir_entry.set_text(chooser.get_filename())
            self._dir_entry.activate()

        chooser.destroy()

    def _dir_activate_cb(self, sender):
        filepath = sender.get_text()
        self._data_obj = Data(filepath)
        self._update_fields()

    def main():
        gtk.main()
    
    if __name__ == "__main__":
        mainwindow = MainWindow()
        main()
