#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:50:06 2024

@author: thibault.chevilliet
"""
#%%
import pandas as pd
from datetime import date
from pydantic import BaseModel
from typing import Optional, NamedTuple

import bridgeslca.models.input_data as data
#%%
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
    length: float
    width: float
    tolerance: float


class RunConfig(BaseModel):
    outliers_raise_error: bool = False
    num_samples: int = 1000


def within_interval(ref_value: float, target_value: float, tolerance: float) -> bool:
    return (ref_value < target_value * (1 + tolerance))&(ref_value > target_value * (1 - tolerance))

class SentierModel:
    def __init__(self, demand: Demand,run_config: RunConfig):
        self.demand = demand

    def get_model_data(self, data : dict) -> list[pd.DataFrame]:  # Duck typing also fine
        self.data = data
        if self.demand.product_iri.ref not in self.data.keys():
            raise ValueError
        return self.data[self.demand.product_iri.ref]

    def check_tolerance(self) -> list:
        return [row for row in data.reported_technology.index if 
                (within_interval(self.demand.width,
                               data.reported_technology.loc[row,"width"],
                               self.demand.tolerance) 
                & within_interval(self.demand.length,
                               data.reported_technology.loc[row, "length"],
                               self.demand.tolerance))]
    
    def prepare(self) -> None:
        self.get_model_data()
        self.data_validity_checks()
        self.resample()

    def make_the_bridge(self) -> dict:
        custom_bridge = {}
        custom_bridge["foundation"] = self.demand.weight / 2
        custom_bridge["piles"] = int(self.demand.lenght / 50)
        print(custom_bridge)
        return custom_bridge

    # try to insert check in the existing df
    def run(self) -> list[Demand]:

        if isinstance(self.check_tolerance(), str):
            return self.data.reported_technology.loc[self.check_tolerance(), :]
        else:
            custom_bridge = self.make_the_bridge()
            for card, parts in enumerate(custom_bridge.keys()):
                uri_of_flow = data.list_uri[parts]
                input_df = custom_bridge[parts] * data.all_data[uri_of_flow]

                input_df
                if card == 0:
                    final_df = input_df.copy()
                else:
                    fianl_df = pd.concat([final_df, input_df], axis=0)

            return fianl_df

            # print("no matching df")
            # return self.demand.amount * self.get_model_data(self.demand)

#%%
list_uri = {
    "Cement": "http://data.europa.eu/xsp/cn2024/cement",
    "Steel": "http://data.europa.eu/xsp/cn2024/steel",
}
D = Demand(
    product_iri=IRI(ref="http://data.europa.eu/xsp/cn2024/911440000080"),
    properties=None,
    amount=2.0,
    temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
    width=200,
    length=710,
    tolerance=0.10,
)
m = SentierModel(demand=D, run_config=RunConfig())
m.run()
# m.check_tolerance()

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
int(3.45)
