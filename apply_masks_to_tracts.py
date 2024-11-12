#!/usr/bin/env python3

import os
from Cingulum_Bundle_tracts.edit_tracts import threshold_tracts
from ROIs_and_Masks.masks_to_b0_space import register_masks_to_b0

patient_number = 18 # plase, update accordingly

for patient in range (1, patient_number):
    print(f'Working in Patient {patient}')
    data_path = '/path/to/subject/folder/'
    MNI_masks_path = 'path/to/masks/in/MNI/space/to/be/registered/to/subject/diffusion/space'
    os.chdir(data_path)
    os.makedirs('MASKSs_to_DWI', exist_ok = True)
    os.makedirs('Cropped_tracts', exist_ok = True)

    B0_volume = 'Corrected_diffusion_data/B0_volume.nii.gz'
    tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
    sides = ['L', 'R']

    # Register the masks to the subject space
    register_masks_to_b0(B0_volume, tracts, sides)

    print('Starting to cut the tracts...')
    threshold_tracts(tracts, sides)

    print('All done!')