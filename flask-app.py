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
from data.db_scripts import themeDict
from data.LD_scripts import *	# LD data and heatmap

debug=True		# Change this to False for deployment
setDebug(debug)	# Set db_scripts debug flag to the same as this file

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
	if req_type!='geneName':
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
			FIN_D_data, FIN_r2_data, TSI_D_data, TSI_r2_data, GBR_D_data, GBR_r2_data = embed_LD_plots(SNP_list, title = SNP_req) # create LD heatmap dataframe using SNP list returned from query
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
		return Response(LD_data.to_csv(sep='\t', index=False),mimetype="text/csv", headers={"Content-disposition": "attachment; filename=LD_results.tsv"})
	



@app.route('/manPlot/<SNP_req>/', methods=['GET','POST'])
def Manhattan_plot(SNP_req):

	SNP_req = SNP_req.lower()		# Ensure snp name is in lowercase letters
	name=SNP_req
	if SNP_req=='all6': # all of chromosome 6
			reqRes,SNP_list=DBreq('6:0-9999999999999', 'coords',manPlot=True)	# Make SQL request
			name ='Chromosome 6'
	else:
		reqRes,SNP_list=DBreq(SNP_req, 'coords',manPlot=True)	# Make SQL request
		if reqRes:						# If the response isn't None
				name='{} SNPS'.format(len(SNP_list))
		else:
			return("manhattan plot parsing failed")                 			# If SNP is not found:

	df=pd.DataFrame(reqRes).T								# Convert sql request response to dataframe, then flip axes (ie vertical becomes horizontal and vice-versa)

	df.rename(columns={0:'index',1:'chr_pos', 2:"chr_id",3:"cumulative_pos", 4:"-logp"},inplace=True)	# rename each of the columns
	df['rsid'] = df.index
	df=df.astype({'chr_id':'int64', 'cumulative_pos':'int64','chr_pos':'int64','index':'int64'})			# cast some columns to int
	df.set_index('index',inplace=True)
	if debug:
		print(df)
		pass

	#### End of Gabriel's code ####

	# Separate by chromosome ID, and colour them
	index_cmap = linear_cmap('chr_id', palette = ['grey','black']*11,low=1,high=22)

	## Format figure
	p = figure(frame_width=800,		# graph size
				plot_height=500, 	# graph size
				title=f"SNPs in {SNP_req} for T1D",# Title added in html
				toolbar_location="right",
				tools="pan,hover,xwheel_zoom,zoom_out,box_zoom,reset,box_select,tap,undo,save",# Tool features added to make graph interactive
				tooltips="""
				<div class="manPlot-tooltip">
    				<span class=tooltip-rsid>@rsid </span>
    				<span class=tooltip-chrPos>@chr_id:@chr_pos</span>
				</div>				
				"""# Shows when mouse is hovered over plot
				)

	# Add circles to the figure to represent the SNPs in the GWAS data
	p.circle(x='cumulative_pos', y='-logp',# x and y-axis
            source=df,
            fill_alpha=0.8,# Transparency of plot
            fill_color=index_cmap,# Colour of plot
            size=7,# Size of plot 
            selection_color="rebeccapurple", # Colour of plot when selected
            hover_color="green"
            )

	# Set the x and y axis labels for the plot
	p.xaxis.axis_label = 'Chromosome'# x-axis label 
	p.yaxis.axis_label = '-logp'# y-axis label
	p.title.text_color = "teal" #colour of title

	# Set the tick locations and labels for the x axis using the cumulative length of the chromosomes 
	p.xaxis.ticker = [119895261, 373943002, 537393504, 716119012, 834845071, 964538826.5, 1147957441, 1306654016,
						1396415411, 1540730893, 1674222993, 1823778230, 1930583064, 2055942929, 2141945578, 2202426536,
						2302961360, 2388903150, 2436333506.5, 2482024730, 2529377491, 2584586808]
	# major_label_overrides used to specify custom axis labels as the chromosome no.
	p.xaxis.major_label_overrides = {119895261: '1', 373943002: '2', 537393504: '3', 716119012: '4', 834845071: '5',
										964538826.5: '6', 1147957441: '7', 1306654016: '8',
										1396415411: '9', 1540730893: '10', 1674222993: '11', 1823778230: '12',
										1930583064: '13', 2055942929: '14', 2141945578: '15',
										2202426536: '16', 2302961360: '17', 2388903150: '18', 2436333506.5: '19',
										2482024730: '20', 2529377491: '21', 2584586808: '22'}
	

	script, div = components(p)

	return render_template("Manplot.html", script=script, div=div,name=name)


@app.route('/themes')
def themePage():
	# Add a theme like so:
	addTheme(name="dark", text="white", contrast="black", mild= "#66a", med= "#559", strong= "#227")
	# mild: main content, least intense colour. strong: header, most intense colour.
	# contrast should always be the opposite of text.
	# I recommend using https://www.w3schools.com/colors/colors_picker.asp to choose colours

	# you can also create a theme like this:
	addTheme("light", "black", "white", "#7e7ece", "#8f8fef", "#a3a3ff")
	addTheme("sunset", "#fff","#000000","#aa8764", "#9b6655","#772222")
	addTheme("Ye Olde Theme", "saddlebrown","cornsilk","antiquewhite", "tan","darkgoldenrod")
	addTheme("Teal", "white", "black", "#3AAFA9", "#2B7A78","17252a")
	addTheme("Pinky", "white", "black", "#895061", "#78244c","59253a")

	

	return render_template("themes.html", themeDict=themeDict)

# Start the web server
if __name__ == '__main__':	
	app.run(debug=debug)