#!/usr/bin/env python3

from fsl.wrappers import fslstats, fslmaths
import os
import subprocess

mask_path = '/mnt/c/Users/ricch/OneDrive/Desktop/ADNI/037_S_7011/Converted_Nii_Files_1/'
os.chdir(mask_path)

tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']
masks = ['1', '2', '3']

soglia = 0.1

print('Applying threshold to each mask...')
for mask in masks:
    for side in sides:
        # Extract the minimum and maximum value in the mask
        min, max = fslstats(f'MASKSs_to_DWI/MASK_{mask}_{side}_to_DWI.nii.gz').R.run()

        # Define the effective cutoff
        soglia_eff = soglia / int(max)

        # Apply threshold to the mask
        fslmaths(f'MASKSs_to_DWI/MASK_{mask}_{side}_to_DWI.nii.gz').thr(soglia_eff).run(f'MASKSs_to_DWI/MASK_{mask}_{side}_to_DWI_{soglia}.nii.gz')

print('Starting to cut the tracts...')
for tract in tracts:
    if tract == 'Subgenual':
        mask = '1'
    elif tract == 'Retrosplenial':
        mask = '2'
    elif tract == 'Parahippocampal':
        mask = '3'
    for side in sides:
        # Define the tckedit command to cut the tracts basing on the thresholded masks
        tckedit_command = f'tckedit {tract}_{side}_tract.tck {tract}_{side}_tract_cropped_{soglia}.tck -mask MASKSs_to_DWI/MASK_{mask}_{side}_to_DWI_{soglia}.nii.gz -force'

        # Now run tckedit
        print('Run tckedit')
        process = subprocess.Popen(tckedit_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Print the output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the process to finish
        process.wait()

        # Check the exit code
        if process.returncode == 0:
            print("tckedit command completed successfully, starting tckmap...")
    
            # poi tckmap per avere i tratti in .nii.gz
            tckmap_command = f'tckmap -template DTI_results/DTIFit_FA.nii.gz {tract}_{side}_tract_cropped_{soglia}.tck -force {tract}_{side}_tract_{soglia}.nii.gz'

            process_fod = subprocess.Popen(tckmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Print the output in real-time
            for line in process_fod.stdout:
                print(line, end='')

            # Wait for the process to finish
            process_fod.wait()

            # Check the exit code
            if process_fod.returncode == 0:
                print('tckmap completed succesfully.')

            else:
                print('ERROR: tckmap failed with exit code: ', process_fod.returncode)

        else:
            print("ERROR: tckedit command failed with exit code", process.returncode)

print('All done!')