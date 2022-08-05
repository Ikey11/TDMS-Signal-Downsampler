'''DataManager
Retrieves files and TDMS file data

'''

import os
import numpy as np
import scipy.io
from nptdms import TdmsFile
from nptdms import tdms


# Extracts the filepaths of all TDMS files in directory
def get_filepaths(directory):
    file_paths = []

    # Walk the tree
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Filter out unsupported files
            if os.path.splitext(filename)[1] != '.tdms':
                continue
            # Create the filepath name
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    # Ensure files are alphabetical
    file_paths.sort()

    return file_paths

def tdms_read(file):
    tdms_file = TdmsFile(file)
    measurements = tdms_file['Measurement']
    data = np.empty([len(measurements.channels()), len(measurements['0'])])
    i = 0
    for channel in measurements.channels():
        data[i][:] = channel[:]
        i += 1
    return data

# Exports decimated data to a .mat file for matlab usage
def mat_save(data):
    scipy.io.savemat("Output/Out.mat", data)

# Exports decimated data back into a tdms file
def tdms_save(data):
    print("cat")