#!/usr/bin/env python3

import subprocess

def create_FOD():

    # Define the dwi2response and dwi2fod commands
    dwi2response_command = 'dwi2response dhollander Corrected_diffusion_data/eddy_corrected_data.nii.gz FODs/response_sfwm.txt FODs/response_gm.txt FODs/response_csf.txt -fslgrad bvecs.bvec bvals.bval -force'
    dwi2fod_command = 'dwi2fod msmt_csd -fslgrad bvecs.bvec bvals.bval Corrected_diffusion_data/eddy_corrected_data.nii.gz FODs/response_sfwm.txt FODs/FOD_wm.nii.gz FODs/response_gm.txt FODs/FOD_gm.nii.gz FODs/response_csf.txt FODs/FOD_csf.nii.gz'

    # Run the dwi2response command using subprocess.Popen 
    process = subprocess.Popen(dwi2response_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Print the output in real-time
    for line in process.stdout:
        print(line, end='')

    # Wait for the process to finish
    process.wait()

    # Check the exit code
    if process.returncode == 0:
        print("DWI2response command completed successfully, starting dwi2fod...")

        process_fod = subprocess.Popen(dwi2fod_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Print the output in real-time
        for line in process_fod.stdout:
            print(line, end='')

        # Wait for the process to finish
        process_fod.wait()

        # Check the exit code
        if process_fod.returncode == 0:
            print('DWI2fod completed succesfully.')
            print('All good! FODs generated correctly.')

        else:
            print('ERROR: DWI2fod failed with exit code: ', process_fod.returncode)
            exit()

    else:
        print("ERROR: DWI2response command failed with exit code", process.returncode)
        exit()

