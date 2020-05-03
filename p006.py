#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:40:54 2020

@author: sureshu
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ClensedSheet2.csv")
fig, ax = plt.subplots(figsize=(15,7))
df.groupby('createTime').count()['traitType'].plot(ax=ax)

