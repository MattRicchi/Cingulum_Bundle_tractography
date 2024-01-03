import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
from itertools import combinations

# Load the CSV data into DataFrames
ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv')
mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv')

measures = ['FA', 'MD', 'RD']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

def run_t_test(df1, df2, measure, tract, side, group1_name, group2_name):
    group1_data = np.array(df1[(df1['measure'] == measure) & (df1['tract'] == tract) & (df1['side'] == side) & (df1['mean'] != 0.0)]['mean'])
    group2_data = np.array(df2[(df2['measure'] == measure) & (df2['tract'] == tract) & (df2['side'] == side) & (df2['mean'] != 0.0)]['mean'])
    
    t_statistic, p_value = ttest_ind(group1_data, group2_data)

    return pd.Series([f'{group1_name} vs {group2_name}', measure, f'{tract}_{side}', t_statistic, p_value],
                     index=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

# Perform t-tests and populate the results DataFrame
group_combinations = list(combinations([('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)], 2))

for (group1_name, group1_df), (group2_name, group2_df) in group_combinations:
    for measure in measures:
        for tract in tracts:
            for side in sides:
                results_df = results_df._append(
                    run_t_test(group1_df, group2_df, measure, tract, side, group1_name, group2_name),
                    ignore_index=True
                )

# Extract p-values for FDR correction separately for each measure
for measure in measures:
    measure_indices = results_df['Measure'] == measure
    p_values = results_df.loc[measure_indices, 'P-value']

    # Perform FDR correction
    reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

    # Update the results DataFrame with corrected p-values
    results_df.loc[measure_indices, 'Corrected p-value'] = corrected_p_values
    results_df.loc[measure_indices, 'Reject Null Hypothesis'] = reject

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Ttest_results.xlsx', index=False)


# Extract p-values for FDR correction separately for each measure
for measure in measures:
    measure_indices = results_df['Measure'] == measure
    p_values = results_df.loc[measure_indices, 'P-value']

    # Perform FDR correction
    reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

    # Update the results DataFrame with corrected p-values
    results_df.loc[measure_indices, 'Corrected p-value'] = corrected_p_values
    results_df.loc[measure_indices, 'Reject Null Hypothesis'] = reject

# # Add a comparison between the tracts
# for measure in measures:
#     for side in sides:
#         group_combinations = list(combinations(tracts, 2))
#         for tract1, tract2 in group_combinations:
#             p_values_tract = []
#             for group_name, group_df in [('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)]:
#                 group1_data = np.array(group_df[(group_df['measure'] == measure) & (group_df['tract'] == tract1) & (group_df['side'] == side) & (group_df['mean'] != 0.0)]['mean'])
#                 group2_data = np.array(group_df[(group_df['measure'] == measure) & (group_df['tract'] == tract2) & (group_df['side'] == side) & (group_df['mean'] != 0.0)]['mean'])
#                 t_statistic, p_value = ttest_ind(group1_data, group2_data)
#                 p_values_tract.append(p_value)

#             # Perform FDR correction for tract comparison
#             reject, corrected_p_values, _, _ = multipletests(p_values_tract, alpha=0.05, method='fdr_bh')

#             # Update the results DataFrame with tract comparison results
#             results_df = results_df._append(
#                 pd.Series([f'{tract1}_{side} vs {tract2}_{side}', measure, f'TractComparison_{side}', t_statistic, p_value, corrected_p_values, reject],
#                           index=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value', 'Corrected p-value', 'Reject Null Hypothesis']),
#                 ignore_index=True
#             )

# # Save the results to an Excel file
# results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Ttest_results.xlsx', index=False)