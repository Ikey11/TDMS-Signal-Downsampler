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


# Main
if __name__ == "__main__":

    # UI
    print("TDMS Signal Downsampler\nBy Mason Becker\n\n")
    while True:
        try:
            # Custom decimation parameters
            print("Decimation Amount (1-13):")
            downsamConfig = int(input())
            if downsamConfig < 1:
                raise Exception
            # Custom output parameters
            print("Output:\n1. Mat file\n2. Mat file and interactable figure\n3. Interactable figure")
            outConfig = int(input())
            if outConfig > 3 or outConfig < 1:
                raise Exception
            if outConfig > 1:
                print("Set custom limit for graph analysis?\n1. Yes\n2. No")
                c = input()
                if c == '2':
                    lim1 = lim2 = 0
                else:
                    print("Set lim1:")
                    lim1 = int(input())
                    print("Set lim2:")
                    lim2 = int(input())
                print("Set channel:")
                channel = int(input())
            break
        except TypeError:
            print("Not a number")
            continue
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
        reduce_data = sig.decimate(data, int(downsamConfig), ftype='iir')
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

    # Data export
    if outConfig < 3:
        DM.mat_save(data)
    if outConfig > 1:
        # Sets limits or undoes erroneous limits
        if lim1 == lim2 == 0 or lim1 < 0 or lim2 > matrix.shape[1] or lim1 > lim2:
            lim1 = 0
            lim2 = matrix.shape[1]
        PL.interactable_compairson(raw_matrix, matrix, channel, lim1, lim2, downsamConfig)