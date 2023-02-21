## Manhattan plot using Bokeh
import pandas as pd
from bokeh.plotting import figure,show
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
         plot_height=400, # graph size
         title = "Hover over a plot to see the SNP ID and chomosomal position", # Title added in html
         toolbar_location=None, 
         tools="hover", # Allows mouse hover to bring up information
         tooltips="@SNPS: (@CHR_ID,@CHR_POS)" # Shows when mouse is hovered over plot
         )

    # Create Manhattan Plot
    p.scatter('cumulative_pos','-logp', # x,y for scatter graph
          source=df, # Source of data from the tsv file
          fill_alpha=0.6, # Thickness of plot border
          fill_color=index_cmap, # Colour of plot
          size=6 # Size of plot .
        )
    p.xaxis.axis_label= 'Chromosome' # x-axis label 
    p.yaxis.axis_label= '-logp' # y-axis label
    
    # Correct the x-axis by replacing the cumulative_pos with the Chromosome position
    p.xaxis.ticker = [119895261, 373943002, 537393504, 716119012, 834845071, 964538826.5, 1147957441, 1306654016, 
    1396415411, 1540730893, 1674222993, 1823778230, 1930583064, 2055942929, 2141945578, 2202426536, 2302961360, 2388903150, 
    2436333506.5, 2453458246, 2551821399, 2584586808]
    p.xaxis.major_label_overrides = {119895261:'1', 373943002:'2', 537393504: '3', 716119012:'4', 834845071:'5', 964538826.5:'6', 1147957441: '7', 1306654016: '8', 
    1396415411:'9', 1540730893:'10', 1674222993:'11', 1823778230:'12', 1930583064:'13', 2055942929:'14', 2088496163 :'14', 2141945578:'15',
    2202426536:'16', 2302961360:'17', 2388903150:'18', 2436333506.5:'19', 2453458246:'20', 2551821399:'21', 2584586808: '22'}
    script, div = components(p)
 
    return render_template("Manplot.html", script=script, div=div,)

# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server 
    app.run(debug=True)