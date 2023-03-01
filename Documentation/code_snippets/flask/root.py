@app.route('/', methods=['GET','POST'])
def index():
	form = QueryForm() # Create form to pass to template
	SNP_req = None
	req_type = None
	if form.validate_on_submit():
		# Get request from text form
		SNP_req = form.SNP_req.data
		# Remove whitespace from request
		SNP_req = SNP_req.replace(' ', '')
		# Get request type from dropdown menu
		req_type = form.req_type.data 
		return redirect(url_for('SNP', SNP_req = SNP_req,req_type=req_type))
	return render_template('index_page.html', form=form, SNP_req=SNP_req, req_type=req_type,debug=debug)