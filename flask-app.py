# General imports:
from flask import Flask, render_template, url_for, redirect, request, Response
import pandas as pd

# Imports for creating and processing forms:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

# Import custom libraries:
from data.db_scripts import *	# Database related stuff
from data.LD_scripts import *	# LD data and heatmap

debug=True	# Change this to False for deployment

# create a flask application object
app = Flask(__name__)
# we need to set a secret key attribute for secure forms
app.config['SECRET_KEY'] = 'change this unsecure key'   # TODO: read about this and change


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
	return render_template('index_page.html', form=form, SNP_req=SNP_req, req_type=req_type,debug=debug)




# Define a route called 'SNP' which accepts a SNP name parameter
@app.route('/SNP/<SNP_req>', methods=['GET','POST'])
def SNP(SNP_req):
	req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	assert req_type != "empty_req_type", "request type is empty"

	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters
	name=SNP_req
	reqRes,SNP_list=DBreq(SNP_req, req_type)	# Make SQL request
	if reqRes:						# If the response isn't None
			assert isinstance(reqRes, dict),"invalid db request return value"
			if debug:
				print ("\nrequest response:",reqRes,"\n")
			l=len(reqRes)
			if l==1:
				name=str(list(reqRes.keys())[0])
			else:
				name=f'{l} SNPS	'
			return render_template('view.html', reqRes=reqRes, name=name, req_type=req_type, len = len(SNP_list), SNP_req = SNP_req,debug=debug)
	else:                 			# If SNP is not found:
		return render_template('not_found.html', name=name)




# Linkage Disequilibrium results 
@app.route('/LD_results/<SNP_req>', methods=['GET','POST'])
def LD_results(SNP_req):
	req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	assert req_type != "empty_req_type", "request type is empty"

	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters

	reqRes,SNP_list=DBreq(SNP_req, req_type)	# Make SQL request
	if reqRes:						# If the response isn't None
			assert isinstance(reqRes, dict),"invalid db request return value"
			if debug:
				print ("request response:",reqRes)
			LD_data = export_LD(SNP_list) # create LD results dataframe using SNP list returned from query
			return render_template('LD_results.html', data=LD_data, name=SNP_req, req_type=req_type)
	else:                 			# If SNP is not found:
		return render_template('not_found.html', name=SNP_req)




# Linkage Disequilibrium results 
@app.route('/LD_heatmap/<SNP_req>', methods=['GET','POST'])
def LD_plot(SNP_req):
	req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	assert req_type != "empty_req_type", "request type is empty"

	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters

	reqRes,SNP_list=DBreq(SNP_req, req_type)	# Make SQL request
	if reqRes:						# If the response isn't None
			assert isinstance(reqRes, dict),"invalid db request return value"
			if debug:
				print ("request response:",reqRes)
			SNP_list = remove_invalid_SNPs(SNP_list)
			FIN_D_data, FIN_r2_data, TSI_D_data, TSI_r2_data, GBR_D_data, GBR_r2_data = embed_LD_plots(SNP_list) # create LD heatmap dataframe using SNP list returned from query
			return render_template('LD_plot.html', 
									FIN_D_data=FIN_D_data, FIN_r2_data=FIN_r2_data, 
									TSI_D_data=TSI_D_data, TSI_r2_data=TSI_r2_data,
									GBR_D_data=GBR_D_data, GBR_r2_data=GBR_r2_data,
									name = SNP_req, req_type=req_type, SNP_list = SNP_list)
	else:                 			# If SNP is not found:
		return render_template('not_found.html', name=SNP_req)




@app.route('/download/<SNP_req>')
def download(SNP_req):
	req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	assert req_type != "empty_req_type", "request type is empty"
	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters
	reqRes,SNP_list=DBreq(SNP_req, req_type)	# Make SQL request
	if reqRes:						# If the response isn't None
		assert isinstance(reqRes, dict),"invalid db request return value"
		if debug:
			print ("request response:",reqRes)
		LD_data = export_LD(SNP_list) # create LD results dataframe using SNP list returned from query
		return Response(LD_data.to_csv(sep='\t'),mimetype="text/csv", headers={"Content-disposition": "attachment; filename=LD_results.tsv"})
	

# Start the web server
if __name__ == '__main__':
	app.run(debug=debug)