import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.stats.multitest import multipletests

merged_data = pd.read_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/merged_data_mean.xlsx')

fa_data = merged_data[merged_data['measure'] == 'FA'].dropna(subset = ['moca'])
md_data = merged_data[merged_data['measure'] == 'MD'].dropna(subset = ['moca'])
rd_data = merged_data[merged_data['measure'] == 'RD'].dropna(subset = ['moca'])

# Create an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Tract', 'Measure', 'Statistic', 'P-Value'])

# Lists to store p-values for correction
p_values = []

# Loop through tracts and measures
for tract in ['Subgenual', 'Retrosplenial', 'Parahippocampal']:
    for measure_data, measure_name in zip([fa_data, md_data, rd_data], ['FA', 'MD', 'RD']):
        
        data_df = measure_data[measure_data['tract'] == tract]
        
        statistic, p_value = pearsonr(np.array(data_df['mean']), np.array(data_df['moca']))

        # Append results to the DataFrame and p_values list
        results_df = results_df._append({
            'Tract': tract,
            'Measure': measure_name,
            'Statistic': statistic,
            'P-Value': p_value
        }, ignore_index=True)

        p_values.append(p_value)

        # Plotting with regression line
        plt.figure(figsize=(10, 6))
        sns.regplot(x='moca', y='mean', data=data_df, ci=None, line_kws={'color': 'red'})
        plt.title(f'{tract} - {measure_name} vs MOCA Index with Regression Line')
        plt.ylabel(f'Mean {measure_name}')
        plt.xlabel('MOCA Index')
        plt.show()

# Correct p-values using Benjamini-Hochberg
results_df['Adjusted P-Value'] = multipletests(p_values, method='fdr_bh')[1]

# Save the results to an Excel file
results_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/correlation_results_bh.xlsx', index=False)