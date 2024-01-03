import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# Load the CSV data into DataFrames
ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv')
mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv')

# Merge the data into a single DataFrame with a hierarchical index
merged_df = pd.concat([ad_df, mci_df, cn_df], ignore_index=True)

# Save the merged DataFrame to a new CSV file
# merged_df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/merged_data.csv', index=False)

# Remove rows with 0 values in the 'mean' column
merged_df = merged_df[merged_df['mean'] != 0.0]

# Separate DataFrames based on 'measure' column
fa_data = merged_df[merged_df['measure'] == 'FA'].copy()
md_data = merged_df[merged_df['measure'] == 'MD'].copy()
rd_data = merged_df[merged_df['measure'] == 'RD'].copy()

# # Save each DataFrame to a new CSV file
# fa_data.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/fa_data.csv', index=False)
# md_data.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/md_data.csv', index=False)
# rd_data.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/rd_data.csv', index=False)

# Perform three-way ANOVA for FA
fa_formula = 'mean ~ C(tract) * C(side) * C(group)'
fa_model = ols(fa_formula, data=fa_data).fit()
fa_anova_table = anova_lm(fa_model, typ=2)

# Print the ANOVA table
print('-------- FA results --------')
print(fa_anova_table)

# Save the ANOVA results to an Excel file
fa_anova_table.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/fa_anova_results.xlsx')

# Perform three-way ANOVA for MD
md_formula = 'mean ~ C(tract) * C(side) * C(group)'
md_model = ols(md_formula, data=md_data).fit()
md_anova_table = anova_lm(md_model, typ=2)

# Print the ANOVA table
print('-------- MD results --------')
print(md_anova_table)

# Save the ANOVA results to an Excel file
md_anova_table.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/md_anova_results.xlsx')

# Perform three-way ANOVA for RD
rd_formula = 'mean ~ C(tract) * C(side) * C(group)'
rd_model = ols(rd_formula, data=rd_data).fit()
rd_anova_table = anova_lm(rd_model, typ=2)

# Print the ANOVA table
print('-------- RD results --------')
print(rd_anova_table)

# Save the ANOVA results to an Excel file
rd_anova_table.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/rd_anova_results.xlsx')