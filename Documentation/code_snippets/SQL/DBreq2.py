    ###### Getting dictionary of results ######
    returnDict={}
    for rsid in request:
        innerDict={}
        req=(rsid,) # Request must be in a tuple

        ### Getting gwas data ###
        if manPlot: # If it's a manhattan plot
            res = cur.execute("SELECT i,chr_pos,chr_id,cumulative_pos,logp FROM gwas WHERE rsid LIKE ?",req)
        else:
            res = cur.execute("SELECT rsid,region,chr_pos,chr_id,p_value,mapped_gene FROM gwas WHERE rsid LIKE ?",req)
        ret=res.fetchone()
        assert ret, "error fetching rsid for "+(rsid)
        
        if not manPlot: # Manhattan plot doesn't need any of the following
            innerDict.update({"gwas":ret})
            ### Getting population data ###
            res=cur.execute("SELECT * FROM population WHERE rsid LIKE ?", req)
            ret=res.fetchone()
            if not ret:
                ret=[_unav for i in range(3)]   
            innerDict.update({"pop":list(ret)})
            innerDict['pop']=[round(i,3) for i in innerDict['pop'] if isinstance(i, float)] # remove allele strings, round to 3 dp

            ### Getting functional data ###
            res=cur.execute("SELECT * FROM functional WHERE rsid LIKE ?", req)
            ret=res.fetchone()
            if not ret:
                ret=(rsid,_unav,_unav,_unav)
            innerDict.update({"func":list(ret)})

            ### Getting ontology data ###
            res=cur.execute("SELECT go,term FROM ontology WHERE rsid LIKE ?", req)
            ret=res.fetchall()
            if not ret:
                ret=[(_unav, _unav)]
            innerDict.update({"ont":list(ret)})

        ### Adding results to inner dictionary ###
        if manPlot:
            returnDict.update({rsid:ret})
        else:
            returnDict.update({rsid:innerDict})

    return(returnDict,list(returnDict.keys()))