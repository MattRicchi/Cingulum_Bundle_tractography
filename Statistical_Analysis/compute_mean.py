import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
# print(df)
for patient in range(1, 19):
    if patient in [1000]:
        continue
    for tract in ['Subgenual', 'Retrosplenial', 'Parahippocampal']:
        for measure in ['FA', 'MD', 'RD']:
            right_side = np.float64(df[(df['patient'] == patient) & (df['tract'] == tract) & (df['measure'] == measure) & (df['side'] == 'R')]['mean'])
            left_side = np.float64(df[(df['patient'] == patient) & (df['tract'] == tract) & (df['measure'] == measure) & (df['side'] == 'L')]['mean'])
            
            mean = (right_side + left_side) / 2
            
            # Append the mean value to the DataFrame
            df = df._append({'patient': patient, 'tract': tract, 'measure': measure, 'side': 'mean_LR', 'mean': mean, 'group':'MCI'}, ignore_index=True)

# Save the updated DataFrame back to the CSV file
df.to_excel('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics_mean.xlsx', index=False)

