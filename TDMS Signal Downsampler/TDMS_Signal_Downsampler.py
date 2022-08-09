"""TDMS Signal Downsampler


Functions
---------
Retreves and downsamples TDMS raw signal data.

Author
---------
Mason Becker

"""

# Imports
import numpy as np  # Array processing
import scipy as sy  # Various signal processing tools
import scipy.signal as sig
import time

# Additional Functions
import plotlib as PL
import DataManager as DM

# Low-pass filter
def lowpass_filter(data, interval, order=8):
    system = sig.dlti(*sig.cheby1(order, 0.05, 0.8 / interval))
    b, a = system.num, system.den
    y = sig.filtfilt(b, a, data, axis=-1)
    return y

# Takes every n value out of a data set and creates a new reduced value
def downsample(data, interval, order=8):
    print("Passing lowpass filter...")
    noiseless = lowpass_filter(data, interval, order)
    print("Downsampling...")
    reduced = np.empty([int(noiseless.shape[0]), int(noiseless.shape[1]/interval)])
    for channel in range(0, noiseless.shape[0]):
        index = 0  # Reduced data datum counter
        for datum in range(0, noiseless.shape[1], interval):
            reduced[channel][index]=noiseless[channel][datum]
            index += 1

    return reduced

# Main
if __name__ == "__main__":

    print("TDMS Signal Downsampler\nBy Mason Becker\n\n")

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
            print("Output:\n1. Mat file [NONFUNCTIONAL]\n2. Mat file and interactable figure\n3. Interactable figure")
            outConfig = int(input())
            if outConfig > 3 or outConfig < 1:
                raise Exception
            if outConfig > 1:
                print("Set custom limit for graph analysis?\n1. Yes\n2. No")
                c = input()
                if c == '1':
                    print("Set lim1:")
                    lim1 = int(input())
                    print("Set lim2:")
                    lim2 = int(input())
                else:
                    lim1 = lim2 = 0
                print("Set channel:")
                channel = int(input())
            break
        except:
            print("Invalid input")
            continue

    # Iterates between each file
    starttime = time.time()
    first = True
    for doc in file:
        # Retreves tdms data
        data = DM.tdms_read(doc)
        print(doc + " shape: " + str(data.shape))

        # Proforms individual decimation process for data handling
        reduce_data = downsample(data, 10)
        
        print(doc + " decimated shape: " + str(reduce_data.shape))

        # Create data matrix
        if first:
            matrix = reduce_data
            raw_matrix = data
            first = False
        else:
            matrix = np.append(matrix, reduce_data, 1)
            raw_matrix = np.append(raw_matrix, data, 1)

    # Data analysis
    print("Time Spent: " + str(time.time() - starttime) + "s")
    print("Final matrix shape: " + str(matrix.shape))
    print("Raw:")
    print(raw_matrix)
    print("Reduced:")
    print(matrix)

    # Data export
    if outConfig < 3:
        DM.mat_save(matrix)
    if outConfig > 1:
        # Sets limits or undoes erroneous limits
        if lim1 == lim2 == 0 or lim1 < 0 or lim2 > raw_matrix.shape[1] or lim1 > lim2:
            lim1 = 0
            lim2 = raw_matrix.shape[1]
        PL.interactable_compairson(raw_matrix, matrix, channel, lim1, lim2, 1000)