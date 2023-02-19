#based on pp05 by conrad https://github.com/conradbessant/webintro

# General imports:
from flask import Flask, render_template, url_for, redirect, request
import pandas as pd

# Imports for creating and processing forms:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

# Import custom library:
from data.db_scripts import *

debug=True	# Change this to False for deployment

# create a flask application object
app = Flask(__name__)
# we need to set a secret key attribute for secure forms
app.config['SECRET_KEY'] = 'change this unsecure key'   # TODO: read about this and change

pop_header = ["Variation", "Finland", "Toscani", "British"]		# Header for population frequencies table


# tell code where to find snp information
# snp_table_filename = getPath('gwas_trimmed.tsv')

# create a class to define the form
class QueryForm(FlaskForm):
	SNP_req = StringField('Enter SNP information: ', validators=[InputRequired()])
	req_type = SelectField("Information type: ", choices=[('rsid', "SNP name(s) (rs value)"), ("coords","genomic coordinates"), ("geneName","gene name")])
	submit = SubmitField('Submit')




# define the action for the top level route
@app.route('/', methods=['GET','POST'])
def index():
	form = QueryForm()		# Create form to pass to template
	SNP_req = None
	req_type = None
	if form.validate_on_submit():
		SNP_req = form.SNP_req.data
		SNP_req = SNP_req.replace(' ', '')		# Removes whitespace from request
		req_type = form.req_type.data
		if debug:								# Only print following if debug mode:
			print('\nUser input: '+SNP_req)		# Print what the user submitted (without checking for correctness)
			print("Input type: "+req_type+'\n')	# Print the type of data submitted
		return redirect(url_for('SNP', SNP_req = SNP_req,req_type=req_type))
	return render_template('index_page.html', form=form, SNP_req=SNP_req, req_type=req_type)




# Define a route called 'SNP' which accepts a SNP name parameter
@app.route('/SNP/<SNP_req>', methods=['GET','POST'])
def SNP(SNP_req):
	req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	assert req_type != "empty_req_type", "request type is empty"

	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters
	SNP_req=SNP_req.split(',')		# Split request by comma separator
	reqRes=DBreq(SNP_req, req_type)	# Make SQL request
	if reqRes:						# If the response isn't None
			assert isinstance(reqRes, dict),"invalid db request return value"
			if debug:
				print ("request response:",reqRes)
			return render_template('view.html', reqRes=reqRes, pop_header=pop_header)
	else:                 			# If SNP is not found:
		return render_template('not_found.html', name=SNP_req)




# Start the web server
if __name__ == '__main__':
	app.run(debug=debug)