# Importing required functions 
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template

df = pd.read_csv('.\data\TSVs\T1D_GWAS_add.tsv', sep='\t')
my_data = df.sample(642)

fig,ax=plt.subplots(figsize=(6,6))
ax=sns.set_style(style="darkgrid")


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('graph.html')

@app.route('/graph')
def graph():
    g=sns.relplot(
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
    g.ax.set_xlabel('Chromosome') # x-axis label
    g.ax.set_xticks(df.groupby('CHR_ID')['cumulative_pos'].median())
    g.ax.set_xticklabels(df['CHR_ID'].unique())
    g.fig.suptitle('Manhatton Plot showing Association between SNPs and T1DM in GWAS')
    #annotations = my_data[my_data['-logp'] > 20].apply(lambda p : g.ax.annotate(p['SNPS'], (p['cumulative_pos'], p['-logp'])), axis=1).to_list()
    #adjust_text(annotations, arrowprops = {'arrowstyle': '->', 'color':'blue'})
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')


# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server 
    app.run(debug=True)