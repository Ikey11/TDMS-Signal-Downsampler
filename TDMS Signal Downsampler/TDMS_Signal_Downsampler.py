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
    # Data reading
    file = DM.get_filepaths(r"Input")

    # Iterates between each file
    first = True
    for doc in file:
        # Retreves tdms data
        data = DM.tdms_read(doc)
        print(doc + " shape: " + str(data.shape))

        # Proforms individual decimation process for data handling
        reduce_data = sig.decimate(data, 2)
        print(doc + " decimated shape: " + str(reduce_data.shape))

        # Create data matrix
        if first:
            matrix = reduce_data
            first = False
        else:
            matrix = np.append(matrix, reduce_data, 1)

    # Preform anti-aliasing process

    # Data analysis
    print("Final matrix shape: " + str(matrix.shape))
    print(matrix)

    # Data export
    PL.channel_plot(matrix, 32)