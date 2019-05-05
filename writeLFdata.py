# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:40:42 2019

@author: Chris
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:32:16 2019

@author: Chris
"""

import numpy as np
import pandas as pd
import getData
#%load_ext blackcellmagic
#%matplotlib inline

global maxvals,minvals
maxvals,minvals = {},{}

def calcEffort(value, col):
    ''' Given a power value and a column name, returns the % of the way
    between min and max that power value is for that source'''
    
    colRange = maxvals[col]-minvals[col]
    effort = (value-minvals[col])/colRange
    return effort

def makecsv():
    ''' Return a df with normalised values. Save it as a csv so it doesn't
    need to be made again.'''
    df = getData.getGridwatchData()
    
    data162 = df.drop([' timestamp', 'id',  'Hour', 'Min', 'DayHour', 
           'Month', 'Day',' ocgt',  ' dutch_ict',
       ' irish_ict', ' ew_ict', ' nemo', ' other', ' north_south',
       ' scotland_england'], axis=1)
    
    data163=pd.DataFrame()
    data163['Year'] = data162['Year']
    
    for i,col in enumerate(set(data162.columns) - set(['Year']),1):
        print(col)
        maxvals[col] = np.percentile(a=data162[col], q=99.99)
        minvals[col] = np.percentile(a=data162[col], q=0.001)
        data163[col] = data162[col].apply(lambda x: np.NaN if \
               ((x>maxvals[col])or(x<minvals[col])) else x)
        data163[col+str(2)] = data163.apply(lambda row: calcEffort(row[col],col),
               axis=1)
        data163.drop(col, inplace=True, axis=1)
        print('col',i,'of',len(set(data162.columns) - set(['Year'])),'complete')

    data163.to_csv('LF.csv')
    print('File created!')
    return data163