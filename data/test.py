### Sandbox for testing ideas and functions. Very much subject to change.


from db_scripts import *
import json

rsids = ['rs1538171', 'rs4320356', 'rs1770','rs2647044','rs11755527','rs9388489','rs9268645','rs9272346','rs3757247','rs924043','rs1050979','rs9405661','rs12665429','rs212408','rs72928038','rs2045258','rs9273363','rs1578060','rs138748427','rs9273367','rs17711850']

def get_gene_ontology(rsid):
    url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search"
    params = {
        "db": "rs",
        "dbReference": rsid,
        "taxonomy": "9606",
#         "includeFields": "go"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results']
        else:
            return []
    else:
        return []

go_data = []
for rsid in rsids:
    go_data.append(get_gene_ontology(rsid))
with open('go_data.tsv', 'w') as f:
    # write header row
    f.write('rsid\tgo_id\tgo_name\tgo_evidence\n')
    # loop through the data and write each row to the file
    for rsid, data in zip(rsids, go_data):
        for item in data:
            print('{}\t{}\t{}\t{}\n'.format(rsid, item['goId'], item['goName'], item['goEvidence']))