import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
 

for measure in ['FA', 'MD', 'RD']:
    data = pd.read_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/merged_data_mean.xlsx')
    data = data[(data['side'] == 'mean_LR') & (data['measure'] == measure)]

    # Setting the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Creating a boxplot of mean as a function of group distinguishing between tracts
    plt.figure(figsize=(12, 8))
    sns.boxplot(x="group", y="mean", hue="tract", data=data)
    plt.title('Boxplot of Mean as a Function of Group Distinguishing Between Tracts')
    plt.xlabel('Group')
    plt.ylabel(f'Mean {measure}')
    plt.legend(title='Tract', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)  # Rotating the x-axis labels for better readability
    plt.tight_layout()  # Adjusting the plot to ensure everything fits without overlapping
    plt.show()


    # Creating the boxplot for mean as a function of group only
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="group", y="mean", data=data)
 
    plt.title("Boxplot of Mean by Group")
    plt.xlabel("Group")
    plt.ylabel(f"Mean {measure}")
    plt.xticks(rotation=45)  # Rotating x labels for better readability
 
    plt.tight_layout()
    plt.show()