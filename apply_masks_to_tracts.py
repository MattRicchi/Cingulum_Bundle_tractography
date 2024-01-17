#!/usr/bin/env python3

import os
from Cingulum_Bundle_tracts.edit_tracts import threshold_tracts
from ROIs_and_Masks.masks_to_b0_space import register_masks_to_b0

for patient in range (1, 6):
    print(f'Working in Patient {patient}')
    data_path = f'/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/control/Control_{patient}/Converted_Nii_Files/'
    MNI_masks_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/Masks_MNI/'
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