#!/usr/bin/env python3

import os
from fsl.wrappers import applywarp

def register_masks_to_b0(eddy_B0_volume, masks):
    masks_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/Masks_MNI/'

    # Register the masks to subject's diffusion space
    print('Starting to register the ROIs to subject space...')

    for mask in masks:
        print(f'Registering mask {mask}')
        MASK = os.path.join(masks_path, f'MASK_CB_{mask}.nii.gz')
        applywarp(MASK, ref = eddy_B0_volume, out = f'MASKSs_to_DWI/MASK_{mask}_to_DWI.nii.gz', 
                  warp = 'T1_weighted/MNItoT1_warp.nii.gz', postmat = 'T1_weighted/T1_2_b0.mat', interp = 'nn')

    print('Done registering the masks to the b0 space!')