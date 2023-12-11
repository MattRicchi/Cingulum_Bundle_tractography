#!/usr/bin/env python3

import os
from fsl.wrappers import flirt, fnirt, applywarp, invwarp

def register_ROIs_to_b0(eddy_B0_volume, T1_weighted, ROIs):
      # Define the useful paths and files
      ROIs_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/ROIs/'
      MNI_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/Brain_references/'
    
      MNI_2mm = os.path.join(MNI_path, 'MNI152_T1_2mm.nii.gz')
      config_file = os.path.join(MNI_path, 'T1_2_MNI152_2mm.cnf')

      # Register the T1 to the b=0 volume
      print('Registering the T1 to the B0')
      flirt(T1_weighted, eddy_B0_volume, dof = 6, cost = 'mutualinfo', out = 'T1_weighted/T1_2_b0.nii.gz', omat = 'T1_weighted/T1_2_b0.mat')
    
      # Register the T1 volume to the MNI space
      print('Registering the T1 to MNI')
      flirt(T1_weighted, MNI_2mm, dof = 12, out = 'T1_weighted/T1toMNI_flirt.nii.gz', omat = 'T1_weighted/T1toMNI_flirt.mat')
      fnirt(T1_weighted, config = config_file, aff = 'T1_weighted/T1toMNI_flirt.mat', 
            iout = 'T1_weighted/T1toMNI_fnirt.nii.gz', fout = 'T1_weighted/T1toMNI_warp.nii.gz')
    
      # Invert the transformation to get the warp from the MNI to the T1 space
      print('Inverting transformation to obtain MNI to T1 warp')
      invwarp('T1_weighted/T1toMNI_warp.nii.gz', T1_weighted, 'T1_weighted/MNItoT1_warp.nii.gz', verbose = True)
    
      # Register the ROIs to the diffusion space of the subject
      print('Starting to register the ROIs to subject space...')
    
      for roi in ROIs:
            print(f'Registering {roi}')
            ROI = os.path.join(ROIs_path, f'{roi}.nii.gz')
            applywarp(ROI, ref = eddy_B0_volume, out = f'ROIs_to_DWI/{roi}_to_DWI.nii.gz', warp = 'T1_weighted/MNItoT1_warp.nii.gz', 
                      postmat = 'T1_weighted/T1_2_b0.mat', interp = 'nn', verbose = True)
      
      print('All done! ROIs registered to B0 space.')
