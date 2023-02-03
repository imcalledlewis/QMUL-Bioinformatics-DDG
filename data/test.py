from db_scripts import *

fileIn = getPath('gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv') # https://www.ebi.ac.uk/gwas/docs/file-downloads
fileOut = getPath('gwas_trimmed.tsv')

data = pd.read_csv(fileIn, sep='\t', low_memory=False)    # Reads gwas tsv
data = data.loc[data['DISEASE/TRAIT']=='Type 1 diabetes']   # Select only rowsclear regarding type 1 diabetes
# # data.loc[data['STUDY'].str.contains('type 1 diabetes')]         # Nadia's code
data = data.loc[data['CHR_ID']=='6']                        # Select only rows for chromosome 6
data = data[["SNPS","REGION","CHR_POS","P-VALUE","MAPPED_GENE"]] # maybe also include STRONGEST SNP-RISK ALLELE and RISK ALLELE FREQUENCY ?

data=removeSpecial(data)    # removes special characters in column names
data=removeDupeSNP(data)    # Remove duplicates (leaving the entry with largest p value)
data=castRS(data, "SNPS")   # converts rs value column to integer

if os.path.exists(fileOut): # If the file exists,
    os.remove(fileOut)     # delete it.
data.to_csv(fileOut, sep='\t')
print('\ndone')