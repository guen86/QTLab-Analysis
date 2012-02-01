from modules.analyse_general import *
from modules.dialogs import InputField
from general import plot_types
from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import View, Item
from enthought.chaco.api import Plot, ArrayPlotData, jet, PlotAxis, LinearMapper, ColorBar, HPlotContainer
from enthought.chaco.tools.api import RangeSelection, RangeSelectionOverlay
from enthought.enable.component_editor import ComponentEditor
from numpy import linspace, sin, exp, meshgrid, zeros
reload(plot_types)
from PyQt4 import QtGui
import inputwin
reload(inputwin)
from inputwin import InputWin

def get_input_params(plotwindow, parameters):
    '''
    Get input parameters
    Input:
        parameters: [(str)] String vector with names of input parameters
    '''
    inputwin = InputWin(parameters)
    if inputwin.exec_():
        return inputwin.getParameters()      

def plot2d(plotwindow, name, x, y, colname_x, colname_y):
    '''
    Plot 2D
    '''
    if(plotwindow._holdon == False):
        # Plot new figure
        plotwindow.lineplot = plot_types.LinePlot(plotwindow, name, colname_x, x, colname_y, y, "line", "blue")
    else:
        # Hold on
        if (hasattr(plotwindow, 'lineplot')) & (plotwindow.lineplot.plot.window != None):
            plotwindow.lineplot.plot_hold_on(x, y, "line")
        else:
            # Plot new figure
            plotwindow.lineplot = plot_types.LinePlot(plotwindow, name, colname_x, x, colname_y, y, "line", "blue")

def plot3d(plotwindow, name, x, y, z, colname_x, colname_y, colname_z):
    '''
    Plot 3D
    '''
    # Get the data in the proper dimensions
    x = get_3d_data_coord(x)
    y = get_3d_data_coord(y)
    if len(z)%len(x) != 0:
        z = append(z, zeros(len(x)*len(y) - len(z)))
    z = reshape(z, (len(y), len(x)))
    plotwindow.imageplot = plot_types.ImagePlot(plotwindow, name, x, y, z, colname_x, colname_y, colname_z)

def plot_waterfall(plotwindow, name, x, y, z, colname_x, colname_y, colname_z):
    '''
    Plot 2D waterfall
    '''
    # Get the data in the proper dimensions
    x = get_3d_data_coord(x)
    y = get_3d_data_coord(y)
    if len(z)%len(x) != 0:
        z = append(z, zeros(len(x)*len(y) - len(z)))
    z = reshape(z, (len(y), len(x)))
    # Plot new figure
    plotwindow.lineplot = plot_types.LinePlot(name, colname_x, x, colname_z, z[0], "line", "blue")

def new_data_point(plotwindow):
    '''
    New data point
    '''
    data = plotwindow._data_obj.get_data()
    dims = plotwindow._data_obj.get_dimensions()
    
    # Get cols
    col_x = plotwindow.ui.x_combobox.currentIndex()
    col_y = plotwindow.ui.y_combobox.currentIndex()
    col_z = plotwindow.ui.z_combobox.currentIndex()
    
    # Get data
    x = data[:,col_x]
    y = data[:,col_y]
    z = data[:,col_z]
    
    # Update plot
    if (dims[col_x]['type'] == 'coordinate') & (dims[col_y]['type'] == 'value'):
        # 2D Plot
        plotwindow.lineplot.update_plot(x,y)
    elif (dims[col_x]['type'] == 'coordinate') & (dims[col_y]['type'] == 'coordinate') & (dims[col_z]['type'] == 'value'):
        # 3D Plot
        # Reshape data
        x = get_3d_data_coord(x)
        y = get_3d_data_coord(y)
        if len(z)%len(x) != 0:
            z = append(z, zeros(len(x)*len(y) - len(z)))
        z = reshape(z, (len(y), len(x)))
        plotwindow.imageplot.update_plot(x,y,z)
    
def run(plotwindow):
    '''
    Run the analysis code
    '''
    parameters = ['test1', 'test2', 'test3', 'test4', 'test1', 'test2', 'test3', 'test4', 'test1', 'test2', 'test3', 'test4', 'test1', 'test2', 'test3', 'test4', 'test1', 'test2', 'test3', 'test4']
    print get_input_params(plotwindow, parameters)
    
    # Get x, y cols
    colname_x = str(plotwindow.ui.x_combobox.currentText())
    colname_y = str(plotwindow.ui.y_combobox.currentText())
    colname_z = str(plotwindow.ui.z_combobox.currentText())
    col_x = plotwindow.ui.x_combobox.currentIndex()
    col_y = plotwindow.ui.y_combobox.currentIndex()
    col_z = plotwindow.ui.z_combobox.currentIndex()
    # Check if the columns are selected
    if (col_x > -1) & (col_y > -1):
        data = plotwindow._data_obj.get_data()
        dims = plotwindow._data_obj.get_dimensions()
        name = plotwindow._data_obj.get_name()
        if (dims[col_x]['type'] == 'coordinate') & (dims[col_y]['type'] == 'value'):
            # Plot 2d if x and y are correctly chosen
            x = data[:,col_x]
            y = data[:,col_y]
            plot2d(plotwindow, name, x, y, colname_x, colname_y)
        elif (dims[col_x]['type'] == 'coordinate') & (dims[col_y]['type'] == 'coordinate') & (dims[col_z]['type'] == 'value'):
            # Plot 3d if x, y and z are correctly chosen
            x = data[:,col_x]
            y = data[:,col_y]
            z = data[:,col_z]
            plot3d(plotwindow, name, x, y, z, colname_x, colname_y, colname_z)
        else:
            print 'Plot error: Please choose X and Y for 2D plot or X, Y and Z for 3D plot.'
    else:
        print 'Plot error: Please choose X and Y for 2D plot or X, Y and Z for 3D plot.'