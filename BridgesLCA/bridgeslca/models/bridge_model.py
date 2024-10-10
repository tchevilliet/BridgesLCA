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

# %%Class definition


# class Demand(BaseModel):
#     product_iri: IRI
#     properties: Optional[list]
#     amount: float
#     spatial_context: IRI = IRI(ref="https://sws.geonames.org/6295630/")
#     temporal_range: SimpleDataRange  # TBD
#     length: float
#     width: float
#     tolerance: Optional[float] | 0.2


def within_interval(ref_value: float, target_value: float, tolerance: float) -> bool:
    return (ref_value < target_value * (1 + tolerance)) & (
        ref_value > target_value * (1 - tolerance)
    )


class BridgeModel(SentierModel):
    
    def __init__(self, demand: Demand, run_config: RunConfig):
        self.demand = demand

    def get_model_data(
        self, all_data: dict, reported_technology: dict
    ) -> list[pd.DataFrame]:  # Duck typing also fine
        self.all_data = all_data
        self.reported_technology = reported_technology

    def check_tolerance(self) -> list:

        return [
            row
            for row in self.reported_technology.index
            if (
                within_interval(
                    self.demand.width,
                    self.reported_technology.loc[row, "width"],
                    self.demand.tolerance,
                )
                & within_interval(
                    self.demand.length,
                    self.reported_technology.loc[row, "length"],
                    self.demand.tolerance,
                )
            )
        ]

    def prepare(self) -> None:
        self.get_model_data()
        self.data_validity_checks()
        self.resample()

    def make_the_bridge(self) -> dict:
        custom_bridge = {}
        custom_bridge["foundation"] = self.demand.width / 2
        custom_bridge["piles"] = int(self.demand.length / 50)
        print(custom_bridge)
        return custom_bridge

    # try to insert check in the existing df
    def run(self, list_uri: dict) -> list[Demand]:

        if len(self.check_tolerance()) > 0:
            return self.reported_technology.loc[self.check_tolerance(), :]
        else:
            custom_bridge = self.make_the_bridge()
            for card, parts in enumerate(custom_bridge.keys()):
                uri_of_flow = list_uri[parts]
                input_df = custom_bridge[parts] * data.all_data[uri_of_flow]

                input_df
                if card == 0:
                    final_df = input_df.copy()
                else:
                    fianl_df = pd.concat([final_df, input_df], axis=0)

            return fianl_df

            # print("no matching df")
            # return self.demand.amount * self.get_model_data(self.demand)


# %%

D = Demand(
    product_iri=IRI(ref="http://data.europa.eu/xsp/cn2024/911440000080"),
    properties=None,
    amount=2.0,
    temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
    width=200,
    length=1710,
    tolerance=0.20,
)
m = SentierModel(demand=D, run_config=RunConfig())
m.get_model_data(data.all_data, data.reported_technology)
m.run(data.list_uri)
# m.check_tolerance()
