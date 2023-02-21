import pandas as pd
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row 
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.transform import linear_cmap
import numpy as np
from flask import Flask, request, render_template, abort, Response


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Team DuckDuck Go"

@app.route('/plot')
def plot():
    df = pd.read_csv('.\data\TSVs\T1D_GWAS_add.tsv', sep='\t')
    df.CHR_ID.unique()
    index_cmap = linear_cmap('CHR_ID', palette = ['grey','black'],low=1,high=22)

    p=figure(plot_width=900, 
         plot_height=500, 
         title = "Manhattan Plot", 
         toolbar_location=None, 
         tools="hover", 
         tooltips="@SNPS: (@CHR_ID,@CHR_POS)"
         )
    p.circle('cumulative_pos','-logp',
          source=df, 
          fill_alpha=0.6,
          fill_color=index_cmap,
          size=10, legend='CHR_ID'
        )
    p.xaxis.axis_label= 'Chromosome'
    p.yaxis.axis_label= '-logp'
    p.legend.location = "top_left"

    script, div = components(p)
 
    return render_template("Manplot.html", script=script, div=div,)

# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server 
    app.run(debug=True)