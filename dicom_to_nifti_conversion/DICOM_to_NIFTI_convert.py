#!/usr/bin/env python3

import os
import time

from create_directory import create_new_directory, DCM2Nii_Directory

folder_to_convert = '/mnt/c/Users/ricch/OneDrive - University of Pisa/DICOM/To_convert'
    
os.chdir(folder_to_convert)

folder_name = 'Converted_Nii_Files'
new_folder_name = create_new_directory(folder_name)

SaveLoc = '' + new_folder_name

print('Directory is called: ' + folder_to_convert)

print('Starting to convert this directory, could take a while...')

start = time.time()

try:    
    DCM2Nii_Directory(folder_to_convert, SaveLoc)
    print('Complete')
except:
    print('Failed to convert all files.')

end = time.time()

print("Time consumed in converting directory: ", (end - start)/60, ' minutes')

