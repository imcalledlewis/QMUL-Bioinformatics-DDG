import numpy as np
import pandas as pd
from math import pi
from bokeh.plotting import figure, output_file, show
from bokeh.transform import linear_cmap
from bokeh.embed import components
from flask import Flask, request, render_template, abort, Response, redirect, url_for
from data.db_scripts import *

# Create a Flask application object
app = Flask(__name__)

 
# Define the root route of the application and specify the methods it accepts
@app.route('/', methods=['GET', 'POST'])
def index():
    # If the request method is POST, get the user input from the form and redirect to the Manhattan plot page
    if request.method == 'POST':
        #Get the value of the 'positions' from the input field 
        positions = request.form['positions']
        # If the 'positions' variable is not empty, redirect to the Manhattan plot page with the 'positions' variable as a query parameter
        # the staryt of a query parameter is '?'
        #the 'url_for' function allows to generate a specific url for a function to redirect a user to a particular page
        if positions:
            return redirect(url_for('Manhattan_plot', positions=positions))
        #If the 'positions' variable is empty, redirect to the entire genomes Manhattan plot 
        else:
            return redirect(url_for('Manhattan_plot'))
    #Render the HTML template for the input page
    return render_template("man_input.html")
    
#Create Manhattan plot page
#Define the route for the Manhattan plot and specify the methods it accepts
@app.route('/plot')
def Manhattan_plot():
    # Get list of chromosome positions from user input
    positions = request.args.get('positions')
    #If the 'positions' variable exists, split it by comma and convert to a list of integers
    if positions:
        # If the input contains a range of positions, create a list of individual positions
        if '-' in positions:
            #If a range of positions is entered splits dash at the "-" and assigns the start and end positions to the variables pos_start and pos_end.
            pos_start, pos_end = [int(pos) for pos in positions.split('-')]
            #Use the range function to generate a list of all positions in the range 
            positions = list(range(pos_start, pos_end + 1))#'+1' makes sure pos_end is included
        #If the input is a comma-separated list, split the string into a list of individual positions
        else:
            positions = [int(pos) for pos in positions.split(',')]

    # Read in the GWAS data as a pandas dataframe
    df = pd.read_csv('./data/TSVs/T1D_GWAS_add.tsv', sep='\t')

    #Filter data by chromosome positions if positions are provided
    if positions:
        df = df[df['cumulative_pos'].isin(positions)]

    # Seperate by chromosome ID, and colour them
    index_cmap = linear_cmap('CHR_ID', palette = ['grey','black']*11,low=1,high=22)

    ## Format figure
    p = figure(frame_width=800,# graph size
               plot_height=500, # graph size
               title="Hover over a plot to see the SNP ID and chomosomal position",# Title added in html
               toolbar_location="right", # location of toolbar
               tools="pan,hover,xwheel_zoom,zoom_out,box_zoom,reset,box_select,tap,undo,save",# Tool features added to make graph interactive
               tooltips="@SNPS: (@CHR_ID,@CHR_POS)"# Shows when mouse is hovered over plot
               )

    #Add circles to the figure to represent the SNPs in the GWAS data
    p.circle(x='cumulative_pos', y='-logp',# x and y-axis
            source=df,
            fill_alpha=0.8,# Transparency of plot
            fill_color=index_cmap,# Colour of plot
            size=7,# Size of plot 
            selection_color="rebeccapurple", # Colour of plot when selected
            hover_color="green"
             )
    
    #Set the x and y axis labels for the plot
    p.xaxis.axis_label = 'Chromosome'# x-axis label 
    p.yaxis.axis_label = '-logp'# y-axis label

    #Set the tick locations and labels for the x axis using the cumulative length of the chromosomes 
    p.xaxis.ticker = [119895261, 373943002, 537393504, 716119012, 834845071, 964538826.5, 1147957441, 1306654016,
                      1396415411, 1540730893, 1674222993, 1823778230, 1930583064, 2055942929, 2141945578, 2202426536,
                      2302961360, 2388903150,
                      2436333506.5, 2482024730, 2529377491, 2584586808]
    #major_label_overrides used to specify custom axis lables as the chromosome no.
    p.xaxis.major_label_overrides = {119895261: '1', 373943002: '2', 537393504: '3', 716119012: '4', 834845071: '5',
                                     964538826.5: '6', 1147957441: '7', 1306654016: '8',
                                     1396415411: '9', 1540730893: '10', 1674222993: '11', 1823778230: '12',
                                     1930583064: '13', 2055942929: '14', 2088496163: '14', 2141945578: '15',
                                     2202426536: '16', 2302961360: '17', 2388903150: '18', 2436333506.5: '19',
                                     2482024730: '20', 2529377491: '21', 2584586808: '22'}
    #change the font colour of the title 
    p.title.text_color = "teal"

    script, div = components(p)

    return render_template("Manplot.html", script=script, div=div)

# Main Driver Function 
if __name__ == '__main__':
  #  Run the application on the local development server 
    app.run(debug=True)
        
