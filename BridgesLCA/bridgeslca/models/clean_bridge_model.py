#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:50:06 2024

@author: thibault.chevilliet
"""
#%% Import needed packages
import pandas as pd
import os
from datetime import date
from pydantic import BaseModel
from typing import Optional, NamedTuple

import bridgeslca.models.clean_input_data as data
import bridgeslca.models.materials_model as mat

#%% Definition of Classes we barely use
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
    tolerance: Optional[float] = 0.2  # default tolerance for both width and lenght

class RunConfig(BaseModel):
    outliers_raise_error: bool = False
    num_samples: int = 1000

def within_interval(ref_value: float, target_value: float, tolerance: float) -> bool:
    print()
    return (ref_value < target_value * (1 + tolerance)) & (
        ref_value > target_value * (1 - tolerance)
    )

class BridgeModel:

    def __init__(self, demand: Demand, run_config: RunConfig):
        self.demand = demand

    def get_model_data(self
                       #,all_data: dict #not needed and is confusing into get_model_data args
                       ,reported_technology: pd.DataFrame
    ) -> list[pd.DataFrame]:  # Duck typing also fine
        #self.all_data = all_data
        self.reported_technology = reported_technology

    def check_tolerance(self) -> list:
        return [row for row in self.reported_technology.index[1:] if (
                within_interval(
                    self.demand.width,
                    self.reported_technology.loc[row, 'Width'],
                    self.demand.tolerance,
                )
                & within_interval(
                    self.demand.length,
                    self.reported_technology.loc[row, 'Length'],
                    self.demand.tolerance,
                )
            )
        ]

    def prepare(self) -> None:
        self.get_model_data()
        self.data_validity_checks()
        self.resample()

    def run(self) -> list[Demand]:
        # if there's a match within the tolerance, we do the average on a narrower sample
        if len(self.check_tolerance()) > 0:
            final_df = mat.all_structural_components(
                self.reported_technology.loc[self.check_tolerance(), :],
                list(self.reported_technology.columns[9:]),
                self.demand.length,
                self.demand.width,
            )
        #if not, we're using average ratio per types
        else:
            final_df = mat.all_structural_components(
                self.reported_technology,
                list(self.reported_technology.columns[9:]),
                self.demand.length,
                self.demand.width,
            )

            return final_df


# %% RUN the model
D = Demand(
    product_iri=IRI(ref="http://data.europa.eu/xsp/cn2024/911440000080"),
    properties=None,
    amount=2.0,
    temporal_range=(date(2000, 1, 1), date(2010, 1, 1)),
    width=11,
    length=44,
    tolerance=0,
)
m = BridgeModel(demand=D, run_config=RunConfig())
m.get_model_data(data.df_bridge)
result = m.run()