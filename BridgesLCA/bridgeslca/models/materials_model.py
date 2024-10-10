#%% Import packages
import pandas as pd
import numpy as np

#%% Define functions
def concrete_20MPa(df, user_length, user_width, user_type=None):
    #if user didn't put any type :
    if user_type is None :
        if user_length >= 80:
            user_type = 'Composite'
        elif user_length <=10 :
            user_type = 'Reinforced Concrete'
        else :
            user_type = 'Prestressed Concrete'
    
    df_per_type = df[df["Type"] == user_type] # filtered data with the right type
    col = "Blinding Concrete C20" # column to do calculation on
    ratio = np.mean(df_per_type[col]/(df_per_type["Length"]*df_per_type["Width"])) #here we use a ratio, but could be a funtion
    
    #we build the result dataframe
    res = pd.DataFrame(index=[col],columns=['IRI','unit','amount','phase'])
    res['IRI'] = 'http://data.europa.eu/xsp/cn2024/382450100080'#not a good IRI, just to try
    res['unit'] = df[col].iloc[0]
    res['amount'] = ratio*user_length*user_width
    res['phase'] = 'construction'
    return res


#%% import data
my_data = pd.read_excel(r"C:\Users\julien.cravero\source\repos\BridgesLCA\BridgesLCA\data\Bridges.xlsx")

#%% Calculation
a = concrete_20MPa(my_data,50,200)
