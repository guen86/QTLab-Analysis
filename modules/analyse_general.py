import lecroy
from data import Data
# from plot_engines.qtgnuplot import Plot2D, Plot3D
from numpy import *
# from lib.network import object_sharer as objsh
import qtclient as qt

measurement = qt.get_instrument_proxy('measurement')
analysis = qt.get_instrument_proxy('analysis')
#start_analysis()

# Load matplotlib and select the GTK Agg back-end
# import matplotlib as mpl
# mpl.use('gtkagg')

# Load pyplot wrappers and set interactive mode on
# import matplotlib.pyplot as plt
# plt.ion()

from numpy import *

##################
# Math functions #
##################

def smoothList(list,strippedXs=False,degree=10):  
    if strippedXs==True: return Xs[0:-(len(list)-(len(list)-degree+1))]  
    smoothed=[0]*(len(list)-degree+1)  
    for i in range(len(smoothed)):  
        smoothed[i]=sum(list[i:i+degree])/float(degree)  
    return smoothed  

def smoothListTriangle(list,strippedXs=False,degree=5):  
    weight=[]  
    window=degree*2-1  
    smoothed=[0.0]*(len(list)-window)  
    for x in range(1,2*degree):weight.append(degree-abs(degree-x))  
    w=array(weight)  
    for i in range(len(smoothed)):  
        smoothed[i]=sum(array(list[i:i+window])*w)/float(sum(w))  
    return smoothed

def smoothListGaussian(list,strippedXs=False,degree=5):  
    window=degree*2-1  
    weight=array([1.0]*window)  
    weightGauss=[]  
    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(exp((4*(frac))**2))  
        weightGauss.append(gauss)  
    weight=array(weightGauss)*weight  
    smoothed=[0.0]*(len(list)-window)  
    for i in range(len(smoothed)):  
        smoothed[i]=sum(array(list[i:i+window])*weight)/sum(weight)  
    return smoothed 

def search_array(elem, arr):
    '''
    Search array for element 'elem'.
    Return indices.
    '''
    arr_ind = arange(0, len(arr))
    found_indices = arr_ind[arr == elem]
    return found_indices

def smooth_data(data,window_size):
    '''
    Smooth data
    '''
    numpoints = len(data)
    points_before = floor((window_size-1)/2)
    points_after = window_size - points_before - 1

    smooth_data = zeros(numpoints)
    for k1 in arange(0,numpoints,1):
        val = 0.
        for k2 in arange(-points_before,points_after+1,1):
            tmp = max([k1+k2,0])
            index = min([tmp,numpoints-1])
            index = int(index)
            val = val + data[index]
        
        smooth_data[k1] = val/window_size
    return smooth_data

######################
# Analysis functions #
######################
    
def get_3d_data_coord(data_col):
    '''
    From the raw data column, get a vector of the values
    Coordinate
    '''
    col_indices = search_array(data_col[0], data_col)
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
    
def analyse_2Dscan(data_obj):
	'''
	Analyse 2D scan measurement
	Input:
		data_obj: data object for the 2D scan
	Output:
		x_vec, y_vec, qpc1_vec, qpc2_vec: matrices containing data of 2D plot, formatted for use with matplotlib.pyplot.pcolor
	'''
	#data_obj = Data(filepath)
	data = data_obj.get_data()
	x_vec = data[:,0]
	y_vec = data[:,1]
	qpc1_vec = data[:,2]
	qpc2_vec = data[:,3]
	
	# Reshape vectors to matrices.
	
	y_index = arange(0,len(y_vec))
	diff_index = y_index[diff(y_vec)>0]
	diff_vec = diff(y_vec)[diff(y_vec)>0]
	if len(diff_index) > 0:
		y_vec_step = mean(diff_vec)
		num_sweep = diff_index[0] + 1
		num_steps = len(diff_index) + 1
		x_vec = array(x_vec[0:num_sweep].tolist()*num_steps)
		y_vec = arange(y_vec[0], y_vec[0]+num_steps*y_vec_step, y_vec_step)
		y_vec = reshape(y_vec, (num_steps,1))
		y_vec_new = reshape(x_vec.copy(), (num_steps, num_sweep))
		for n in arange(0,num_steps):
			y_vec_new[n] = y_vec[n].tolist()*num_sweep
		x_vec = reshape(x_vec, (num_steps, num_sweep))
		qpc1_vec = append(qpc1_vec, zeros(num_steps*num_sweep - len(qpc1_vec)))
		qpc1_vec = reshape(qpc1_vec, (num_steps, num_sweep))
		qpc2_vec = append(qpc2_vec, zeros(num_steps*num_sweep - len(qpc2_vec)))
		qpc2_vec = reshape(qpc2_vec, (num_steps, num_sweep))
        #plt.pcolor(x_vec, y_vec, qpc1_vec)
        return x_vec, y_vec, qpc1_vec, qpc2_vec
		
def analyse_timetrace_rows(data_obj):
	'''
	Analyse all rows for a timetrace measurement
	'''
	CurrentRow = analysis.get_CurrentRow()
	MaximumMinMax_vec = []
	for row in arange(CurrentRow, len(data_obj.get_data())):
		analysis.set_CurrentRow(row+1)
		MaximumMinMax_vec_part = analyse_timetrace_data_row(data_obj, row)
		plt.hist(MaximumMinMax_vec_part, bins=100)
		MaximumMinMax_vec = MaximumMinMax_vec + MaximumMinMax_vec_part
	plt.hist(MaximumMinMax_vec, bins=100)

def analyse_timetrace_data_row(data_obj, row):
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