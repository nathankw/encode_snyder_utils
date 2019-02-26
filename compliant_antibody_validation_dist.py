import encode_utils.connection as euc
conn = euc.Connection("prod")

dico = {}
# All released antibodies from Snyder's team that are 'characterized to standards', 'partially characterized',
# or 'characterized to standards with exemption' in human datasets. 
url = "https://www.encodeproject.org/search/?type=AntibodyLot&status=released&lot_reviews.status=characterized+to+standards&targets.organism.scientific_name=Homo+sapiens&characterizations.lab.title=Michael+Snyder%2C+Stanford&lot_reviews.status=partially+characterized&lot_reviews.status=characterized+to+standards+with+exemption"

# An AntibodyLot has many Characterizations - one for each target (gene). 
# A Characterization has many characterization_reviews, one for each cell line, primary cell, tissue, etc.
results= conn.search(url=url)
for i in results:
    ab = conn.get(i["@id"])
    chars = ab["characterizations"]
    for char in chars:
        target = char["target"]["label"]
        try:
            reviews = char["characterization_reviews"]
        except KeyError:
            continue
        for r in reviews:
            lane_status = r["lane_status"]
            if not lane_status == "compliant":
                continue
            btn = r["biosample_ontology"]["term_name"]
            if btn not in dico:
                dico[btn] = {}
            dico[btn][target] = 1
