import os
import re
import pandas as pd

# Read the specified column of the specified sheet in an Excel file
file_path = 'D:/Pycharm/project/total_gene_families_at_each_node.xlsx'
sheet_name = 'node_16'
column_name = 'Gene_family'
df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[column_name])

# get file names
file_names = []
for value in df[column_name]:
    matches = re.findall(r'\d+', str(value))
    if matches:
        file_names.append(matches[0] + '.faa')
    else:
        file_names.append('')

# create a excel file and write data
output_file_path = 'D:/Pycharm/project/results/Gene_family_annotation.xlsx'
output_df = pd.DataFrame({'Gene_family': df[column_name], 'file_names': file_names})
output_df['Annotation'] = ''

# extract annotation and save the information to the file
file_dir = 'D:/Pycharm/project/orthologues_run_Friday'
for i, file_name in enumerate(output_df['file_names']):
    file_path = os.path.join(file_dir, file_name)
    if os.path.isfile(file_path) and file_name.endswith('.faa'):
        with open(file_path, 'r') as f:
            content = f.readline().strip()
            matches = re.findall(r'\d{1}\.\d{5} (.+) \(Bacteria', content)
            if matches:
                annotation = matches[0]
                output_df.loc[i, 'Annotation'] = annotation
            else:
                output_df.loc[i, 'Annotation'] = 'null'

# save results
output_df.to_excel(output_file_path, index=False)
