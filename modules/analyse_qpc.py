import lecroy
from data import Data
from plot_engines.qtgnuplot import Plot2D, Plot3D
from numpy import *
from lib.network import object_sharer as objsh
from analysis import qtclient as qt

measurement = qt.get_instrument_proxy('measurement')
analysis = qt.get_instrument_proxy('analysis')
#start_analysis()

# Load matplotlib and select the GTK Agg back-end
import matplotlib as mpl
mpl.use('gtkagg')

# Load pyplot wrappers and set interactive mode on
import matplotlib.pyplot as plt
plt.ion()


def start_analysis():
    '''
    Start analysis of data as defined in virtual instrument 'measurement'.
    '''
    if (measurement.get_data_updated()==True) & (measurement.get_data_done()==False):
        # Get names of columns
        data_obj = Data(measurement.get_data_path())
        dimensions = data_obj.get_dimensions()
        column_names = []
        for dimension in dimensions:
            column_names.append(dimension['name'])
        analysis.set_column_names(column_names)

        # Connect to measurement instrument object
        measurement.connect('changed', check_data_changed)
    else:
        print 'Data file isn\'t ready yet.'

def check_data_changed(*args):
    '''
    Check if the data object has changed or if the measurement is finished.
    If yes, analyse the data.
    '''
    if (measurement.get_data_updated()==True) & (measurement.get_data_done()==False):
        data_obj = Data(measurement.get_data_path())
        data = data_obj.get_data()
        v_sweep = data[:,1]
        v_step = data[:,2]
        plt.plot(v_sweep, v_step, 
    else:
        return False