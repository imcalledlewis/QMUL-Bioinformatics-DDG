# Testing ground for various ideas. Very much subject to change.

from db_scripts import *

fileIn = 'gwas_trimmed.tsv'
filepath = getPath(fileIn)
data = pd.read_csv(filepath, sep='\t')

dupeList = data.duplicated(subset='SNPS',keep=False)    # Get list of duplicate values
dupes=data[dupeList]                                    # Select dataframe using above list
# dupes=dupes.sort_values("SNPS")                  # Sort dataframe

dupesDict={}
for index,row in dupes.iterrows():              # Iterate through df of duplicates, one row at a time
    rsVal=row["SNPS"]                           # SNP name
    snpTuple=(index,row["P_VALUE"])             # Tuple containing index and p-val 
    if rsVal in dupesDict:                      # If it's seen the snp before,
        dictList=dupesDict[rsVal]               # go to the value for the snp,
        dictList.append(snpTuple)               # and add the index/ p-val tuple.
    else:                                       # If it hasn't seen the snp before,
        dupesDict.update({rsVal:[snpTuple]})    # create a listing for it.

naughtyList=[]  # List of index, p-vals we want to drop
for i in dupesDict:
    snp = dupesDict[i]  # get list of (index, pVal)
    sortByP=sorted(snp,key=lambda x: 0-x[1])    # Sort by p-value
    sortByP=sortByP[1:]                         # Select all but greatest p value
    naughtyList.append(sortByP)
    
# print(naughtyList)

dropList=[]     # List of indices for rows we want to drop
for i in naughtyList:
    for j in i:
        dropList.append(j[0])

# print(dropList)
# print(dupesDict)


print(data.drop(dropList))
# print (data)