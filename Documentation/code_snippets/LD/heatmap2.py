LD_matrix_df = pd.DataFrame(columns=[SNP_list]) # One column per SNP in list (Since a list object is passed, could just pass the SNP list
for SNP_1 in SNP_list:
    # Create empty list
    LD_value_list = []
    # Sub-loop - Loops to create list of datapoints
    for SNP_2 in SNP_list:
        if SNP_1 == SNP_2:
            SNP_Datapoint = 1
            LD_value_list.append(SNP_Datapoint)
        else:
            #try:
            # Search for specific row containing value
            LD_row = LD_df.loc[((LD_df['SNP_1'] == SNP_1) & (LD_df['SNP_2'] == SNP_2) | 
                                (LD_df['SNP_1'] == SNP_2) & (LD_df['SNP_2'] == SNP_1))] 
            # Extract value and add to list
            SNP_Datapoint = LD_row['GBR_r2'].tolist()[0] # currently using Finnish data
            LD_value_list.append(SNP_Datapoint)
            #except:
                #invalid_list.append((SNP_main,SNP_second))
    # Convert into dataframe row and transpose
    row = pd.DataFrame(LD_value_list).T
    row.columns = LD_matrix_df.columns
    LD_matrix_df = pd.concat([LD_matrix_df, row])