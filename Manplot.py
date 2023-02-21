## Manhattan plot using Bokeh
import pandas as pd
import numpy as np
from bokeh.plotting import figure,show
from bokeh.models import ColumnDataSource, FixedTicker, FuncTickFormatter
from bokeh.transform import linear_cmap
from bokeh.embed import components
from flask import Flask, request, render_template, abort, Response


app = Flask(__name__)
# Create index page
@app.route('/')
def index():
    return "Hello Team DuckDuck Go"

@app.route('/plot')
def plot():
    df = pd.read_csv('.\data\TSVs\T1D_GWAS_add.tsv', sep='\t') # View data using pandas
    # Seperate by chromosome ID, and colour them
    df.CHR_ID.unique()
    index_cmap = linear_cmap('CHR_ID', palette = ['grey','black']*11,low=1,high=22)
    # Format figure
    p=figure(plot_width=900, # graph size
         plot_height=500, # graph size
         title = None, # Title added in html
         toolbar_location=None, 
         tools="hover", # Allows mouse hover to bring up information
         tooltips="@SNPS: (@CHR_ID,@CHR_POS)" # Shows when mouse is hovered over plot
         )

    # Create Manhattan Plot
    p.scatter('cumulative_pos','-logp', # x,y for scatter graph
          source=df, # Source of data from the tsv file
          fill_alpha=0.6, # Thickness of plot border
          fill_color=index_cmap, # Colour of plot
          size=6 # Size of plot '.'
          #legend='CHR_ID' # Removed legend as it will be in the x-axis
        )
    p.xaxis.axis_label= 'Chromosome' # x-axis label 
    p.yaxis.axis_label= '-logp' # y-axis label
    #p.legend.location = "top_left" # legend will be removed once x-axis is fixed
    script, div = components(p)
 
    return render_template("Manplot.html", script=script, div=div,)

# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server 
    app.run(debug=True)