#based on pp05 by conrad https://github.com/conradbessant/webintro

# General imports:
from flask import Flask, render_template, url_for, redirect, request
import pandas as pd

# Imports for creating and processing forms:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

debug=True	# Change this to False for deployment

# create a flask application object
app = Flask(__name__)
# we need to set a secret key attribute for secure forms
app.config['SECRET_KEY'] = 'change this unsecure key'   # TODO: read about this and change

# tell code where to find snp information
snp_table_filename = 'data/gwas_trimmed.tsv'

# create a class to define the form
class QueryForm(FlaskForm):
	SNP_req = StringField('Enter SNP information: ', validators=[InputRequired()])
	req_type = SelectField("Information type: ", choices=[('SNPname', "SNP name(s) (rs value)"), ("coords","genomic coordinates"), ("geneName","gene name")])
	submit = SubmitField('Submit')

# define the action for the top level route
@app.route('/', methods=['GET','POST'])
def index():
	form = QueryForm()                  # Create form to pass to template
	SNP_req = None
	req_type = None
	if form.validate_on_submit():
		SNP_req = form.SNP_req.data
		req_type = form.req_type.data
		if debug:
			print('\n\nUser input: '+SNP_req)		# Print what the user submitted (without checking for correctness)
			print("Input type: "+req_type+'\n\n')	# Print the type of data submitted
		return redirect(url_for('SNP', SNP_req = SNP_req,req_type=req_type))
	return render_template('index_page.html', form=form, SNP_req=SNP_req, req_type=req_type)

# define a route called 'SNP' which accepts a SNP name parameter
@app.route('/SNP/<SNP_req>', methods=['GET','POST'])
def SNP(SNP_req):
	req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	# load snp data from TSV file into pandas dataframe with snp name as index
	df = pd.read_csv(snp_table_filename,sep='\t',index_col='SNPS')

	SNP_req = SNP_req.lower()		# ensure snp name is in lowercase letters
	try:                            # try to extract row for specified SNP
		row = df.loc[SNP_req]
									# if snp is found, return some information about it:
		return render_template('view.html', name=SNP_req, chr_pos=str(row.CHR_POS), req_type=req_type)
	except KeyError:                # If SNP not found:
		return render_template('not_found.html', name=SNP_req)

# start the web server
if __name__ == '__main__':
	app.run(debug=debug)
