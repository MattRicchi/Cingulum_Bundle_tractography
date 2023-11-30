#!/usr/bin/env python3

import os
import shutil
from fsl.wrappers import applywarp, fslmaths, flirt

data_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/control/'
masks_MNI_folder = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/Masks_MNI/'
brain_reference = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/Brain_references/'

os.chdir(data_path)

MNI_2mm = os.path.join(brain_reference, 'MNI152_T1_2mm.nii.gz')

tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']

for control in range(1, 6):
    # Enter the control folder
    os.chdir(os.path.join(data_path, f'Control_{control}/Converted_Nii_Files/'))
    print(f'Working in control_{control}...')
    
    # Register the B0 eddy corrected volume to the T1
    print('Registering the b0 volume to the T1')
    flirt('Corrected_diffusion_data/B0_volume.nii.gz', 'INPUTS/t1.nii.gz', cost = 'mutualinfo', dof = 6, 
          out = 'Corrected_diffusion_data/B0toT1.nii.gz', omat = 'Corrected_diffusion_data/B0toT1.mat')
    
    # Create a new folder to save the tracts to the MNI
    os.makedirs('Tracts_to_MNI', exist_ok = True)

    # Now register the tracts to the MNI space and binarize them
    for tract in tracts:
        for side in sides:
            print(f'Registering tract {tract}_{side} to MNI')
            applywarp(f'{tract}_{side}_tract.nii.gz', ref = MNI_2mm, out = f'Tracts_to_MNI/{tract}_{side}_tract_MNI.nii.gz', 
                      warp = 'T1_weighted/T1toMNI_warp.nii.gz', premat = 'Corrected_diffusion_data/B0toT1.mat', interp = 'nn', verbose = True)
            
            print(f'Binarizing tract {tract}_{side}')
            fslmaths(f'Tracts_to_MNI/{tract}_{side}_tract_MNI.nii.gz').bin().run(f'Tracts_to_MNI/{tract}_{side}_tract_MNI_bin.nii.gz')

# Now copy the control_1 tracts into the Masks_MNI folder 
os.chdir(os.path.join(data_path, 'Control_1/Converted_Nii_Files/Tracts_to_MNI/'))
print('Copying control 1 tracts to MASK MNI folder')
for tract in tracts:
    for side in sides:
        shutil.copy2(f'{tract}_{side}_tract_MNI_bin.nii.gz', f'{masks_MNI_folder}/MASK_CB_{tract}_{side}.nii.gz')

# Now sum all the tract together to obtain the masks
os.chdir(data_path)
print('starting to sum all the tracts together to get the masks')

for control in range(2, 6):
    # Enter the control folder
    os.chdir(os.path.join(data_path, f'Control_{control}/Converted_Nii_Files/Tracts_to_MNI'))

    for tract in tracts:
        for side in sides:
            mask = os.path.join(masks_MNI_folder, f'MASK_CB_{tract}_{side}.nii.gz')
            fslmaths(mask).add(f'{tract}_{side}_tract_MNI_bin.nii.gz').run(mask)
