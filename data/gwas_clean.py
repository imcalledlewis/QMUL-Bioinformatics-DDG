import pandas as pd
import os
import re

fileIn = 'gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv' # https://www.ebi.ac.uk/gwas/docs/file-downloads
fileOut = 'gwas_trimmed.tsv'

path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
filepath = os.path.join(path, fileIn)               # Sets path relative to current file
data = pd.read_csv(filepath, sep='\t', low_memory=False)
data = data.loc[data['DISEASE/TRAIT']=='Type 1 diabetes']   # Select only rows regarding type 1 diabetes
data = data.loc[data['CHR_ID']=='6']                        # Select only rows for chromosome 6
data = data[["SNPS","SNP_ID_CURRENT","REGION","CHR_POS","P-VALUE","RISK ALLELE FREQUENCY"]] # maybe also include STRONGEST SNP-RISK ALLELE ?

rename_dict={}
for col in data.columns:
    newCol = re.sub(r'\W+', '_', col)   # Replaces special characters and whitespace with underscores
    rename_dict.update({col:newCol})
data=data.rename(columns=rename_dict)

filepath = os.path.join(path, fileOut)
os.remove(filepath)
data.to_csv(filepath, sep='\t')
print("\ndone")