from flask import Flask, render_template
import pandas as pd

#Create flask object 
app = Flask(__name__)
# tell code where to find protein information

#Define the action for the top level route
@app.route('/')
def index():
        return 'Welcome to Team Duck'
    
@app.route('/GENE_NAME/<gene>')
def display_table(gene):
    #Read the CSV file
    data = pd.read_csv('GO_trimmed.csv')
    #Filter the data to only include rows where the 'SYMBOL' column matches the input gene
    filtered_data = data.loc[data['SYMBOL'] == gene]
    #Pass the filtered data to the 'table.html' template
    return render_template('table.html', data=filtered_data)
# define a routed called 'SNP' that accepts a SNP name parameter

    #except:
        # if protein is not found a key error is thrown and we end up here
        #return "We don't have any functional information about a SNP called %s." % Uploaded_variation

#start the server
if __name__ == '__main__' :
    app.run(debug=True) 