import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set the color palette to a colorblind-friendly palette
sns.set_palette("colorblind", n_colors=3)
merged_data = pd.read_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/merged_data_mean.xlsx')

# Increase text dimensions
plt.rcParams.update({'font.size': 14, 'legend.fontsize': 12, 'axes.labelsize': 16, 'axes.titlesize': 18, 'xtick.labelsize': 14, 'ytick.labelsize': 14})

########### FA ###########

data = merged_data[(merged_data['side'] == 'mean_LR') & (merged_data['measure'] == 'FA')]

# Setting the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating a boxplot of mean as a function of group distinguishing between tracts
plt.figure(figsize=(12, 8))
sns.boxplot(x="group", y="mean", hue="tract", data=data)
plt.xlabel('')
plt.ylabel('FA')
plt.legend(title='Subdivision', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot to a file 
plt.savefig('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Statistical_analysis/Boxplots/boxplot_FA.png')

########### MD ###########

data = merged_data[(merged_data['side'] == 'mean_LR') & (merged_data['measure'] == 'MD')]
data['mean'] = data['mean'] * 1000

# Setting the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating a boxplot of mean as a function of group distinguishing between tracts
plt.figure(figsize=(12, 8))
sns.boxplot(x="group", y="mean", hue="tract", data=data)
plt.xlabel('')
plt.ylabel(r'MD $(10^{-3} \, \text{mm}^2/\text{s})$')
plt.legend(title='Subdivision', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot to a file 
plt.savefig('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Statistical_analysis/Boxplots/boxplot_MD.png')

########### RD ###########

data = merged_data[(merged_data['side'] == 'mean_LR') & (merged_data['measure'] == 'RD')]
data['mean'] = data['mean'] * 1000

# Setting the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating a boxplot of mean as a function of group distinguishing between tracts
plt.figure(figsize=(12, 8))
sns.boxplot(x="group", y="mean", hue="tract", data=data)
plt.xlabel('')
plt.ylabel(r'RD $(10^{-3} \, \text{mm}^2/\text{s})$')
plt.legend(title='Subdivision', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot to a file 
plt.savefig('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/Statistical_analysis/Boxplots/boxplot_RD.png')

plt.show()
