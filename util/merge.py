from pathlib import Path

import pandas

import ch2.CreateDataset


# Merge data to one file per sensor, each file contains data merged from multiple samplings of the same sensor
def by_sampling(in_base_dir: str, out_base_dir: str, file_mapping: dict):
    Path(out_base_dir).mkdir(exist_ok=True, parents=True)  # If the output directory does not exist, create it
    for out_file, in_files in file_mapping.items():
        merge_result = pandas.DataFrame()  # Create an empty DataFrame for each sensor
        for in_file in in_files:
            data = pandas.read_csv(Path(in_base_dir) / in_file)
            merge_result = merge_result.append(data)
        merge_result.to_csv(Path(out_base_dir).joinpath(out_file))  # Save the merged DataFrame to a file


# Merge data from different sensor data files from time_merge() to one file. It contains data from multiple samplings of all sensors
def by_sensor(in_base_dir: str, in_files: dict, intervals_ms: list, out_base_dir: str, merge_result_file: str):
    Path(out_base_dir).mkdir(exist_ok=True, parents=True)  # If the output directory does not exist, create it
    min_interval = min(intervals_ms)
    least_granularity_table = None
    for interval in intervals_ms:
        data_set = ch2.CreateDataset.CreateDataset(Path(in_base_dir), interval)
        for file_name, arg in in_files['data'].items():
            data_set.add_numerical_dataset(file_name, arg['timestamp'], arg['columns'], prefix=arg['prefix'])  # Add data to the data set
        if interval == min_interval:  # Only save the data set of the least granularity (time interval)
            least_granularity_table = data_set.data_table
    least_granularity_table.rename_axis('time', inplace=True)  # Add name for the index column
    least_granularity_table.to_csv(Path(out_base_dir).joinpath(merge_result_file))
    return least_granularity_table
