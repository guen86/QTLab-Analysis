import lecroy
from data import Data
from numpy import *
from lib.network import object_sharer as objsh
import qtclient as qt

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
        CurrentRow = analysis.get_CurrentRow()
        MaximumMinMax_vec = []
        for row in arange(CurrentRow, len(data_obj.get_data())):
            analysis.set_CurrentRow(row+1)
            MaximumMinMax_vec_part = analyse_data_row(data_obj, row)
            plt.hist(MaximumMinMax_vec_part, bins=100)
            MaximumMinMax_vec = MaximumMinMax_vec + MaximumMinMax_vec_part
        plt.hist(MaximumMinMax_vec, bins=100)
    else:
        return False

def analyse_data_row(data_obj, row):
    '''
    Analyse the data row.
    '''
    # Get file index and filepath of .trc file
    column_names = analysis.get_column_names()
    data = data_obj.get_data()
    data = data[row]
    file_index = int(data[column_names.index('Filename index')])
    filename = data_obj.get_filename()
    filename = filename.replace('.dat', '%s.trc' %file_index)
    filepath_c3 = data_obj.get_dir() + '/' + 'C3_' + filename
    filepath_c4 = data_obj.get_dir() + '/' + 'C4_' + filename
    # Read .trc file
    [time_vec_c3, data_vec_c3] = lecroy.read_timetrace(filepath_c3)
    [time_vec, data_vec_c4] = lecroy.read_timetrace(filepath_c4)
    data_vec = data_vec_c3 + data_vec_c4
    NumberOfSegmentsAcquired  = int(data[column_names.index('Number of acquired segments')])
    time_vec = reshape(time_vec, (NumberOfSegmentsAcquired,-1))
    data_vec = reshape(data_vec, (NumberOfSegmentsAcquired,-1))
    MaximumMinMax_vec = []
    for segment in arange(1,NumberOfSegmentsAcquired):
        time_seg = time_vec[segment,:]
        data_seg = data_vec[segment,:]
        [data_vec_stage, NumberOfFlanks_vec, Occupation_vec, FinalOccupation_vec, MinMax_vec] = find_tunnel_events_via_threshold_loop(time_seg,data_seg)
        MaximumMinMax_vec.append(max(MinMax_vec))
    return MaximumMinMax_vec
        
        
def find_tunnel_events_via_threshold_loop(time_vec,data_vec):
    '''
    Find tunnel events through looping the threshold.
    Outputs the occupation, final occupation, etc.
    Input:
        data_vec: 1 WFM pulse
    Output:
        
    '''

    # Init variables
    stage = analysis.get_WhichStages()[0]
    WhichStages = measurement.get_WhichStages()
    stage = stage - WhichStages[0] # get index of stage in WFM_pulselength
    timestep = time_vec[1] - time_vec[0]
    WFM_pulseLength = (measurement.get_t_vec_init()[WhichStages[0]-1:WhichStages[1]]/timestep).round()
    IgnoreAtEnd = (analysis.get_ignoreAtEnd() / timestep).round()
    IgnoreAtStart = (analysis.get_ignoreAtStart() / timestep).round()
    StageStart = len(data_vec) - sum(WFM_pulseLength) + sum(WFM_pulseLength[0:stage])

    data_vec = data_vec[(StageStart + IgnoreAtStart):(StageStart + WFM_pulseLength[stage] - IgnoreAtEnd)]
    thresh_step = (max(data_vec) - min(data_vec))/(analysis.get_numberOfThreshold()-1)
    thresh_vec = arange(min(data_vec), max(data_vec)+thresh_step, thresh_step)

    NumberOfFlanks_vec = []
    Occupation_vec = []
    FinalOccupation_vec = []
    MinMax_vec = []

    for threshold in thresh_vec:
        Digi = ceil((data_vec-threshold)/1000)
        NumberOfFlanks_vec.append(sum(diff(Digi) != 0))
        Occupation_vec.append(mean(Digi))
        FinalOccupation_vec.append(Digi[-1])
        MinMax_vec.append(mean(data_vec[Digi==1].tolist())-mean(data_vec[Digi==0].tolist()))
        
    return data_vec, NumberOfFlanks_vec, Occupation_vec, FinalOccupation_vec, MinMax_vec