# Create Empty dataframe 
LD_dataset = pd.DataFrame(columns=['SNP_1', 'SNP_2', 'FIN_D\'', 'FIN_r2', 'TSI_D\'', 'TSI_r2', 'GBR_D\'', 'GBR_r2'])
# Indexes the respective LD calculation for each pair and adds it to the data
for SNP_1,SNP_2 in zip(SNP_1_list,SNP_2_list):
    # Finland
    FIN_D = LD_D_FIN[SNP_1].loc[SNP_2]
    FIN_r2 = LD_r2_FIN[SNP_1].loc[SNP_2]
    # Italy - Tuscany
    TSI_D = LD_D_TSI[SNP_1].loc[SNP_2]
    TSI_r2 = LD_r2_TSI[SNP_1].loc[SNP_2]
    # British
    GBR_D = LD_D_GBR[SNP_1].loc[SNP_2]
    GBR_r2 = LD_r2_GBR[SNP_1].loc[SNP_2]
    # Create row of data and combine with LD dataset dataframe
    row_list = [SNP_1, SNP_2, FIN_D, FIN_r2, TSI_D, TSI_r2, GBR_D, GBR_r2]
    row = pd.DataFrame(row_list).T

    row.columns = LD_dataset.columns
    LD_dataset = pd.concat([LD_dataset, row])
# Write out LD dataset as a TSV
LD_dataset.to_csv('LD_T1DM_Chr6.tsv', sep="\t", index=False)