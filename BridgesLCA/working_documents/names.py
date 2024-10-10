#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 11:10:34 2024

@author: thibault.chevilliet
"""

from rdflib import Graph
from io import StringIO
from rdflib import URIRef
from rdflib.namespace import RDF, SKOS
from rdflib import Literal
from rdflib.namespace import XSD
import sentier_data_tools as sdt
import pandas as pd
import seaborn as sns


#%%
g_components=Graph()
g_components.parse("/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/working_documents/Ontology/brcomp_ontology.ttl")
g_materials=Graph()
g_materials.parse("/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/working_documents/Ontology/brmat_ontology.ttl")

   
path= "/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/data/Bridges.xlsx"

df=pd.read_excel(path,sheet_name="bridges_data")
#%%

for c in df.columns:
    for (s,p,o) in g_materials : 
        if s[22:] in str(c) and len(s)!=21  :
            print((s,c))

#%%
bridges_vocab = {c : {'material' : '', 'component' :''} for c in df.columns[9:]}

#Method 1: link to bridge ontology from TU Dresden separating material and component
for c in df.columns:
    for (s,p,o) in g_components : 
        if s[24:] in str(c) and len(s)!=23  :
            bridges_vocab[c]['component'] = str(s)
            
for c in df.columns:
    for (s,p,o) in g_materials : 
        if s[23:] in str(c) and len(s)!=21  :
            bridges_vocab[c]['material'] = str(s)

bridges_vocab['Blinding Concrete C20']['component'] = 'https://w3id.org/brcomp#Footing'
bridges_vocab['Concrete for Deck C45']['component'] = 'https://w3id.org/brcomp#GirderDeck'
bridges_vocab['Reinforcing Steel']['material'] = 'https://w3id.org/bmat#ReinforecementSteel'
bridges_vocab['Reinforcing Steel']['component'] = 'https://w3id.org/brot#Component'
bridges_vocab['Structural Steel for Deck']['component'] = 'https://w3id.org/brcomp#GirderDeck'
bridges_vocab['Structural Steel for Deck']['material'] = 'https://w3id.org/bmat#BuildingMaterial'
bridges_vocab['Structural Steel for Piles']['material'] = 'https://w3id.org/bmat#BuildingMaterial'
bridges_vocab['Structural Steel for Railings']['material'] = 'https://w3id.org/bmat#BuildingMaterial'

#Method 2: change material URI to link material to EU vocab
for c in df.columns :
    if "concrete" in c.lower() :
        bridges_vocab[c]['material'] =  "http://data.europa.eu/cpv/cpv/44114000"
    if "steel" in c.lower() :
        bridges_vocab[c]['material'] = " http://data.europa.eu/cpv/cpv/14622000"

#Method 3: link material to CPA 2.1 in EU vocab --> concrete products for construction and steel products
for c in df.columns :
    if "concrete" in c.lower() :
        bridges_vocab[c]['material'] =   "http://data.europa.eu/ehl/cpa21/23611"
    if "steel" in c.lower() :
        bridges_vocab[c]['material'] =  "http://data.europa.eu/ehl/cpa21/24312"

# #Method 4: link material to CPA 2.1 in EU vocab --> cement and steel to compare with I/O results
# for c in df.columns :
#     if "concrete" in c.lower() :
#         bridges_vocab[c]['material'] = "http://data.europa.eu/ehl/cpa21/235"  
#     if "steel" in c.lower() :
#         bridges_vocab[c]['material'] = "http://data.europa.eu/ehl/cpa21/241" 

#Translate in raw products to get a footprint 
"cement" = "http://data.europa.eu/ehl/cpa21/235" 
"steel" = "http://data.europa.eu/ehl/cpa21/241" 
"stone" = "http://data.europa.eu/ehl/cpa21/081"

 


