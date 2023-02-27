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
    LD_results_df = pd.DataFrame(columns=['SNP_1', 'SNP_2', 'FIN_D\'', 'FIN_r2', 'TSI_D\'', 'TSI_r2', 'GBR_D\'', 'GBR_r2']) 
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

def LD_plot(LD, labels, title):

    n = LD.shape[0]

    figure = plt.figure()

    # mask triangle matrix
    mask = np.tri(n, k=0)
    LD_masked = np.ma.array(LD, mask=mask)

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
                   coordinate_matrix[:, 0].reshape(n + 1, n + 1), np.flipud(LD_masked), edgecolors = "white", linewidth = 1.5, cmap = 'OrRd')
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation='vertical', fontsize=8)
    plt.colorbar()

    # add title
    plt.title(f"{title}", loc = "center")
    
    return figure

def multiple_LD_matrix(SNP_list):
# call LD_heatmap_matrix for all 6 plots
    FIN_D  = LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'FIN' ,plot_type = 'D\'')
    FIN_r2 = LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'FIN' ,plot_type = 'r2')
    TSI_D  = LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'TSI' ,plot_type = 'D\'')
    TSI_r2 = LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'TSI' ,plot_type = 'r2')
    GBR_D  = LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'GBR' ,plot_type = 'D\'')
    GBR_r2 = LD_heatmap_matrix(SNP_list, LD_dataset_file = "data/TSVs/LD_T1DM_Chr6.tsv" ,pop = 'GBR' ,plot_type = 'r2')

    return FIN_D, FIN_r2, TSI_D, TSI_r2, GBR_D, GBR_r2

def multiple_LD_plot(SNP_list):
# call LD_heatmap_matrix for all 6 plots and then create and return 6 LD plots
    FIN_D, FIN_r2, TSI_D, TSI_r2, GBR_D, GBR_r2 =  multiple_LD_matrix(SNP_list)
    FIN_D_plot  = LD_plot(FIN_D,SNP_list,"Finnish $D\'$")
    FIN_r2_plot = LD_plot(FIN_r2,SNP_list,"Finnish $r^2$")
    TSI_D_plot  = LD_plot(TSI_D,SNP_list,"Toscani (Italian) $D\'$")
    TSI_r2_plot = LD_plot(TSI_r2,SNP_list,"Toscani (Italian) $r^2$")
    GBR_D_plot  = LD_plot(GBR_D,SNP_list,"British $D\'$")
    GBR_r2_plot = LD_plot(GBR_r2,SNP_list,"British $r^2$")
    
    return FIN_D_plot, FIN_r2_plot, TSI_D_plot, TSI_r2_plot, GBR_D_plot, GBR_r2_plot

def embed_LD_plots(SNP_list):
# prepares all 6 LD plots for embedding into html 
    FIN_D_plot,FIN_r2_plot,TSI_D_plot,TSI_r2_plot,GBR_D_plot,GBR_r2_plot = multiple_LD_plot(SNP_list)
    # Finnish D prime plot
    buf = BytesIO() # create temporary buffer
    FIN_D_plot.savefig(buf, format="png") # save figure in temporary buffer
    FIN_D_png = base64.b64encode(buf.getbuffer()).decode("ascii") # prepare for embedding
    # Finnish r2 plot
    buf = BytesIO() # create temporary buffer
    FIN_r2_plot.savefig(buf, format="png") # save figure in temporary buffer
    FIN_r2_png = base64.b64encode(buf.getbuffer()).decode("ascii") # prepare for embedding
    # Toscani D prime plot
    buf = BytesIO() # create temporary buffer
    TSI_D_plot.savefig(buf, format="png") # save figure in temporary buffer
    TSI_D_png = base64.b64encode(buf.getbuffer()).decode("ascii") # prepare for embedding
    # Toscani r2 plot
    buf = BytesIO() # create temporary buffer
    TSI_r2_plot.savefig(buf, format="png") # save figure in temporary buffer
    TSI_r2_png = base64.b64encode(buf.getbuffer()).decode("ascii") # prepare for embedding
    # British D prime plot
    buf = BytesIO() # create temporary buffer
    GBR_D_plot.savefig(buf, format="png") # save figure in temporary buffer
    GBR_D_png = base64.b64encode(buf.getbuffer()).decode("ascii") # prepare for embedding
    # British r2 plot
    buf = BytesIO() # create temporary buffer
    GBR_r2_plot.savefig(buf, format="png") # save figure in temporary buffer
    GBR_r2_png = base64.b64encode(buf.getbuffer()).decode("ascii") # prepare for embedding

    return FIN_D_png, FIN_r2_png, TSI_D_png, TSI_r2_png, GBR_D_png, GBR_r2_png