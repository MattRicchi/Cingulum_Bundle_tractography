import pandas as pd
from scipy.stats import chi2_contingency

# Sample data
data = {'Sex': ['F', 'M', 'F', 'M', 'F', 'F', 'F', 'M', 'M', 'F', 'F', 'F', 'F', 'M', 'M', 'F', 'M', 'F', 'F', 'M', 'F', 'F', 'M', 'F', 'F', 'M', 'F', 'F', 'M', 'F', 'M', 'F', 'F', 'M', 'F', 'F', 'M', 'F', 'F', 'F', 'M', 'M', 'M', 'F'], 
        'Category': ['AD', 'AD', 'AD', 'AD', 'AD', 'AD', 'AD', 'AD', 'AD', 'AD', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'CN', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI', 'MCI']}
df = pd.DataFrame(data)

# Get the number of subjects
num_subjects = df.shape[0]

# Create a contingency table
contingency_table = pd.crosstab(df['Sex'], df['Category'])

# Perform chi-square test
chi2_test, pval, dof, expected = chi2_contingency(contingency_table)
print('Number of subjects:', num_subjects)
print('Chi-square statistic:', chi2_test)
print('P-value:', pval)
print('Degrees of freedom:', dof)
