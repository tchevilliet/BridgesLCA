# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:00:04 2024

@author: StefanoMerciai
"""
import pandas as pd

# dataframe
d = {
    "Cement": [10, 100, 200, 300],
    "Steel": [1, 10, 20, 30],
    "width": [11, 110, 220, 330],
    "length": [100, 300, 700, 1000],
}
# dataframe that includes the existing reported bridges
reported_technology = pd.DataFrame(
    data=d, index=["bridge_1", "bridge_2", "bridge_3", "bridge_4"]
)


# dataframe that includes the recipes of components of bridges
all_data = {
    "http://data.europa.eu/xsp/cn2024/foundation": pd.DataFrame(
        {"Cement": [100], "Steel": [10]}, index=["foundation"]
    ),
    "http://data.europa.eu/xsp/cn2024/piles": pd.DataFrame(
        {"Cement": [35], "Steel": [10]}, index=["piles"]
    ),
    "http://data.europa.eu/xsp/cn2024/cement": pd.DataFrame(
        {"limestone": [10], "water": [5]}
    ),
    "http://data.europa.eu/xsp/cn2024/steel": pd.DataFrame(
        {"iron ore": [1], "land": [4]}
    ),
}

list_uri = {
    "bridge_1": "http://data.europa.eu/xsp/cn2024/bridge_1",
    "bridge_2": "http://data.europa.eu/xsp/cn2024/bridge_2",
    "bridge_3": "http://data.europa.eu/xsp/cn2024/bridge_3",
    "bridge_4": "http://data.europa.eu/xsp/cn2024/bridge_4",
    "Cement": "http://data.europa.eu/xsp/cn2024/cement",
    "Steel": "http://data.europa.eu/xsp/cn2024/steel",
    "foundation": "http://data.europa.eu/xsp/cn2024/foundation",
    "piles": "http://data.europa.eu/xsp/cn2024/piles",
}
