import requests
import xml.etree.ElementTree as ET
import flask
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

#Goals: Identify active ingredient, identify other drugs with same active ingredient, 
#what does this drug do exactly?

app = flask.Flask(__name__)

@app.route('/')
def main_page():
    return flask.render_template('index.html')
    
@app.route('/drug', methods=['GET'])
def results_page():
    drug_name = flask.request.args.get('medlinesearch','blank',type=str)
    blang = medline_bling(drug_name)
    return flask.jsonify({"drug":str.lower(drug_name), "definition":blang[0], "others":blang[1]})

def medline_bling(drug_name):
    #Call the ND-FRT API find the active ingredient in the drug get their concept_nui id.
    url = "https://rxnav.nlm.nih.gov/REST/Ndfrt/search.json?"
    params = {"conceptName":drug_name, "kindName":"INGREDIENT_KIND"}
    r = requests.get(url, params=params)
    try:
        concept_nui = r.json()["groupConcepts"][0]["concept"][0]["conceptNui"]
    except (TypeError, KeyError):
        return "Error: Drug Not Found", ["Error: Drug Not Found", "Error: Drug Not Found"]

    #Call the ND-FRT API find out what this active ingredient/drug does (generally).
    url2 = "https://rxnav.nlm.nih.gov/REST/Ndfrt/properties.json?"
    params2 = {"nui":concept_nui, "propertyName":"MeSH_Definition"}
    r = requests.get(url2, params=params2)
    try:
        definition = r.json()["groupProperties"][0]["property"][0]["propertyValue"]
    except (TypeError, KeyError):
        return "Error: Drug Not Found", ["Error: Drug Not Found", "Error: Drug Not Found"]

    #Call the RxNorms API. Convert the nui id into an rxNormId.
    url3 = "https://rxnav.nlm.nih.gov/REST/rxcui.json?"
    params3 = {"idtype":"NUI", "id":concept_nui}
    r = requests.get(url3, params=params3)
    try:
        rxNormId = r.json()["idGroup"]["rxnormId"]
    except (TypeError, KeyError):
        return "Error: Drug Not Found", ["Error: Drug Not Found", "Error: Drug Not Found"]

    #Call the RxNorm API. Use the rxNormId to find other drugs with the same ingredient.
    url4 = "https://rxnav.nlm.nih.gov/REST/brands.json?"
    params4 = {"ingredientids":rxNormId}
    r = requests.get(url4, params=params4)
    try:
        other_drugs = [drug["name"] for drug in r.json()["brandGroup"]["conceptProperties"]]
    except (TypeError, KeyError):
        return "Error: Drug Not Found", ["Error: Drug Not Found", "Error: Drug Not Found"]

    return definition, other_drugs


if __name__ == '__main__':
    app.debug = True
    app.run()
