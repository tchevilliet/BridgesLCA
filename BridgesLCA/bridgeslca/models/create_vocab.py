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
        SKOS.closeMatch,
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

# export
bonsai_db_uri.serialize(destination=path_file)
