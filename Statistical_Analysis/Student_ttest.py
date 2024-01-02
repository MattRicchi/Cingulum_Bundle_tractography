# import pandas as pd
# import numpy as np
# from scipy.stats import ttest_ind

# # Load the CSV data into DataFrames
# ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv')
# mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
# cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv')

# measures = ['FA', 'MD', 'RD']
# tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
# sides = ['L', 'R']

# print('------------------------------------')
# print('------------- CN vs AD -------------')
# print('------------------------------------')

# for measure in measures:
#     for tract in tracts:
#         for side in sides:
#             t_statistic, p_value = ttest_ind(np.array(cn_df[(cn_df['measure'] == measure) & (cn_df['tract'] == tract) & (cn_df['side'] == side)]['mean']), 
#                                              np.array(ad_df[(ad_df['measure'] == measure) & (ad_df['tract'] == tract) & (ad_df['side'] == side)]['mean']))

#             print(f'Student t-test of {measure} in {tract}_{side}')
#             print("T-statistic:", t_statistic)
#             print("P-value:", p_value)


# print('------------------------------------')
# print('------------- CN vs MCI -------------')
# print('------------------------------------')

# for measure in measures:
#     for tract in tracts:
#         for side in sides:
#             t_statistic, p_value = ttest_ind(np.array(cn_df[(cn_df['measure'] == measure) & (cn_df['tract'] == tract) & (cn_df['side'] == side)]['mean']), 
#                                              np.array(mci_df[(mci_df['measure'] == measure) & (mci_df['tract'] == tract) & (mci_df['side'] == side)]['mean']))

#             print(f'Student t-test of {measure} in {tract}_{side}')
#             print("T-statistic:", t_statistic)
#             print("P-value:", p_value)


# print('------------------------------------')
# print('------------- AD vs MCI -------------')
# print('------------------------------------')

# for measure in measures:
#     for tract in tracts:
#         for side in sides:
#             t_statistic, p_value = ttest_ind(np.array(ad_df[(ad_df['measure'] == measure) & (ad_df['tract'] == tract) & (ad_df['side'] == side)]['mean']), 
#                                              np.array(mci_df[(mci_df['measure'] == measure) & (mci_df['tract'] == tract) & (mci_df['side'] == side)]['mean']))

#             print(f'Student t-test of {measure} in {tract}_{side}')
#             print("T-statistic:", t_statistic)
#             print("P-value:", p_value)

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

# Extract p-values for FDR correction
p_values = results_df['P-value']

# Perform FDR correction
reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Add corrected p-values to the results DataFrame
results_df['Corrected p-value'] = corrected_p_values
results_df['Reject Null Hypothesis'] = reject

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Ttest_results.xlsx', index=False)
