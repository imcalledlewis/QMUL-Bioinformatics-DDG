#based on pp05 by conrad https://github.com/conradbessant/webintro


# General imports:
from flask import Flask, render_template, url_for, redirect
import pandas as pd

# Imports for creating and processing forms:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

# create a flask application object
app = Flask(__name__)
# we need to set a secret key attribute for secure forms
app.config['SECRET_KEY'] = 'change this unsecure key'   # TODO: read about this and change

# tell code where to find snp information
snp_table_filename = 'data/gwas_trimmed.tsv'

# create a class to define the form
class QueryForm(FlaskForm):
	SNP_name = StringField('Enter SNP information: ', validators=[InputRequired()])
	infoType = SelectField("Information type: ", choices=["SNP name(s) (rs value)", "genomic coordinates", "gene name"])
	submit = SubmitField('Submit')

# define the action for the top level route
@app.route('/', methods=['GET','POST'])
def index():
	form = QueryForm()                  # Create form to pass to template
	SNP_name = None
	if form.validate_on_submit():
		SNP_name = form.SNP_name.data
		print('\n\n'+SNP_name+'\n\n')   # Print what the user submitted (without checking for correctness) 
		return redirect(url_for('SNP', SNP_name = SNP_name))
	return render_template('index_page.html', form=form, SNP_name=SNP_name)

# define a route called 'SNP' which accepts a SNP name parameter
@app.route('/SNP/<SNP_name>')
def SNP(SNP_name):

    # load snp data from TSV file into pandas dataframe with snp name as index
    df = pd.read_csv(snp_table_filename,sep='\t',index_col='SNPS')

    SNP_name = SNP_name.lower()     # ensure snp name is in lowercase letters
    try:                            # try to extract row for specified SNP
        row = df.loc[SNP_name]
                                    # if snp is found, return some information about it:
        return render_template('view.html', name=SNP_name, chr_pos=str(row.CHR_POS))
    except KeyError:                # If SNP not found:
        return render_template('not_found.html', name=SNP_name)

# start the web server
if __name__ == '__main__':
	app.run(debug=True)
