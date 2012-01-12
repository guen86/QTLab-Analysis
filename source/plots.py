from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import View, Item
from enthought.chaco.api import Plot, ArrayPlotData, jet
from enthought.enable.component_editor import ComponentEditor
from numpy import exp, linspace, meshgrid

class ImagePlot(HasTraits):
    plot = Instance(Plot)
    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=500, height=500, resizable=True, title="Chaco Plot")

    def __init__(self):
        super(ImagePlot, self).__init__()
        x = linspace(0, 10, 50)
        y = linspace(0, 5, 50)
        xgrid, ygrid = meshgrid(x, y)
        z = exp(-(xgrid*xgrid+ygrid*ygrid)/100)
        plotdata = ArrayPlotData(imagedata = z)
        plot = Plot(plotdata)
        plot.img_plot("imagedata", colormap=jet)
        self.plot = plot

if __name__ == "__main__":
    ImagePlot().configure_traits()