#!/usr/bin/env python3

import os
import csv
from fsl.wrappers import fslmaths, fslstats

tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']
measures = ['FA', 'MD', 'RD']

# Create a global CSV file to store data for all patients
output_csv_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv'

with open(output_csv_path, 'w') as global_csvfile:
    global_writer = csv.DictWriter(global_csvfile, fieldnames=['patient', 'tract', 'side', 'measure', 'mean', 'std'])
    global_writer.writeheader()

    for patient in range(1, 19):
        # # Skip patients 7 and 8
        # if patient in [7, 8]:
        #     print(f'Skipping patient {patient}...')
        #     continue

        print(f'Working in patient {patient}...')
        data_path = f'/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/MCI_{patient}/Converted_Nii_Files/'
        os.chdir(data_path)
        os.makedirs('DTI_metrics_tracts', exist_ok=True)

        # First compute the RD map as (L2+L3)/2
        os.chdir(os.path.join(data_path, 'DTI_results'))
        print('Computing RD map')
        fslmaths('DTIFit_L2.nii.gz').add('DTIFit_L3.nii.gz').div(2).run('DTIFit_RD.nii.gz')

        os.chdir(data_path)
        print('Extracting the DTI metrics from the tracts')
        
        for measure in measures:
            for tract in tracts:
                for side in sides:
                    # Extract the DTI metrics from the tracts
                    fslmaths(f'DTI_results/DTIFit_{measure}.nii.gz').mas(f'Cropped_tracts/{tract}_{side}_tract_cropped.nii.gz').run(
                        f'DTI_metrics_tracts/{measure}_{tract}_{side}.nii.gz')

                    # Save the mean and std for each metric
                    metric_mean, metric_std = fslstats(f'DTI_metrics_tracts/{measure}_{tract}_{side}.nii.gz').M.S.run()

                    # Write data to the global CSV file
                    global_writer.writerow({
                        'patient': patient,
                        'tract': tract,
                        'side': side,
                        'measure': measure,
                        'mean': metric_mean,
                        'std': metric_std
                    })
