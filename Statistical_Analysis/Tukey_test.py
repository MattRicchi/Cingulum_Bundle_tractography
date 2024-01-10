import pandas as pd
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load the CSV data into DataFrames
ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics_mean.csv')
mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics_mean.csv')
cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics_mean.csv')

merged_df = pd.concat([ad_df, mci_df, cn_df], ignore_index=True)
merged_df = merged_df[merged_df['side'] == 'mean_LR']

measures = ['FA', 'MD', 'RD']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']

# Create an Excel writer object
excel_writer = pd.ExcelWriter('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Tukey_groups_results.xlsx', engine='xlsxwriter')

# Perform a Tukey test and p-value correction for each measurement separately
for measure in measures:
    # Define empty DataFrame for final results
    results_groups_df = pd.DataFrame(columns=['group1', 'group2', 'meandiff', 'p-adj', 'tract'])

    # Compare the groups for each tract
    for tract in tracts:
        data_df = merged_df[(merged_df['measure'] == measure) & (merged_df['tract'] == tract)]
        all_data = np.array(data_df['mean'])
        all_labels = np.array(data_df['group'])

        # Tukey HSD test
        tukey_results = pairwise_tukeyhsd(all_data, all_labels)

        # Append the results to the results_groups_df
        tukey_results_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])
        tukey_results_df['tract'] = tract  # Move this line outside the inner loop
        results_groups_df = results_groups_df._append(tukey_results_df, ignore_index=True)

    # Assign 'measure' outside the inner loop
    results_groups_df['measure'] = measure

    # Save the results to a sheet named after the metric
    results_groups_df.to_excel(excel_writer, sheet_name=measure, index=False)

# Save and close the Excel file
excel_writer._save()
