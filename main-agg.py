import glob
from datetime import datetime
import os
import re
from pathlib import Path

import pandas

import util.merge
import util.preview
import util.util
import extern

activity_type = ['walking', 'running', 'cycling', 'aboard a moving vehicle', 'undefined']


def get_activity_type(sampling_path_name: str):
    r = {
        'walking': [
            r'(\b|[^A-Za-z])walk(ing)?(\b|[^A-Za-z])',
        ],
        'running': [
            r'(\b|[^A-Za-z])run(ning)?(\b|[^A-Za-z])', r'(\b|[^A-Za-z])jog(ging)?(\b|[^A-Za-z])', r'(\b|[^A-Za-z])sprint(ing)?(\b|[^A-Za-z])',
        ],
        'cycling': [
            r'(\b|[^A-Za-z])cycl(e|ing)(\b|[^A-Za-z])', r'(\b|[^A-Za-z])bik(e|ing)(\b|[^A-Za-z])',
        ],
        'aboard a moving vehicle': [
            r'(\b|[^A-Za-z])vehicle(\b|[^A-Za-z])',
            r'(\b|[^A-Za-z])car(\b|[^A-Za-z])', r'(\b|[^A-Za-z])automobile(\b|[^A-Za-z])', r'(\b|[^A-Za-z])auto(\b|[^A-Za-z])',
            r'(\b|[^A-Za-z])bus(\b|[^A-Za-z])', r'(\b|[^A-Za-z])train(\b|[^A-Za-z])', r'(\b|[^A-Za-z])tram(\b|[^A-Za-z])', r'(\b|[^A-Za-z])metro(\b|[^A-Za-z])',
            r'(\b|[^A-Za-z])driv(e|ing)(\b|[^A-Za-z])',
            r'(\b|[^A-Za-z])motorcycl(e|ing)(\b|[^A-Za-z])', r'(\b|[^A-Za-z])motorbik(e|ing)(\b|[^A-Za-z])',
            r'(\b|[^A-Za-z])ATV(\b|[^A-Za-z])', r'(\b|[^A-Za-z])quad(\b|[^A-Za-z])',
        ],
    }
    for activity, patterns in r.items():
        for pattern in patterns:
            if re.search(pattern, sampling_path_name, re.IGNORECASE):
                return activity
    return 'undefined'


if __name__ == '__main__':
    data_type = ''
    # data_type = 'raw'
    # data_type = 'clipped'
    in_base = f'dat/{data_type}'
    out_base = f'res/{data_type}'
    # person = 'Andy'
    # person = 'Suzukaze'
    # person = 'Ezio'
    # in_base_pers = f'{in_base}/{person}'  # The directory where the raw data is stored
    # out_base_pers = f'{out_base}/{person}'  # The directory where the outputs are stored
    # time_merge_out_dir_pers = f'{out_base_pers}/time-merge'  # The directory where the outputs of time_merge() are stored
    out_file_base = 'aggregated-data'
    overwrite = False
    always_print_statistics = True

    # Specify how to merge the data from different sensors
    sensor_merge_in = {
        'data': {
            'Accelerometer.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'a_'},
            'Gravity.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'g_'},
            'Gyroscope.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'omega_'},
            'Location.csv': {'timestamp': 'time', 'columns': ['latitude', 'longitude', 'altitude', 'bearing', 'speed'], 'prefix': 'loc_'},
            'Magnetometer.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'B_'},
            'Orientation.csv': {'timestamp': 'time', 'columns': ['yaw', 'pitch', 'roll', 'qw', 'qx', 'qy', 'qz'], 'prefix': 'o_'},
        },
        'labels': {}
    }

    # time_merge_arg = {}  # Map every sensor to a list of csv files that contain data from its different samplings
    # for file in sensor_merge_in['data'].keys():
    #     time_merge_arg[file] = []  # Create an empty list for each sensor
    # raw_data_files = glob.glob(f'{in_base_pers}/**/*.csv', recursive=True)  # read all csv files in the raw data directory
    # for file in raw_data_files:  # Organize and map the csv files by their sensor names
    #     path = Path(file)
    #     if path.name in sensor_merge_in['data'].keys():
    #         time_merge_arg[path.name].append(file)
    # print('Merging data from different timestamps...')
    # util.merge.by_sampling('.', time_merge_out_dir_pers, time_merge_arg)
    # print(extern.completion_hint)

    # intervals = [60 * 10 ** 3]
    # intervals = [1000]
    intervals = [250]
    # intervals = [200]
    # intervals = [125]
    # intervals = [100]
    # intervals = [50]
    min_interval = min(intervals)
    # intervals = [60 * 10 ** 3, 250]
    print('Merging data from different sensors...')
    # util.merge.by_sensor(time_merge_out_dir_pers, sensor_merge_in, intervals, out_base_pers, f'aggregated-data-{datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")}.csv')

    table = {}
    for t in activity_type:
        table[t] = pandas.DataFrame(columns=[
            'a_x', 'a_y', 'a_z',
            'g_x', 'g_y', 'g_z',
            'omega_x', 'omega_y', 'omega_z',
            'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed',
            'B_x', 'B_y', 'B_z',
            'o_yaw', 'o_pitch', 'o_roll', 'o_qw', 'o_qx', 'o_qy', 'o_qz',
        ], dtype=object)
    sampling_paths = []
    for rel_path, folders, files in os.walk(in_base):  # Recursively find all the samplings
        for folder in folders:
            matches = re.search(extern.sampling_time_re, folder)  # Each sampling is required to be stored in a directory whose name contains a timestamp
            if matches:  # This is a sampling
                sampling_path = os.path.relpath(f'{rel_path}/{folder}', in_base)
                sampling_paths.append(sampling_path)

    for sampling_path in sampling_paths:
        if not overwrite and os.path.exists(f'{out_base}/{sampling_path}/{out_file_base}.csv'):
            print(f'Skipping {sampling_path} because the output file already exists.')
            if always_print_statistics:
                data_table = pandas.read_csv(f'{out_base}/{sampling_path}/{out_file_base}.csv', index_col=0)
                util.util.print_statistics(data_table)
                table[get_activity_type(sampling_path)] = table[get_activity_type(sampling_path)].append(data_table, ignore_index=True)
            continue
        print(f'Sampling {sampling_path}')
        data_table = util.merge.by_sensor(f'{in_base}/{sampling_path}', sensor_merge_in, intervals, out_base + f'/{sampling_path}', f'{out_file_base}.csv')
        util.util.print_statistics(data_table)
        table[get_activity_type(sampling_path)] = table[get_activity_type(sampling_path)].append(data_table, ignore_index=True)
        util.preview.preview_data_set(
            f'{out_base}/{sampling_path}',
            {'data': {f'{out_file_base}.csv': extern.aggregated_data_preview_arg}},
            [min_interval],
            None,
            False,
            True,
            f'{out_base}/{sampling_path}/{out_file_base}'
        )

    for activity in activity_type:
        print('Statistics for', activity)
        print(f'Observations: {len(table[activity])}')
        util.util.print_statistics(table[activity], True)

    print(extern.completion_hint)
