import numpy as np
import pandas as pd
from itertools import combinations
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

###############################################
##################### AGE #####################

# Age data for different groups
AD_age = np.array([76, 72, 75, 84, 84, 82, 59, 68, 86, 75])
CN_age = np.array([74, 81, 53, 68, 78, 77, 78, 76, 83, 85, 80, 73, 73, 80, 74, 57])
MCI_age = np.array([86, 69, 75, 73, 77, 74, 68, 79, 76, 71, 74, 68, 74, 79, 79, 79, 89, 75])

# Perform one-way ANOVA
statistic, p_value = f_oneway(AD_age, CN_age, MCI_age)

# Print the results
print("One-way ANOVA results:")
print("F-statistic:", statistic)
print("p-value:", p_value)

# Check for statistical significance
alpha = 0.05
if p_value < alpha:
    print("The age distributions are statistically significantly different.")
else:
    print("There is no significant difference in age distributions among the groups.")

# Create a DataFrame to store the results
results_df = pd.DataFrame({"F-statistic": [statistic], "p-value": [p_value]})

# Save the results to an Excel file
results_df.to_excel("/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AGE_anova_results.xlsx", index=False)
print("Results saved to AGE_anova_results.xlsx")

################################################
##################### MMSE #####################

# MMSE for different groups 
AD_MMSE = np.array([29, 20, 18, 24, 29, 26, 21, 30, 16])
AD_label = ['AD'] * len(AD_MMSE)
CN_MMSE = np.array([30, 26, 30, 30, 27, 29, 30, 30, 27, 27, 28, 28, 27, 27, 30, 29])
CN_label = ['CN'] * len(CN_MMSE)
MCI_MMSE = np.array([29, 24, 25, 28, 28, 25, 27, 29, 29, 24, 28, 30, 26, 28, 28])
MCI_label = ['MCI'] * len(MCI_MMSE)

# Perform One-way ANOVA test 
statistic_mmse, p_value_mmse = f_oneway(AD_MMSE, CN_MMSE, MCI_MMSE)

# Print the results
print("One-way ANOVA results:")
print("F-statistic:", statistic_mmse)
print("p-value:", p_value_mmse)

# Create a DataFrame to store the ANOVA results
results_mmse_df = pd.DataFrame({"F-statistic": [statistic_mmse], "p-value": [p_value_mmse]})

# Save the ANOVA results to an Excel file for MMSE
mmse_anova_results_file = "/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MMSE_anova_results.xlsx"
results_mmse_df.to_excel(mmse_anova_results_file, sheet_name='ANOVA', index=False)
print("ANOVA Results saved to MMSE_anova_results.xlsx")

# Check for statistical significance
alpha = 0.05
if p_value_mmse < alpha:
    print("The MMSE distributions are statistically significantly different. Performing Tukey post hoc test.")

    all_data = np.concatenate([AD_MMSE, CN_MMSE, MCI_MMSE])
    group_labels = np.concatenate([AD_label, CN_label, MCI_label])

    # Perform Tukey test
    tukey_results = pairwise_tukeyhsd(all_data, group_labels)
    Tukey_results_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])

    # Save the Tukey results to the same Excel file but in a different sheet
    with pd.ExcelWriter(mmse_anova_results_file, engine='openpyxl', mode='a') as writer:
        Tukey_results_df.to_excel(writer, sheet_name='Tukey', index=False, startrow=0, header=True)
        writer._save()

    print("Tukey Results saved to MMSE_anova_results.xlsx")
else:
    print("There is no significant difference in MMSE distributions among the groups.")