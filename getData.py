# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:37:04 2019

@author: Chris
"""

import numpy as np
import pandas as pd

import datetime
#%load_ext blackcellmagic
#%matplotlib inline

def nowtime():
    now=datetime.datetime.now()
    return "".join([str(i) for i in (now.day,0,now.month,now.year,now.hour,now.minute)])

#def checkRow(row, thresh=7e4):
#    if row[' demand'] < thresh:
#        return row[' demand']
#    else:
#        for i in range(5,12):
#            if (data161[' demand'][row['id']-i])<thresh:
#                return (data161[' demand'][row['id']-i])

def getGridwatchData():
    data16 = pd.read_csv('gridwatch.csv', index_col=1,skip_blank_lines=True, header=[0], parse_dates=True)
    #data10.drop('Belgium-UK',1,level=0,inplace=True)
    data16.head()
    data16.iloc[638919,10] = 1510
    data16.iloc[638920,10] = 1510
    data16[data16['id']==638925].loc[:,' solar'] = 1510
    data16['Hour'] = data16.index.hour
    data16['Min'] = data16.index.minute
    data16['DayHour'] = data16['Hour'] + data16['Min']/60
    data16['Year'] = data16.index.year
    data16['Month'] = data16.index.month
    data16['Day'] = data16.index.day
    data16[data16['DayHour']==1.5].head()
    data16[' solar'].max()
    
    data161 = data16.reset_index()
    return data161
