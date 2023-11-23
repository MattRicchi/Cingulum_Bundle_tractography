#!/usr/bin/env python3

import os
import time
from fsl.wrappers import fslmaths, fslstats, bet, fslroi, eddy, dtifit
from preprocessing_functions.denoising import dwi_denoise
from preprocessing_functions.distorsions_correction import synb0_correct
from ROIs_and_Masks.Register_ROIs_to_diffusion_space import register_ROIs_to_b0
from create_FOD import create_FOD
from Cingulum_Bundle_tracts.generate_tracts import subgenual_tract, retrosplenial_tract, parahippocampal_tract
from ROIs_and_Masks.masks_to_b0_space import register_masks_to_b0

data_path = '/mnt/c/Users/ricch/OneDrive/Desktop/ADNI/patient_6/'

T1_weighted = 'INPUTS/t1.nii.gz'
eddy_corrected_data = 'Corrected_diffusion_data/eddy_corrected_data.nii.gz'
eddy_B0_volume = 'Corrected_diffusion_data/B0_volume.nii.gz'
ROIs = ['1_L', '1_R', '2_L', '2_R', '3_L', '3_R', '4_L', '4_R', '5_L', '5_R', '6_L', '6_R', 'midsagittal']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
masks = ['1', '2', '3']
sides = ['L', 'R']

os.chdir(data_path)
os.makedirs('Corrected_diffusion_data', exist_ok = True)
os.makedirs('DTI_results', exist_ok = True)
os.makedirs('T1_weighted', exist_ok = True)
os.makedirs('ROIs_to_DWI', exist_ok = True)
os.makedirs('FODs', exist_ok = True)
os.makedirs('MASKSs_to_DWI', exist_ok = True)

user_input = input("Please, make sure that the Docker Engine is running.").lower()
if user_input == '':
    pass

start = time.time()

# Start from DWI denoising
dwi_denoise('DTI_data.nii.gz')

# Extract b0 volume and save it into INPUTS folder
fslroi('DTI_data_denoised.nii.gz', 'INPUTS/b0.nii.gz', 0, 1)

# Run the DWI distorsions correction
synb0_correct()

# Brain extract the corrected data
os.chdir(os.path.join(data_path, 'OUTPUTS'))

fslroi('b0_u.nii.gz', 'b0_volume.nii.gz', 0, 1)
bet('b0_volume.nii.gz', 'b0_brain.nii.gz', mask = True)

os.chdir(data_path)

# Run eddy correct
print('Starting eddy...')
eddy('DTI_data_denoised.nii.gz', mask = 'OUTPUTS/b0_brain.nii.gz', index = 'index.txt', acqp = 'INPUTS/acqparams.txt',bvals = 'bvals.bval', 
     bvecs = 'bvecs.bvec', topup = 'OUTPUTS/topup', out = 'Corrected_diffusion_data/eddy_corrected_data', data_is_shelled = True, verbose = True)

# Extract the eddy corrected b=0 volume
print('Extracting the B0_volume')
fslroi(eddy_corrected_data, eddy_B0_volume, 0, 1)

# Brain extract the b=0 volume
print('Brain extracting the b0 volume')
bet(eddy_B0_volume, 'Corrected_diffusion_data/B0_brain.nii.gz', mask = True)

# Now run the DTI fit 
print('eddy correct done! Starting DTI fit...')
dtifit(eddy_corrected_data, 'DTI_results/DTIFit', 'Corrected_diffusion_data/B0_brain_mask.nii.gz', 
       'bvecs.bvec', 'bvals.bval', verbose = True)

# Now register the ROIs to the b0 subject space
print('Starting to register the ROIs to the subject diffusion space.')
register_ROIs_to_b0(eddy_B0_volume, T1_weighted, ROIs)

# Create FODs
print('Creating FODs...')
create_FOD()

# Generate the CB tracts
print('Generate the Subgenual tract')
subgenual_tract(sides)

print('Generating the Retrosplenial tract')
retrosplenial_tract(sides)

print('Generating Parahippocampal tract')
parahippocampal_tract(sides)

# Register the masks to the b0 subject space
# print('Registering the masks to the b0 subject space')
# register_masks_to_b0(eddy_B0_volume, masks)

end = time.time()
print('Time used to process: ', (end - start) / (60*60), 'hours.')