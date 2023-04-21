# This script was written by [Fan Dong](https://ca.linkedin.com/in/fan-dong-1203b9147) and modified by Lianchun.

import os
import re
import pandas as pd

def get_filenames_from_proteinname(proteinname: str):
    """
    The input is a string indicting the name of specific protein.
    This function is going to find the file names that contain this protein name in the text.
    """

    def exist_desired_name(file_name, proteinname):
        with open(os.path.join(directory, file_name), 'r') as f:
            content = '\n'.join(f.readlines())

            proteinname = proteinname.replace('|', '\|')
            regex_pattern = re.compile(f">{proteinname} \[")
            match_reuslt = re.search(regex_pattern, content)

            if match_reuslt is None:
                return False
            else:
                return True

    directory = 'D:/Pycharm/project/orthologues_run_Friday'
    file_names = os.listdir(directory)
    desired_names = [x for x in file_names if exist_desired_name(x, proteinname)]
    return desired_names

# directory 'orthologues_run_Friday' contains all the results of orthologues.py

def find_species_gene_from_uml_rec():
    """
    Find the species_gene from each .uml_rec files
    """

    def find_species_genes(file_name):
        """
        Find the species_gene from a given file
        """
        with open(file_name, 'r') as f:
            content = f.readlines()
        result = content[11].split(':')[0].replace('(', "").split('.')[0]
        return result

    fold_name = r'D:\OneDrive - University of Calgary\bioinformatics\homework\ancestral reconstruction\root2'
    fruit = []
    target_file_names = [x for x in os.listdir(fold_name) if x.endswith('.uml_rec')]
    for i, uml_rec in enumerate(target_file_names):
        file_path = os.path.join(fold_name, uml_rec)
        fruit.append([uml_rec, find_species_genes(file_path)])

        # print the progress
        if i % 1000 == 0:
            print(f"Processing progress: {i}/{len(target_file_names)}")

    df = pd.DataFrame(fruit, columns=['uml_rec', 'species_gene'])
    return df
# There are *.uml_rec files in directory root2,

species_gene_df = find_species_gene_from_uml_rec()
species_gene_df.to_csv(
    r"D:\OneDrive - University of Calgary\bioinformatics\homework\ancestral reconstruction\fruit.csv", index=False)
print(species_gene_df.head(20))


fold_name = r"D:\OneDrive - University of Calgary\bioinformatics\homework\ancestral reconstruction\gene family at each node"
df_2 = pd.DataFrame()
for file_name in os.listdir(fold_name):
    df_2 = pd.concat([df_2, pd.read_csv(os.path.join(fold_name, file_name))])
df_merge = pd.merge(df_2, species_gene_df.rename(columns={"uml_rec": "Gene_family"}), on='Gene_family', how='left')
df_merge.to_csv(r"D:\OneDrive - University of Calgary\bioinformatics\homework\ancestral reconstruction\df_merge.csv", index=False)
df_merge = pd.read_csv(r"D:\OneDrive - University of Calgary\bioinformatics\homework\ancestral reconstruction\df_merge.csv")


def extract_protein(file_name: str) -> str:
    """
    Extract the protein from the first line.
    The regex rule is:
    Start from: a period with several digits and a space
    End before: a space and '(Bacteria'
    """
    with open(os.path.join(directory, file_name), 'r') as f:
        content = f.readline()
    search_result = re.search(r'\.\d+ (.+) \(Bacteria', content)
    if search_result is not None:
        return search_result.group(1)
    else:
        return None


file_name_ = []
file_protein_ = []
directory = 'D:/Pycharm/project/orthologues_run_Friday'
for i, proteinname in enumerate(df_merge['species_gene']):
    file_names_list_for_proteinname = get_filenames_from_proteinname(proteinname)
    file_name = file_names_list_for_proteinname[0]
    protein = extract_protein(file_name)
    file_name_.append(file_name)
    file_protein_.append(protein)

    if i % 100 == 0:
        print(f"{i}/{len(df_merge)} \t Finished.")

df_merge['gene_cluster'] = file_name_
df_merge['protein'] = file_protein_
df_merge.to_csv(r'C:\Users\ylc_c\OneDrive\desktop\df_merge_Apr_20.csv', index=False)

# df_merge_Apr_20.csv is the final output file.

# Still updating...