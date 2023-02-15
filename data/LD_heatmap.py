import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from itertools import permutations

# Load in LD dataset as pandas dataframe
LD_df = pd.read_table('LD_T1DM_Chr6.tsv')
# SNP_list should come from user input, for now test using known subset of SNPs
SNP_list = ['rs1265057',
 'rs116763857',
 'rs9264758',
 'rs9501130',
 'rs3093664',
 'rs3134938']
# Takes list of SNPs (SNP_list) returned from user and creates a pair of lists containing the 1st and 2nd SNP of each combination
SNP_combinations = list(itertools.combinations(SNP_list,2))
SNP_1_list = []
SNP_2_list = []
for SNP_pair in SNP_combinations:
    SNP_1_list.append(SNP_pair[0])
    SNP_2_list.append(SNP_pair[1])
# Create empty dataframe for matrix
LD_matrix_df = pd.DataFrame(columns=[SNP_list]) # One column per SNP in list (Since a list object is passed, could just pass the SNP list
# Loop to build matrix of LD values
for SNP_main in SNP_list:
    # Loops to create list of LD values for dataframe row
    LD_value_list = []
    for SNP_second in SNP_list:
        # sets LD value to 1 if both SNP rsIDs are identical
        if SNP_main == SNP_second:
            SNP_Datapoint = 1
            LD_value_list.append(SNP_Datapoint)
        else:
            # Search for specific row containing value
            LD_row = LD_df.loc[((LD_df['SNP_1'] == SNP_main) & (LD_df['SNP_2'] == SNP_second) | 
                        (LD_df['SNP_1'] == SNP_second) & (LD_df['SNP_2'] == SNP_main))] 
            # Extract value and add to list (currently testing using Finnish data for D prime values)
            SNP_Datapoint = LD_row['FIN_D\''].tolist()[0] # To change population and/or metric, edit 'FIN_D\'' to another column heading in LD_T1DM_Chr6.tsv (e.g. TSI_r2)
            LD_value_list.append(SNP_Datapoint)
    # Convert into dataframe row, transpose and concat row to matrix dataframe
    row = pd.DataFrame(LD_value_list).T
    row.columns = LD_matrix_df.columns
    LD_matrix_df = pd.concat([LD_matrix_df, row])



# function for LD heatmap plot
def ld_plot(ld, labels: list[str]):
    """
    ld_plot(ld, labels: list[str])
    Plot of a Linkage Disequilibrium (LD) matrix
    :param ld: A symmetric LD matrix
    :param labels: A list of position names
    """
    n = ld.shape[0]

    figure = plt.figure()

    # mask triangle matrix
    mask = np.tri(n, k=0)
    ld_masked = np.ma.array(ld, mask=mask)

    # create rotation/scaling matrix
    t = np.array([[1, 0.5], [-1, 0.5]])
    # create coordinate matrix and transform it
    coordinate_matrix = np.dot(np.array([(i[1], i[0])
                                         for i in itertools.product(range(n, -1, -1), range(0, n + 1, 1))]), t)
    # plot
    ax = figure.add_subplot(1, 1, 1)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.tick_params(axis='x', which='both', top=False)
    plt.pcolor(coordinate_matrix[:, 1].reshape(n + 1, n + 1),
                   coordinate_matrix[:, 0].reshape(n + 1, n + 1), np.flipud(ld_masked), edgecolors = "white", linewidth = 1.5, cmap = 'OrRd')
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation='vertical', fontsize=8)
    plt.colorbar()
    
    return figure

# call ld_plot() function to create LD heatmap figure and export as a PNG file
figure = ld_plot(ld=LD_matrix_df, labels=SNP_list)
figure.savefig('LD_heatmap_plot.png')