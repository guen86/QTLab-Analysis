# main_window.py
# Main window for analysis client

import gtk
import sys
from gettext import gettext as _L
import logging

import plotting

import lib.gui as gui
from lib.gui import dropdowns, qtwindow, stopbutton, orderedbox

import qtclient as qt
from analyse_general import *

# Plot
# Load matplotlib and select the GTK Agg back-end
import matplotlib as mpl
mpl.use('gtkagg')

# Load pyplot wrappers and set interactive mode on
import matplotlib.pyplot as plt

class MainWindow:

    def __init__(self):
        '''
        Initialization of main window
        '''
        self._plottype = 'none'
        
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        # Set title
        self.window.set_title("QTLab Analysis")
        
        # Handler for delete_event
        self.window.connect("delete_event", self.delete_event)
        
        # Border for the window
        self.window.set_border_width(10)
        
        # Buttons
        self.plot2d_button = gtk.Button("Plot XY")
        self.plot2d_button.connect("clicked", self.plot2d_cb)
        
        self.plot3d_button = gtk.Button("Plot XYZ")
        self.plot3d_button.connect("clicked", self.plot3d_cb)
        
        # Dropdowns
        self._data_dropdown = dropdowns.NamedListDropdown(qt.data)
        self._data_dropdown.connect('changed', self._data_dropdown_changed_cb)
        
        self._colnames_dropdown_x = dropdowns.StringListDropdown([])
        self._colnames_dropdown_y = dropdowns.StringListDropdown([])
        self._colnames_dropdown_z = dropdowns.StringListDropdown([])
        
        # Checkboxes
        self._hold_check = gtk.CheckButton('Hold on')
        self._hold_check.set_active(False)
        
        self._newfig_check = gtk.CheckButton('New figure')
        self._newfig_check.set_active(False)
        self._nfig = 1
        
        self._liveplot_check = gtk.CheckButton('Live plot')
        self._liveplot_check.set_active(False)
        self._liveplot_check.connect("clicked", self._liveplot_cb)
        self._hid = 0 # Proxy connect hid
        
        # Pack vbox
        self.vbox = gui.pack_vbox([
            gui.pack_hbox([
                gtk.Label(_L('Choose data: ')),
                self._data_dropdown], True, True),
            gui.pack_hbox([
                gtk.Label(_L('X: ')),
                self._colnames_dropdown_x], True, True),
            gui.pack_hbox([
                gtk.Label(_L('Y: ')),
                self._colnames_dropdown_y], True, True),
            gui.pack_hbox([
                gtk.Label(_L('Z: ')),
                self._colnames_dropdown_z], True, True),
            self.plot2d_button,
            self.plot3d_button,
            gui.pack_hbox([self._hold_check,
            self._newfig_check,
            self._liveplot_check], True,True),
        ], False, False)
        self.window.add(self.vbox)
        
        self._data_dropdown.show()
        self._colnames_dropdown_x.show()
        self._colnames_dropdown_y.show()
        self._colnames_dropdown_z.show()
        self.plot2d_button.show()
        self.plot3d_button.show()
        self.vbox.show_all()
        self.window.show()

    def search_array(self, elem, arr):
        '''
        Search array for element 'elem'.
        Return indices.
        '''
        arr_ind = arange(0, len(arr))
        found_indices = arr_ind[arr == elem]
        return found_indices
    
    def get_3d_data_coord(self, data_col):
        '''
        From the raw data column, get a vector of the values
        Coordinate
        '''
        col_indices = self.search_array(data_col[0], data_col)
        if len(col_indices)<=1:
            nextindex = -1
            coord_vec = data_col
        else:
            nextindex = col_indices[1]
        if nextindex == 1:
            num_sweep = sum((array(data_col)==data_col[0])*1)
            coord_vec = array([])
            for n in arange(0,len(data_col),num_sweep):
                coord_vec = append(coord_vec, data_col[n])
        if nextindex > 1:
            coord_vec = data_col[0:nextindex]
        return coord_vec
        
    def plot2d_cb(self, *args):
        '''
        Plot 2D graph
        '''
        # Plottype for live plot
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
        
        # Plot
        self.create_figure(colname_x, colname_y, data_obj.get_name())
        plt.plot(x,y)
        
    def plot3d_cb(self, *args):
        '''
        Plot 3D graph
        '''
        # Plottype for live plot
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
            x = self.get_3d_data_coord(data[:,col_x])
            y = self.get_3d_data_coord(data[:,col_y])
            z = data[:,col_z]
            if len(z)%len(x) != 0:
                z = append(z, zeros(len(x)*len(y) - len(z)))
            z = reshape(z, (len(y), len(x)))
        else:
            raise ValueError('Plot error: X should be coordinate, Y should be coordinate and Z should be value!')
        
        # Plot
        self.create_figure(colname_x, colname_y, data_obj.get_name())
        plt.pcolor(x,y,z)
    
    def update_plot(self, *args):
        '''
        Update live plot
        '''
        print 'New data point added'
        if self._plottype == '3d':
            self.plot3d_cb()
        elif self._plottype == '2d':
            self.plot2d_cb()
        
    def create_figure(self, xlabel, ylabel, title):
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
    
    def live_plotting(self, func):
        '''
        Do live plotting on current data object if checkbox is set to 'on'
        '''
        #Live plotting
        
    
    def delete_event(self, widget, event):
        gtk.main_quit()
        return False
        
    def _data_dropdown_changed_cb(self, widget):
        '''
        Callback for data dropdown list
        '''
        self._liveplot_check.set_active(False)
        if self._hid != 0:
            self._data_obj.disconnect(self._hid)
        self._data_obj = self._data_dropdown.get_item()
        dims = self._data_obj.get_dimensions()
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

    def main():
        gtk.main()
    
    if __name__ == "__main__":
        mainwindow = MainWindow()
        main()