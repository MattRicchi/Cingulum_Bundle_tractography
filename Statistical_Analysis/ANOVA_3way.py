import pandas as pd
from scipy.stats import f_oneway
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# Load the CSV data into DataFrames
ad_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv')
mci_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
cn_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv')

# Merge the data into a single DataFrame with a hierarchical index
merged_df = pd.concat([ad_df, mci_df, cn_df], ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/merged_data.csv')

# Separate DataFrames based on 'measure' column
fa_df = merged_df[merged_df['measure'] == 'FA'].copy()
md_df = merged_df[merged_df['measure'] == 'MD'].copy()
rd_df = merged_df[merged_df['measure'] == 'RD'].copy()

# Save each DataFrame to a new CSV file
fa_df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/fa_data.csv', index=False)
md_df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/md_data.csv', index=False)
rd_df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/rd_data.csv', index=False)

# Load the separated DataFrames
fa_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/fa_data.csv')
md_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/md_data.csv')
rd_df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/rd_data.csv')

# Perform three-way ANOVA for FA
formula = 'mean ~ C(tract) * C(side) * C(group)'
model = ols(formula, data=fa_df).fit()
anova_table = anova_lm(model, typ=2)

# Print the ANOVA table
print('-------- FA results --------')
print(anova_table)

# Perform three-way ANOVA for MD
formula = 'mean ~ C(tract) * C(side) * C(group)'
model = ols(formula, data=md_df).fit()
anova_table = anova_lm(model, typ=2)

# Print the ANOVA table
print('-------- MD results --------')
print(anova_table)

# Perform three-way ANOVA for RD
formula = 'mean ~ C(tract) * C(side) * C(group)'
model = ols(formula, data=rd_df).fit()
anova_table = anova_lm(model, typ=2)

# Print the ANOVA table
print('-------- RD results --------')
print(anova_table)