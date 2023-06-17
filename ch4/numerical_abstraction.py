import numpy
import pandas
import scipy.stats


# Here we need a bit more work: Create time points, assuming discrete time steps with fixed △t.
def get_slope(data):
    times = numpy.array(range(0, len(data.index)))
    data = data.astype(numpy.float32)

    # Check for NaN's
    mask = ~numpy.isnan(data)

    # If we have no data but NaN we return NaN.
    if len(data[mask]) == 0:
        return numpy.nan
    # Otherwise we return the slope.
    else:
        slope, _, _, _, _ = scipy.stats.linregress(times[mask], data[mask])
        return slope


# TODO Add your own aggregation function here:
# def my_aggregation_function(self, data)

# This function aggregates a list of values using the specified aggregation function
def aggregate_value(data_table: pandas.DataFrame, window_size: int, aggregation_function: str):
    window = str(window_size) + 's'
    # Compute the values and return the result.
    if aggregation_function == 'mean':
        return data_table.rolling(window, min_periods=window_size).mean()
    elif aggregation_function == 'max':
        return data_table.rolling(window, min_periods=window_size).max()
    elif aggregation_function == 'min':
        return data_table.rolling(window, min_periods=window_size).min()
    elif aggregation_function == 'median':
        return data_table.rolling(window, min_periods=window_size).median()
    elif aggregation_function == 'std':
        return data_table.rolling(window, min_periods=window_size).std()
    elif aggregation_function == 'slope':
        return data_table.rolling(window, min_periods=window_size).apply(get_slope)

    # TODO: add your own aggregation function here
    else:
        return numpy.nan


def abstract(data_table: pandas.DataFrame, columns: list, window_size: int, aggregation_function_name: str):
    for column in columns:
        aggregations = aggregate_value(data_table[column], window_size, aggregation_function_name)
        data_table[f'{column}_{aggregation_function_name}'] = aggregations
