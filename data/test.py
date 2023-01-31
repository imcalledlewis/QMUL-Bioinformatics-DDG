import requests
from db_scripts import *

def get_go_terms(rsid):
    query_url = f"https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect=biological_process&geneProductId={rsid}"
    response = requests.get(query_url)
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    if response.status_code == 200:
        results = response.json()["results"]
        go_terms = [result["goName"] for result in results]
        return go_terms
    else:
        return []

rsids = ["rs1538171", "rs4320356", "rs1770","rs2647044","rs11755527","rs9388489","rs9268645","rs9272346","rs3757247","rs924043","rs1050979","rs9405661","rs12665429","rs212408","rs72928038","rs2045258","rs9273363","rs1578060","rs138748427","rs9273367","rs17711850"]
# all_go_terms = []
# for rsid in rsids:
#     go_terms = get_go_terms(rsid)
#     print(go_terms)
#     break
    # all_go_terms.append(go_terms)

# print(all_go_terms)


print(get_go_terms("rs1538171"))



requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?limit=1"

r = requests.get(requestURL, headers={ "Accept" : "application/json"})

responseBody = r.text
print(responseBody)