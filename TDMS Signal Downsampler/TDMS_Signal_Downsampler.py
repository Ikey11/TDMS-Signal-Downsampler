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

## Attempts to produce a unique factorization for input integer
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

## Runs Scipy's decimation command recursively using factorized intervals to fit the function's parameters
def sig_decimate(data, factors, order=8):
    print("Decimating...")
    reduced = decimate(data, factors[0], order, ftype='iir')
    print(reduced.shape)

    # Preform recursion in accordence with interval factors
    if len(factors) > 1:
        reduced = sig_decimate(reduced, factors = factors[1:], order=order) # Slice a factor off and run recursion
    return reduced

## Main Process
if __name__ == "__main__":

    # Credits
    print("TDMS Signal Downsampler\nBy Mason Becker\n")

    # Find each avaliable file in Input directory
    file = DM.get_filepaths(r"Input")
    # User confirmation
    print("Input:")
    for doc in file:
        print(doc)
    print("Total files: " + str(len(file)) + "\n")

    # Specify file parameters
    while True:
        try:
            # Decimation factor
            print("Decimate factor (Ensure number consists of prime factors under 13):")
            intervalConfig = int(input())
            factors = factorize(intervalConfig)
            # Display working method and present warnings
            print("Factors: {0}".format(factors))
            for factor in factors:
                if factor > 13:
                    print("Warning: decimation factor contains prime factors over 13, this may lead to an inaccurate output.")
                    print("Continue with decimation?\n1. Yes\n2. No")
                    if input() != '1':
                        raise Exception("Resetting...")
                    else:
                        break

            # Determine output type
            print("Output type:\n1. MatLab file\n2. MatLab file and interactable figure\n3. Interactable figure")
            outConfig = int(input())
            if outConfig > 3 or outConfig < 1:
                print("Invalid input, please try again...")
                continue
            # MatLab output configuration
            if outConfig == 1:
                print("Output Set to MatLab file!")
                print("Compare raw and decimated data? [Warning: This may be very computationally taxing if used on a large set of data.]\n1. Yes\n2. No")
                if input() != '1':
                    keep_raw = False
                else:
                    keep_raw = True
            # Configuration for interactable figure
            if outConfig > 1:
                if outConfig == 2 : print("Output Set to MatLab file and Interactable figure!")
                else : print("Output Set to Interactable figure!")
                print("Compare raw and decimated data? [Warning: This may be very computationally taxing if used on a large set of data.]\n1. Yes\n2. No")
                if input() != '1':
                    keep_raw = False
                    print("Only outputting decimated data!")
                    print("Return:\n1. Color plot\n2. Individual channel")
                    if input() == '1':
                        color_chart = True
                    else:
                        color_chart = False
                        print("Set figure channel:")
                        channel = int(input())
                else:
                    keep_raw = True
                    print("Saving raw data for comparison!")
                    print("Compare:\n1. Color plot\n2. Individual channels")
                    if input() == '1':
                        color_chart = True
                    else:
                        color_chart = False
                        print("Set figure channel:")
                        channel = int(input())
            break # End user input
        except TypeError: # Prevent crashes due to casting
            print("Invalid input!")
        except: # For resetting the program
            print("Resetting...")

    starttime = time() # Begin timer
    # Iterates between each file
    for doc in range(len(file)):
        # Return progress
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

        # Decimates with account to the specified data's neighbores
        reduce_data = sig_decimate(data_sum, factors)
        print(str(doc) + " decimated shape: " + str(reduce_data.shape))

        # Create data matrix
        if doc == 0:
            # Trim excess and append data
            matrix = reduce_data[:, 0 : ceil(data.shape[1]/intervalConfig)]
            if keep_raw: 
                raw_matrix = data
        else:
            # Trim excess and append data
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