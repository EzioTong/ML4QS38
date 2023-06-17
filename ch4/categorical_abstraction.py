import numpy as np
import scipy.stats as stats

pattern_prefix = 'temp_pattern_'
before = '(b)'
co_occurs = '(c)'
cache = {}


# Determine the time points a pattern occurs in the dataset given a windows size.
def determine_pattern_times(data_table, pattern, window_size):
    times = []

    # If we have a pattern of length one
    if len(pattern) == 1:
        # If it is in the cache, we get the times from the cache.
        if to_string(pattern) in cache:
            times = cache[to_string(pattern)]
        # Otherwise we identify the time points at which we observe the value.
        else:
            timestamp_rows = data_table[data_table[pattern[0]] > 0].index.values.tolist()
            times = [data_table.index.get_loc(i) for i in timestamp_rows]
            cache[to_string(pattern)] = times

    # If we have a complex pattern (<n> (b) <m> or <n> (c) <m>)
    elif len(pattern) == 3:
        # We compute the time points of <n> and <m>
        time_points_first_part = determine_pattern_times(data_table, pattern[0], window_size)
        time_points_second_part = determine_pattern_times(data_table, pattern[2], window_size)

        # If it co-occurs we take the intersection.
        if pattern[1] == co_occurs:
            # No use for co-occurences of the same patterns...
            if pattern[0] == pattern[2]:
                times = []
            else:
                times = list(set(time_points_first_part) & set(time_points_second_part))
        # Or we take all the time points from <m> at which we observed <n>, given window size.
        elif pattern[1] == before:
            for t in time_points_second_part:
                if len([i for i in time_points_first_part if ((i >= t - window_size) & (i < t))]):
                    times.append(t)
    return times


# Create a string representation of a pattern.
def to_string(pattern):
    # If we just have one component, return the string.
    if len(pattern) == 1:
        return str(pattern[0])
    # Otherwise, return the merger of the strings of all components.
    else:
        name = ''
        for p in pattern:
            name = name + to_string(p)
        return name


# Selects the patterns from 'patterns' that meet the minimum support in the dataset given the window size.
def select_k_patterns(data_table, patterns, min_support, window_size):
    selected_patterns = []
    for pattern in patterns:
        # Determine the times at which the pattern occurs.
        times = determine_pattern_times(data_table, pattern, window_size)
        # Compute the support
        support = float(len(times)) / len(data_table.index)
        # If we meet the minimum support, append the selected patterns
        # and set the value to 1 at which it occurs.
        if support >= min_support:
            selected_patterns.append(pattern)
            print(to_string(pattern))
            # Set the occurrence of the pattern in the row to 0.
            data_table[pattern_prefix + to_string(pattern)] = 0
            # data_table[pattern_prefix + to_string(pattern)][times] = 1
            data_table.iloc[times, data_table.columns.get_loc(pattern_prefix + to_string(pattern))] = 1
    return data_table, selected_patterns


# extends a set of k-patterns with the 1-patterns that have sufficient support.
def extend_k_patterns(k_patterns, one_patterns):
    new_patterns = []
    for k_p in k_patterns:
        for one_p in one_patterns:
            # Add a before relationship
            new_patterns.append([k_p, before, one_p])
            # Add a co-occurs relationship.
            new_patterns.append([k_p, co_occurs, one_p])
    return new_patterns


# Function to abstract our categorical data.
# Note that we assume a list of binary columns representing the different categories.
# 'exact': The column names should match exactly. 'like': Should include the specified name.
# We also express a minimum support, a windows size between succeeding patterns
# and a maximum size for the number of patterns.
def abstract(data_table, columns, match, min_support, window_size, max_pattern_size):
    # Find all the relevant columns of binary attributes.
    column_names = list(data_table.columns)
    selected_patterns = []

    relevant_dataset_columns = []
    for i in range(0, len(columns)):  # match columns
        if match[i] == 'exact':
            relevant_dataset_columns.append(columns[i])
        else:
            relevant_dataset_columns.extend([name for name in column_names if columns[i] in name])

    # Generate the one patterns first
    potential_1_patterns = [[pattern] for pattern in relevant_dataset_columns]

    new_data_table, one_patterns = select_k_patterns(data_table, potential_1_patterns, min_support, window_size)
    selected_patterns.extend(one_patterns)
    print(f'Number of patterns of size 1 is {len(one_patterns)}')

    k = 1
    k_patterns = one_patterns

    # And generate all following patterns.
    while (k < max_pattern_size) & (len(k_patterns) > 0):
        k = k + 1
        potential_k_patterns = extend_k_patterns(k_patterns, one_patterns)
        new_data_table, selected_new_k_patterns = select_k_patterns(new_data_table, potential_k_patterns, min_support, window_size)
        selected_patterns.extend(selected_new_k_patterns)
        print(f'Number of patterns of size {k} is {len(selected_new_k_patterns)}')

    return new_data_table
