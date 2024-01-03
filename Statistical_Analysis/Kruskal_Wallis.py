import pandas as pd
from scipy.stats import kruskal


# Load the CSV data into DataFrames
fa_data = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/fa_data.csv')
md_data = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/md_data.csv')
rd_data = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/rd_data.csv')

# Perform Kruskal-Wallis test for FA
fa_data_grouped = fa_data.groupby(['tract', 'side', 'group'])['mean'].apply(list)
fa_kruskal_result = kruskal(*fa_data_grouped.values)

# Print the Kruskal-Wallis test result
print('-------- FA Kruskal-Wallis results --------')
print(fa_kruskal_result)

# Perform Kruskal-Wallis test for MD
md_data_grouped = md_data.groupby(['tract', 'side', 'group'])['mean'].apply(list)
md_kruskal_result = kruskal(*md_data_grouped.values)

# Print the Kruskal-Wallis test result
print('-------- MD Kruskal-Wallis results --------')
print(md_kruskal_result)

# Perform Kruskal-Wallis test for RD
rd_data_grouped = rd_data.groupby(['tract', 'side', 'group'])['mean'].apply(list)
rd_kruskal_result = kruskal(*rd_data_grouped.values)

# Print the Kruskal-Wallis test result
print('-------- RD Kruskal-Wallis results --------')
print(rd_kruskal_result)
