# Importing required functions 
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template

df = pd.read_csv('.\data\TSVs\T1D_GWAS_add.tsv', sep='\t')

my_data = df.sample(642)

# Flask constructor 
app = Flask(__name__)
  
# Generate a scatter plot and returns the figure
def get_plot():
    sns.relplot(
    data = my_data, # for whole genome this number will be 10000, or however many you want to see
    x= 'cumulative_pos',
    y= '-logp',
    aspect = 4, # size of graph
    hue = 'CHR_ID', # for whole genome this is the chromosome
    palette= ['grey','black'] * 11, #random colour scheme, can be changed to any colour(s)
    linewidth=0,
    size=4,
    legend=None
)
    return sns
  
# Root URL
@app.get('/')
def single_converter():
    # Get the matplotlib plot 
    plot = get_plot()
  
    # Save the figure in the static directory 
    plot.savefig(os.path.join('static', 'plot.png'))
  
    return render_template('graph.html')
  
# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server 
    app.run(debug=True)