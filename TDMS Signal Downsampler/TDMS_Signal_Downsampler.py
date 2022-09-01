"""TDMS Signal Downsampler


Functions
---------
Retreves and downsamples TDMS raw signal data.

Author
---------
Mason Becker

"""

# Imports
from numpy import empty, append  # Array processing
from scipy.signal import cheby1, dlti, filtfilt, decimate, cosine  # Low-pass filter mechanics
from time import time  # Compilation time
from math import sqrt, ceil

# Additional Functions
import plotlib as PL
import DataManager as DM

# Attempts to produce a unique factorization for input integer
def factorize(n):
    factors = []
    # even case
    while n % 2 == 0:
        factors.append(2)
        n = n / 2

    # odd case
    for i in range(3, int(sqrt(n)) + 1, 2):
        while(n % i == 0):
            factors.append(i)
            n = n / i
    
    # Catch remainder
    if n > 2:
        factors.append(n)

    return factors

# Low-pass filter
def lowpass_filter(data, factors, order=8):
    system = dlti(*cheby1(order, 0.05, 0.8 / factors[0]))
    b, a = system.num, system.den
    y = filtfilt(b, a, data, axis=-1)

    # Preform recursion in accordence with interval factors
    if len(factors) > 1:
        y = lowpass_filter(y, factors = factors[1:], order=order) # Slice a factor off and run recursion
    return y

# Takes every n value out of a data set and creates a new reduced value
def downsample(data, interval, order=8):
    print("Passing lowpass filter...")
    noiseless = lowpass_filter(data, factors = factorize(interval), order=order)
    print("Downsampling...")
    reduced = empty([int(noiseless.shape[0]), ceil(noiseless.shape[1]/interval)])
    for channel in range(0, noiseless.shape[0]):
        index = 0  # Reduced data datum counter
        for datum in range(0, noiseless.shape[1], interval):
            reduced[channel][index]=noiseless[channel][datum]
            # TBD: Conserve remaining data
            index += 1

    return reduced

def sig_decimate(data, factors, order=8):
    print("Decimating...")
    reduced = decimate(data, factors[0], order, ftype='iir')
    print(reduced.shape)

    # Preform recursion in accordence with interval factors
    if len(factors) > 1:
        reduced = sig_decimate(reduced, factors = factors[1:], order=order) # Slice a factor off and run recursion
    return reduced

# Main
if __name__ == "__main__":

    print("TDMS Signal Downsampler\nBy Mason Becker\n")

    # Data reading
    file = DM.get_filepaths(r"Input")

    print("Input:")
    for doc in file:
        print(doc)
    print("Total files: " + str(len(file)) + "\n")

    # UI
    while True:
        try:
            # Custom output parameters
            print("Decimate factor:")
            intervalConfig = int(input())
            print("Output:\n1. Mat file\n2. Mat file and interactable figure\n3. Interactable figure")
            outConfig = int(input())
            if outConfig > 3 or outConfig < 1:
                raise Exception
            if outConfig == 1:
                print("Compair raw and decimated? [Warning: This may be very computationally taxing if used on a large set of data.]\n1. No\n2. Yes")
                if input() != '2':
                    keep_raw = False
                else:
                    keep_raw = True
            if outConfig > 1:
                print("Compair raw and decimated? [Warning: This may be very computationally taxing if used on a large set of data.]\n1. No\n2. Yes")
                if input() != '2':
                    keep_raw = False
                    print("Compair:\n1. Color plot\n2. Individual channel")
                    if input() == '1':
                        color_chart = True
                    else:
                        color_chart = False
                        print("Set figure channel:")
                        channel = int(input())
                else:
                    keep_raw = True
                    print("Compair:\n1. Color plot\n2. Individual channels")
                    if input() == '1':
                        color_chart = True
                    else:
                        color_chart = False
                        print("Set figure channel:")
                        channel = int(input())
            break
        except:
            print("Invalid input")
            continue

    # Iterates between each file
    starttime = time()
    print(factorize(intervalConfig))
    for doc in range(len(file)):
        print("File (" + str(doc) + "/" + str(len(file)) + ")")

        # Retreves tdms data
        if doc > 0:
            dataB = DM.tdms_read(file[doc - 1])
        data = DM.tdms_read(file[doc])
        if doc < len(file) - 1:
            dataA = DM.tdms_read(file[doc + 1])
        # Accumulates the 3 portions into one data set
        if doc == 0 and doc < len(file) - 1: # Only after
            data_sum = append(data, dataA, 1)
        elif doc > 0 and doc == len(file) - 1: # Only before
            data_sum = append(dataB, data, 1)
        elif doc > 0 and doc < len(file) - 1: # Before and after
            data_sum = append(dataB, append(data, dataA, 1), 1)
        else: # If only one file
            data_sum = data
        print("Collected matrix: " + str(data_sum.shape))

        # Decimates with account to the specified data's neighbores
        reduce_data = sig_decimate(data_sum, factorize(intervalConfig))
        print(str(doc) + " decimated shape: " + str(reduce_data.shape))

        # Create data matrix
        if doc == 0:
            trimmed = reduce_data[:, 0 : ceil(data.shape[1]/intervalConfig)]
            print("Trimmed shape: " + str(trimmed.shape))
            matrix = trimmed
            if keep_raw: 
                raw_matrix = data
        else:
            matrix = append(matrix, reduce_data[:, ceil(dataB.shape[1]/intervalConfig) : ceil(dataB.shape[1]/intervalConfig) + ceil(data.shape[1]/intervalConfig)], 1)
            if keep_raw: 
                raw_matrix = append(raw_matrix, data, 1)
    # Data analysis
    print("Time Spent: " + str(time() - starttime) + "s")
    print("Final matrix shape: " + str(matrix.shape))

    # Data export
    if outConfig < 3:
        DM.mat_save(matrix)
        if keep_raw:
            DM.mat_save(raw_matrix, 'Output/Out_Raw.mat')
    if outConfig > 1:
        # Desides what figure output
        if keep_raw: 
            if color_chart:
                PL.interactable_compairson(raw_matrix, matrix, intervalConfig)
            else:
                PL.direct_compare(raw_matrix, matrix, channel, 0, raw_matrix.shape[1], intervalConfig)
        else: 
            if color_chart:
                PL.waterfall_plot(matrix)
            else:
                PL.channel_plot(matrix, channel)