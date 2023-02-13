from db_scripts import *
import collections

# fileIn = getPath('filtered_go_data.tsv')

# df=pd.read_csv(fileIn,sep='\t')
# dupesDict={}
# for i, row in df.iterrows():
#     snp=row['rsid']
#     go=row['go_id']
#     if snp in dupesDict:                        # If it's seen the snp before,
#             dupesDict[snp].append(go)           # add the go term
#     else:                                       # If it hasn't seen the snp before,
#         dupesDict.update({snp:[go]})            # create a listing for it.

    
# dupeDF=pd.DataFrame(dupesDict).T
# dupes=dupeDF.duplicated(keep=False)
# dupeNum= dupes.tolist().count(True)
# colNum=len(dupes)
# print(colNum, "SNPs, of which", dupeNum, "are duplicates")
# print (":(" if colNum == dupeNum else ":)")



# def get_gene_ontology(rsid):
#     url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search"
#     params = {
#         "db": "rs",         # rsid
#         "dbReference": rsid,
#         "taxonomy": "9606", # homo sapiens
#         # "limit":"1"
#     }
#     response = requests.get(url, params=params)
#     assert response.status_code == 200, "unexpected response code"  # verify that response code is ok; throw error if not
#     data = response.json()
#     assert 'results' in data, "no results for "+rsid                # verify that results are found; throw error if not
#     return data['results']


import requests


fileIn = getPath('gwas_trimmed.tsv')
fileOut = getPath('gene_ont.tsv')
df=pd.read_csv(fileIn,sep='\t')
ids = df["MAPPED_GENE"].tolist()
l=len(ids)
geneDict={"gene":[],"goID":[],"annotation":[],"evidence":[]}

t=0             # total count
succ=0          # successes

for i,gene_id in enumerate(ids):
        t+=1
        url = f"https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId={gene_id}"
        response = requests.get(url)
        if response.status_code == 200:
                succ+=1
                data = response.json()
                for item in data["results"]:
                        geneDict["gene"].append(gene_id)
                        geneDict["goID"].append(item["goId"])
                        geneDict["annotation"].append(item["annotation"])
                        geneDict["evidence"].append(item["evidence"])

        prog=round((i/l)*100,1)
        if prog%10==0:  # print once every 10%
            print(round(prog),'%,',l-i,"left")

print(t, "genes,",succ,"successes")

if succ !=0:
        print(":)")
        df2=pd.DataFrame(geneDict)
        df2.to_csv(fileOut,sep='\t',index=False)

else:
        print(":(")