# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:03:17 2024

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

path_repo = os.path.join(path_home, "Departier_repo")
path_folder = os.path.join(path_repo, "BridgesLCA/BridgesLCA/vocab")
os.path.exists(path_folder)
path_file = os.path.join(path_folder, "bonsai.ttl")

# bonsai_db_uri = Graph().parse(path_file)


# bonsai does not have URI yet (here it is just invented)
bonsai_db_uri = Graph()  # dictionary

# cement
cement_uri = URIRef("https://lca.aau.dk/FootprintAnalyser/M_CMNT")

bonsai_db_uri.add(
    (
        cement_uri,  # Subject
        RDF.type,
        SKOS.Concept,
    )
)
bonsai_db_uri.add(
    (
        cement_uri,  # Subject
        SKOS.closeMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/235"),
    )
)
(
    (
        cement_uri,  # Subject
        SKOS.narrower,
        URIRef("http://data.europa.eu/ehl/cpa21/236"),
    )
)
bonsai_db_uri.add(
    (
        cement_uri,  # Subject
        SKOS.definition,
        Literal("Production of cement, lime and plaster, market of", lang="en"),
    )
)
bonsai_db_uri.add((cement_uri, SKOS.notation, Literal("M_CMNT", lang="en")))


# steel
steel_uri = URIRef("https://lca.aau.dk/FootprintAnalyser/M_STEL")

bonsai_db_uri.add(
    (
        steel_uri,  # Subject
        RDF.type,
        SKOS.Concept,
    )
)
bonsai_db_uri.add(
    (
        steel_uri,  # Subject
        SKOS.closeMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/24"),
    )
)
bonsai_db_uri.add(
    (
        steel_uri,  # Subject
        SKOS.narrower,
        URIRef("http://data.europa.eu/ehl/cpa21/241"),
    )
)
bonsai_db_uri.add(
    (
        steel_uri,  # Subject
        SKOS.definition,
        Literal(
            "Production of basic iron and steel and of ferro-alloys and first products thereof, market of",
            lang="en",
        ),
    )
)

bonsai_db_uri.add((steel_uri, SKOS.notation, Literal("M_STEL", lang="en")))

# sand and steel
sand_uri = URIRef("https://lca.aau.dk/FootprintAnalyser/M_SDCL")

bonsai_db_uri.add(
    (
        sand_uri,  # Subject
        RDF.type,
        SKOS.Concept,
    )
)
bonsai_db_uri.add(
    (
        sand_uri,  # Subject
        SKOS.closeMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/0812"),
    )
)
bonsai_db_uri.add(
    (
        sand_uri,  # Subject
        SKOS.definition,
        Literal(
            "Sand and clay, market of",
            lang="en",
        ),
    )
)

bonsai_db_uri.add((sand_uri, SKOS.notation, Literal("M_SDCL", lang="en")))

# bitumen
bitumen_uri = URIRef("https://lca.aau.dk/FootprintAnalyser/M_BITU")

bonsai_db_uri.add(
    (
        bitumen_uri,  # Subject
        RDF.type,
        SKOS.Concept,
    )
)
bonsai_db_uri.add(
    (
        bitumen_uri,  # Subject
        SKOS.relatedMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/192042"),
    )
)
bonsai_db_uri.add(
    (
        bitumen_uri,  # Subject
        SKOS.definition,
        Literal(
            "Bitumen, market of",
            lang="en",
        ),
    )
)

bonsai_db_uri.add((bitumen_uri, SKOS.notation, Literal("M_BITU", lang="en")))

# stone
stone_uri = URIRef("https://lca.aau.dk/FootprintAnalyser/M_STON")

bonsai_db_uri.add(
    (
        stone_uri,  # Subject
        RDF.type,
        SKOS.Concept,
    )
)
bonsai_db_uri.add(
    (
        stone_uri,  # Subject
        SKOS.closeMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/0811"),
    )
)
bonsai_db_uri.add(
    (
        stone_uri,  # Subject
        SKOS.definition,
        Literal(
            "Stone, market of",
            lang="en",
        ),
    )
)
bonsai_db_uri.add((stone_uri, SKOS.notation, Literal("M_STON", lang="en")))

# export vocabulary
bonsai_db_uri.serialize(destination=path_file)
bonsai_db_uri.serialize()

# ------------------------import Bonsai

path_home = Path.home()


