#!/usr/bin/env python3
import subprocess

##################################################################################
############################### SUBGENUAL TRACT ##################################
##################################################################################

def subgenual_tract(sides):
    print('Reconstructing Subgenual Cingulum tract')

    for side in sides:
        # Generate the command to run tckgen for the Subgenual tract
        tckgen_command = f'tckgen FODs/FOD_wm.nii.gz -fslgrad bvecs.bvec bvals.bval -seed_image ROIs_to_DWI/1_{side}_to_DWI.nii.gz -include ROIs_to_DWI/2_{side}_to_DWI.nii.gz -exclude ROIs_to_DWI/midsagittal_to_DWI.nii.gz -mask Corrected_diffusion_data/B0_brain_mask.nii.gz -force Subgenual_{side}_tract.tck'

        # Generate the command to run tckmap for the Subgenual tract
        tckmap_command = f'tckmap -template DTI_results/DTIFit_FA.nii.gz Subgenual_{side}_tract.tck -force Subgenual_{side}_tract.nii.gz'

        # Now run tckgen
        process = subprocess.Popen(tckgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Print the output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the process to finish
        process.wait()

        # Check the exit code
        if process.returncode == 0:
            print("tckgen command completed successfully, starting tckmap...")

            process_fod = subprocess.Popen(tckmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Print the output in real-time
            for line in process_fod.stdout:
                print(line, end='')

            # Wait for the process to finish
            process_fod.wait()

            # Check the exit code
            if process_fod.returncode == 0:
                print('Subgenual tract generated succesfully.')

            else:
                print('ERROR: tckmap failed with exit code: ', process_fod.returncode)
                exit()

        else:
            print("ERROR: tckgen command failed with exit code", process.returncode)
            exit()

##################################################################################
############################# RETROSPLENIAL TRACT ################################
##################################################################################

def retrosplenial_tract(sides):
    print('Reconstructing Restrosplenial Cingulum tract')

    for side in sides:
        # Generate the command to run tckgen for the Subgenual tract
        tckgen_command = f'tckgen FODs/FOD_wm.nii.gz -fslgrad bvecs.bvec bvals.bval -seed_image ROIs_to_DWI/3_{side}_to_DWI.nii.gz -include ROIs_to_DWI/4_{side}_to_DWI.nii.gz -exclude ROIs_to_DWI/midsagittal_to_DWI.nii.gz -mask Corrected_diffusion_data/B0_brain_mask.nii.gz -force Retrosplenial_{side}_tract.tck'

        # Generate the command to run tckmap for the Subgenual tract
        tckmap_command = f'tckmap -template DTI_results/DTIFit_FA.nii.gz Retrosplenial_{side}_tract.tck -force Retrosplenial_{side}_tract.nii.gz'

        # Now run tckgen
        process = subprocess.Popen(tckgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Print the output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the process to finish
        process.wait()

        # Check the exit code
        if process.returncode == 0:
            print("tckgen command completed successfully, starting tckmap...")

            process_fod = subprocess.Popen(tckmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Print the output in real-time
            for line in process_fod.stdout:
                print(line, end='')

            # Wait for the process to finish
            process_fod.wait()

            # Check the exit code
            if process_fod.returncode == 0:
                print('Retrosplenial tract generated succesfully.')

            else:
                print('ERROR: tckmap failed with exit code: ', process_fod.returncode)
                exit()

        else:
            print("ERROR: tckgen command failed with exit code", process.returncode)
            exit()

##################################################################################
############################ PARAHIPPOCAMPAL TRACT ###############################
##################################################################################

def parahippocampal_tract(sides):
    print('Reconstructing Parahippocampal Cingulum tract')

    for side in sides:
        # Generate the command to run tckgen for the Subgenual tract
        tckgen_command = f'tckgen FODs/FOD_wm.nii.gz -fslgrad bvecs.bvec bvals.bval -seed_image ROIs_to_DWI/5_{side}_to_DWI.nii.gz -include ROIs_to_DWI/4_{side}_to_DWI.nii.gz -exclude ROIs_to_DWI/3_{side}_to_DWI.nii.gz -exclude ROIs_to_DWI/6_{side}_to_DWI.nii.gz -exclude ROIs_to_DWI/midsagittal_to_DWI.nii.gz -mask Corrected_diffusion_data/B0_brain_mask.nii.gz -force Parahippocampal_{side}_tract.tck'

        # Generate the command to run tckmap for the Subgenual tract
        tckmap_command = f'tckmap -template DTI_results/DTIFit_FA.nii.gz Parahippocampal_{side}_tract.tck -force Parahippocampal_{side}_tract.nii.gz'

        # Now run tckgen
        process = subprocess.Popen(tckgen_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Print the output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the process to finish
        process.wait()

        # Check the exit code
        if process.returncode == 0:
            print("tckgen command completed successfully, starting tckmap...")

            process_fod = subprocess.Popen(tckmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Print the output in real-time
            for line in process_fod.stdout:
                print(line, end='')

            # Wait for the process to finish
            process_fod.wait()

            # Check the exit code
            if process_fod.returncode == 0:
                print('tckmap completed succesfully.')
                print('All tracts generate correctly! Now masks_to_b0_space.py')

            else:
                print('ERROR: tckmap failed with exit code: ', process_fod.returncode)
                exit()

        else:
            print("ERROR: tckgen command failed with exit code", process.returncode)
            exit()

