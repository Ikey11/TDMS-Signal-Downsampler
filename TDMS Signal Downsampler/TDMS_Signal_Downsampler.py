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

# Additional Functions
import plotlib as PL
import DataManager as DM

# Takes every n value out of a data set and creates a new reduced value
def downsample(data, interval):
    c = 0  # Counter
    reduced = np.empty([int(data.shape[0]), int(data.shape[1]/interval)])
    for channel in range(0, data.shape[0]):
        index = 0  # Reduced data datum counter
        for datum in range(0, data.shape[1]):
            c += 1
            if c == interval:
                reduced[channel][index]=data[channel][datum]
                index += 1
                c = 0

    return reduced

# Main
if __name__ == "__main__":

    # UI
    print("TDMS Signal Downsampler\nBy Mason Becker\n\n")
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
    

    # Data reading
    file = DM.get_filepaths(r"Input")

    # Iterates between each file
    first = True
    for doc in file:
        # Retreves tdms data
        data = DM.tdms_read(doc)
        print(doc + " shape: " + str(data.shape))

        # Proforms individual decimation process for data handling
        reduce_data = downsample(data, 1000)
        
        print(doc + " decimated shape: " + str(reduce_data.shape))

        # Create data matrix
        if first:
            matrix = reduce_data
            raw_matrix = data
            first = False
        else:
            matrix = np.append(matrix, reduce_data, 1)
            raw_matrix = np.append(raw_matrix, data, 1)

    # Preform anti-aliasing process

    # Data analysis
    print("Final matrix shape: " + str(matrix.shape))
    print("Raw:")
    print(raw_matrix)
    print("Reduced:")
    print(matrix)

    # Data export
    if outConfig < 3:
        DM.mat_save(matrix)
    if outConfig > 1:
        print("Channel: " + str(channel))
        for i in range(0, len(matrix[channel])):
            print(str(i) + ": " + str(matrix[channel][i]))
        # Sets limits or undoes erroneous limits
        if lim1 == lim2 == 0 or lim1 < 0 or lim2 > raw_matrix.shape[1] or lim1 > lim2:
            lim1 = 0
            lim2 = raw_matrix.shape[1]
        PL.interactable_compairson(raw_matrix, matrix, channel, lim1, lim2, 1000)