import pandas as pd
import os
import re

# https://www.ebi.ac.uk/gwas/docs/file-downloads



path = os.path.dirname(os.path.abspath(__file__))       # sets path relative to current file
filepath = os.path.join(path, 'gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv')
data = pd.read_csv(filepath, sep='\t', low_memory=False)
data = data.loc[data['DISEASE/TRAIT']=='Type 1 diabetes']   # select only rows regarding type 1 diabetes
data = data.loc[data['CHR_ID']=='6']                        # select only rows for chromosome 6
#print(data.head())

rename_dict={}                      # Empty dictionary to be filled later
for col in data.columns:
    newCol=re.sub(" ", "_", col)    # Column name with space replaced by underscore
    rename_dict.update({col:newCol})
data=data.rename(columns=rename_dict)

filepath = os.path.join(path, 'gwas_trimmed2.tsv')
data.to_csv(filepath, sep='\t')
print("\ndone")