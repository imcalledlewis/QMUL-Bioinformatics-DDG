# Load LD dataset and create empty dataframe for filtered results
LD_df = pd.read_table(LD_dataset_file)
LD_results_df = pd.DataFrame(columns=['SNP_1', 'SNP_2', 'FIN_D\'', 'FIN_r2', 'TSI_D\'', 'TSI_r2', 'GBR_D\'', 'GBR_r2']) 
# create a pair of lists containing the 1st and 2nd SNP of each combination
SNP_1_list, SNP_2_list = SNP_pair_lists(SNP_list)
# Loop indexing LD dataset using each pair of SNPs
for SNP_1,SNP_2 in zip(SNP_1_list,SNP_2_list):
    LD_row = LD_df.loc[((LD_df['SNP_1'] == SNP_1) & (LD_df['SNP_2'] == SNP_2) | 
                        (LD_df['SNP_1'] == SNP_2) & (LD_df['SNP_2'] == SNP_1))] 
    LD_results_df = pd.concat([LD_results_df, LD_row])