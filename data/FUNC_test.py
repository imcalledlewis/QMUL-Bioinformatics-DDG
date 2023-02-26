from flask import Flask, render_template
import pandas as pd

#Create flask object 
app = Flask(__name__)

# tell code where to find protein information
FUNCT_table_filename = 'Func_trimmed.csv'


#Define the action for the top level route
@app.route('/')
def index():
        return 'Welcome to Team Duck'
    
    
# define a routed called 'SNP' that accepts a SNP name parameter
@app.route('/Functional_score/<Uploaded_variation>')
def Functional_score(Uploaded_variation):
    df = pd.read_csv(FUNCT_table_filename, sep='\,', index_col= 0) # load protein data from TSV file into pandas dataframe
    Uploaded_variation = Uploaded_variation.lower() # All rs values are lower case changes any input in to lowercase
    
    try:  # try to extract row for specified protein
        row = df.loc[Uploaded_variation]
        # if protein is found, return some information about it
        return render_template('Functional_view.html', name=Uploaded_variation,CADD_PHRED=str(row.CADD_PHRED), CADD_RAW=str(row.CADD_RAW),  Allele=str(row.Allele))      
# original test code        
        #return '<h1>' + Uploaded_variation + '</h1>' \
        #+ '<p>CADD PHRED score: ' + str(row.CADD_PHRED) + '</p>' \
        #+ '<p>CADD RAW score: ' + str(row.CADD_RAW) + '</p>' \
        #+ '<p>Varient Allele used for consequence calculation: ' + str(row.Allele) + '</p>'
       
    except:
        # if protein is not found a key error is thrown and we end up here
        return "We don't have any functional information about a SNP called %s." % Uploaded_variation

#start the server
if __name__ == '__main__' :
    app.run(debug=True) 