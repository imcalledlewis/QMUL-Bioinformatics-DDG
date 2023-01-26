import pandas as pd

# https://www.ebi.ac.uk/gwas/docs/file-downloads
data = pd.read_csv('gwas_catalog_v1.0-associations_e108_r2023-01-14.tsv', sep='\t', low_memory=False)
data = data.loc[data['DISEASE/TRAIT']=='Type 1 diabetes']   # select only rows regarding type 1 diabetes
data = data.loc[data['CHR_ID']=='6']                        # select only rows for chromosome 6
data = data.replace(" ","_")                                # Replaces spaces with underscores
data.to_csv('gwas_trimmed.tsv', sep='\t')