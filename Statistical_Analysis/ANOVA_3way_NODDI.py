import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from os.path import join

groups = ['CN', 'AD', 'MCI']
tracts = ['Subgenual', 'Retrosplenial', 'Parahippocampal']
sides = ['L', 'R']

database_path = '/path/to/DATABASE'

# Load the CSV data into DataFrames
ad_df = pd.read_csv(join(database_path,'AD/global_tract_metrics.csv'))
mci_df = pd.read_csv(join(database_path,'/MCI/global_tract_metrics.csv'))
cn_df = pd.read_csv(join(database_path,'/CN/global_tract_metrics.csv'))

ad_df['group'] = 'AD'
mci_df['group'] = 'MCI'
cn_df['group'] = 'CN'

# Merge the data into a single DataFrame with a hierarchical index
merged_df = pd.concat([ad_df, mci_df, cn_df], ignore_index=True)

# Remove rows with 0 values in the 'mean' column
merged_df = merged_df[merged_df['mean'] != 0.0]

# Separate DataFrames based on 'measure' column
ODI_data = merged_df[merged_df['measure'] == 'SD2BinghamDistributed_1_SD2Bingham_1_odi'].copy()
NDI_data = merged_df[merged_df['measure'] == 'Bingham_NDI'].copy()
beta_fraction_data = merged_df[merged_df['measure'] == 'SD2BinghamDistributed_1_SD2Bingham_1_beta_fraction'].copy()
p_volume0_data = merged_df[merged_df['measure'] == 'partial_volume_0'].copy()
p_volume1_data = merged_df[merged_df['measure'] == 'partial_volume_1'].copy()
intra_neurite_data = merged_df[merged_df['measure'] == 'SD2BinghamDistributed_1_partial_volume_0'].copy()

formula = 'mean ~ C(tract) * C(side) * C(group)'

########################################################
######################### ODI ##########################
########################################################

# Perform three-way ANOVA for ODI
ODI_model = ols(formula, data=ODI_data).fit()
ODI_anova_table = anova_lm(ODI_model, typ=2)

# Print the ANOVA table
print('-------- ODI results --------')
print(ODI_anova_table)

# Save the ANOVA results to an Excel file
ODI_anova_table.to_excel(join(database_path,'/Bingham_ODI_anova_results.xlsx'))


########################################################
######################### NDI ##########################
########################################################

# Perform three-way ANOVA for NDI
NDI_model = ols(formula, data=NDI_data).fit()
NDI_anova_table = anova_lm(NDI_model, typ=2)

# Print the ANOVA table
print('-------- NDI results --------')
print(NDI_anova_table)

# Save the ANOVA results to an Excel file
NDI_anova_table.to_excel(join(database_path,'/Bingham_NDI_anova_results.xlsx'))


########################################################
######################### Beta #########################
########################################################

# Perform three-way ANOVA for RD
beta_model = ols(formula, data=beta_fraction_data).fit()
beta_anova_table = anova_lm(beta_model, typ=2)

# Print the ANOVA table
print('-------- Beta Fraction results --------')
print(beta_anova_table)

# Save the ANOVA results to an Excel file
beta_anova_table.to_excel(join(database_path,'/Bingham_BETA_anova_results.xlsx'))

########################################################
###################### P Volume 0 ######################
########################################################

# Perform three-way ANOVA for RD
p_volume0_model = ols(formula, data=p_volume0_data).fit()
p_volume0_table = anova_lm(p_volume0_model, typ=2)

# Print the ANOVA table
print('-------- Partial Volume 0 results --------')
print(p_volume0_table)

# Save the ANOVA results to an Excel file
p_volume0_table.to_excel(join(database_path,'/Bingham_volume0_anova_results.xlsx'))

########################################################
###################### P Volume 1 ######################
########################################################

# Perform three-way ANOVA for RD
p_volume1_model = ols(formula, data=p_volume1_data).fit()
p_volume1_table = anova_lm(p_volume1_model, typ=2)

# Print the ANOVA table
print('-------- Partial Volume 1 results --------')
print(p_volume1_table)

# Save the ANOVA results to an Excel file
p_volume1_table.to_excel(join(database_path,'/Bingham_volume1_anova_results.xlsx'))

########################################################
#################### Intra Neurite #####################
########################################################

# Perform three-way ANOVA for RD
intra_neurite_model = ols(formula, data=intra_neurite_data).fit()
intra_neurite_table = anova_lm(intra_neurite_model, typ=2)

# Print the ANOVA table
print('-------- Partial Intra Neurite results --------')
print(intra_neurite_table)

# Save the ANOVA results to an Excel file
intra_neurite_table.to_excel(join(database_path,'/Bingham_intraNeurite_anova_results.xlsx'))