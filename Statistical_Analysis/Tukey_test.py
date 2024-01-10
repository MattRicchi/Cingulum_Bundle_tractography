import pandas as pd
import numpy as np
from itertools import combinations
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load the CSV data into DataFrames
ad_df = pd.read_csv('C:/Users/Probook 455 G6/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics_mean.csv')
mci_df = pd.read_csv('C:/Users/Probook 455 G6/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics_mean.csv')
cn_df = pd.read_csv('C:/Users/Probook 455 G6/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics_mean.csv')

measures = ['FA', 'MD', 'RD']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']

def run_tukey_test(df1, df2, measure, tract, group1_name, group2_name):
    
    group1_data = np.array(df1[(df1['measure'] == measure) & (df1['tract'] == tract) & (df1['side'] == 'mean_LR') & (df1['mean'] != 0.0)]['mean'])
    group2_data = np.array(df2[(df2['measure'] == measure) & (df2['tract'] == tract) & (df2['side'] == 'mean_LR') & (df2['mean'] != 0.0)]['mean'])

    # Combine data and group labels for Tukey test
    all_data = np.concatenate([group1_data, group2_data])
    
    group1_label = [group1_name] * len(group1_data)
    group2_label = [group2_name] * len(group2_data)
    
    group_labels = np.concatenate([group1_label, group2_label])

    # Perform Tukey test
    tukey_results = pairwise_tukeyhsd(all_data, group_labels)

    # Convert results to DataFrame
    results_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])

    return results_df

def run_tukey_test_tract(df1, df2, measure, tract1, tract2):
    group1_data = np.array(df1[(df1['measure'] == measure) & (df1['side'] == 'mean_LR') & (df1['mean'] != 0.0)]['mean'])
    group2_data = np.array(df2[(df2['measure'] == measure) & (df2['side'] == 'mean_LR') & (df2['mean'] != 0.0)]['mean'])
    
    # Combine data and group labels for Tukey test
    all_data = np.concatenate([group1_data, group2_data])
    
    group1_label = [tract1] * len(group1_data)
    group2_label = [tract2] * len(group2_data)
    
    group_labels = np.concatenate([group1_label, group2_label])

    # Perform Tukey test
    tukey_results = pairwise_tukeyhsd(all_data, group_labels)

    # Convert results to DataFrame
    results_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])

    return results_df

# Perform a Tukey test and p-value correction for each measurement separately
for measure in measures:
    # Define empty DataFrame for final results
    results_df = pd.DataFrame(columns=['Comparison', 'tract', 'measure', 'meandiff', 'p-adj'])

    group_combinations = list(combinations([('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)], 2))

    # Compare the groups
    for (group1_name, group1_df), (group2_name, group2_df) in group_combinations:
        for tract in tracts:
            tukey_results_df = run_tukey_test(group1_df, group2_df, measure, tract, group1_name, group2_name)
            tukey_results_df['Comparison'] = f'{group1_name} vs {group2_name}'
            tukey_results_df['measure'] = measure
            tukey_results_df['tract'] = tract
            results_df = results_df._append(tukey_results_df, ignore_index=True)
            
    print(results_df.drop(columns=['group1', 'group2']))
    results_df.to_excel(f'C:/Users/Probook 455 G6/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/{measure}_Tukey_GROUPS.xlsx', index=False)

    # Define empty DataFrame for final results
    results_df_tracts = pd.DataFrame(columns=['Comparison', 'Group', 'measure', 'meandiff', 'p-adj'])

    # Compare tracts within each group
    tract_combinations = list(combinations(tracts, 2))
    for tract1, tract2 in tract_combinations:
        for group_name_tract, group_df_tract in [('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)]:
            df1 = group_df_tract[group_df_tract['tract'] == tract1]
            df2 = group_df_tract[group_df_tract['tract'] == tract2]
            tukey_results_df = run_tukey_test_tract(df1, df2, measure, tract1, tract2)
            tukey_results_df['Comparison'] = f'{tract1} vs {tract2}'
            tukey_results_df['Group'] = group_name_tract
            tukey_results_df['measure'] = measure
            results_df_tracts = results_df_tracts._append(tukey_results_df, ignore_index=True)
                
    print(results_df_tracts.drop(columns=['group1', 'group2']))
    results_df_tracts.to_excel(f'C:/Users/Probook 455 G6/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/{measure}_Tukey_TRACTS.xlsx', index=False)

                
    # # Extract p-values for FDR correction
    # p_values_all = results_df_tracts['P-value']

    # # Perform FDR correction for all comparisons
    # reject_all, corrected_p_values_all, _, _ = multipletests(p_values_all, alpha=0.05, method='fdr_bh')

    # # Update the results DataFrame with corrected p-values for all comparisons
    # results_df_tracts['Corrected p-value'] = corrected_p_values_all
    # results_df_tracts['Reject Null Hypothesis'] = reject_all
    # print(results_df_tracts)

    # # Save the results to an Excel file
    # results_df_tracts.to_excel(f'C:/Users/Probook 455 G6/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/{measure}_Tukey_TRACTS.xlsx', index=False)
