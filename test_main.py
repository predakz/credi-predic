# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 16:46:10 2023

@author: Paul
"""

import pytest
import main

def test_check_data():
    result = main.check_data(main.data)
    assert(result==1)