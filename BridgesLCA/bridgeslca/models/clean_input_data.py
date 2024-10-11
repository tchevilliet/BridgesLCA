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

path_vocab = os.path.join(path_repo, "BridgesLCA/BridgesLCA/working_documents/names.py")
assert os.path.exists(path_file)

df_bridge = pd.read_excel(path_file, sheet_name="bridges_data")


# ##################### Data for toy-model
# # dataframe
# d = {
#     "Cement": [10, 100, 200, 300],
#     "Steel": [1, 10, 20, 30],
#     "width": [11, 110, 220, 330],
#     "length": [100, 300, 700, 1000],
# }
# # dataframe that includes the existing reported bridges
# reported_technology = pd.DataFrame(
#     data=d, index=["bridge_1", "bridge_2", "bridge_3", "bridge_4"]
# )