import pandas as pd
import numpy as np
import itertools
from itertools import permutations
import matplotlib.pyplot as plt

# Imports for displaying plots via flask
from matplotlib.figure import Figure
import base64 
from io import BytesIO

# function which takes a list of SNPs + LD calculations dataset and returns a pandas dataframe
def export_LD(SNP_list,LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv"):
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
    # Loop indexing LD dataset using each pair of SNPs
    for SNP_1,SNP_2 in zip(SNP_1_list,SNP_2_list):
        LD_row = LD_df.loc[((LD_df['SNP_1'] == SNP_1) & (LD_df['SNP_2'] == SNP_2) | 
                            (LD_df['SNP_1'] == SNP_2) & (LD_df['SNP_2'] == SNP_1))] 
        LD_results_df = pd.concat([LD_results_df, LD_row])
    return LD_results_df

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

def LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'FIN' ,plot_type = 'D\''):
# Takes LD dataset dataframe and SNP list and creates a dataframe for heatmap plot
    # Load LD dataset as pandas dataframe
    LD_df = pd.read_table(LD_dataset_file)
    # Create empty dataframe
    LD_matrix_df = pd.DataFrame(columns=[SNP_list]) # One column per SNP in list (SInce a list object is passed, could just pass the SNP list
    for SNP_main in SNP_list:
        # Create empty list
        LD_value_list = []
        # Sub-loop - Loops to create list of datapoints
        for SNP_second in SNP_list:
            if SNP_main == SNP_second:
                SNP_Datapoint = 1
                LD_value_list.append(SNP_Datapoint)
            else:
                #try:
                # Search for specific row containing value
                LD_row = LD_df.loc[((LD_df['SNP_1'] == SNP_main) & (LD_df['SNP_2'] == SNP_second) | 
                            (LD_df['SNP_1'] == SNP_second) & (LD_df['SNP_2'] == SNP_main))] 
                # Extract value and add to list
                SNP_Datapoint = LD_row[f'{pop}_{plot_type}'].tolist()[0] # defaults using Finnish data for Dprime values
                LD_value_list.append(SNP_Datapoint)
                #except:
                    #invalid_list.append((SNP_main,SNP_second))
        # Convert into dataframe row and transpose
        row = pd.DataFrame(LD_value_list).T
        row.columns = LD_matrix_df.columns
        LD_matrix_df = pd.concat([LD_matrix_df, row])
    return LD_matrix_df

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