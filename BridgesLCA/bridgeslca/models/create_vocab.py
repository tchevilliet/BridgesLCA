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
        SKOS.relatedMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/235"),
    )
)
bonsai_db_uri.add(
    (
        cement_uri,  # Subject
        SKOS.definition,
        Literal("Production of cement, lime and plaster, market of", lang="en"),
    )
)
bonsai_db_uri.add((cement_uri, SKOS.notation, Literal("M_CMNT", lang="en")))  # Subject


# steel
cement_uri = URIRef("https://lca.aau.dk/FootprintAnalyser/M_STEL")

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
        SKOS.relatedMatch,
        URIRef("http://data.europa.eu/ehl/cpa21/241"),
    )
)
bonsai_db_uri.add(
    (
        cement_uri,  # Subject
        SKOS.definition,
        Literal(
            "Production of basic iron and steel and of ferro-alloys and first products thereof, market of",
            lang="en",
        ),
    )
)
bonsai_db_uri.add((cement_uri, SKOS.notation, Literal("M_STEL", lang="en")))  # Subject
