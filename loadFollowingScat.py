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
from bokeh.layouts import column, row, gridplot
from bokeh.palettes import Category10, Category20, Inferno
import colorcet as cc
import seaborn as sns
from numpy import linspace
from scipy.stats.kde import gaussian_kde


###########################################################################
# Creates a grid of scatter plots that is too big - crashes the computer
#######################################################################

import datetime
#%load_ext blackcellmagic
#%matplotlib inline

def nowtime():
    now=datetime.datetime.now()
    return "".join([str(i) for i in (now.day,0,now.month,now.year,now.hour,now.minute)])

# csv file is generated using writeLFdata.py
# df gives the fraction of power that the source's capacity that it is 
# currently generating at
df = pd.read_csv('LF4052019182.csv')
df.drop('Unnamed: 0',inplace=True, axis=1)
#if output_folder != None:
output_folder="C:/Users/Chris/Documents/Documents/Python2018/DataVisCW/Plots"
output_file(output_folder+"loadFollowing"+nowtime()+".html")

#dataSource = ColumnDataSource(df)


#fig = figure(title='Load following')

dataSource = ColumnDataSource(df)
ylist = [' nuclear2', ' coal2', ' hydro2', ' wind2', ' oil2', ' ccgt2',
         ' biomass2', ' solar2', ' ocgt2', ' pumped2', ' french_ict2']
DSdict, figDict, lineDict = {},{},{}
figList = []
for y,year in enumerate([2013]):#df['Year'].unique()):
#    DSname = 'DS'+str(year)
#    DSdict[DSname] = ColumnDataSource(df[df['Year']==year])
    for i,source in enumerate(ylist[1]):
        print(year, source)
        #figname = source[1:-1]+str(year)
        #print(figname)
        #figDict[figname] = figure(title = source+str(year))
        a = figure(title=source+str(year), plot_height=180, plot_width=180)
        #linename =figname + 'line'
        #lineDict[linename] = 
        #figDict[figname].
        a.circle(x=df[' demand2'],
                y=df[source], 
                #source=DSdict[DSname], 
                     color = Category20[(len(ylist)+1)][0],
                      size=0.1, fill_alpha=0.002)
        if i == 0:
            figList.append([a])#[figDict[figname]])
        else:
            figList[y].append(a)#figDict[figname])
        #show(a)#figDict[figname])
    #line_width=1) 
    #hover = HoverTool(tooltips =[('Cat',line),('MW','$y')], renderers=[lines])
    #fig.add_tools(hover)

#output_notebook()

layout = gridplot(figList)
show(layout)