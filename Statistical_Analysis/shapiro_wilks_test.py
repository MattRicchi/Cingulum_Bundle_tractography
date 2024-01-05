import os
import pandas as pd
import numpy as np
from scipy import stats

# Function to extract data for a specific combination of measure, tract, and side
def extract_data(data, measure, tract, side):
    subset = data[(data['tract'] == tract) & (data['side'] == side)]['mean']
    
    # Exclude 0.0 values
    subset = subset[subset != 0.0]
    
    return np.array(subset)

metrics = ['fa', 'md', 'rd']
tracts = ['subgenual', 'retrosplenial', 'parahippocampal']
sides = ['l', 'r']

# Now check the normality of DTI metrics results
######################## AD ########################

# Load the global CSV file into a DataFrame
global_csv_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics.csv'
df = pd.read_csv(global_csv_path)

# Iterate over metrics, tracts, and sides
print('--------------------------------')
print('---------- AD results ----------')
print('--------------------------------')
for metric in metrics:
    for tract in tracts:
        for side in sides:
            # Extract data for AD patients
            data = extract_data(df[df['measure'] == metric.upper()], metric.upper(), tract.capitalize(), side.upper())
            
            # Perform the Shapiro-Wilks test
            res = stats.shapiro(data)

            # Print the results
            print(f'Shapiro-Wilk test for {metric.upper()} in {tract.capitalize()}_{side.upper()}: p-value={res.pvalue}')

######################## CN ########################

# Load the global CSV file into a DataFrame
global_csv_path = '/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/CN/global_tract_metrics.csv'
df = pd.read_csv(global_csv_path)

# Iterate over metrics, tracts, and sides
print('--------------------------------')
print('---------- CN results ----------')
print('--------------------------------')
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

# Iterate over metrics, tracts, and sides
print('--------------------------------')
print('---------- MCI results ----------')
print('--------------------------------')
for metric in metrics:
    for tract in tracts:
        for side in sides:
            # Extract data for MCI patients
            data = extract_data(df[df['measure'] == metric.upper()], metric.upper(), tract.capitalize(), side.upper())

            # Perform the Shapiro-Wilks test
            res = stats.shapiro(data)

            # Print the results
            print(f'Shapiro-Wilk test for {metric.upper()} in {tract.capitalize()}_{side.upper()}: p-value={res.pvalue}')
