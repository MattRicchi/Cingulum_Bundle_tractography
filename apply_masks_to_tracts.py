#!/usr/bin/env python3

from fsl.wrappers import fslstats, fslmaths
import os
from Cingulum_Bundle_tracts.edit_tracts import threshold_tracts

data_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/CN_1/Converted_Nii_Files/'
os.chdir(data_path)
os.makedirs('Thresholded_masks', exist_ok = True)
os.makedirs('Cropped_tracts', exist_ok = True)

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
        fslmaths(f'{tract}_{side}_tract.nii.gz').thr(soglia_eff).run(f'Thresholded_masks/{tract}_{side}_tract_thr.nii.gz')

print('Starting to cut the tracts...')
threshold_tracts(tracts, sides)

print('All done!')