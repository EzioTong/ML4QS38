import glob
import os
import re
from pathlib import Path

import extern
import util.preview

if __name__ == '__main__':
    downsample_arg = {
        'data': {
            'Accelerometer.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'a_'},
            'Gravity.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'g_'},
            'Gyroscope.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'omega_'},
            'Location.csv': {
                'timestamp': 'time',
                'columns': ['latitude', 'longitude', 'altitude', 'bearing', 'speed'],
                'prefix': 'loc_',
                'disp': {
                    'columns': ['loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed'],
                    'matches': ['exact', 'exact', 'exact', 'exact', 'exact'],
                    'elements': ['line', 'line', 'line', 'line', 'line']
                }
            },
            'Magnetometer.csv': {'timestamp': 'time', 'columns': ['x', 'y', 'z'], 'prefix': 'B_'},
            'Orientation.csv': {'timestamp': 'time', 'columns': ['yaw', 'pitch', 'roll', 'qw', 'qx', 'qy', 'qz'], 'prefix': 'o_'},
        },
        'labels': {}
    }
    # downsample_arg = {
    #     'data': {
    #         'aggregated-data.csv': {
    #             'timestamp': 'time',
    #             'columns': ['a_x', 'a_y', 'a_z', 'g_x', 'g_y', 'g_z', 'omega_x', 'omega_y', 'omega_z', 'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed', 'B_x', 'B_y', 'B_z', 'o_yaw', 'o_pitch', 'o_roll', 'o_qw', 'o_qx', 'o_qy', 'o_qz'],
    #             'disp': {
    #                 'columns': ['a_', 'g_', 'omega_', 'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed', 'B_', 'o_'],
    #                 'matches': ['like', 'like', 'like', 'exact', 'exact', 'exact', 'exact', 'exact', 'like', 'like'],
    #                 'elements': ['line', 'line', 'line', 'line', 'line', 'line', 'line', 'line', 'line', 'line']
    #             }
    #         }
    #     },
    #     'labels': {}
    # }

    # files = glob.glob('res/**/*.csv', recursive=True)
    files = glob.glob('dat/Suzukaze/2023-06-10_22-27-10', recursive=True)

    # dat_root = 'dat/raw'
    dat_root = 'dat/raw/Ezio'
    # dat_root = 'dat/clipped'
    sampling_paths = []
    for root, dirs, files in os.walk(dat_root):  # Recursively find all the samplings
        for dir in dirs:
            matches = re.search(extern.sampling_time_re, dir)  # Each sampling is required to be stored in a directory whose name contains a timestamp
            if matches:  # This is a sampling
                sampling_paths.append(f'{root}/{dir}')
    for sampling_path in sampling_paths:
        util.preview.preview_data_set(sampling_path, downsample_arg, [250], 'avg', True, False)

    # arg = {
    #     'data': {
    #         'aggregated-data.csv': {
    #             'timestamp': 'time',
    #             'columns': ['a_x', 'a_y', 'a_z', 'g_x', 'g_y', 'g_z', 'omega_x', 'omega_y', 'omega_z', 'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed', 'B_x', 'B_y', 'B_z', 'o_yaw', 'o_pitch', 'o_roll', 'o_qw', 'o_qx', 'o_qy', 'o_qz'],
    #             'disp': {
    #                 'columns': ['a_', 'g_', 'omega_', 'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed', 'B_', 'o_'],
    #                 'matches': ['like', 'like', 'like', 'exact', 'exact', 'exact', 'exact', 'exact', 'like', 'like'],
    #                 'elements': ['line', 'line', 'line', 'line', 'line', 'line', 'line', 'line', 'line', 'line']
    #             }
    #         }
    #     },
    #     'labels': {}
    # }
    #
    # files = glob.glob('res/**/*.csv', recursive=True)
    # for file in files:
    #     preview_data_set(str(Path(file).parent), arg, [250], aggregation=None, True, False)
