# Importing required functions
import numpy as np
import pandas as pd
import seaborn as sns
import geneview as gv
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from matplotlib.figure import Figure
import io
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template, send_file

fig,ax=plt.subplots(figsize=(8,8))
ax=sns.set(style="darkgrid")

df = pd.read_csv('./TSVs/T1D_GWAS_add.tsv', sep='\t')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Home'

@app.route('/plot')
def plot():
    g=sns.relplot(
    data = df.sample(642), # for whole genome this number will be 10000, or however many you want to see
    x= 'cumulative_pos',
    y= '-logp',
    aspect = 4, # size of graph
    hue = 'CHR_ID', # for whole genome this is the chromosome
    palette= ['grey','black'] * 11, #random colour scheme, can be changed to any colour(s)
    linewidth=0,
    size=4,
    legend=None
    )
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    return render_template('plot.html', plot_url=plot_data)


# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server 
    app.run(debug=True)