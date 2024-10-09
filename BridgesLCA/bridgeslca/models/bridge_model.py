#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:50:06 2024

@author: thibault.chevilliet
"""
import pandas as pd


from datetime import date
from pydantic import BaseModel
from typing import Optional, NamedTuple

import bridgeslca.models.input_data as data

# import sentier_data_tools as sdt
data.all_data


class IRI(BaseModel):
    # Can look up info
    ref: str


class SimpleDataRange(NamedTuple):
    start: date
    end: date


class Demand(BaseModel):
    product_iri: IRI
    properties: Optional[list]
    amount: float
    spatial_context: IRI = IRI(ref="https://sws.geonames.org/6295630/")
    temporal_range: SimpleDataRange  # TBD
    lenght = int
    weight = int
    tolerance = float


class RunConfig(BaseModel):
    outliers_raise_error: bool = False
    num_samples: int = 1000


class SentierModel:
    def __init__(self, demand: Demand, run_config: RunConfig):
        self.demand = demand

    def get_model_data(
        self, demand: Demand
    ) -> list[pd.DataFrame]:  # Duck typing also fine
        if self.demand.product_iri.ref in data.all_data.keys():
            inputs_df = data.all_data[self.demand.product_iri.ref]

        else:
            print(" no DF")

        return inputs_df
    
    def check_tolerance

    def prepare(self) -> None:
        self.get_model_data()
        self.data_validity_checks()
        self.resample()

    def run(self) -> list[Demand]:

        return self.demand.amount * self.get_model_data(self.demand)


list_uri = {
    "Cement": "http://data.europa.eu/xsp/cn2024/cement",
    "Steel": "http://data.europa.eu/xsp/cn2024/steel",
}
D = Demand(
    product_iri=IRI(ref="http://data.europa.eu/xsp/cn2024/911440000080"),
    properties=None,
    amount=2.0,
    temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
)
m = SentierModel(demand=D, run_config=RunConfig())
m.run()

for col in m.run():

    new_D = Demand(
        product_iri=IRI(ref=list_uri[col]),
        properties=None,
        amount=m.run().loc[0, col],
        temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
    )
    m_new = SentierModel(demand=new_D, run_config=RunConfig())
    print(m_new.run())


m.get_model_data()
foundation = pd.DataFrame({"Cement": [1], "Steel": [10]})

D.product_iri.ref

data.list_uri
