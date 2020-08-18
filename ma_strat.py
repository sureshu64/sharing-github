#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:21:53 2020
@author: sureshu
"""

import talib as tb
import threading
import pandas as pd
from gs_utils import signal_reporter, ma_report_printing, strat_wise_MA_append

# Module to analyze the data based on indicators and 
# generate necessary signals

class AsyncMAStrat(threading.Thread):
    
    def __init__(self, name, smaDf, user_item):

        threading.Thread.__init__(self)
        self.name = name
        #
        # init the properties
        #
        # deepcopy of the Dat Frame object
        self.smaDf = smaDf.copy()
        self.alreadyPrinted = []
        self.user_item = user_item
        self.justMA = ''
        self.tp = 0
        #
        # get the MA
        #
        self.smaDf = self.calculate_ma_data()


    # get the MAs to determine the crpssing, only if needed
    def calculate_ma_data(self):
            
        # get the MA from talib
        self.justMA = self.user_item.strip().split(' ')[2][1::] + self.user_item.strip().split(' ')[3]
        self.tp = int(self.user_item.strip().split(' ')[3])
        self.smaDf[self.justMA] = tb.MA(self.smaDf['Close'], timeperiod=self.tp)
        
        # drop rows with NaN
        return (self.smaDf.dropna())



    def run(self):

        self.alreadyPrinted = []

        #
        # LONG Signal
        #
        # long signal without MACD filters
        # open is less than MA and close is greeater than MA
        # bar opens in one side of MA and closes on the other side
        signal_reporter(self.smaDf[(self.smaDf['Close'] > self.smaDf[self.justMA]) & \
                              (self.smaDf['Open'] < self.smaDf[self.justMA])], \
                               'Long', 'Cross', self.alreadyPrinted, self.justMA, '', self.name)
        
        #
        # SHORT Signal
        #
        # save the processed dataframe
        signal_reporter(self.smaDf[(self.smaDf['Close'] < self.smaDf[self.justMA]) & \
                              (self.smaDf['Open'] > self.smaDf[self.justMA])],\
                               'Short', 'Cross', self.alreadyPrinted, self.justMA, '', self.name)

        #    
        # gapped over MA
        #
        # LONG Signal
        #
        # Scenario 1: BUY DAY: Put this logic back ... till further notice
        #             Open crossed over MA lower than prev close and 
        #             the opening price is lower than close...climbing back
        signal_reporter(self.smaDf[(self.smaDf.shift(periods=1)['Close'] > \
                                         self.smaDf.shift(periods=1)[self.justMA]) & \
                                   (self.smaDf['Open'] < self.smaDf[self.justMA]) & \
                                   (self.smaDf['Open'] < self.smaDf['Close'])],\
                                    'Long', 'Gap', self.alreadyPrinted, self.justMA, '', self.name)
        #
        # SHORT Signal
        #
        # Scenario 2: Open crossed over MA.  Open lower than prev close and the 
        #             opening price is higher than close.  Valid Short.
        #             going down
        signal_reporter(self.smaDf[(self.smaDf.shift(periods=1)['Close'] > \
                                         self.smaDf.shift(periods=1)[self.justMA]) & \
                                   (self.smaDf['Open'] < self.smaDf[self.justMA]) & \
                                   (self.smaDf['Open'] > self.smaDf['Close'])],\
                                    'Short', 'Gap', self.alreadyPrinted, self.justMA, '', self.name)

        #
        # LONG Signal
        #
        # Scanario 3: Open crossed over MA. Open higher than prev close and the 
        #             opening price is less than close.  Valid Long
        #             climbing up
        signal_reporter(self.smaDf[(self.smaDf.shift(periods=1)['Close'] < \
                                         self.smaDf.shift(periods=1)[self.justMA]) & \
                                   (self.smaDf['Open'] > self.smaDf[self.justMA]) & \
                                   (self.smaDf['Open'] < self.smaDf['Close'])],\
                                    'Long', 'Gap', self.alreadyPrinted, self.justMA, '', self.name)

        #
        # SHORT Signal
        #
        # Scenario 4: SELL DAY: Open crossed over MA. Open higher than prev close 
        #             and the opening price is lower than close.
        #             Going down after crossing.  
        #             Put this logic back ... till further notice
        signal_reporter(self.smaDf[(self.smaDf.shift(periods=1)['Close'] < \
                                         self.smaDf.shift(periods=1)[self.justMA]) & \
                                   (self.smaDf['Open'] > self.smaDf[self.justMA]) & \
                                   (self.smaDf['Open'] > self.smaDf['Close'])],\
                                    'Short', 'Gap', self.alreadyPrinted, self.justMA, '', self.name)

        # accumulate the print records for all the market
        strat_wise_MA_append(self.name, self.alreadyPrinted, self.user_item, self.justMA)
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
