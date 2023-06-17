import os

completion_hint = os.linesep + 24 * '*' + 8 * ' ' + "COMPLETE" + 8 * ' ' + 24 * '*' + os.linesep
sampling_time_re = r'\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d'
aggregated_data_preview_arg = {
    'timestamp': 'time',
    'columns': ['a_x', 'a_y', 'a_z', 'g_x', 'g_y', 'g_z', 'omega_x', 'omega_y', 'omega_z', 'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed', 'B_x', 'B_y', 'B_z', 'o_yaw', 'o_pitch', 'o_roll', 'o_qw', 'o_qx', 'o_qy', 'o_qz'],
    'disp': {
        'columns': ['a_', 'g_', 'omega_', 'loc_latitude', 'loc_longitude', 'loc_altitude', 'loc_bearing', 'loc_speed', 'B_', 'o_'],
        'matches': ['like', 'like', 'like', 'exact', 'exact', 'exact', 'exact', 'exact', 'like', 'like'],
        'elements': ['line', 'line', 'line', 'line', 'line', 'line', 'line', 'line', 'line', 'line']
    }
}
