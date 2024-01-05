import numpy as np
from scipy.stats import f_oneway
import pandas as pd

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
print("Results saved to anova_results.xlsx")
