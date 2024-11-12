import pandas as pd
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn
from os.path import join

database_path = '/path/to/DATABASE/'

# Load the CSV data into DataFrames
fa_data = pd.read_csv(join(database_path,'fa_data.csv'))
md_data = pd.read_csv(join(database_path,'md_data.csv'))
rd_data = pd.read_csv(join(database_path,'rd_data.csv'))

# Function to perform Kruskal-Wallis test and Dunn's post-hoc test
def kruskal_dunn(data, measure):
    data_grouped = data.groupby(['tract', 'side', 'group'])['mean'].apply(list)

    kruskal_result = kruskal(*data_grouped.values)
    
    print(f'-------- {measure} Kruskal-Wallis results --------')
    print(kruskal_result)
    
    # Perform Dunn's post-hoc test
    posthoc_result_group = posthoc_dunn(data, val_col='mean', group_col='group', p_adjust='fdr_bh')
    print(f'-------- GROUP Dunn\'s post-hoc results --------')
    print(posthoc_result_group)

    posthoc_result_tract = posthoc_dunn(data, val_col='mean', group_col='tract', p_adjust='fdr_bh')
    print(f'-------- TRACT Dunn\'s post-hoc results --------')
    print(posthoc_result_tract)

    posthoc_result_side = posthoc_dunn(data, val_col='mean', group_col='side', p_adjust='fdr_bh')
    print(f'-------- SIDE Dunn\'s post-hoc results --------')
    print(posthoc_result_side)

    # Create an Excel writer with the measure name in the file name
    excel_file_path = f'/mnt/c/Users/ricch/OneDrive - University of Pisa/Cingulum_bundle_study/DATABASE/results_Kruskal_{measure}.xlsx'
    print(f'Saving results to: {excel_file_path}')
    excel_writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

    # Write Kruskal-Wallis result to Excel
    pd.DataFrame({'Kruskal-Wallis p-value': [kruskal_result.pvalue]}).to_excel(excel_writer, sheet_name='Kruskal_Wallis')

    # Write Dunn's post-hoc results to Excel
    posthoc_result_group.to_excel(excel_writer, sheet_name='Dunn_GROUP')
    posthoc_result_tract.to_excel(excel_writer, sheet_name='Dunn_TRACT')
    posthoc_result_side.to_excel(excel_writer, sheet_name='Dunn_SIDE')

    # Save the Excel file
    excel_writer._save()

# Perform Kruskal-Wallis and Dunn's post-hoc tests for FA
kruskal_dunn(fa_data, 'FA')

# Perform Kruskal-Wallis and Dunn's post-hoc tests for MD
kruskal_dunn(md_data, 'MD')

# Perform Kruskal-Wallis and Dunn's post-hoc tests for RD
kruskal_dunn(rd_data, 'RD')