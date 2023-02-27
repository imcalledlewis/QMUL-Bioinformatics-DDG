import pandas as pd
import os
import re
import sqlite3
import requests
import collections

_database = "snps.db"
_unav = "Data unavailable"
themeDict={}

def setDebug(debug):
    global db_debug
    db_debug=debug

def getPath(file,tsv=None): # Returns the absolute path to a file that is in same folder as script
    filenames=('tsv', 'csv', 'txt')
    ext=file.split('.')                                 # Gets extension of file
    ext=ext[-1].lower()
    path = os.path.dirname(os.path.abspath(__file__))   # Gets current path of file
    if (tsv==True) or (tsv==None and any([x == ext for x in filenames])):   # If it's a table storing file:
            filepath = os.path.join(path,"TSVs",file)                       # Sets path relative to current file, inside 'TSVs' folder
    else:
            filepath = os.path.join(path,file)                              # Sets path relative to current file
    return filepath

def DBpath():   # Returns the absolute path to the database
    return(getPath(_database))

def DBreq(request, request_type, manPlot=False):       # Makes SQL request

    ###### Setting up database connection ######
    filepath=DBpath()                   # Sets database path
    assert os.path.exists(filepath),"Database file not found"
    conn = sqlite3.connect(filepath)    # Opens db file
    cur = conn.cursor()                 # Sets cursor

    ###### Getting rsids from request ######
    if request_type=="rsid":
        request=request.split(',')		    # Split request by comma separator

    elif request_type=="coords":            # co-ordinate (6:1234-6:5678) search
        if '-' not in request:              # If there's only one coord,
            request=(request+"-"+request)   # pretend it's a range and the start/ stop are the same
        request=request.split('-')		    # Split request by hyphen separator
        assert len(request)==2, "Too many coordinate inputs"
        coords_chr=[i.split(':')[0] for i in request]   # Gets the chromosome from each coord
        coords_loc=[i.split(':')[1] for i in request]   # Gets the location from each coord
        assert len(coords_chr)==2, "Can't understand co-ord input"
        assert coords_chr[0]==coords_chr[1], "Unequal chromosome input"

        req=(coords_chr[0],coords_loc[0],coords_loc[1])
        res = cur.execute("SELECT rsid FROM gwas WHERE chr_id LIKE ? AND chr_pos BETWEEN ? AND ?",req)
        ret=res.fetchall()
        request=[i[0] for i in ret]         # SQL request returns list of singleton tuples, this line converts them to flat list

    elif request_type=='geneName':          # Gene symbol (eg IRF4) search
        req=(request,)                      # Request must be in a tuple
        res = cur.execute("SELECT rsid FROM gwas WHERE mapped_gene LIKE ?",req)
        ret=res.fetchall()
        request=[i[0] for i in ret]         # SQL request returns list of singleton tuples, this line converts them to flat list
        
    else:
        raise Exception("Unsupported type "+str(request_type))



    ###### Getting dictionary of results ######
    returnDict={}
    for rsid in request:
        innerDict={}
        req=(rsid,)                  # Request must be in a tuple

        ### Getting gwas data ###
        if manPlot:         # If it's a manhattan plot
            res = cur.execute("SELECT i,chr_pos,chr_id,cumulative_pos,logp FROM gwas WHERE rsid LIKE ?",req)
            # res = cur.execute("SELECT i FROM gwas WHERE rsid LIKE ?",req)
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
            innerDict['pop']=[round(i,3) for i in innerDict['pop'] if isinstance(i, float)]    # remove allele strings, round to 3 dp

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


    return(returnDict,list(returnDict.keys()))  # snp_list is keys
    # return(returnDict,request)        # Nasim's code - revert if my change breaks his stuff

def removeDupeSNP(dataframe):                                   # Removes duplicates from a pandas dataframe, leaving only greatest p-value
    dataframe.reset_index(drop=True)                            # Resets index back to 0
    dupeList = dataframe.duplicated(subset='snps',keep=False)   # Get list of duplicate values
    dupes=dataframe[dupeList]                                   # Select dataframe using above list

    dupesDict={}
    for index,row in dupes.iterrows():              # Iterate through df of duplicates, one row at a time
        rsVal=row["snps"]                           # SNP name (rs value)
        snpTuple=(index,row["p_value"])             # Tuple containing index and p-val 
        if rsVal in dupesDict:                      # If it's seen the snp before,
            dictList=dupesDict[rsVal]               # go to the value for the snp,
            dictList.append(snpTuple)               # and add the index/ p-val tuple.
        else:                                       # If it hasn't seen the snp before,
            dupesDict.update({rsVal:[snpTuple]})    # create a listing for it.

    naughtyList=[]                                  # List of lists of (index, p-val) we want to drop
    for i in dupesDict:
        snp = dupesDict[i]                          # Get list of (index, pVal)
        sortByP=sorted(snp,key=lambda x: 0-x[1])    # Sort by p-value
        sortByP=sortByP[1:]                         # Select all but greatest p value
        naughtyList.append(sortByP)

    dropList=[]                         # List of indices for rows we want to drop
    for i in naughtyList:               # Enter first list
        for j in i:                     # Enter second list
            dropList.append(j[0])       # Add the index from each tuple

    return(dataframe.drop(dropList))    # Return dataframe without duplicate values

def removeDupeGeneMap(GeneMap):
    try:
        GeneMap=GeneMap.split(', ')
        uniques=""
        for item in GeneMap:
            if item not in uniques: # If the item hasn't been seen before, 
                uniques+=(item)     # add it to the list.
                uniques+=(", ")     # Also add ' ,'
        return (uniques[:-2])       # Remove last ' ,'
    except:
        return (_unav)     # Return this if geneMap is empty


def removeSpecial(dataframe):     # Replaces special characters and whitespace with underscores
    renameDict={}
    for col in dataframe.columns:
        newCol = re.sub(r'\W+', '_', col)
        newCol = newCol.strip('_')      # Remove leading and trailing underscores
        newCol = newCol.lower()         # Makes lowercase
        renameDict.update({col:newCol}) # Renames columns
    return(dataframe.rename(columns=renameDict))

def pdDB(tsv_path,table_name,dtype):    # Adds tsv to SQL database
    conn = sqlite3.connect(DBpath())    # Opens (or creates) a db file
    cur = conn.cursor()                 # Sets cursor

    df = pd.read_csv(tsv_path, sep='\t')
    df.to_sql(name=table_name, con=conn, index=False, dtype=dtype)

    # res = cur.execute("SELECT * FROM SNP")
    # assert res.fetchone(), "error in database creation"

def castRS(dataframe,rsCol):   # Receives a dataframe, returns df with "rs" removed from rs value
    raise Exception("castRS is deprecated")   # this function isn't being used any more

def clear():    # Clears screen, platform independent
    os.system('cls' if os.name=='nt' else 'clear') 


def addTheme(name, textColour="white", contrast_bg="black", mild_bg= "#66a", med_bg= "#559", strong_bg= "#227"):
    l=[textColour, contrast_bg, mild_bg, med_bg, strong_bg]
    themeDict.update({name:l})