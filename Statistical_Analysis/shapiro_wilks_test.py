import os
import pandas as pd
import numpy as np
from scipy import stats

# First test the age distributions of AD, CN, MCI
# Define the np arrays containing the ages of participants
print('Shapiro-Wilk test to check for normality of age distribution')
AD_age = np.array([76, 72, 75, 84, 84, 82, 59, 68, 86, 75])
CN_age = np.array([74, 81, 53, 68, 78, 77, 78, 76, 83, 85, 80, 73, 73, 80, 74, 57])
MCI_age = np.array([86, 69, 75, 73, 77, 74, 68, 79, 76, 71, 74, 68, 74, 79, 79, 79, 89, 75])

# Perform the tests
AD_res = stats.shapiro(AD_age)
CN_res = stats.shapiro(CN_age)
MCI_res = stats.shapiro(MCI_age)

# Print the results
print('-------- AD age --------')
print(f'Mean age (std): {np.mean(AD_age)}({np.std(AD_age)})')
print('AD statistics: ', AD_res.statistic)
print('AD p-value: ', AD_res.pvalue)

print('-------- CN age --------')
print(f'Mean age (std): {np.mean(CN_age)}({np.std(CN_age)})')
print('CN statistics: ', CN_res.statistic)
print('CN p-value: ', CN_res.pvalue)

print('-------- MCI age --------')
print(f'Mean age (std): {np.mean(MCI_age)}({np.std(MCI_age)})')
print('MCI statistics: ', MCI_res.statistic)
print('MCI p-value: ', MCI_res.pvalue)

########################################################################################################################################################
########################################################################################################################################################

metrics = ['fa', 'md', 'rd']
tracts = ['subgenual', 'retrosplenial', 'parahippocampal']
sides = ['l', 'r']

# Now check the normality of DTI metrics results
######################## AD ########################

# Load the global CSV file into a DataFrame
global_csv_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv'
df = pd.read_csv(global_csv_path)

# Separate data based on measure (FA, MD, RD)
fa_data = df[df['measure'] == 'FA']
md_data = df[df['measure'] == 'MD']
rd_data = df[df['measure'] == 'RD']

# Function to extract data for a specific combination of measure, tract, and side
def extract_data(data, measure, tract, side):
    subset = data[(data['tract'] == tract) & (data['side'] == side)]['mean']
    return np.array(subset)

print('--------------------------------')
print('---------- AD results ----------')
print('--------------------------------')

# Iterate over metrics, tracts, and sides
for metric in metrics:
    for tract in tracts:
        for side in sides:
            # Extract data for AD patients
            data = extract_data(df[df['measure'] == metric.upper()], metric.upper(), tract.capitalize(), side.upper())
            print(data)
            # Perform the Shapiro-Wilks test
            res = stats.shapiro(data)

            # Print the results
            print(f'Shapiro-Wilk test for {metric.upper()} in {tract.capitalize()}_{side.upper()}: p-value={res.pvalue}')


######################## CN ########################

# Load the global CSV file into a DataFrame
global_csv_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv'
df = pd.read_csv(global_csv_path)

# Separate data based on measure (FA, MD, RD)
fa_data = df[df['measure'] == 'FA']
md_data = df[df['measure'] == 'MD']
rd_data = df[df['measure'] == 'RD']

# Function to extract data for a specific combination of measure, tract, and side
def extract_data(data, measure, tract, side):
    subset = data[(data['tract'] == tract) & (data['side'] == side)]['mean']
    return np.array(subset)

print('--------------------------------')
print('---------- CN results ----------')
print('--------------------------------')

# Iterate over metrics, tracts, and sides
for metric in metrics:
    for tract in tracts:
        for side in sides:
            # Extract data for CN patients
            data = extract_data(df[df['measure'] == metric.upper()], metric.upper(), tract.capitalize(), side.upper())

            # Perform the Shapiro-Wilks test
            res = stats.shapiro(data)

            # Print the results
            print(f'Shapiro-Wilk test for {metric.upper()} in {tract.capitalize()}_{side.upper()}: p-value={res.pvalue}')


######################## MCI ########################

# Load the global CSV file into a DataFrame
global_csv_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv'
df = pd.read_csv(global_csv_path)

# Separate data based on measure (FA, MD, RD)
fa_data = df[df['measure'] == 'FA']
md_data = df[df['measure'] == 'MD']
rd_data = df[df['measure'] == 'RD']

# Function to extract data for a specific combination of measure, tract, and side
def extract_data(data, measure, tract, side):
    subset = data[(data['tract'] == tract) & (data['side'] == side)]['mean']
    return np.array(subset)

print('--------------------------------')
print('---------- MCI results ----------')
print('--------------------------------')

# Iterate over metrics, tracts, and sides
for metric in metrics:
    for tract in tracts:
        for side in sides:
            # Extract data for MCI patients
            data = extract_data(df[df['measure'] == metric.upper()], metric.upper(), tract.capitalize(), side.upper())

            # Perform the Shapiro-Wilks test
            res = stats.shapiro(data)

            # Print the results
            print(f'Shapiro-Wilk test for {metric.upper()} in {tract.capitalize()}_{side.upper()}: p-value={res.pvalue}')