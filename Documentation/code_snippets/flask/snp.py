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