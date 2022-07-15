
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 2022

@author: Ellen
"""
# Create a dataframe of upstream or downstream partners 
# Based on synapse predictions
# Choose population or neuron to query
# choose synapse threshhold and whether to get pre or postsynaptic partners


if __name__ == '__main__':
    pass

import pandas as pd
import numpy as np 
import os
import cloudvolume as cv

def build_synapse_df(neurons,prepost,thresh,client): # example: build_synapse_df(MN_df.SegID.to_list(),"pre",3,client)
    i = 0
    while i < len(neurons):
        iSeg = neurons[i]

        if prepost == "pre":
            temp_df = client.materialize.synapse_query(post_ids = iSeg)
            v = temp_df[['pre_pt_root_id']]

        if prepost == "post":
            temp_df = client.materialize.synapse_query(pre_ids = iSeg)
            v = temp_df[['post_pt_root_id']]
            
        threshed = temp_df[v.replace(v.apply(pd.Series.value_counts)).gt(thresh-1).all(1)]
        
        if i == 0:
            syn_df = threshed
        else:
            syn_df = partners_df.append(threshed)

        i = i+1
    return syn_df

