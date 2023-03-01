# Take list of SNPs and creates a pair of lists containing the 1st and 2nd SNP of each combination  
def SNP_pair_lists(SNP_list):
    SNP_combinations = list(itertools.combinations(SNP_list,2))
    SNP_1_list = [] # 1st SNP of pair
    SNP_2_list = [] # 2nd SNP of pair
    for SNP_pair in SNP_combinations:
        SNP_1_list.append(SNP_pair[0])
        SNP_2_list.append(SNP_pair[1])
    return SNP_1_list, SNP_2_list

SNP_1_list, SNP_2_list = SNP_pair_lists(SNP_list)