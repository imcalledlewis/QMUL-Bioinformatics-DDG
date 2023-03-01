def remove_invalid_SNPs(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv"):
# remove SNPs returned from query which have no LD values in LD dataset
    # Load LD dataset as pandas dataframe
    LD_df = pd.read_table(LD_dataset_file)
    # checks for SNPs in subset which are not in LD dataset
    invalid_list = []
    for SNP in SNP_list:
        if SNP not in LD_df['SNP_1'].tolist(): # check if SNP is in LD dataset
            invalid_list.append(SNP) # add to list of invalid SNPs
    print(invalid_list)
    # remove invalid SNPs from SNP list passed to LD plot
    for SNP in invalid_list:
        SNP_list.remove(SNP)
    return SNP_list

SNP_list = remove_invalid_SNPs(SNP_list)