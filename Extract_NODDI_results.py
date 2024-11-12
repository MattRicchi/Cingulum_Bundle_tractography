#!/usr/bin/env python3

import os
import csv
from fsl.wrappers import fslmaths, fslstats
from os.path import join

tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']
Bingham_measures = ['SD2BinghamDistributed_1_SD2Bingham_1_odi', 'Bingham_NDI', 'SD2BinghamDistributed_1_SD2Bingham_1_beta_fraction', 'partial_volume_0', 'partial_volume_1', 'SD2BinghamDistributed_1_partial_volume_0', 'Bingham_MSE']

# Create a global CSV file to store data for all patients
output_csv_path = 'path/for/file/with/output/data/global_tract_metrics.csv'

with open(output_csv_path, 'w') as global_csvfile:
    global_writer = csv.DictWriter(global_csvfile, fieldnames=['patient', 'tract', 'side', 'measure', 'mean', 'std'])
    global_writer.writeheader()

    for patient in range(1, 13):
        # Skip patients 7 and 8
        if patient in [7, 8]:
            print(f'Skipping patient {patient}...')
            continue

        CB_data_path = f'/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/AD_{patient}/Converted_Nii_Files/'

        print(f'Working in patient {patient}...')
        Bingham_data_path = f'/path/to/DATABASE/AD/AD_{patient}/Bingham_Fit_Results/'
        
        os.chdir(Bingham_data_path)
        os.makedirs('Bingham_metrics_tracts', exist_ok=True)

        print('Extracting the Bingham metrics from the tracts')
        
        for measure in Bingham_measures:
            for tract in tracts:
                for side in sides:
                    # Extract the Bingham metrics from the tracts
                    fslmaths(f'{measure}.nii').mas(join(CB_data_path, f'Cropped_tracts/{tract}_{side}_tract_cropped.nii.gz')).run(
                        f'Bingham_metrics_tracts/{measure}_{tract}_{side}.nii.gz')

                    # Save the mean and std for each metric
                    metric_mean, metric_std = fslstats(f'Bingham_metrics_tracts/{measure}_{tract}_{side}.nii.gz').M.S.run()

                    # Write data to the global CSV file
                    global_writer.writerow({
                        'patient': patient,
                        'tract': tract,
                        'side': side,
                        'measure': measure,
                        'mean': metric_mean,
                        'std': metric_std
                    })
