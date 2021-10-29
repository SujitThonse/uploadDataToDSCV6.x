import requests
import pprint
import json
from requests.models import InvalidURL
import tqdm

# Suppress ssl verification warning
requests.packages.urllib3.disable_warnings()

# URL of the provider connector
providerConnectorUrl = ""

s = requests.Session()

# Basic Credentials to access provider connector
# s.auth = ("admin", "EnrA69AdZTYb")
#s.auth = ("admin", "password")
s.auth = ("", "")
s.verify = False

# URL of the IDS Broker

# Resource catalog
resourceCatalog = {"title": "Broker test Catalog", "description": "list of equipment"}

# Metadata of a resource
resourceMetadata = {
  "title": "Example to test broker registration",
  "description": "resource details for testing",
  "keywords": [
    "demo",
    "test"
  ],
  "paymentMethod": "free",
  "publisher": "https://demoresource.sap.org/",
  "language": "EN",
  "license": "http://opendatacommons.org/licenses/odbl/1.0/",
  "sovereign": "https://demoresource.sap.org/",
  "ids:VIN":"EXA-2233"
}

# Representation of a resource
representationResource = {"title":"Data representation", "mediaType":"JSON", "language": "EN"}

# Artifact of a resource
artifactResource = {"title":"hellworld data", "accessUrl": "https://sandbox.api.service.nhs.uk/hello-world/hello/world"}

# Contract start and end dates
contractDuration = {
            "start": "2021-09-20T13:33:44.995+02:00",
            "end": "2021-12-20T13:33:44.995+02:00",
        }

# TERMS OF THE CONTRACT
contractRules = {
            "value": """{
        "@context" : {
            "ids" : "https://w3id.org/idsa/core/",
            "idsc" : "https://w3id.org/idsa/code/"
        },
        "@type": "ids:Permission",
        "@id": "https://w3id.org/idsa/autogen/permission/cf1cb758-b96d-4486-b0a7-f3ac0e289588",
        "ids:action": [
            {
            "@id": "idsc:USE"
            }
        ],
        "ids:description": [
            {
            "@value": "provide-access",
            "@type": "http://www.w3.org/2001/XMLSchema#string"
            }
        ],
        "ids:title": [
            {
            "@value": "Example Usage Policy",
            "@type": "http://www.w3.org/2001/XMLSchema#string"
            }
        ]
        }"""
        }

def create_catalog():
    response = s.post(providerConnectorUrl + "/api/catalogs", json=resourceCatalog)
    pprint.pprint("*********************RESOURCE Catalogue***********************************")
    pprint.pprint(resourceCatalog)
    pprint.pprint("********************************************************")
    return response.headers["Location"]

def create_offered_resource():
    response = s.post(providerConnectorUrl + "/api/offers", json=resourceMetadata)
    pprint.pprint("*********************RESOURCE DETAILS***********************************")
    pprint.pprint(resourceMetadata)
    resourceId = response.headers["Location"]
    pprint.pprint("***************************************RESOURCE ID: "+resourceId)
    print("\n")
    return resourceId


def create_representation():
    response = s.post(providerConnectorUrl + "/api/representations", json=representationResource)
    pprint.pprint("****************REPRESENTATION OF A RESOURCE***************************")
    pprint.pprint(representationResource)
    pprint.pprint("********************************************************")
    print("\n")
    return response.headers["Location"]


def create_artifact():
    response = s.post(providerConnectorUrl + "/api/artifacts", json=artifactResource)
    pprint.pprint("*********************ARTIFACT DETAILS***********************************")
    pprint.pprint(artifactResource)
    pprint.pprint("********************************************************")
    print("\n")
    return response.headers["Location"]


def create_contract():
    response = s.post(providerConnectorUrl + "/api/contracts", json=contractDuration)
    pprint.pprint("*********************CONTRACT DURATION***********************************")
    pprint.pprint(contractDuration)
    pprint.pprint("********************************************************")
    print("\n")
    return response.headers["Location"]


def create_rule_allow_access():
    response = s.post(providerConnectorUrl + "/api/rules", json=contractRules)
    pprint.pprint("*********************CONTRACT RULES***********************************")
    pprint.pprint(contractRules)
    pprint.pprint("********************************************************")
    print("\n")
    return response.headers["Location"]


def add_resource_to_catalog(catalog, resource):
    response = s.post(catalog + "/offers", json=[resource])


def add_catalog_to_resource(resource, catalog):
    response = s.post(resource + "/catalogs", json=[catalog])


def add_representation_to_resource(resource, representation):
    response = s.post(resource + "/representations", json=[representation])


def add_artifact_to_representation(representation, artifact):
    response = s.post(representation + "/artifacts", json=[artifact])


def add_contract_to_resource(resource, contract):
    response = s.post(resource + "/contracts", json=[contract])


def add_rule_to_contract(contract, rule):
    response = s.post(contract + "/rules", json=[rule])

# register connector
def registerConnectorAtBroker():
    url = providerConnectorUrl + "/api/ids/connector/update"
    params = {"recipient": brokerUrl}
    pprint.pprint("***********REGISTERING CONNECTOR AT BROKER**********************")
    print("\n")
    response = s.post(url, params=params)
    pprint.pprint(response)
    pprint.pprint(response.content)
    return response

# register connector's resource
def registerResourceAtBroker(resourceId):
    url = providerConnectorUrl + "/api/ids/resource/update"
    params = {"recipient": brokerUrl, "resourceId": resourceId}
    pprint.pprint("***********REGISTERING RESOURCE AT BROKER**********************")
    print("\n")
    response = s.post(url, params=params)
    pprint.pprint(response)
    pprint.pprint(response.content)
    return response

# get resource details
def getBaseResourceList(recipient):
    url = providerConnectorUrl + "/api/offers"
    params = {}
    if recipient is not None:
        params["recipient"] = recipient

    return s.get(url, params=params)

print("\n")
pprint.pprint("######## Creating IDS resources ########")
print("\n")

# Create resources
catalog = create_catalog()
offers = create_offered_resource()
representation = create_representation()
artifact = create_artifact()
contract = create_contract()
use_rule = create_rule_allow_access()

# Link resources
add_resource_to_catalog(catalog, offers)
add_representation_to_resource(offers, representation)
add_artifact_to_representation(representation, artifact)
add_contract_to_resource(offers, contract)
add_rule_to_contract(contract, use_rule)

# register connector at broker
#registerConnectorAtBroker()

#register resource at broker
#registerResourceAtBroker(offers)

# print resource list
response = getBaseResourceList(providerConnectorUrl + "/api/ids/data")
pprint.pprint("######## Successfully created IDS Resource ########")
print("\n")
