#!/usr/bin/env python3

import subprocess

def dwi_denoise(DWI_data):
    # Defie the denoise command
    dwidenoise_command = f'dwidenoise {DWI_data} DTI_data_denoised.nii.gz'

    # Use subprocess.Popen to run the denoise command
    process = subprocess.Popen(dwidenoise_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Print the output in real-time
    for line in process.stdout:
        print(line, end='')

    # Wait for the process to finish
    process.wait()

    # Check the exit code
    if process.returncode == 0:
        print('Denoising completed successfully!')
        return
    else:
        print('ERROR: Denoising failed with exit code', process.returncode)
        exit()