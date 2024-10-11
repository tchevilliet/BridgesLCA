#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 18:35:47 2024

@author: thibault.chevilliet
"""

import pandas as pd
import seaborn as sns

df = pd.read_excel("/home/thibault.chevilliet@enpc.fr/Bureau/DDS Autumn School/BridgesLCA/BridgesLCA/data/bridgesdbUS.xlsx")

#%%
g= sns.regplot(data = df[(df['Length 049']<=300)
                             &(df['Length 049']>=10)
                             &(df['Kind of material and/or design 43A']=='Wood or Timber')
                             ]
                   ,x='Length 049'
                   ,y='Width (Deck) 052'
                   #,hue = 'Kind of material and/or design 43A'
                   )