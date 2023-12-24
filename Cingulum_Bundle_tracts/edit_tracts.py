#!/usr/bin/env python3
import subprocess

def threshold_tracts(tracts, sides):
    for tract in tracts:
        for side in sides:
            # Define the tckedit command to cut the tracts basing on the thresholded masks
            tckedit_command = f'tckedit {tract}_{side}_tract.tck Cropped_tracts/{tract}_{side}_tract_cropped.tck -mask MASKSs_to_DWI/MASK_{tract}_{side}_to_DWI.nii.gz -force'

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
                tckmap_command = f'tckmap -template DTI_results/DTIFit_FA.nii.gz Cropped_tracts/{tract}_{side}_tract_cropped.tck -force Cropped_tracts/{tract}_{side}_tract_cropped.nii.gz'

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