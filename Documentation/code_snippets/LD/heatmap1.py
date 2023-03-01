# load LD dataset
LD_df = pd.read_table('LD_T1DM_Chr6.tsv')
# checks for SNPs in subset which are not in LD dataset
SNP_list = remove_invalid_SNPs(SNP_list)
# create a pair of lists containing the 1st and 2nd SNP of each combination
SNP_1_list, SNP_2_list = SNP_pair_lists(SNP_list)