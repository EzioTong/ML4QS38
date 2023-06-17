from pathlib import Path

import ch2.CreateDataset
import util.VisualizeDataset


def preview_data_set(in_base_dir: str, in_arg: dict, intervals_ms: list, aggregation='avg', show: bool = True, save_figure: bool = True, path_name_wo_ext: str = None):
    for interval in intervals_ms:
        data_set = ch2.CreateDataset.CreateDataset(Path(in_base_dir), interval)
        data_chart = util.VisualizeDataset.VisualizeDataset()
        disp_columns = []
        disp_matches = []
        disp_elements = []
        for file_name, arg in in_arg['data'].items():
            data_set.add_numerical_dataset(file_name, arg['timestamp'], arg['columns'], aggregation, prefix=arg['prefix'] if 'prefix' in arg.keys() else '')  # Add data to the data set
            if 'disp' in arg.keys():  # Custom display arguments always override the default ones
                disp_columns.extend(arg['disp']['columns'])
                disp_matches.extend(arg['disp']['matches'])
                disp_elements.extend(arg['disp']['elements'])
            else:
                if 'prefix' in arg.keys():  # Allocate a prefix for each file. The columns with the same prefix will be displayed together in the same plot.
                    disp_columns.append(arg['prefix'])
                    disp_matches.append('like')
                    disp_elements.append('line')
                else:  # If a prefix is not specified, we assume that all columns are to be displayed
                    disp_columns.extend(arg['columns'])
                    disp_matches.extend(['like'] * len(arg['columns']))
                    disp_elements.extend(['line'] * len(arg['columns']))
        data_chart.plot_dataset(data_set.data_table, disp_columns, disp_matches, disp_elements, show, save_figure, path_name_wo_ext)
