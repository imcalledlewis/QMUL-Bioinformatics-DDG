from db_scripts import *
import collections

fileIn = getPath('filtered_go_data.tsv')

df=pd.read_csv(fileIn,sep='\t')
dupesDict={}
for i, row in df.iterrows():
    snp=row['rsid']
    go=row['go_id']
    if snp in dupesDict:                        # If it's seen the snp before,
            dupesDict[snp].append(go)           # add the go term
    else:                                       # If it hasn't seen the snp before,
        dupesDict.update({snp:[go]})            # create a listing for it.

    
dupeDF=pd.DataFrame(dupesDict).T
dupes=dupeDF.duplicated(keep=False)
dupeNum= dupes.tolist().count(True)
colNum=len(dupes)
print(colNum, "SNPs, of which", dupeNum, "are duplicates")
print (":(" if colNum == dupeNum else ":)")