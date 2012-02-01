from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import View, Item, Group
from enthought.chaco.api import Plot, ArrayPlotData, jet, PlotAxis, LinearMapper, ColorBar, HPlotContainer, ColormappedSelectionOverlay
from enthought.chaco.tools.api import LineInspector, PanTool, RangeSelection, RangeSelectionOverlay, ZoomTool
from enthought.enable.component_editor import ComponentEditor
from enthought.chaco import default_colormaps
from enthought.enable.qt4.image import Window
from numpy import *
from numpy.random import random
from enthought.traits.ui.menu import Action, CloseAction, Menu, MenuBar, NoButtons, Separator, OKCancelButtons
from PyQt4 import QtGui
from enthought.chaco.toolbar_plot import ToolbarPlot 
from chaco.tools.toolbars.plot_toolbar import PlotToolbar

class LinePlot(QtGui.QWidget):
    def __init__(self, parent, title, x, y, xtitle, ytitle, type="line", color="blue"):
        QtGui.QWidget.__init__(self)
        
        # Create the subclass's window
        self.enable_win = self._create_window(title, x, y, xtitle, ytitle, type, color)
        
        layout = QtGui.QVBoxLayout()
        
        layout.setMargin(0)
        layout.addWidget(self.enable_win.control)

        self.setLayout(layout)

        self.resize(650,650)

        self.show()

    def _create_window(self, title, xtitle, x, ytitle, y, type="line", color="blue"):
        self.plotdata = ArrayPlotData(x=x, y=y)
        plot = ToolbarPlot(self.plotdata)
        plot.plot(('x', 'y'), type=type, color=color)
        plot.title = title
        plot.x_axis.title = xtitle
        plot.y_axis.title = ytitle
        self.plot = plot
        self._hid = 0
        self._colors = ['blue', 'red', 'black', 'green', 'magenta', 'yellow']
        
        # Add some tools
        self.plot.tools.append(PanTool(self.plot, constrain_key="shift"))
        self.plot.overlays.append(ZoomTool(component=self.plot, tool_mode="box", always_on=False))
        
        return Window(self, -1, component=plot)
    
    def update_plot(self, x,y):
        '''
        Update plot
        '''
        self.plotdata.set_data('x', x)
        self.plotdata.set_data('y', y)
        self.plot.data = self.plotdata
        self.plot.request_redraw()
    
    def plot_hold_on(self, x, y, type="line"):
        '''
        Plot if hold on
        '''
        self._hid = self._hid + 1
        self.plotdata.set_data('x' + str(self._hid), x)
        self.plotdata.set_data('y' + str(self._hid), y)
        self.plot.plot(('x' + str(self._hid), 'y' + str(self._hid)), type=type, color=self._colors[self._hid%len(self._colors)])
        self.plot.request_redraw()

class ImagePlot(QtGui.QWidget):
    def __init__(self, parent, title, x, y, z, xtitle, ytitle, ztitle):
        QtGui.QWidget.__init__(self)
        
        # Create the subclass's window
        self.enable_win = self._create_window(title, x, y, z, xtitle, ytitle, ztitle)
        
        layout = QtGui.QVBoxLayout()
        
        layout.setMargin(0)
        layout.addWidget(self.enable_win.control)

        self.setLayout(layout)

        self.resize(650,650)

        self.show()

    def _create_window(self, title, x, y, z, xtitle, ytitle, ztitle):
        '''
        - Left-drag pans the plot.
    	- Mousewheel up and down zooms the plot in and out.
        - Pressing "z" brings up the Zoom Box, and you can click-drag a rectangular
        region to zoom.  If you use a sequence of zoom boxes, pressing alt-left-arrow
        and alt-right-arrow moves you forwards and backwards through the "zoom
        history".
        '''
        # Create window
        self._plotname = title
        self.data = ArrayPlotData()
        self.plot = ToolbarPlot(self.data, hiding=False, auto_hide=False)
        self.update_plot(x, y, z)
        self.plot.title = title
        self.plot.x_axis.title = xtitle
        self.plot.y_axis.title = ytitle
        
        cmap_renderer = self.plot.plots[self._plotname][0]
        
        # Create colorbar
        self._create_colorbar()
        self._colorbar.plot = cmap_renderer
        self._colorbar.padding_top = self.plot.padding_top
        self._colorbar.padding_bottom = self.plot.padding_bottom
        
        # Add some tools
        self.plot.tools.append(PanTool(self.plot, constrain_key="shift"))
        self.plot.overlays.append(ZoomTool(component=self.plot, tool_mode="box", always_on=False))
        
        # Create a container to position the plot and the colorbar side-by-side
        container = HPlotContainer(use_backbuffer = True)
        container.add(self.plot)
        container.add(self._colorbar)
        self.container = container

        # Return a window containing our plot container
        return Window(self, -1, component=self.container)

    def update_plot(self, x, y, z):
        self.data.set_data('x', x)
        self.data.set_data('y', y)
        self.data.set_data('z', z)
        
        if self.plot.plots.has_key(self._plotname):
            self.plot.delplot(self._plotname)

        # determine correct bounds
        xstep = (x.max() - x.min())/(len(x)-1)
        ystep = (y.max() - y.min())/(len(y)-1)
        x0, x1 = x.min() - xstep/2, x.max() + xstep/2
        y0, y1 = y.min() - ystep/2, y.max() + ystep/2
        
        self.plot.img_plot('z',
                   name = self._plotname,
                   xbounds = (x0, x1),
                   ybounds = (y0, y1),
                   colormap = jet)

    def _create_colorbar(self):
        cmap = self.plot.color_mapper
        self._colorbar = ColorBar(index_mapper=LinearMapper(range=cmap.range),
                                  color_mapper=cmap,
                                  orientation='v',
                                  resizable='v',
                                  width=30,
                                  padding=30)

if __name__ == "__main__":
    ImagePlot().configure_traits()