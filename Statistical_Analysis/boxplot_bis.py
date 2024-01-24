import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set the color palette to a colorblind-friendly palette
sns.set_palette("colorblind", n_colors=3)
merged_data = pd.read_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/merged_data_mean.xlsx')

# Increase text dimensions
plt.rcParams.update({'font.size': 14, 'legend.fontsize': 12, 'axes.labelsize': 16, 'axes.titlesize': 18, 'xtick.labelsize': 14, 'ytick.labelsize': 14})

########### RD ###########

data = merged_data[(merged_data['side'] == 'mean_LR') & (merged_data['measure'] == 'RD')]

# Setting the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating a boxplot of mean as a function of group distinguishing between tracts
plt.figure(figsize=(12, 8))
box_plot = sns.boxplot(x="group", y="mean", hue="tract", data=data)
plt.xlabel('')
plt.ylabel('RD')
plt.legend(title='Subdivision', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Extracting median, Q1, and Q3 values for each boxplot
results = []
for group, group_data in data.groupby('group'):
    for tract, box_data in group_data.groupby('tract'):
        median = box_data['mean'].median()
        q1 = box_data['mean'].quantile(0.25)
        q3 = box_data['mean'].quantile(0.75)
        results.append({
            'Group': group,
            'Tract': tract,
            'Median': median * 1000,
            'Q1': q1 * 1000,
            'Q3': q3 * 1000
        })

# Save results to an Excel file
result_df = pd.DataFrame(results)
result_df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Statistical_analysis/Boxplots/boxplot_results_RD.xlsx', index=False)

plt.show()
