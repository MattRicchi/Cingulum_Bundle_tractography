import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests

# Load the CSV data into DataFrames
ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics_mean.csv')
mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics_mean.csv')
cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics_mean.csv')

measures = ['FA', 'MD', 'RD']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Comparison', 'Measure', 'Tract', 'T-statistic', 'P-value'])

def run_t_test(df1, df2, measure, tract, group1_name, group2_name):
    t_statistic, p_value = ttest_ind(
        np.array(df1[(df1['measure'] == measure) & (df1['tract'] == tract) & (df1['side'] == 'mean_LR')]['mean']),
        np.array(df2[(df2['measure'] == measure) & (df2['tract'] == tract) & (df2['side'] == 'mean_LR')]['mean'])
    )
    return pd.Series([f'{group1_name} vs {group2_name}', measure, f'{tract}', t_statistic, p_value],
                     index=['Comparison', 'Measure', 'Tract', 'T-statistic', 'P-value'])

# Perform t-tests and populate the results DataFrame
for group1_name, group1_df in [('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)]:
    for group2_name, group2_df in [('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)]:
        if group1_name != group2_name:
            for measure in measures:
                for tract in tracts:
                        results_df = results_df._append(run_t_test(group1_df, group2_df, measure, tract, group1_name, group2_name), ignore_index=True)

# Extract p-values for FDR correction
p_values_all = results_df['P-value']

# Perform FDR correction for all comparisons
reject_all, corrected_p_values_all, _, _ = multipletests(p_values_all, alpha=0.05, method='fdr_bh')

# Update the results DataFrame with corrected p-values for all comparisons
results_df['Corrected p-value'] = corrected_p_values_all
results_df['Reject Null Hypothesis'] = reject_all
print(results_df)

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Ttest_results.xlsx', index=False)