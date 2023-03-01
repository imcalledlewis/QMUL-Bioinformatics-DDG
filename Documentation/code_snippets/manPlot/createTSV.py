import pandas as pd
import numpy as np

df = pd.read_csv('./TSVs/GWAS_T1D.tsv', sep='\t') # Make the table readable using pandas

# -log the P-values and column to the table
df['-logp']= - np.log(df['p_value'])

# Put variants in order by max position in chromosome
running_pos = 0 # moves all integers down so first pos is 0
 
cumulative_pos = [] # create list of new series for position in whole genome

for chrom, group_df in df.groupby('chr_id'): # Group the region in each chromosome together
    cumulative_pos.append(group_df['chr_pos'] + running_pos) 
    running_pos+= group_df['chr_pos'].max() #tells us the last position in each chromosome

# Position of variant relative to whole chromosome, add column to the table    
df['cumulative_pos'] = pd.concat(cumulative_pos) 
df.to_csv('./TSVs/GWAS_T1D_add.tsv', sep ='\t')