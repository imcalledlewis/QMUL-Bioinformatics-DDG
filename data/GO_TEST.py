from flask import Flask, render_template
import pandas as pd

#Create flask object 
app = Flask(__name__)
# tell code where to find protein information

#Define the action for the top level route
@app.route('/')
def index():
        return 'Welcome to Team Duck'

# define a routed called GENE_RS that accepts a Gene symbol parameter   
@app.route('/GENE_RS/<RSid>')
def display_table_RSid(RSid):
    #Read the CSV file
    data = pd.read_csv('GO_trimmed.csv')
    #Filter the data to only include rows where the 'Uploaded_variation' column matches the input RSid
    filtered_data = data.loc[data['Uploaded_variation'] == RSid]
    #Pass the filtered data to the 'table.html' template
    return render_template('table.html', data=filtered_data)

# define a routed called GENE_SYM that accepts a Gene symbol parameter   
@app.route('/GENE_SYM/<gene>')
def display_table_SYM(gene):
    #Read the CSV file
    data = pd.read_csv('GO_trimmed.csv')
    #Filter the data to only include rows where the 'SYMBOL' column matches the input gene
    filtered_data = data.loc[data['SYMBOL'] == gene]
    #Pass the filtered data to the 'table.html' template
    return render_template('table.html', data=filtered_data)

# define a routed called GENE_NAME that accepts a Gene name parameter  
@app.route('/GENE_NAME/<gene>')
def display_table_NAME(gene):
    #Read the CSV file
    data = pd.read_csv('GO_trimmed.csv')
    #Filter the data to only include rows where the 'Gene' column matches the input gene
    filtered_data = data.loc[data['Gene'] == gene]
    #Pass the filtered data to the 'table.html' template
    return render_template('table.html', data=filtered_data)

# define a routed called GENE_LOC that accepts Loc A a parameter    
@app.route('/GENE_LOC/<Loc>')
def display_table_LOC(Loc):
    #Read the CSV file
    data = pd.read_csv('GO_trimmed.csv')
    #Filter the data to only include rows where the 'Location' column matches the input Loc
    filtered_data = data.loc[data['Location'] == Loc]
    #Pass the filtered data to the 'table.html' template
    return render_template('table.html', data=filtered_data)

#start the server
if __name__ == '__main__' :
    app.run(debug=True) 
