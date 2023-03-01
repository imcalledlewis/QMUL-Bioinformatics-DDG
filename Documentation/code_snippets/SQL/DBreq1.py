def DBreq(request, request_type, manPlot=False):

    ###### Setting up database connection ######
    filepath=DBpath()                   # Sets database path
    assert os.path.exists(filepath),"Database file not found"
    conn = sqlite3.connect(filepath)    # Opens db file
    cur = conn.cursor()                 # Sets cursor

    ###### Getting rsids from request ######
    if request_type=="rsid":
        request=request.split(',') # Split request by comma separator

    elif request_type=="coords": # co-ordinate (6:1234-6:5678) search
        if '-' not in request: # If there's only one coord,
            request=(request+"-"+request) # pretend it's a range and the start/ stop are the same.
        request=request.split('-') # Split request by hyphen separator
        assert len(request)==2, "Too many coordinate inputs"
        coords_chr=[i.split(':')[0] for i in request] # Gets the chromosome from each coord
        coords_loc=[i.split(':')[1] for i in request] # Gets the location from each coord
        assert len(coords_chr)==2, "Can't understand co-ord input"
        assert coords_chr[0]==coords_chr[1], "Unequal chromosome input"
        req=(coords_chr[0],coords_loc[0],coords_loc[1])
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