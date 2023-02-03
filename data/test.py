# ### Sandbox for testing ideas and functions. Very much subject to change.

from db_scripts import *
import json

path=getPath("gwas_trimmed.tsv",tsv=True)
df=pd.read_csv(path,sep='\t')
print(df.head())