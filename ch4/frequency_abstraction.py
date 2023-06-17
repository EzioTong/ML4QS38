import numpy
import pandas

temp_list = []
freqs = None


# Find the amplitudes of the different frequencies using a fast fourier transformation. Here,
# the sampling rate expresses
# the number of samples per second (i.e. Frequency is Hertz of the dataset).
def FFT(data):
    # Create the transformation, this includes the amplitudes of both the real and imaginary part.
    # print(data.shape)
    transformation = numpy.fft.rfft(data, len(data))
    # real
    real_ampl = transformation.real
    # max
    max_freq = freqs[numpy.argmax(real_ampl[0:len(real_ampl)])]
    # weigthed
    freq_weighted = float(numpy.sum(freqs * real_ampl)) / numpy.sum(real_ampl)

    # pse
    PSD = numpy.divide(numpy.square(real_ampl), float(len(real_ampl)))
    PSD_pdf = numpy.divide(PSD, numpy.sum(PSD))

    # Make sure there are no zeros.
    if numpy.count_nonzero(PSD_pdf) == PSD_pdf.size:
        pse = -numpy.sum(numpy.log(PSD_pdf) * PSD_pdf)
    else:
        pse = 0

    real_ampl = numpy.insert(real_ampl, 0, max_freq)
    real_ampl = numpy.insert(real_ampl, 0, freq_weighted)
    row = numpy.insert(real_ampl, 0, pse)

    temp_list.append(row)

    return 0


# Get frequencies over a certain window.
def abstract(data_table: pandas.DataFrame, columns: list, window_size: int, sampling_rate: float):
    window_size = int(window_size)
    global freqs
    freqs = (sampling_rate * numpy.fft.rfftfreq(window_size)).round(3)

    for column in columns:
        column_list = []
        # prepare column names
        column_list.append(column + '_max_freq')
        column_list.append(column + '_freq_weighted')
        column_list.append(column + '_PSE')

        column_list = column_list + [f'{column}_{str(freq)}Hz' for freq in freqs]

        # rolling statistics to calculate frequencies, per window size. 
        # Pandas Rolling method can only return one aggregation value. 
        # Therefore, values are not returned but stored in temp class variable 'temp_list'.

        # note to self! Rolling window_size would be nicer and more logical! In older version window size is actually 41. (ws + 1)
        data_table[column].rolling(window_size + 1).apply(FFT)

        # Pad the missing rows with nans
        frequencies = numpy.pad(numpy.array(temp_list), ((window_size, 0), (0, 0)), 'constant', constant_values=numpy.nan)
        # add new freq columns to frame

        data_table[column_list] = pandas.DataFrame(frequencies, index=data_table.index)

        # reset temp-storage array
        del temp_list[:]

    return data_table
