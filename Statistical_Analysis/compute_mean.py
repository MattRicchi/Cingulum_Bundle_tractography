import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics.csv')
# print(df)
for patient in range(1, 19):
    if patient in [110]:
        continue
    for tract in ['Subgenual', 'Retrosplenial', 'Parahippocampal']:
        for measure in ['FA', 'MD', 'RD']:
            right_side = np.float64(df[(df['patient'] == patient) & (df['tract'] == tract) & (df['measure'] == measure) & (df['side'] == 'R')]['mean'])
            left_side = np.float64(df[(df['patient'] == patient) & (df['tract'] == tract) & (df['measure'] == measure) & (df['side'] == 'L')]['mean'])
            # print(right_side)
            mean = (right_side + left_side) / 2
            
            # Append the mean value to the DataFrame
            df = df._append({'patient': patient, 'tract': tract, 'measure': measure, 'side': 'mean_LR', 'mean': mean, 'group':'MCI'}, ignore_index=True)

# Save the updated DataFrame back to the CSV file
df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/MCI/global_tract_metrics_mean.csv', index=False)


# # Group by 'tract' and 'measure' columns and calculate the mean for each group
# grouped_df = df.groupby(['tract', 'measure']).mean().reset_index()

# # Add a new 'side' column with 'mean' for each row
# grouped_df['side'] = 'mean'

# # Concatenate the original DataFrame with the new rows containing mean values
# result_df = pd.concat([df, grouped_df], ignore_index=True)

# # Sort the DataFrame by 'tract', 'measure', and 'side'
# result_df.sort_values(by=['tract', 'measure', 'side'], inplace=True)

# # Save the result back to a CSV file
# result_df.to_csv('/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/AD/global_tract_metrics_mean.csv', index=False)
