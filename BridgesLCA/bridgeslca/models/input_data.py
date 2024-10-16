# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:00:04 2024

@author: StefanoMerciai
"""
import pandas as pd
import numpy as np
import os
from pathlib import Path

from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF, SKOS
from rdflib import Literal
from os.path import dirname

path_home = os.getcwd()

#path_repo = os.path.join(path_home, "Departier_repo") #Stefano's
path_repo = os.path.join(path_home, "Bureau/DDS Autumn School") #Thibault's
path_file = os.path.join(path_repo, "BridgesLCA/BridgesLCA/data/Bridges.xlsx")

assert os.path.exists(path_file)


df_bridge = pd.read_excel(path_file, sheet_name="bridges_data")
df_bridge_copy = df_bridge.copy()
df_bridge=df_bridge.set_index("Name")
#%%
new_col = []
for card, val in enumerate(df_bridge.iloc[0, :]):
    if not val == val:
        new_col.append(df_bridge.columns[card])
    else:

        new_col.append(df_bridge.columns[card] + "[" + val + "]")

# All in comments to avoid issues

# df_bridge_mod = pd.DataFrame(data=df_bridge_copy.iloc[1:, :].values, columns=new_col)
# df_bridge_mod = df_bridge_mod.set_index("Name")

# # create dictionary with URI as key and BOM as argument
# uri_bridge = "http://www.example.com/concepts#bridge"

# brdge_db_uri = Graph()  # ontoly
# bridge_db_dict = {}

# # rows (name of the bridges)
# for card, bridge in enumerate(df_bridge_mod.index):

#     clean_bridge_name = bridge.replace(" ", "_")
#     fake_uri = "http://www.example.com/concepts#" + clean_bridge_name

#     brdge_db_uri.add((URIRef(fake_uri), RDF.type, SKOS.Concept))  # Subject

#     brdge_db_uri.add(
#         (
#             URIRef(fake_uri),  # Subject
#             SKOS.prefLabel,
#             Literal(bridge, lang="fr"),
#         )
#     )

#     brdge_db_uri.add(
#         (
#             URIRef(fake_uri),  # Subject
#             SKOS.narrower,
#             URIRef(uri_bridge),
#         )
#     )

#     # create dictionary (our databse of existing bridges)
#     bridge_db_dict[fake_uri] = df_bridge_mod.iloc[card, :]

# for card, col_field in enumerate(df_bridge.columns):

#     clean_col_field = col_field.replace(" ", "_")
#     fake_uri = "http://www.example.com/concepts#" + clean_col_field

#     unit_flow = df_bridge.iloc[0, card]

#     brdge_db_uri.add((URIRef(fake_uri), RDF.type, SKOS.Concept))  # Subject

#     brdge_db_uri.add(
#         (
#             URIRef(fake_uri),  # Subject
#             SKOS.prefLabel,
#             Literal(col_field, lang="fr"),
#         )
#     )


# brdge_db_uri.serialize()
# dict_name_uri = {}  # dictionary with Name as key anr URI as argument
# for a, b, c in brdge_db_uri.triples((None, SKOS.prefLabel, None)):
#     dict_name_uri[str(c)] = str(a)


# # all the bridges
# path_file = os.path.join(path_repo, "BridgesLCA/BridgesLCA/data/bridgesdbUS.xlsx")

# df_bridge_US = pd.read_excel(path_file, sheet_name="Sheet1")

# df_bridge_US_select = df_bridge_US[
#     df_bridge_US["Kind of material and/or design 43A"] == "Prestressed Concrete"
# ]


# Data for toy-model

# dataframe
d = {
    "Cement": [10, 100, 200, 300],
    "Steel": [1, 10, 20, 30],
    "width": [11, 110, 220, 330],
    "length": [100, 300, 700, 1000],
}
# dataframe that includes the existing reported bridges
reported_technology = pd.DataFrame(
    data=d, index=["bridge_1", "bridge_2", "bridge_3", "bridge_4"]
)


# dataframe that includes the recipes of components of bridges
all_data = {
    "http://data.europa.eu/xsp/cn2024/foundation": pd.DataFrame(
        {"Cement": [100], "Steel": [10]}, index=["foundation"]
    ),
    "http://data.europa.eu/xsp/cn2024/piles": pd.DataFrame(
        {"Cement": [35], "Steel": [10]}, index=["piles"]
    ),
    "http://data.europa.eu/xsp/cn2024/cement": pd.DataFrame(
        {"limestone": [10], "water": [5]}
    ),
    "http://data.europa.eu/xsp/cn2024/steel": pd.DataFrame(
        {"iron ore": [1], "land": [4]}
    ),
}

list_uri = {
    "bridge_1": "http://data.europa.eu/xsp/cn2024/bridge_1",
    "bridge_2": "http://data.europa.eu/xsp/cn2024/bridge_2",
    "bridge_3": "http://data.europa.eu/xsp/cn2024/bridge_3",
    "bridge_4": "http://data.europa.eu/xsp/cn2024/bridge_4",
    "Cement": "http://data.europa.eu/xsp/cn2024/cement",
    "Steel": "http://data.europa.eu/xsp/cn2024/steel",
    "foundation": "http://data.europa.eu/xsp/cn2024/foundation",
    "piles": "http://data.europa.eu/xsp/cn2024/piles",
}
