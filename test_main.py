# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 16:46:10 2023

@author: Paul
"""

import pytest
import pandas as pd
import dill as pickle
import main

def test_transform_userdata():
    data = pd.read_csv('cleaned_data.csv', index_col=0)
    transformers = pickle.load(open('Pickles/transformers.pkl', 'rb'))
    list_transformers = [i for i in transformers]
    result = main.transform_userdata(pd.DataFrame(data.loc[[456248]]),list_transformers,transformers)
    assert(result==1)