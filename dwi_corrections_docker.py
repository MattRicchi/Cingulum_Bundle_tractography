#!/usr/bin/env python3
'''
Script per la correzioni di DWI in assenza della RevPol.
INPUTS: cartella contenente t1.nii.gz, b0.nii.gz e acqparam.txt
OUTPUTS: viene creata durante l'esecuzione e contiene i risultati del Docker
licence.txt: file con licenza di freesurfer, deve essere nella working directory
Dopo il docker, lo script esegue eddy. I file bvals.bval, bvecs.bvec e index.txt devono essere nella working directory
I risultati vengono salvati nella cartella Corrected_diffusion_data
Dopo eddy viene lanciato dtifit, i risultati sonoo salvati nella cartella DTI_results
'''

import subprocess
import os 
from fsl.wrappers import eddy, fslroi, bet, dtifit
import time

start = time.time()

data_path = '/mnt/c/Users/ricch/OneDrive/Desktop/ADNI/Converted_Nii_Files/'

os.chdir(data_path)
os.makedirs('Corrected_diffusion_data', exist_ok = True)
os.makedirs('DTI_results', exist_ok = True)

user_input = input("Is the Docker engine running? (yes/no) ['yes']: ").lower()

if user_input == 'yes' or user_input == '':
    # Run the Docker command for distorsions correction
    docker_command = "docker run --rm -v $(pwd)/INPUTS/:/INPUTS/ -v $(pwd)/OUTPUTS:/OUTPUTS/ -v $(pwd)/license.txt:/extra/freesurfer/license.txt --user $(id -u):$(id -g) leonyichencai/synb0-disco:v3.0"

    # Use subprocess.Popen to run the Docker command
    process = subprocess.Popen(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Print the output in real-time
    for line in process.stdout:
        print(line, end='')

    # Wait for the process to finish
    process.wait()

    # Check the exit code
    if process.returncode == 0:
        print("Docker command completed successfully, starting eddy now...")

        os.chdir(os.path.join(data_path, 'OUTPUTS'))

        fslroi('b0_u.nii.gz', 'b0_volume.nii.gz', 0, 1)
        bet('b0_volume.nii.gz', 'b0_brain.nii.gz', mask = True)

        os.chdir(data_path)

        eddy('DTI_data.nii.gz', mask = 'OUTPUTS/b0_brain.nii.gz', index = 'index.txt', acqp = 'INPUTS/acqparams.txt',bvals = 'bvals.bval', 
             bvecs = 'bvecs.bvec', topup = 'OUTPUTS/topup', out = 'Corrected_diffusion_data/eddy_corrected_data', data_is_shelled = True, verbose = True)
        
        # Extract the b=0 volume
        print('Extracting the B0_volume')
        fslroi('Corrected_diffusion_data/eddy_corrected_data.nii.gz', 'Corrected_diffusion_data/B0_volume.nii.gz', 0, 1)
        eddy_B0_volume = 'Corrected_diffusion_data/B0_volume.nii.gz'

        # Brain extract the b=0 volume
        print('Brain extracting the b0 volume')
        bet(eddy_B0_volume, 'Corrected_diffusion_data/B0_brain.nii.gz', mask = True)

        # Now run the DTI fit 
        print('eddy correct done! Starting DTI fit...')
        dtifit('Corrected_diffusion_data/eddy_corrected_data.nii.gz', 'DTI_results/DTIFit', 'Corrected_diffusion_data/B0_brain_mask.nii.gz', 
               'bvecs.bvec', 'bvals.bval', verbose = True)
        
        end = time.time()

        print('All done! Total time for script: ', (end - start) / (60), ' minutes.' )
        print('Now you can run Register_ROIs_to_diffusion_space.py')

    else:
        print("ERROR: Docker command failed with exit code", process.returncode)
elif user_input == 'no':
    print('Please, start the Docker engine and run the script again.')
else:
    print("Invalid input. Please enter 'yes' or 'no'.")

