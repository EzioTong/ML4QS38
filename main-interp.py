import os
import re

import pandas

import util.preview
import ch3.Kalman_filter
import extern

if __name__ == '__main__':
    in_base = 'res'
    # in_base = 'res/clipped'
    in_file = 'aggregated-data.csv'
    delta_t = [250]
    # delta_t = [200]
    # delta_t = [125]
    # delta_t = [100]
    # delta_t = [50]
    preview = False
    out_file_base = 'aggregated-data-Kalman-filtered'
    overwrite = False

    sampling_paths = []
    for rel_path, folders, files in os.walk(in_base):  # Recursively find all the samplings
        for folder in folders:
            matches = re.search(extern.sampling_time_re, folder)  # Each sampling is required to be stored in a directory named as a timestamp
            if matches:  # This is a sampling
                sampling_paths.append(f'{rel_path}/{folder}')

    for sampling_path in sampling_paths:
        if not overwrite and os.path.isfile(f'{sampling_path}/{out_file_base}.csv'):
            print(f'Skipping Kalman filter on sampling: {sampling_path} (already exists)')
            continue
        print('Applying Kalman filter on sampling: ', sampling_path)
        original_data = pandas.read_csv(f'{sampling_path}/{in_file}', index_col=0)
        processed_data = original_data.copy()
        value_columns = list(original_data.columns.values)
        observation_count = len(original_data.index)
        for column in value_columns:
            missing_rate = (observation_count - original_data[column].count()) / observation_count
            if missing_rate > 0:
                ch3.Kalman_filter.modified_Kalman_filter(processed_data, column)
        processed_data.to_csv(f'{sampling_path}/{out_file_base}.csv')
        if preview:
            util.preview.preview_data_set(
                sampling_path,
                {
                    'data': {
                        f'{in_file}': extern.aggregated_data_preview_arg,
                        f'{out_file_base}.csv': extern.aggregated_data_preview_arg,
                    },
                },
                delta_t,
                None,
                True,
                True,
                f'{sampling_path}/aggregated-data-not-filtered-vs-filtered'
            )
        else:
            util.preview.preview_data_set(
                sampling_path,
                {'data': {f'{out_file_base}.csv': extern.aggregated_data_preview_arg}},
                delta_t,
                None,
                False,
                True,
                f'{sampling_path}/{out_file_base}'
            )

    print(extern.completion_hint)
