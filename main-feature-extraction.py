import time
import os
import re

import pandas

import ch4.numerical_abstraction
import ch4.frequency_abstraction
import extern

in_base = 'res/clipped'
# in_file = 'aggregated-data.csv'
in_file = 'aggregated-data-Kalman-filtered.csv'
delta_t = [250]
out_file_base = 'aggregated-data-with-extracted-features'
overwrite = False

start_time = time.time()

sampling_paths = []
for rel_path, folders, files in os.walk(in_base):  # Recursively find all the samplings
    for folder in folders:
        matches = re.search(r'\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d', folder)  # Each sampling is required to be stored in a directory named as a timestamp
        if matches:  # This is a sampling
            sampling_paths.append(f'{rel_path}/{folder}')

for sampling_path in sampling_paths:
    print('Extracting features on sampling', sampling_path)
    original_data_set = pandas.read_csv(f'{sampling_path}/{in_file}', index_col=0)

    processed_data_set = original_data_set.copy()
    processed_data_set.index = pandas.to_datetime(processed_data_set.index)
    # Compute the number of milliseconds covered by an instance based on the first two rows
    ms_per_instance = (processed_data_set.index[1] - processed_data_set.index[0]).microseconds / 10 ** 3
    window_size = int(0.5 * 60 * 10 ** 3 / ms_per_instance)  # the number of samples in 0.5 minute
    sampling_rate = 1000.0 / ms_per_instance  # unit: Hz

    # Numerical abstraction
    selected_predictor_columns = [c for c in original_data_set.columns if not 'label' in c]
    aggregation_functions = ['mean', 'median', 'std', 'slope']
    for aggregation_function in aggregation_functions:
        ch4.numerical_abstraction.abstract(processed_data_set, selected_predictor_columns, window_size, aggregation_function)

    # Frequency abstraction
    periodic_predictor_columns = [
        'a_x', 'a_y', 'a_z',
        'g_x', 'g_y', 'g_z',
        'omega_x', 'omega_y', 'omega_z',
        'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed',
        'B_x', 'B_y', 'B_z',
        'o_yaw', 'o_pitch', 'o_roll', 'o_qw', 'o_qx', 'o_qy', 'o_qz',
    ]
    processed_data_set = ch4.frequency_abstraction.abstract(processed_data_set, periodic_predictor_columns, 10000.0 / ms_per_instance, sampling_rate)

    window_overlap = 0.9
    skipped_points = int((1 - window_overlap) * window_size)
    processed_data_set = processed_data_set.iloc[::skipped_points, :]

    if not os.path.exists(sampling_path) or overwrite:
        processed_data_set.to_csv(f'{sampling_path}/{out_file_base}.csv')
    else:
        print(f'File {sampling_path}/{out_file_base}.csv already exists.')

    print(extern.completion_hint)
