# import requests
# from db_scripts import *
# clear()

# rsids = ['rs1538171', 'rs4320356', 'rs1770','rs2647044','rs11755527','rs9388489','rs9268645','rs9272346','rs3757247','rs924043','rs1050979','rs9405661','rs12665429','rs212408','rs72928038','rs2045258','rs9273363','rs1578060','rs138748427','rs9273367','rs17711850']

# fileIn = getPath('gwas_trimmed.tsv')
# fileOut = getPath('go_data_new.tsv')

# def get_gene_ontology(rsid):
#     url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search"
#     params = {
#         "db": "rs",
#         "dbReference": rsid,
#         "taxonomy": "9606",
#         # "limit":"1"
#     }
#     response = requests.get(url, params=params)
#     assert response.status_code == 200, "unexpected response code"  # verify that response code is ok; throw error if not
#     data = response.json()
#     assert 'results' in data, "no results for "+rsid                # verify that results are found; throw error if not
#     return data['results']

# def get_go_term(GOid):
#     url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{GOid}"
#     response = requests.get(url)
#     assert response.status_code == 200, "unexpected response code"  # verify that response code is ok; throw error if not
#     data = response.json()
#     assert 'results' in data, "no results for "+GOid                # verify that results are found; throw error if not
#     return data['results'][0]                                       # return first row


# dupesDict={}
# for rsid in rsids:
#     l=[]        # reset list each time
#     snpRes=get_gene_ontology(rsid)
#     for row in snpRes:
#         goID=row['goId']
#         l.append(goID)

#     dupesDict.update({rsid:l})

# df=pd.DataFrame(dupesDict).T
# dupes=df.duplicated(keep=False)
# dupeNum= dupes.tolist().count(True)
# print(len(dupes), "columns, of which", dupeNum, "are duplicates")
# print (":(" if len(dupes) == dupeNum else ":)")


from db_scripts import *
# clear()

fileIn = getPath('go_data_new.tsv')

df=pd.read_csv(fileIn,sep='\t')
dupesDict={}
for i, row in df.iterrows():
    snp=row['rsid']
    go=row['goID']
    if snp in dupesDict:                        # If it's seen the snp before,
            dupesDict[snp].append(go)           # add the go term
    else:                                       # If it hasn't seen the snp before,
        dupesDict.update({snp:[go]})            # create a listing for it.

    
dupeDF=pd.DataFrame(dupesDict).T
print(dupeDF,'\n')
dupes=dupeDF.duplicated(keep=False)
dupeNum= dupes.tolist().count(True)
print(len(dupes), "SNPs, of which", dupeNum, "are duplicates")
print (":(" if len(dupes) == dupeNum else ":)")