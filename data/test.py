# Testing ground for various ideas. Very much subject to change.

from db_scripts import *

fileIn = 'gwas_trimmed.tsv'
filepath = getPath(fileIn)
data = pd.read_csv(filepath, sep='\t')

dupeList = data.duplicated(subset='SNPS',keep=False)    # Get list of duplicate values
dupes=data[dupeList]                                    # Select dataframe using above list
dupes.sort_values("SNPS",inplace=True)                  # Sort dataframe


# sort
# list of lists,
# rank, use key= pval
# 