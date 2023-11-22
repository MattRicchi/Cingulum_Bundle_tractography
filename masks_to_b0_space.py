#!/usr/bin/env python3

import os
from fsl.wrappers import applywarp

# Define the directory of the dwi data
data_path = "/mnt/c/Users/ricch/OneDrive/Desktop/ADNI/037_S_7011/Converted_Nii_Files_1"
os.chdir(data_path)
os.makedirs('MASKSs_to_DWI', exist_ok = True)

masks_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/Masks_MNI/'

eddy_B0_volume = 'Corrected_diffusion_data/B0_volume.nii.gz'

masks = ['1_L', '1_R', '2_L', '2_R', '3_L', '3_R']

# Register the masks to subject's diffusion space
print('Starting to register the ROIs to subject space...')

for mask in masks:
    print(f'Registering mask {mask}')
    MASK = os.path.join(masks_path, f'MASK_CB_{mask}.nii.gz')
    applywarp(MASK, ref = eddy_B0_volume, out = f'MASKSs_to_DWI/MASK_{mask}_to_DWI.nii.gz', 
              warp = 'T1_weighted/MNItoT1_warp.nii.gz', postmat = 'T1_weighted/T1_2_b0.mat', interp = 'nn')

print('Done registering the masks to the b0 space! Now run apply_masks_to_tracts.py')