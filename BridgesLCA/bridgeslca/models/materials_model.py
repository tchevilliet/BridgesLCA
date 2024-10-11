# %% Import packages
import pandas as pd
import numpy as np
import os
from pathlib import Path

from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF, SKOS
from rdflib import Literal
#from names import bridges_vocab #import the dictionary with columns names and IRIs

# path_home = os.getcwd()

# path_repo = os.path.join(path_home, "Departier_repo")
# path_file = os.path.join(path_repo, "BridgesLCA/BridgesLCA/data/Bridges.xlsx")

# %% Define functions


# Define a function that creates the data for one structural component only
def one_structural_component(df: pd.DataFrame,
                             column: str,
                             vocab : dict,
                             user_length: float,
                             user_width: float,
                             user_type=None,) -> pd.DataFrame:
    # if user didn't put any type :
    if user_type is None:
        if user_length >= 400:
            user_type = "Special Prestressed Concrete"
        elif user_length >= 80 and user_length < 400:
            user_type = "Composite"
        elif user_length >= 10 and user_length < 80:
            user_type = "Prestressed Concrete"
        else:
            user_type = "Reinforced Concrete"

    if user_type == "Special Prestressed Concrete":
        df_per_type = df[
            (df["Type"] == "Cantilever Prestressed Concrete")
            | (df["Type"] == "Extradosed Prestressed Concrete")
        ]
    else:
        df_per_type = df[df["Type"] == user_type]  # filtered data with the right type

    ratio = np.mean(
        df_per_type[column] / (df_per_type["Length"] * df_per_type["Width"])
    )  # here we use a ratio, but could be a function

    # we build the result dataframe
    res = pd.DataFrame(
        index=[column], 
        columns=["material_IRI","component_IRI","unit", "amount", "phase"])
    res["material_IRI"] = vocab[column]['material']
    res["component_IRI"] = vocab[column]['component']
    res["unit"] = df[column].iloc[0]
    res["amount"] = ratio * user_length * user_width
    res["phase"] = "construction"
    return res


# Loop on all columns we want to analyze in the Excel file source
def all_structural_components(df: pd.DataFrame,
                              columns: list,
                              vocab : dict,
                              user_length: float,
                              user_width: float,
                              user_type=None) -> pd.DataFrame:
    for card, col in enumerate(columns):
        if card == 0:
            res = one_structural_component(df,
                                           col,
                                           vocab,
                                           user_length,
                                           user_width,
                                           user_type
                                           )
        else:
            res = pd.concat([res,one_structural_component(df,
                                                          col,
                                                          vocab,
                                                          user_length,
                                                          user_width
                                                          )
                             ])
    return res


# %% import data

path_home = os.getcwd()

path_repo = os.path.join(path_home, "Departier_repo")
path_file = os.path.join(path_repo, "BridgesLCA/BridgesLCA/data/Bridges.xlsx")

# my_data = pd.read_excel('/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/data/Bridges.xlsx')
my_data = pd.read_excel(path_file)


my_list = list(my_data.columns[9:])
# %% Calculation
# Need to define bridges_vocab before use
#a = all_structural_components(my_data,my_list,bridges_vocab, 500, 20)

# %%
