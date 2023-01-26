# Simple example of a web application
# pp05: Now with a form to enter protein name

from flask import Flask, render_template, url_for, redirect
import pandas as pd

# import libraries needed create and process forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

# create a flask application object
app = Flask(__name__)
# we need to set a secret key attribute for secure forms
app.config['SECRET_KEY'] = 'change this unsecure key'

# tell code where to find protein information
snp_table_filename = 'gwas_trimmed.tsv'

# create a class to define the form
class QueryForm(FlaskForm):
	SNP_name = StringField('Enter a valid UniProt protein name:', validators=[InputRequired()])
	submit = SubmitField('Submit')

# define the action for the top level route
@app.route('/', methods=['GET','POST'])
def index():
	# this route has been updated to use a template containing a form
	form = QueryForm()  # create form to pass to template
	SNP_name = None
	if form.validate_on_submit():
		SNP_name = form.SNP_name.data
		print('\n\n\n'+SNP_name+'\n\n\n')
		return redirect(url_for('SNP', SNP_name = SNP_name))
	return render_template('index_page.html', form=form, SNP_name=SNP_name)

# define a route called 'SNP' which accepts a SNP name parameter
@app.route('/SNP/<SNP_name>')
def SNP(SNP_name):

    # load protein data from TSV file into pandas dataframe with protein name as index
    df = pd.read_csv(snp_table_filename,sep='\t',index_col='SNPS')

    SNP_name = SNP_name.lower()  # ensure snp name is in lowercase letters
    try:  # try to extract row for specified protein
        row = df.loc[SNP_name]
        # if protein is found, return some information about it
        return render_template('view.html', name=SNP_name, chr_pos=str(row.CHR_POS))
    except:
        # if protein is not found a key error is thrown and we end up here
        return render_template('not_found.html', name=SNP_name)

# start the web server
if __name__ == '__main__':
	app.run(debug=True)
