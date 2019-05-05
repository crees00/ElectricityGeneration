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
import matplotlib.pyplot as plt

import ipywidgets as widgets
from ipywidgets import interact
from bokeh.io import output_file, show, output_notebook, curdoc, push_notebook
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import HoverTool, Slider,ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, CrosshairTool, DatetimeTickFormatter, Range1d
from bokeh.models import CheckboxGroup, RadioGroup, Toggle, CheckboxButtonGroup, Button
from bokeh.models.widgets import Select
from bokeh.layouts import column, row
from bokeh.palettes import Category10, Category20, Inferno
import colorcet as cc
import seaborn as sns
from numpy import linspace
from scipy.stats.kde import gaussian_kde

import getData


import datetime
#%load_ext blackcellmagic
#%matplotlib inline

def nowtime():
    now=datetime.datetime.now()
    return "".join([str(i) for i in (now.day,0,now.month,now.year,now.hour,now.minute)])

def calcEffort(value, col):
    ''' Given a power value and a column name, returns the % of the way
    between min and max that power value is for that source'''
    
    colRange = maxvals[col]-minvals[col]
    effort = (value-minvals[col])/colRange
    return effort

df = getData.data161.copy()

data162 = df.drop([' timestamp', 'id',  'Hour', 'Min', 'DayHour', 
       'Month', 'Day'], axis=1)

maxvals,minvals = {},{}
data163=pd.DataFrame()
data163['Year'] = data162['Year']
for col in (set(data162.columns) - set(['Year'])):
    #mean = (data162[col]).mean()
    #sd = data162[col].std()
    maxvals[col] = np.percentile(a=data162[col], q=99.99)
    minvals[col] = np.percentile(a=data162[col], q=0.001)
    print(col,maxvals[col],data162[col].max(),minvals[col],data162[col].min())
    #print(data162[col]>maxval)
    data163[col] = data162[col].apply(lambda x: np.NaN if \
           ((x>maxvals[col])or(x<minvals[col])) else x)
    data163[col+str(2)] = data163.apply(lambda row: calcEffort(row[col],col),
           axis=1)
    data163.drop(col, inplace=True, axis=1)
    #data162.loc[col,(data162[col] < minval)] = np.NaN
    #df4 = data162[(np.abs(stats.zscore(data161.drop('Year', axis=1))) < 3).all(axis=1)]
#filename = 'LF31.csv'
#data162.to_csv(filename)
#data161[' demand'] = data161.apply(lambda row: checkRow(row,1e5),axis=1)

#maxDict = {}
#minDict = {}
#
#sources = [' demand', ' coal', ' nuclear', ' ccgt', ' wind',
#       ' pumped', ' hydro', ' biomass', ' oil', ' solar', ' ocgt',
#       ' french_ict', ' dutch_ict', ' irish_ict', ' ew_ict', ' nemo', ' other',
#       ' north_south', ' scotland_england']
#for source in sources:
#    maxDict[source] = df[source].max()
#    minDict[source] = df[source].min()

# For each source, at each time point calculate the % way between min and max
# i.e. max = 100%, min = 0







data163.to_csv('LF'+nowtime()+'.csv')