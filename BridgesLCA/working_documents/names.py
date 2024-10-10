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
g=Graph()
g.parse("/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/working_documents/Ontology/brcomp_ontology.ttl")

   
path= "/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/data/Bridges_JC.xlsx"

df=pd.read_excel(path,sheet_name="Feuil1")


for c in df.columns :        
    for (s,p,o) in g : 
        if o in c :
            print(s)
bridges_vocab = {c: 0 for c in df.columns[]}