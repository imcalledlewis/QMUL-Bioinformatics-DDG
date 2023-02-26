# General imports:
from flask import Flask, render_template, url_for, redirect, request, Response,abort
import pandas as pd

import numpy as np
import pandas as pd
from math import pi
from bokeh.plotting import figure, output_file, show
from bokeh.transform import linear_cmap
from bokeh.embed import components
# from flask import Flask, request, render_template, abort, Response, redirect, url_for

# Imports for creating and processing forms:
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

# Import custom libraries:
from data.db_scripts import *	# Database related stuff
from data.LD_scripts import *	# LD data and heatmap

debug=True	# Change this to False for deployment
setDebug(debug)

# create a flask application object
app = Flask(__name__)
# we need to set a secret key attribute for secure forms
app.config['SECRET_KEY'] = 'change this unsecure key'   # TODO: read about this and change

# Exceptions:
class db_err(Exception):	# Unspecified error
	pass
class myBad(db_err):		# Server side error
	pass
class yourBad(db_err):		# User side error
	pass




# create a class to define the form
class QueryForm(FlaskForm):
	SNP_req = StringField('Enter SNP information: ', validators=[InputRequired()])
	req_type = SelectField("Information type: ", choices=[('auto', 'Automatically detect'),('rsid', "SNP name(s) (rs value)"), ("coords","genomic coordinates"), ("geneName","gene name")])
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

	if req_type == 'auto':
		if re.search(r'rs\d+',SNP_req):
			req_type='rsid'
		elif re.search(r'\d:\d+', SNP_req):
			req_type='coords'
		elif re.search(r'\w{1,10}', SNP_req):
			req_type='geneName'
		else:
			# raise()
			# pass
			raise Exception("couldn't determine request type")
			req_type= None
		if debug:
			print("detected type:", req_type)

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
			return render_template('view.html', reqRes=reqRes, name=name, req_type=req_type, len=len(SNP_list), SNP_req=SNP_req,debug=debug,SNP_list=SNP_list)
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
	

######################################################################################################################################

# @app.route('/plot', methods=['GET','POST'])
@app.route('/manPlot/<SNP_req>/', methods=['GET','POST'])
def Manhattan_plot(SNP_req):
	# req_type=request.args.get('req_type',default="empty_req_type")	# Gets type of information inputted (the bit after "?")
	# assert req_type != "empty_req_type", "request type is empty"



	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters
	name=SNP_req
	reqRes,SNP_list=DBreq(SNP_req, 'coords',manPlot=True)	# Make SQL request
	if reqRes:						# If the response isn't None
			assert isinstance(reqRes, dict),"invalid db request return value"
			if debug:
				# print ("\nrequest response:",reqRes,"\n")
				pass
			name='{} SNPS'.format(len(SNP_list))
			# return render_template('view.html', reqRes=reqRes, name=name, req_type=req_type, len=len(SNP_list), SNP_req=SNP_req,debug=debug,SNP_list=SNP_list)
	else:
		return("manhattan plot parsing failed")                 			# If SNP is not found:
		# return render_template('not_found.html', name=name)

	df=pd.DataFrame(reqRes).T
	df.rename_axis("rsid", axis="columns",inplace=True)
	df.rename(columns={0:"chr_id",1:"cumulative_pos", 2:"-logp"},inplace=True)
	print(df)	
	# return("test")

	#If the 'positions' variable exists, split it by comma and convert to a list of integers
	# if positions:
	# 	positions = [int(pos) for pos in positions.split(',')]

	# Read in the GWAS data as a pandas dataframe
	# df = pd.read_csv('T1D_GWAS_add.tsv', sep='\t')



	#Filter data by chromosome positions if positions are provided
	# if positions:
	# 	df = df[df['cumulative_pos'].isin(positions)]

	# Separate by chromosome ID, and colour them
	df.chr_id.unique()
	index_cmap = linear_cmap('chr_id', palette = ['grey','black']*11,low=1,high=22)

	## Format figure
	p = figure(frame_width=800,		# graph size
				plot_height=500, 	# graph size
				title="Hover over a plot to see the SNP ID and chromosomal position",# Title added in html
				toolbar_location="right",
				tools="pan,hover,xwheel_zoom,zoom_out,box_zoom,reset,box_select,tap,undo,save",# Tool features added to make graph interactive
				tooltips="@SNPS: (@CHR_ID,@CHR_POS)"# Shows when mouse is hovered over plot
				)

	# Add circles to the figure to represent the SNPs in the GWAS data
	p.circle('cumulative_pos', '-logp',# Seperate by chromosome ID, and colour them
				source=df,# Source of data from the tsv file
				fill_alpha=0.6,# Thickness of plot border
				fill_color=index_cmap,# Colour of plot
				size=6,# Size of plot 
				selection_color="red" 
				)

	# Set the x and y axis labels for the plot
	p.xaxis.axis_label = 'Chromosome'# x-axis label 
	p.yaxis.axis_label = '-logp'# y-axis label

	# Set the tick locations and labels for the x axis using the cumulative length of the chromosomes 
	p.xaxis.ticker = [119895261, 373943002, 537393504, 716119012, 834845071, 964538826.5, 1147957441, 1306654016,
						1396415411, 1540730893, 1674222993, 1823778230, 1930583064, 2055942929, 2141945578, 2202426536,
						2302961360, 2388903150,
						2436333506.5, 2482024730, 2529377491, 2584586808]
	# major_label_overrides used to specify custom axis labels as the chromosome no.
	p.xaxis.major_label_overrides = {119895261: '1', 373943002: '2', 537393504: '3', 716119012: '4', 834845071: '5',
										964538826.5: '6', 1147957441: '7', 1306654016: '8',
										1396415411: '9', 1540730893: '10', 1674222993: '11', 1823778230: '12',
										1930583064: '13', 2055942929: '14', 2088496163: '14', 2141945578: '15',
										2202426536: '16', 2302961360: '17', 2388903150: '18', 2436333506.5: '19',
										2482024730: '20', 2529377491: '21', 2584586808: '22'}
	# change the font colour of the title 
	p.title.text_color = "teal"

	script, div = components(p)

	return render_template("Manplot.html", script=script, div=div,name=name)









# Start the web server
if __name__ == '__main__':
	app.run(debug=debug)