path_file = Path(
    path_home / "Departier_repo" / "BridgesLCA/BridgesLCA/data/ghg_for_all.csv"
)
assert os.path.exists(path_file)

bonsai_footprints = pd.read_csv(path_file, header=[0])


# product needed
input_with_footptint = []
for uri, x, bonsai_code in bonsai_db_uri.triples((None, SKOS.notation, None)):
    input_with_footptint.append(str(bonsai_code))


footprint = bonsai_footprints[
    bonsai_footprints["Exio prod code"].isin(input_with_footptint)
]

# --------------- import output data of the model
path_home = Path.home()
path_file = Path(
    path_home / "Departier_repo" / "BridgesLCA/BridgesLCA/data/exported_results_df.csv"
)
assert os.path.exists(path_file)

output_model = pd.read_csv(path_file, header=[0])

# create diction with CPA iri as keys, and bonsai code as argument
map_iri = {}
for bonsai_uri, x, cpa_code in bonsai_db_uri.triples((None, SKOS.closeMatch, None)):
    for bonsai_code, x, bonsai_code in bonsai_db_uri.triples(
        (bonsai_uri, SKOS.notation, None)
    ):

        map_iri[str(cpa_code)] = str(bonsai_code)

for bonsai_uri, x, cpa_code in bonsai_db_uri.triples((None, SKOS.relatedMatch, None)):
    for bonsai_code, x, bonsai_code in bonsai_db_uri.triples(
        (bonsai_uri, SKOS.notation, None)
    ):
        map_iri[str(cpa_code)] = str(bonsai_code)

for bonsai_uri, x, cpa_code in bonsai_db_uri.triples((None, SKOS.narrower, None)):
    for bonsai_code, x, bonsai_code in bonsai_db_uri.triples(
        (bonsai_uri, SKOS.notation, None)
    ):
        map_iri[str(cpa_code)] = str(bonsai_code)

        map_iri["http://data.europa.eu/ehl/cpa21/236"] = "M_CMNT"
        map_iri["http://data.europa.eu/ehl/cpa21/081"] = "M_SDCL"

    input_with_footptint.append(str(bonsai_code))
# create the mapping
final_mapping = {}
for material in output_model["material_IRI"]:
    if material in map_iri.keys():
        final_mapping[material] = map_iri[material]
    else:
        final_mapping[material] = "bad mattch"
    print(material)

# merge
output_model["Exio prod code"] = output_model["material_IRI"].map(final_mapping)
# ------------roug calculation
final_output = pd.merge(output_model, footprint, on=["Exio prod code"], how="left")
for col in final_output.columns[-49:]:
    final_output[col] = final_output[col] * final_output["amount"]


# ------------------------------------------- insert concrete
concrete_conv = pd.read_excel(
    path_home / "Downloads" / "Concrete.xlsx", sheet_name="conversion"
)

output_model_concrete = pd.merge(
    output_model, concrete_conv, on=["material_IRI"], how="left"
)

output_model_concrete.loc[~output_model_concrete["input"].isna(), "amount"] = (
    output_model_concrete.loc[~output_model_concrete["input"].isna(), "amount"]
    * output_model_concrete.loc[~output_model_concrete["input"].isna(), "amout_input"]
)
# assign iri
output_model_concrete.loc[~output_model_concrete["input"].isna(), "material_IRI"] = (
    output_model_concrete.loc[~output_model_concrete["input"].isna(), "input_iri"]
)


# create the mapping
final_mapping = {}
for material in output_model_concrete["material_IRI"]:
    if material in map_iri.keys():
        final_mapping[material] = map_iri[material]
    else:
        final_mapping[material] = "bad mattch"
    print(material)

# merge
output_model_concrete["Exio prod code"] = output_model_concrete["material_IRI"].map(
    final_mapping
)
# ------------roug calculation
final_output_concrete = pd.merge(
    output_model_concrete, footprint, on=["Exio prod code"], how="left"
)
for col in final_output_concrete.columns[-49:]:
    final_output_concrete[col] = (
        final_output_concrete[col] * final_output_concrete["amount"]
    )

data_for_countries = final_output_concrete[final_output_concrete.columns[-49:]].sum()
data_for_countries = data_for_countries.to_frame()
data_for_countries = data_for_countries.rename(columns={0: "kg CO2-eq"})

data_for_countries.to_csv(
    path_home
    / "Departier_repo"
    / "BridgesLCA/BridgesLCA/results/result_for_countries_example.csv"
)
