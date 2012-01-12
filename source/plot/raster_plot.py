# Raster plotting
#
# A class for raster (color, however you want to name it) plots and the
# required data class. derived from the qwt classes, but adapted (for speed) and
# plus some convenient methods.
#
# Author: Wolfgang Pfaff <w.pfaff@tudelft.nl>

import numpy as np
from PyQt4 import Qt, QtCore, QtGui
from PyQt4.Qwt5 import Qwt
from plot import Plot, CmapJack

class RasterPlot(Plot):
    """
    Cyclops 2D raster plot.
    """
    def __init__(self, parent):
        Plot.__init__(self, parent)

        # the plot and its data
        self._raster_data = RasterData(self)
        self._plot_item = Qwt.QwtPlotSpectrogram()
        self._plot_item.setData(self._raster_data)
        self._plot_item.attach(self)
        
        # enable colormap and -bar
        self._cbar = self.axisWidget(Qwt.QwtPlot.yRight)
        self._cbar.setColorBarEnabled(True)
        self.enableAxis(Qwt.QwtPlot.yRight)
        self.set_cbar()

    # TODO: this is only a not-so-great workaround.
    # better: make a more general class for color maps that generates a
    # QwtColorMap with appropriate color stops. This could then also
    # be used for log colormaps, etc.
    def set_cbar(self, cmap=CmapJack(), limits=None):
        self._cmap = cmap

        # function can be called before we created the data, make sure
        # this doesn't lead to trouble
        if hasattr(self, '_raster_data'):            
            self._raster_data.limits = limits
            range_ = self._raster_data.range()
            limits = (range_.minValue(),
                      range_.maxValue())        

            self._plot_item.setColorMap(self._cmap)
            self._cbar.setColorMap(range_, self._cmap)
            self.setAxisScale(Qwt.QwtPlot.yRight, limits[0], limits[1])

    def set_data(self, data, xvals, yvals):
        # prepare the data
        bounding_rect = Qt.QRectF(xvals[0], yvals[0],
                xvals[-1]-xvals[0], yvals[-1]-yvals[0])
        self._raster_data = RasterData(self, bounding_rect)
        self._raster_data.set_data(data, xvals, yvals)

        # make sure zooming works correctly
        # FIXME: create a method for manual axis updates in plot class
        if hasattr(self, '_zoomer'):
            self._zoomer.setZoomBase(bounding_rect)
        
        # update visual appearance
        self.setAxisScale(Qwt.QwtPlot.xBottom, xvals[0], xvals[-1])
        self.setAxisScale(Qwt.QwtPlot.yLeft, yvals[0], yvals[-1])
        self.set_cbar(self._cmap)
        self._plot_item.setData(self._raster_data)
        self.replot()

    def set_data_lines(self, lines, data):
        self._raster_data.set_data_lines(lines, data)
        self.replot()

    # redefine autoscale and limits to also work with the colorbar axis
    def setAxisAutoScale(self, axis, auto=True):
        if axis != Qwt.QwtPlot.yRight:
            Plot.setAxisAutoScale(self, axis, auto)
        else:
            if not hasattr(self, '_cmap'):
                self._cmap = CmapJack()
            if auto:
                self.set_cbar(self._cmap, None)
            else:
                self.set_cbar(self._cmap, (self._axis_limits[axis][0],
                                           self._axis_limits[axis][1]))

            Plot.setAxisAutoScale(self, axis, auto)

# the data as required by the raster plot widget
# overloads some functions for our purposes.
# for more info, please refer to the Qwt documentation.
class RasterData(Qwt.QwtRasterData):
    """
    The data as required for the raster plot.
    """
    def __init__(self, plot, rect=Qt.QRectF()):
        Qwt.QwtRasterData.__init__(self, rect)

        self._plot = plot        
        self._xvals = np.array([0,1])
        self._yvals = np.array([0,1])
        self._data = np.array([[0,0],[0,0]])
        self._xstep = 1
        self._ystep = 1
        self.limits = None
    
    def copy(self):
        return self

    def range(self):
        if self.limits == None:
            return(Qwt.QwtDoubleInterval(self._data.min(), self._data.max()))
        else:
            return(Qwt.QwtDoubleInterval(self.limits[0], self.limits[1]))

    # as long as this fits (in terms of screen pixels),
    # make the resolution such that the plot fits correctly
    # (with 2px per point, so we can display half points, needed
    # at the plot boundaries). if the plot has more points than
    # the plot widget elements, set the available pixels as resolution.
    def rasterHint(self, rect):
        w = self._plot.size().width()
        h = self._plot.size().height()
        if self._xvals.size > w/2:
            xpts = w
        else:
            xpts = self._xvals.size*2-2
        if self._yvals.size > h/2:
            ypts = h
        else:
            ypts = self._yvals.size*2-2
            
        return QtCore.QSize(xpts,ypts)

    def set_data(self, data, xvals, yvals):
        self._data = data
        self._xvals = xvals
        self._yvals = yvals
        self._xstep = self._xvals[1] - self._xvals[0]
        self._ystep = self._yvals[1] - self._yvals[0]
        self.setBoundingRect(Qt.QRectF(xvals[0], yvals[0],
                xvals[-1]-xvals[0], yvals[-1]-yvals[0]))

    def set_data_lines(self, lines, data):
        self._data[lines,:] = data        

    # getting the correct value for each pixel on the plot canvas.
    # the rounding 'error' for the y-value is because the plot uses
    # the top left as origin when using rasterHint to determine
    # where to take values.
    def value(self, x, y):        
        i = int(abs(x-self._xvals[0])/self._xstep + 0.5)
        j = int(abs(y-self._yvals[0])/self._ystep + 0.49999)
        if 0 <= i < len(self._xvals) and 0 <= j < len(self._yvals):
            return self._data[j,i]
        else:
            return self._data.min()
