#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:50:06 2024

@author: thibault.chevilliet
"""
# %%Import needed packages
import pandas as pd
from datetime import date
from pydantic import BaseModel
from typing import Optional, NamedTuple
import sentier_data_tools as sdt
from sentier_data_tools.unit_conversion import *
from sentier_data_tools.example import WaterElectrolysisModel, create_example_local_datastorage

from sentier_data_tools import (
    DatasetKind,
    Demand,
    Flow,
    FlowIRI,
    GeonamesIRI,
    ModelTermIRI,
    ProductIRI,
    UnitIRI,
    SentierModel,
)
# %%Class definition

class BridgeModel(SentierModel):
    provides = {
        ProductIRI(
            "https://w3id.org/brot#Bridge"
        ): "bridge",
    }
    needs = {
        ModelTermIRI(
            "https://w3id.org/bridge#overalLength"
        ): "length",
        ModelTermIRI(
            "https://vocab.sentier.dev/model-terms/electrolyser/product_lifetime"
        ): "width"
    }
    def run(self) -> tuple[list[Demand], list[Flow]]:
        return (1,1)
    
    def get_model_data(self) : 
        super().get_model_data(self.bridge, kind=DatasetKind.COMPOSITION)
        
        
    def get_bridge_inventory(self) -> None:
        bom_bridge= self.get_model_data(
            self, product=self.bridge, kind=DatasetKind.BOM
        )
    
    
    def prepare(self) -> None:
        self.get_model_data()
        self.data_validity_checks()
        self.resample()
    


# %%

D = Demand(
    product_iri=ProductIRI("https://w3id.org/brot#Bridge"),
    unit_iri = UnitIRI("https://vocab.sentier.dev/units/quantity-kind/Length"),
    amount = 1.0
    # properties=None,
    # amount=2.0,
    # temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
    # width=200,
    # length=1710,
    # tolerance=0.20,
)
#%%
m = SentierModel(demand=D, run_config=sdt.RunConfig())
m.get_model_data()

