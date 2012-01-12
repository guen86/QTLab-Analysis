from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import View, Item, Group
from enthought.chaco.api import Plot, ArrayPlotData, jet, PlotAxis, LinearMapper, ColorBar, HPlotContainer, ColormappedSelectionOverlay
from enthought.chaco.tools.api import LineInspector, PanTool, RangeSelection, RangeSelectionOverlay, ZoomTool
from enthought.enable.component_editor import ComponentEditor
from enthought.chaco import default_colormaps
from numpy import *
from numpy.random import random
from enthought.traits.ui.menu import Action, CloseAction, Menu, MenuBar, NoButtons, Separator

class LinePlot(HasTraits):
    plot = Instance(Plot)
    traits_view = View(
        Item('plot',editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="QTLab Analysis Plot")

    def __init__(self, title, xtitle, x, ytitle, y, type="line", color="blue"):
        super(LinePlot, self).__init__()
        plotdata = ArrayPlotData(x=x, y=y)
        self.plotdata = plotdata
        plot = Plot(self.plotdata)
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

class ImagePlot(HasTraits):
    #plot = Instance(Plot)
    # traits_view = View(
        # Group(Item('container',
                    # editor=ComponentEditor(),
                    # show_label=False)),
        # width=500, height=500,
        # buttons=NoButtons,
        # resizable=True, title="QTLab Analysis Plot")
        # Item('plot', editor=ComponentEditor(), show_label=False),
        # width=500, height=500, resizable=True, title="QTLab Analysis Plot")
    # def __init__(self, title, xtitle, x, ytitle, y, z):
        # super(ImagePlot, self).__init__()
        # self.create_plot(title, xtitle, x, ytitle, y, z)

    def _create_window(self, title, xtitle, x, ytitle, y, z):
        '''
        - Left-drag pans the plot.
    	- Mousewheel up and down zooms the plot in and out.
        - Pressing "z" brings up the Zoom Box, and you can click-drag a rectangular
        region to zoom.  If you use a sequence of zoom boxes, pressing alt-left-arrow
        and alt-right-arrow moves you forwards and backwards through the "zoom
        history".
        '''
        self._plotname = title
        # Create window
        self.data = ArrayPlotData()
        self.plot = Plot(self.data)      
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
        # selection = ColormappedSelectionOverlay(cmap_renderer, fade_alpha=0.35, selection_type="mask")
        # cmap_renderer.overlays.append(selection)
        
        # Create a container to position the plot and the colorbar side-by-side
        container = HPlotContainer(use_backbuffer = True)
        container.add(self.plot)
        container.add(self._colorbar)
        self.container = container

        # Return a window containing our plot container
        return Window(self, -1, component=container)

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
        
        # self.plot.plot(("x", "y", "z"),
                    # type = "img_plot",
                    # name = self._plotname,
                    # color_mapper = jet,
                    # marker = "square",
                    # fill_alpha = 0.5,
                    # marker_size = 6,
                    # outline_color = "black",
                    # border_visible = True,
                    # bgcolor = "white")

    def _create_colorbar(self):
        cmap = self.plot.color_mapper
        self._colorbar = ColorBar(index_mapper=LinearMapper(range=cmap.range),
                                  color_mapper=cmap,
                                  orientation='v',
                                  resizable='v',
                                  width=30,
                                  padding=30)
        
        # self._colorbar.tools.append(RangeSelection(component=self._colorbar))
        # self._colorbar.overlays.append(RangeSelectionOverlay(component=self._colorbar,
                                                        # border_color="white",
                                                        # alpha=0.8,
                                                        # fill_color="lightgray"))
        # self.colorbar_axis = PlotAxis(self._colorbar)
        # self._colorbar.underlays.append(self.colorbar_axis)

if __name__ == "__main__":
    ImagePlot().configure_traits()