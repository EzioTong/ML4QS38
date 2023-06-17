import numpy
import pandas
import pykalman


def modified_Kalman_filter(data_table: pandas.DataFrame, column: str, mode: str = 'smooth'):
    original_array = data_table[column].values.astype(numpy.single)
    masked_array = numpy.ma.masked_invalid(original_array)

    # Initialize the Kalman filter with the trivial transition and observation matrices.
    f = pykalman.KalmanFilter(transition_matrices=[[1]], observation_matrices=[[1]])
    # Find the best other parameters based on the data (e.g. Q)
    f = f.em(masked_array, n_iter=5)

    # And apply the filter.
    if mode == 'filter':
        (new_data, filtered_state_covariances) = f.filter(masked_array)
    elif mode == 'smooth':
        (new_data, filtered_state_covariances) = f.smooth(masked_array)
    # modify the column in-place
    for i in range(0, len(data_table.index)):
        if numpy.isnan(original_array[i]):
            data_table.loc[data_table.index[i], column] = new_data[i]
