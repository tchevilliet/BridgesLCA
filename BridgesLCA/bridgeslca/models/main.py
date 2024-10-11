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
import seaborn as sns

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
    tolerance=0
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


#%% get results and plot for several demand

l_length = range(5,500,10)

demands= [cbm.Demand(product_iri=cbm.IRI(ref="http://data.europa.eu/xsp/cn2024/911440000080"),
                     properties=None,
                     amount=2.0,
                     temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
                     width=6,
                     length=l,
                     #   bridges_type = 'Prestressed Concrete',
                     tolerance=0) for l in l_length]

models = [cbm.BridgeModel(d, run_config=cbm.RunConfig()) for d in demands]
for m in models :
    m.get_model_data(data.df_bridge)
results = [m.run(bridges_vocab) for m in models]

# q_concrete = [r[r['material_IRI']=='http://data.europa.eu/ehl/cpa21/23611']['amount'].sum() for r in results]
# g= sns.scatterplot(x=l_length,y=q_concrete)
# g.figure.savefig("/home/thibault.chevilliet@enpc.fr/Bureau/conc_vs_length.pdf")
# g.figure.clf()

FUs = []
for r in results :
    tmp ={v : 0 for v in d_to_read.values()}
    for row in r.index :
        tmp[d_to_read[r.at[row,'material_IRI']]] += r.at[row,'amount']
    FUs.append(tmp)

scores = []
for fu in FUs :
    my_functional_unit, data_objs, _ = bd.prepare_lca_inputs(fu, method=chosen_meth)
    my_lca = bc.LCA(demand=my_functional_unit, data_objs=data_objs)
    my_lca.lci()
    my_lca.lcia()
    scores.append(my_lca.score)
    
g= sns.scatterplot(x=l_length,y=scores)
g.figure.savefig("/home/thibault.chevilliet@enpc.fr/Bureau/lca_score_vs_length.pdf")
g.figure.clf()


# l_scores = []


# #Export csv for Stefano
# l_brid = [int((5-5)/10),int((25-5)/10),int((55-5)/10),int((105-5)/10),int((205-5)/10),int((425-5)/10)]
# for l in l_brid :
#     results[l].to_csv(f"/home/thibault.chevilliet@enpc.fr/Bureau/For Stefano/bridge{l*10+5}.csv")

