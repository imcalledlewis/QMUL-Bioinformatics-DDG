def DBreq(request, request_type, manPlot=False):

    ###### Setting up database connection ######
    filepath=DBpath()                   # Sets database path
    assert os.path.exists(filepath),"Database file not found"
    conn = sqlite3.connect(filepath)    # Opens db file
    cur = conn.cursor()                 # Sets cursor

    ###### Getting rsids from request ######
    if request_type=="rsid":
        request=request.split(',') # Split request by comma separator

    elif request_type=="coords": # co-ordinate (6:1234-5678) search
        coord1,coord2=request.split('-') # Split request by hyphen separator
        chr,coord1=coord1.split(':') # Get chromosome by splitting by colon
        req=(chr,coord1,coord2)
        res = cur.execute("SELECT rsid FROM gwas WHERE chr_id LIKE ? AND chr_pos BETWEEN ? AND ?",req)
        ret=res.fetchall()
        request=[i[0] for i in ret] # SQL request returns list of singleton tuples, this line converts them to flat list

    elif request_type=='geneName': # Gene symbol (eg IRF4) search
        req=(request,) # Request must be in a tuple
        res = cur.execute("SELECT rsid FROM gwas WHERE mapped_gene LIKE ?",req)
        ret=res.fetchall()
        request=[i[0] for i in ret] # SQL request returns list of singleton tuples, this line converts them to flat list
        
    else:
        raise Exception("Unsupported type "+str(request_type))