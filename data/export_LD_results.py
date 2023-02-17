import pandas as pd
import itertools
from itertools import permutations

# function which takes a list of SNPs + LD calculations dataset and returns a pandas dataframe
def export_LD(SNP_list,LD_dataset_file):
    # Take list of SNPs (SNP_list) returned from user and creates a pair of lists containing the 1st and 2nd SNP of each combination
    SNP_combinations = list(itertools.combinations(SNP_list,2))
    SNP_1_list = []
    SNP_2_list = []
    for SNP_pair in SNP_combinations:
        SNP_1_list.append(SNP_pair[0])
        SNP_2_list.append(SNP_pair[1])
    # Load LD dataset and create empty dataframe for filtered results
    LD_df = pd.read_table(LD_dataset_file)
    LD_results_df = pd.DataFrame(columns=['SNP_1', 'SNP_2', 'FIN_D\'', 'FIN_r2', 'TSI_D\'', 'TSI_r2 ', 'GBR_D\'', 'GBR_r2 ']) 
    # Loop indexing LD dataset using each pair of SNPs and adding rows to results dataframe
    for SNP_1,SNP_2 in zip(SNP_1_list,SNP_2_list):
        LD_row = LD_df.loc[(LD_df['SNP_1'] == SNP_1) & (LD_df['SNP_2'] == SNP_2)]
        LD_results_df = pd.concat([LD_results_df, LD_row])
    return LD_results_df
    