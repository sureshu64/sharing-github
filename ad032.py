#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 07:03:54 2020

@author: sureshu
"""

# demonstrate the calculation of covariance and corelation
# this is usually calculated for pair of arguments
#import numpy as np
import pandas as pd
import pandas_datareader.data as web

all_data = {ticker: web.get_data_yahoo(ticker)
            for ticker in ['AAPL', 'IBM', 'MSFT', 'GOOG']}

price = pd.DataFrame({ticker: data['Adj Close']
                     for ticker, data in all_data.items()})
volume = pd.DataFrame({ticker: data['Volume']
                       for ticker, data in all_data.items()})

print(price)
print(volume)

returns = price.pct_change()
print(returns.tail())

print("\nCorrelation between MSFT and IBM %.2f " % returns['MSFT'].corr(returns['IBM']))
print("\nCovariance between MSFT and IBM %.5f " % returns['MSFT'].cov(returns['IBM']))

# print the correlation of all the ticker to 2 decimal places
format = lambda df1: '%.2f' % df1

df2 = returns.corr().applymap(format)
print(df2)
