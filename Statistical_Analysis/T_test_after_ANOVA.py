import pandas as pd
import numpy as np
from os.path import join
from itertools import combinations
from statsmodels.stats.multitest import multipletests
from scipy.stats import ttest_ind

database_path = '/path/to/DATABASE/'

# Load the CSV data into DataFrames
ad_df = pd.read_excel(join(database_path,'AD/global_tract_metrics_mean.xlsx'))
mci_df = pd.read_excel(join(database_path,'MCI/global_tract_metrics_mean.xlsx'))
cn_df = pd.read_excel(join(database_path,'CN/global_tract_metrics_mean.xlsx'))

measures = ['FA', 'MD', 'RD']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']

def run_t_test(df1, df2, measure, tract, group1_name, group2_name):

    group1_data = np.array(df1[(df1['measure'] == measure) & (df1['tract'] == tract) & (df1['side'] == 'mean_LR') & (df1['mean'] != 0.0)]['mean'])
    group2_data = np.array(df2[(df2['measure'] == measure) & (df2['tract'] == tract) & (df2['side'] == 'mean_LR') & (df2['mean'] != 0.0)]['mean'])

    t_statistic, p_value = ttest_ind(group1_data, group2_data)

    return pd.Series([f'{group1_name} vs {group2_name}', measure, f'{tract}', t_statistic, p_value],
                     index=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

# Perform a t test and p-value correction for each measurement separately
for measure in measures:
    # Define empty DataFrame for final results
    results_df = pd.DataFrame(columns=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

    group_combinations = list(combinations([('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)], 2))

    # Compare the groups
    for (group1_name, group1_df), (group2_name, group2_df) in group_combinations:
        for tract in tracts:
            results_df = results_df._append(
                run_t_test(group1_df, group2_df, measure, tract, group1_name, group2_name), ignore_index=True)
            
    # Extract p-values for FDR correction
    p_values_all = results_df['P-value']

    # Perform FDR correction for all comparisons
    reject_all, corrected_p_values_all, _, _ = multipletests(p_values_all, alpha=0.05, method='fdr_bh')

    # Update the results DataFrame with corrected p-values for all comparisons
    results_df['Corrected p-value'] = corrected_p_values_all
    results_df['Reject Null Hypothesis'] = reject_all
    print(results_df)

    # Save the results to an Excel file
    results_df.to_excel(join(database_path, f'{measure}_Ttest_GROUPS.xlsx'), index=False)

    # Define empty DataFrame for final results
    results_df_tracts = pd.DataFrame(columns=['Comparison', 'Measure', 'Group', 'T-statistic', 'P-value'])

    # Compare tracts within each group
    tract_combinations = list(combinations(tracts, 2))
    for tract1, tract2 in tract_combinations:
            for group_name, group_df in [('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)]:
                group1_data = np.array(group_df[(group_df['measure'] == measure) & (group_df['tract'] == tract1) & (group_df['side'] == 'mean_LR') & (group_df['mean'] != 0.0)]['mean'])
                group2_data = np.array(group_df[(group_df['measure'] == measure) & (group_df['tract'] == tract2) & (group_df['side'] == 'mean_LR') & (group_df['mean'] != 0.0)]['mean'])
                t_statistic, p_value = ttest_ind(group1_data, group2_data)

                # Update the results DataFrame with tract comparison results
                results_df_tracts = results_df_tracts._append(
                    pd.Series([f'{tract1} vs {tract2}', measure, group_name, t_statistic, p_value],
                              index=['Comparison', 'Measure', 'Group', 'T-statistic', 'P-value']), ignore_index = True)
                
    # Extract p-values for FDR correction
    p_values_all = results_df_tracts['P-value']

    # Perform FDR correction for all comparisons
    reject_all, corrected_p_values_all, _, _ = multipletests(p_values_all, alpha=0.05, method='fdr_bh')

    # Update the results DataFrame with corrected p-values for all comparisons
    results_df_tracts['Corrected p-value'] = corrected_p_values_all
    results_df_tracts['Reject Null Hypothesis'] = reject_all
    print(results_df_tracts)

    # Save the results to an Excel file
    results_df_tracts.to_excel(join(database_path, f'{measure}_Ttest_TRACTS.xlsx'), index=False)