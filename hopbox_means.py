#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:08:03 2024

@author: patrick.woods
"""    
    
#v2
def hopbox_means(csv, est_h2 = False):
    '''
    

    Parameters
    ----------
    csv : string
        A string corresponding to the name of the .csv file produced by HopBox. 
        This .csv file is typically called 'Features.csv'
    est_h2 : Boolean
        Defaults to False. If set to False, the function will only return a
        dataframe coontaining the genotypie means for each trait reported
        in the Features.csv file. If set to True, the function will instead 
        calculate the heritability for each trait in the Features.csv file.
    Returns
    -------
    None.

    '''
    
    import pandas as pd
    import numpy as np
    
    file = pd.read_csv(csv)
    file_group = file.groupby(['QR_info'])
    
    means_df = pd.DataFrame()
    
    h2_df = pd.DataFrame()
    
    if est_h2 == False:
        
        for i in file.iloc[:,4:]:
            mean = file_group[i].mean()
        
            means_df = pd.concat([means_df, mean], axis = 1)
        
        return means_df
    
    else:
        
        import rpy2.robjects as robjects #needed to access R functionality
        import rpy2.robjects.packages as rpackages #needed to access R functionality
        from rpy2.robjects import Formula
        from rpy2.robjects.vectors import StrVector #needed to access R functionality
        from rpy2.robjects import pandas2ri #needed to convert R objects to Pandas objects
        pandas2ri.activate() #activates the conversion functionality of the previously imported code
    
        lme4 = rpackages.importr('lme4')
        nlme = rpackages.importr('nlme')
        base = rpackages.importr('base')
        stats = rpackages.importr('stats')
        
        
        
        for i in file.iloc[:,4:]:
            
            
            
            mod_r = lme4.lmer(base.paste0(i, '~ (1|QR_info)'),
                        data=file)
            
        # extrating variance components and converting them to R dataframe
            var_comp = base.as_data_frame(nlme.VarCorr(mod_r))
            pd_df = pandas2ri.rpy2py_dataframe(var_comp)
            G = pd_df.iloc[0, 3]
            error = pd_df.iloc[1, 3]
            total_var = G + error
            heritability = G/total_var * 100
    
            heritability_dict = {i : [heritability]}
            
            heritability_df = pd.DataFrame(heritability_dict)
            
            h2_df = pd.concat([h2_df,heritability_df], axis = 1)
            
            h2_df_long = pd.melt(h2_df, var_name='Feature', value_name='Heritability')
            
        return h2_df_long
    

hopbox_means('Features.csv', est_h2=True) 


