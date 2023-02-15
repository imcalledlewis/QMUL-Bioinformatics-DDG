import pandas as pd
import itertools
from itertools import permutations

# SNP_list should come from user input, for now test using known subset of SNPs
SNP_list = ['rs138181578',
 'rs9354144',
 'rs72928038',
 'rs1538171',
 'rs114631266',
 'rs2471863',
 'rs34941730']
# Takes list of SNPs (SNP_list) returned from user and creates a pair of lists containing the 1st and 2nd SNP of each combination
SNP_combinations = list(itertools.combinations(SNP_list,2))
SNP_1_list = []
SNP_2_list = []
for SNP_pair in SNP_combinations:
    SNP_1_list.append(SNP_pair[0])
    SNP_2_list.append(SNP_pair[1])
# Load LD dataset and create empty dataframe for filtered results
LD_df = pd.read_table('LD_T1DM_Chr6.tsv')
LD_results = pd.DataFrame(columns=['SNP_1', 'SNP_2', 'FIN_D\'', 'FIN_r2', 'TSI_D\'', 'TSI_r2 ', 'GBR_D\'', 'GBR_r2 ']) 
# Loop indexing LD dataset using each pair of SNPs
for SNP_1,SNP_2 in zip(SNP_1_list,SNP_2_list):
    LD_row = LD_df.loc[(LD_df['SNP_1'] == SNP_1) & (LD_df['SNP_2'] == SNP_2)]
    LD_results = pd.concat([LD_results, LD_row])
# Write out LD results dataframe as a TSV file
LD_results.to_csv('LD_results.tsv', sep="\t", index=False )