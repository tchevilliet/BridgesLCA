#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 10:58:53 2024

@author: thibault.chevilliet
"""

import pandas as pd

import bw2data as bd
import bw2io as bi
import bw2calc as bc
import bw2analyzer as bwa
#%%
proj_name = "2024-09-20_new"

# # Méthode en deux temps via fonction perso
# eidb_path = '/home/thibault.chevilliet@enpc.fr/Documents/Bases de données/Ecoinvent/ecoinvent 3.9.1_cutoff_ecoSpold02/datasets/'
# eidb_name = 'ei391_cutoff'
# perso.import_bdd(proj_name, eidb_path, eidb_name)

# Nouvelle méthode Chris Mutel avec import ecoinvent 
# ET biosphere directement adaptée (à privilégier)
bd.projects.set_current(proj_name)
version = '3.10' #version ecoinvent
model = 'cutoff' # modèle choisi (cut-off / apos / consequential / EN15804)
username = 'pontsparistech77'
mdp = 'pontsparistech77'
try :
    bi.import_ecoinvent_release(version,model,username,mdp)
except ValueError:
    print("This database already exists.")
    pass

# On met les bdd importée dans une variable pour faciliter leur utilisation
#ecoinvent
eidb_name = f"ecoinvent-{version}-{model}"
eidb = bd.Database(eidb_name)
#biosphere
biodb_name = f"ecoinvent-{version}-biosphere"
biodb = bd.Database(biodb_name)
#%%Choosing activities and method
act_concrete = eidb.search("concrete production, 35MPa, for civil engineering, for exterior use, with cement, Portland")[0]
act_steel = eidb.search("market for reinforcing steel")[0]

chosen_meth = [m for m in bd.methods if "climate change: fossil" in str(m)][3]
d_to_read = {"http://data.europa.eu/ehl/cpa21/235" : act_concrete,
             "http://data.europa.eu/ehl/cpa21/241" : act_steel}

#%%reading the output of our model and building FU

df_to_assess = pd.read_csv("/home/thibault.chevilliet@enpc.fr/Bureau/exported_results_df.csv")
df_to_assess = df_to_assess.set_index('Unnamed: 0')
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

