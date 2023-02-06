import requests
from db_scripts import *

#rsids = ['rs1538171', 'rs4320356', 'rs1770','rs2647044','rs11755527','rs9388489','rs9268645','rs9272346','rs3757247','rs924043','rs1050979','rs9405661','rs12665429','rs212408','rs72928038','rs2045258','rs9273363','rs1578060','rs138748427','rs9273367','rs17711850']

fileIn = getPath('gwas_trimmed.tsv')
fileOut = getPath('go_data_new.tsv')

def get_go_term(GOid):
    url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{GOid}"
    response = requests.get(url)
    assert response.status_code == 200, "unexpected response code"  # verify that response code is ok; throw error if not
    data = response.json()
    assert 'results' in data, "no results for "+GOid                # verify that results are found; throw error if not
    return data['results'][0]

results=get_go_term("GO:0030170")
print(results)