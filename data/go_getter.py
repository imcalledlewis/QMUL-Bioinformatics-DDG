import requests
from db_scripts import *
# clear()

# rsids = ['rs1538171', 'rs4320356', 'rs1770','rs2647044','rs11755527','rs9388489','rs9268645','rs9272346','rs3757247','rs924043','rs1050979','rs9405661','rs12665429','rs212408','rs72928038','rs2045258','rs9273363','rs1578060','rs138748427','rs9273367','rs17711850']

fileIn = getPath('gwas_trimmed.tsv')
fileOut = getPath('go_data_new_gene.tsv')

df = pd.read_csv(fileIn, sep="\t")

# Extract the list of rsids from the dataframe
# rsids = df["rsid"].tolist()
rsids = df["MAPPED_GENE"].tolist()


def get_gene_ontology(rsid):
    url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search"
    params = {
        "db": "rs",
        "dbReference": rsid,
        "taxonomy": "9606",
        # "limit":"1"
    }
    response = requests.get(url, params=params)
    assert response.status_code == 200, "unexpected response code"  # verify that response code is ok; throw error if not
    data = response.json()
    assert 'results' in data, "no results for "+rsid                # verify that results are found; throw error if not
    return data['results']

def get_go_term(GOid):
    url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{GOid}"
    response = requests.get(url)
    assert response.status_code == 200, "unexpected response code"  # verify that response code is ok; throw error if not
    data = response.json()
    assert 'results' in data, "no results for "+GOid                # verify that results are found; throw error if not
    return data['results'][0]                                       # return first row


with open(fileOut, 'w') as tsv:
    tsv.write("rsid\tqualifier\tterm\tgoID\n")
    l=len(rsids)
    print (l, "rsids")
    for i, rsid in enumerate(rsids):
        snpRes=get_gene_ontology(rsid)
        for row in snpRes:
            qualifier=row['qualifier']
            goID=row['goId']
            GOres=get_go_term(goID)  # Uses the results of the previous search to look at the go terms
            term=GOres['name']
            tsv.write(f"{rsid}\t{qualifier}\t{term}\t{goID}\n")
            # print(goID)
        prog=round((i/l)*100,1)
        if prog%10==0:
            print(round(prog),'%,',l-i,"left")
print("\ndone\n")