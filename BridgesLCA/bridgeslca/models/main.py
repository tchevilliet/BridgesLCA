#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:59:20 2024

@author: thibault.chevilliet
"""
#%% Import nice packages
import pandas as pd
import os
from datetime import date
from pydantic import BaseModel
from typing import Optional, NamedTuple

import bw2data as bd
import bw2io as bi
import bw2calc as bc
import bw2analyzer as bwa

#%% Import our modules
import bridgeslca.models.materials_model as mat
import bridgeslca.models.clean_input_data as data
import bridgeslca.models.clean_bridge_model as cbm
import bridgeslca.models.to_lci as to_lci
from bridgeslca.models.names import bridges_vocab

# %% RUN the model
D = cbm.Demand(
    product_iri=cbm.IRI(ref="http://data.europa.eu/xsp/cn2024/911440000080"),
    properties=None,
    amount=2.0,
    temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
    width=6,
    length=100,
#   bridges_type = 'Prestressed Concrete',
    tolerance=0,
)
m = cbm.BridgeModel(demand=D, run_config=cbm.RunConfig())
m.get_model_data(data.df_bridge)
result = m.run(bridges_vocab)

#%% LCA Calculation
act_concrete = to_lci.eidb.search("concrete production, 35MPa, for civil engineering, for exterior use, with cement, Portland")[0]
act_steel = to_lci.eidb.search("market for reinforcing steel")[0]

chosen_meth = [m for m in bd.methods if "climate change: fossil" in str(m)][3]
d_to_read = {"http://data.europa.eu/ehl/cpa21/23611" : act_concrete,
              "http://data.europa.eu/ehl/cpa21/24312" : act_steel}

#%%reading the output of our model and building FU

df_to_assess = result

FU ={v : 0 for v in d_to_read.values()}
for row in df_to_assess.index :
    FU[d_to_read[df_to_assess.at[row,'material_IRI']]] += df_to_assess.at[row,'amount']
#%% Perform LCA
my_functional_unit, data_objs, _ = bd.prepare_lca_inputs(FU, method=chosen_meth)
my_lca = bc.LCA(demand=my_functional_unit, data_objs=data_objs)
my_lca.lci()
my_lca.lcia()
my_lca.score

df_inventory = my_lca.to_dataframe(matrix_label="inventory")
df_characterized_inventory = my_lca.to_dataframe(matrix_label="characterized_inventory")
