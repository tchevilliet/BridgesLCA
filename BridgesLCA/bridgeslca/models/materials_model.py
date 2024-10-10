#%% Import packages
import pandas as pd
import numpy as np

#%% Define functions

#Define a function that creates the data for one structural component only
def one_structural_component(df, c, user_length, user_width, user_type=None):
    #if user didn't put any type :
    if user_type is None :
        if user_length >= 80:
            user_type = 'Composite'
        elif user_length <10 :
            user_type = 'Reinforced Concrete'
        else :
            user_type = 'Prestressed Concrete'
    
    df_per_type = df[df["Type"] == user_type] # filtered data with the right type
    ratio = np.mean(df_per_type[c]/(df_per_type["Length"]*df_per_type["Width"])) #here we use a ratio, but could be a function
    
    #we build the result dataframe
    res = pd.DataFrame(index=[c],columns=['IRI','unit','amount','phase'])
    res['IRI'] = 'http://data.europa.eu/xsp/cn2024/382450100080'#not a good IRI, just to try
    res['unit'] = df[c].iloc[0]
    res['amount'] = ratio*user_length*user_width
    res['phase'] = 'construction'
    return res

#Loop on all columns we want to analyze in the Excel file source
def all_structural_components(df, c_list, user_length, user_width, user_type=None):
    res = pd.DataFrame(columns=['IRI','unit','amount','phase'])
    for c in c_list:
        res = pd.concat([res, one_structural_component(df, c, user_length, user_width, user_type=None)])
    return res

#%% import data
my_data = pd.read_excel(r"C:\Users\julien.cravero\source\repos\BridgesLCA\BridgesLCA\data\Bridges.xlsx")

my_list = list(my_data.columns[9:])
#%% Calculation
a = all_structural_components(my_data,my_list, 100, 1)

# %%
