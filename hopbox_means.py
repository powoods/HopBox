#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:08:03 2024

@author: patrick.woods
"""

#v1


def hopbox_means(csv):
    '''
    

    Parameters
    ----------
    csv : string
        A string correspondign to the name of the .csv file produced by HopBox. This .csv file is typically called 'Features.csv'
    Returns
    -------
    None.

    '''
    
    import pandas as pd
    import numpy as np
    
    file = pd.read_csv(csv)
    file_group = file.groupby(['QR_info'])
    
    means_df = pd.DataFrame()
    
    for i in file.iloc[:,4:]:
        mean = file_group[i].mean()
        
        means_df = pd.concat([means_df, mean], axis = 1)
        
    return means_df
   
 
hopbox_means('Features.csv') 
    
    
    
    
    
    
    




