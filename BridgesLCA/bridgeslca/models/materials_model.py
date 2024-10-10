# %% Import packages
import pandas as pd
import numpy as np
import os
from pathlib import Path

from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF, SKOS
from rdflib import Literal


path_home = os.getcwd()

path_repo = os.path.join(path_home, "Departier_repo")
path_file = os.path.join(path_repo, "BridgesLCA/BridgesLCA/data/Bridges.xlsx")

# %% Define functions


# Define a function that creates the data for one structural component only
def one_structural_component(
    df: pd.DataFrame,
    columns: list,
    user_length: float,
    user_width: float,
    user_type=None,
) -> pd.DataFrame:
    # if user didn't put any type :
    if user_type is None:
        if user_length >= 80:
            user_type = "Composite"
        elif user_length < 10:
            user_type = "Reinforced Concrete"
        else:
            user_type = "Prestressed Concrete"

    df_per_type = df[df["Type"] == user_type]  # filtered data with the right type

    col_name_widht = [x for x in df_per_type.columns if "Width" in x]
    col_name_lenght = [x for x in df_per_type.columns if "Length" in x]
    ratio = np.mean(
        df_per_type[columns]
        / (df_per_type[col_name_lenght[0]] * df_per_type[col_name_widht[0]])
    )  # here we use a ratio, but could be a function

    # we build the result dataframe
    res = pd.DataFrame(index=[columns], columns=["IRI", "unit", "amount", "phase"])
    res["IRI"] = (
        "http://data.europa.eu/xsp/cn2024/382450100080"  # not a good IRI, just to try
    )
    res["unit"] = df[columns].iloc[0]
    res["amount"] = ratio * user_length * user_width
    res["phase"] = "construction"
    return res


# Loop on all columns we want to analyze in the Excel file source
def all_structural_components(
    df: pd.DataFrame,
    columns: list,
    user_length: float,
    user_width: float,
    user_type=None,
) -> pd.DataFrame:
    # res = pd.DataFrame(columns=["IRI", "unit", "amount", "phase"])
    for card, col in enumerate(columns):
        if card == 0:
            res = one_structural_component(
                df, col, user_length, user_width, user_type=None
            )
        else:
            res = pd.concat(
                [
                    res,
                    one_structural_component(
                        df, col, user_length, user_width, user_type=None
                    ),
                ]
            )
    return res


# %% import data

# my_data = pd.read_excel(
#    r"C:\Users\julien.cravero\source\repos\BridgesLCA\BridgesLCA\data\Bridges.xlsx"
# )
# my_data = pd.read_excel(path_file)


# my_list = list(my_data.columns[9:])
# %% Calculation
# a = all_structural_components(my_data, my_list, 100, 1)

# %%
