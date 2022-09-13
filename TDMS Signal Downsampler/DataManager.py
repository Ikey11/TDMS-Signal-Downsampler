'''DataManager
Retrieves files and TDMS file data

'''

from os import mkdir, walk  # File and folder managagment
from os.path import exists, splitext, join  # File reconition
from numpy import empty  # Data allocation
from scipy.io import savemat  # Saving .mat file
from nptdms import TdmsFile, tdms  # TDMS interactions


## Extracts the filepaths of all TDMS files in directory
def get_filepaths(directory = "Input"):
    # Creates input directory
    if not exists("Output"):
        mkdir("Output")
    if not exists(directory):
        mkdir(directory)
        print(directory + "and Output Directory made!\nInsert TDAS data and press enter to continue...")
        input()

    file_paths = []
    # Walk the tree
    for root, directories, files in walk(directory):
        for filename in files:
            # Filter out unsupported files
            if splitext(filename)[1] != '.tdms':
                continue
            # Create the filepath name
            filepath = join(root, filename)
            file_paths.append(filepath)
    # Ensure files are alphabetical
    file_paths.sort()

    return file_paths

## Packages all data from TDMS file into a single matrix
def tdms_read(file, min = 0, max = None):
    tdms_file = TdmsFile(file)
    print("Reading: " + tdms_file.properties['name'])
    measurements = tdms_file['Measurement']
    data = empty([len(measurements.channels()[min : max]), len(measurements[str(min)])])
    i = 0
    for channel in measurements.channels() if max == None else measurements.channels()[min : max]:
        data[i][:] = channel[:]
        i += 1
    print("Matrix created! Shape: " + str(data.shape))
    return data

## Exports decimated data to a .mat file for matlab usage
def mat_save(data, address="Output/Out.mat"):
    print("Saving...")
    savemat(address, {'Data' : data})
    print("Save complete!")