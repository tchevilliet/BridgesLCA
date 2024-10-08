#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:50:06 2024

@author: thibault.chevilliet
"""
#%%
from datetime import date
from pydantic import BaseModel
from typing import Optional, NamedTuple
import pandas as pd
#import sentier_data_tools as sdt

#%%

class IRI(BaseModel):
    # Can look up info
    ref: str

class SimpleDataRange(NamedTuple):
    start : date
    end : date
        
class Demand(BaseModel):
    product_iri: IRI
    properties: Optional[list]
    amount: float
    spatial_context: IRI = IRI(ref="https://sws.geonames.org/6295630/")
    temporal_range: SimpleDataRange # TBD


class RunConfig(BaseModel):
    outliers_raise_error: bool = False
    num_samples: int = 1000


class SentierModel:
    def __init__(self, demand: Demand, run_config: RunConfig):
        pass

    def get_model_data(self) -> list[pd.DataFrame]:  # Duck typing also fine
        pass

    def prepare(self) -> None:
        self.get_model_data()
        self.data_validity_checks()
        self.resample()

    def run(self) -> list[Demand]:
        pass
    


#%%

D = Demand(product_iri=IRI(ref='http://data.europa.eu/xsp/cn2024/911440000080'),
           properties = None,
           amount = 1.0,
           temporal_range = (date(2000,1,1),date(2010,1,1)))
m = SentierModel(demand=D,run_config=RunConfig())

df1 = pd.DataFrame({"Cement":[1], "Steel":[10]})
