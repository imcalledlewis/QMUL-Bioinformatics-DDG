import pandas as pd
import os
import re

fileIn = 'gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv'
fileOut = 'gwas_trimmed.tsv'

# https://www.ebi.ac.uk/gwas/docs/file-downloads

path = os.path.dirname(os.path.abspath(__file__))           # Sets path relative to current file
filepath = os.path.join(path, fileIn)
data = pd.read_csv(filepath, sep='\t', low_memory=False)
data = data.loc[data['DISEASE/TRAIT']=='Type 1 diabetes']   # Select only rows regarding type 1 diabetes
data = data.loc[data['CHR_ID']=='6']                        # Select only rows for chromosome 6

rename_dict={}                          # Empty dictionary to be filled later
for col in data.columns:
    newCol = re.sub(r'[\W]+', '_', col)  # Replaces special characters and whitespace with underscores
    rename_dict.update({col:newCol})
data=data.rename(columns=rename_dict)

filepath = os.path.join(path, fileOut)
os.remove(filepath)
data.to_csv(filepath, sep='\t')
print("\ndone")