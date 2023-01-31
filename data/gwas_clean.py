from db_scripts import *

fileIn = 'gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv' # https://www.ebi.ac.uk/gwas/docs/file-downloads
fileOut = 'gwas_trimmed.tsv'

filepath = getPath(fileIn)
data = pd.read_csv(filepath, sep='\t', low_memory=False)    # Reads gwas tsv
data = data.loc[data['DISEASE/TRAIT']=='Type 1 diabetes']   # Select only rows regarding type 1 diabetes
data = data.loc[data['CHR_ID']=='6']                        # Select only rows for chromosome 6
data = data[["SNPS","REGION","CHR_POS","P-VALUE"]] # maybe also include STRONGEST SNP-RISK ALLELE and RISK ALLELE FREQUENCY ?
data.reset_index(drop=True,inplace=True)    # Resets index back to 0

rename_dict={}
for col in data.columns:
    newCol = re.sub(r'\W+', '_', col)   # Replaces special characters and whitespace with underscores
    rename_dict.update({col:newCol})
data=data.rename(columns=rename_dict)

data=removeDupes(data)      # Remove duplicates (leaving the entry with largest p value)

filepath = getPath(fileOut)
os.remove(filepath)
data.to_csv(filepath, sep='\t')
print("\ndone\n")