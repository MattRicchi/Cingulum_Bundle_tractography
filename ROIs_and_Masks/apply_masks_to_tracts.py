#!/usr/bin/env python3

from fsl.wrappers import fslstats, fslmaths
import os
import subprocess
from Cingulum_Bundle_tracts.edit_tracts import threshold_tracts

data_path = '/mnt/c/Users/ricch/OneDrive/Desktop/ADNI/037_S_7011/Converted_Nii_Files_1/'
os.chdir(data_path)

tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']

soglia = 0.1

print('Applying threshold to each tract...')
for tract in tracts:
    for side in sides:
        # Extract the minimum and maximum value in the tract
        min, max = fslstats(f'{tract}_{side}_tract.nii.gz').R.run()

        # Define the effective cutoff threshold
        soglia_eff = soglia * int(max)

        # Apply threshold to the tract
        fslmaths(f'{tract}_{side}_tract.nii.gz').thr(soglia_eff).run(f'{tract}_{side}_tract_thr.nii.gz')

print('Starting to cut the tracts...')
threshold_tracts(tracts, sides)

print('All done!')