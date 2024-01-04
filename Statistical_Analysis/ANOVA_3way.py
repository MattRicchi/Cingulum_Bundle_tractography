import pandas as pd
from itertools import combinations
from statsmodels.stats.multitest import multipletests
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from Student_ttest_OLD import run_t_test

groups = ['CN', 'AD', 'MCI']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']

# Load the CSV data into DataFrames
ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv')
mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv')

# Merge the data into a single DataFrame with a hierarchical index
merged_df = pd.concat([ad_df, mci_df, cn_df], ignore_index=True)

# Remove rows with 0 values in the 'mean' column
merged_df = merged_df[merged_df['mean'] != 0.0]

# Separate DataFrames based on 'measure' column
fa_data = merged_df[merged_df['measure'] == 'FA'].copy()
md_data = merged_df[merged_df['measure'] == 'MD'].copy()
rd_data = merged_df[merged_df['measure'] == 'RD'].copy()

########################################################
########################## FA ##########################
########################################################

# Perform three-way ANOVA for FA
fa_formula = 'mean ~ C(tract) * C(side) * C(group)'
fa_model = ols(fa_formula, data=fa_data).fit()
fa_anova_table = anova_lm(fa_model, typ=2)

# Print the ANOVA table
print('-------- FA results --------')
print(fa_anova_table)

# Save the ANOVA results to an Excel file
fa_anova_table.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/fa_anova_results.xlsx')

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

# Perform t-tests and populate the results DataFrame
group_combinations = list(combinations([('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)], 2))

# Compare the groups
for (group1_name, group1_df), (group2_name, group2_df) in group_combinations:
    for tract in tracts:
        for side in sides:
            results_df = results_df._append(
                run_t_test(group1_df, group2_df, 'FA', tract, side, group1_name, group2_name),
                ignore_index = True)

fa_data_sub = fa_data[fa_data['tract'] == 'Subgenual']
fa_data_retro = fa_data[fa_data['tract'] == 'Retrosplenial']
fa_data_para = fa_data[fa_data['tract'] == 'Parahippocampal']

# Compare the tracts
tracts_combinations = list(combinations([('Subgenual', fa_data_sub), ('Retrosplenial', fa_data_retro), ('Parahippocampal', fa_data_para)], 2))

for (tract1, tract1_data), (tract2, tract2_data) in tracts_combinations:
    for side in sides:
        for group in groups: 
            results_df = results_df._append(
                run_t_test(tract1_data, tract2_data, 'FA', group, side, tract1, tract2), 
                ignore_index = True)
            
# Extract p-values for FDR correction
p_values = results_df['P-value']

# Perform FDR correction
reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Update the results DataFrame with corrected p-values
results_df['Corrected p-value'] = corrected_p_values
results_df['Reject Null Hypothesis'] = reject

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/FA_Ttest_results.xlsx', index=False)


########################################################
########################## MD ##########################
########################################################

# Perform three-way ANOVA for MD
md_formula = 'mean ~ C(tract) * C(side) * C(group)'
md_model = ols(md_formula, data=md_data).fit()
md_anova_table = anova_lm(md_model, typ=2)

# Print the ANOVA table
print('-------- MD results --------')
print(md_anova_table)

# Save the ANOVA results to an Excel file
md_anova_table.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/md_anova_results.xlsx')

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

# Perform t-tests and populate the results DataFrame
group_combinations = list(combinations([('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)], 2))

for (group1_name, group1_df), (group2_name, group2_df) in group_combinations:
    for tract in tracts:
        for side in sides:
            results_df = results_df._append(
                run_t_test(group1_df, group2_df, 'MD', tract, side, group1_name, group2_name),
                ignore_index=True)
            
# Extract p-values for FDR correction
p_values = results_df['P-value']

# Perform FDR correction
reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Update the results DataFrame with corrected p-values
results_df['Corrected p-value'] = corrected_p_values
results_df['Reject Null Hypothesis'] = reject

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MD_Ttest_results.xlsx', index=False)


########################################################
########################## RD ##########################
########################################################

# Perform three-way ANOVA for RD
rd_formula = 'mean ~ C(tract) * C(side) * C(group)'
rd_model = ols(rd_formula, data=rd_data).fit()
rd_anova_table = anova_lm(rd_model, typ=2)

# Print the ANOVA table
print('-------- RD results --------')
print(rd_anova_table)

# Save the ANOVA results to an Excel file
rd_anova_table.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/rd_anova_results.xlsx')

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Comparison', 'Measure', 'Tract_Side', 'T-statistic', 'P-value'])

# Perform t-tests and populate the results DataFrame
group_combinations = list(combinations([('CN', cn_df), ('AD', ad_df), ('MCI', mci_df)], 2))

for (group1_name, group1_df), (group2_name, group2_df) in group_combinations:
    for tract in tracts:
        for side in sides:
            results_df = results_df._append(
                run_t_test(group1_df, group2_df, 'RD', tract, side, group1_name, group2_name),
                ignore_index=True)
            
# Extract p-values for FDR correction
p_values = results_df['P-value']

# Perform FDR correction
reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Update the results DataFrame with corrected p-values
results_df['Corrected p-value'] = corrected_p_values
results_df['Reject Null Hypothesis'] = reject

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/RD_Ttest_results.xlsx', index=False)