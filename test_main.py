# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 16:46:10 2023

@author: Paul
"""

import pytest
import pandas as pd
import main

def test_check_data():
    data = pd.read_csv('cleaned_data.csv', index_col=0)
    result = main.check_data(data)
    assert(result==1)