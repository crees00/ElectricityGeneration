# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:02:42 2019

@author: Chris
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import *
import re

from bokeh.io import output_file, show, output_notebook, curdoc, push_notebook
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, \
Legend, DatetimeTickFormatter, CrosshairTool
from bokeh.models.widgets import Select, Tabs, Panel, Slider, TextInput, DateRangeSlider, RangeSlider
from bokeh.models.glyphs import VBar
from bokeh.layouts import column, row
from bokeh.palettes import Category10, Category20, Inferno, Category20b
import colorcet as cc
import seaborn as sns
from numpy import linspace
from scipy.stats.kde import gaussian_kde


import datetime

data12 = pd.read_csv('gridwatchAllCols.csv', index_col=1,skip_blank_lines=True, header=[0], parse_dates=True)
data12.loc['2013-05-15']#=='2011-05-27'
data12['Hour'] = data12.index.hour
data12['Min'] = data12.index.minute
data12['DayHour'] = data12['Hour'] + data12['Min']/60
data12['Year'] = data12.index.year
data12[data12['DayHour']==1.5].head()
data12['Month'] = data12.index.month
data12['Day'] = data12.index.day
data121 = data12.reset_index()
data122 = data121.drop(' timestamp', axis=1)

def nowtime():
    now=datetime.datetime.now()
    return "".join([str(i) for i in (now.day,0,now.month,now.year,now.hour,now.minute)])

## TWIN RIDGE PLOT - NOT KDE ##
#from bokeh.palettes import *

output_file("plots/twinridgeplot"+nowtime()+".html")

def ridge(category, data, scale=800):
    return list(zip([category]*len(data), scale*data))

years = data122['Year'].unique()
print(years, type(years[0]))
palette1 =[cc.coolwarm[i*10+160] for i in range(len(years)+1)]#Category20b[len(years)]# [cc.kr[i*10+150] for i in range(len(years)+1)]
palette2 =[cc.coolwarm[100-i*10] for i in range(len(years)+1)]#Category20[len(years)] #[cc.kb[i*10+150] for i in range(len(years)+1)]




def plotHistoRidges(listOfPairs):
    ''' Input = list of lists [[' nuclear', ' wind'],[' coal',' wind'],...]
    Makes a plot for each one'''
    for pair in listOfPairs:
        print(pair)
        xmin,xmax,num = 0,max(data122[pair].max()),500
        x = linspace(xmin,xmax,num)
        xnew = list(x)
        xnew.insert(0,xmin - (xmax-xmin)/num)
        xnew.append(xmax + (xmax-xmin)/num)
        source = ColumnDataSource(data=dict(xnew=xnew))
        source2 = ColumnDataSource(data=dict(xnew=xnew))
        
        p = figure(plot_width=900,y_range=[str(year) for year in reversed(years)], 
                    x_range=(-5, xmax),#,toolbar_location=None)
                   title = 'Histogram showing power output for each 5min interval throughout the year')
        
        p.xaxis.axis_label = 'Power output (MW)'
        
            #p.yaxis.axis_label = 'Pr(x)'
            #p.grid.grid_line_color="white"
            
            
            
        p.outline_line_color = None
        p.background_fill_color = "#efefef"
        
        p.xaxis.ticker = FixedTicker(ticks=list(range(0, xmax,1000)))
        
        p.ygrid.grid_line_color = None
        p.xgrid.grid_line_color = "#dddddd"
        p.xgrid.ticker = p.xaxis[0].ticker
        
        p.axis.minor_tick_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.axis_line_color = None
        
        p.y_range.range_padding = 0.1
        
        for i, year in enumerate(reversed(years)):
            print(i)
            hist, edges = np.histogram(data122[data122['Year']==year].loc[:,pair[0]].reset_index(drop=True),
                                       density=True, bins=200, range=(0,xmax))
            hist2, edges2 = np.histogram(data122[data122['Year']==year].loc[:,pair[1]].reset_index(drop=True),
                                       density=True, bins=200, range=(0,xmax))
            scaler = 1/ (1000*np.max([np.max(hist),np.max(hist2)]))
            y = ridge(str(year), hist)#*scaler)
            y2 = ridge(str(year), hist2)#*scaler)
        
            p.quad(top=y, bottom=((str(year),0),)*len(y), left=edges[:-1], right=edges[1:],
                   fill_color=palette1[9-i], line_color=palette1[9-i], alpha=0.5, 
                   legend=pair[0][1:].capitalize())
            p.quad(top=y2, bottom=((str(year),0),)*len(y2), left=edges[:-1], right=edges[1:],
                   fill_color=palette2[9-i], line_color=palette2[9-i], alpha=0.5, 
                   legend=pair[1][1:].capitalize())
         #  print('Sum: hist',np.sum(hist),'hist2',np.sum(hist2))
         #   print('Max: hist',np.max(hist)*1000,'hist2',np.max(hist2)*1000)
            #p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend="PDF")
            #p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")
        
            #p.y_range.start = 0
            #p.legend.location = "center_right"
            #p.legend.background_fill_color = "#fefefe"
        
        
        
        #layout = p
        show(p)

plotHistoRidges([[' nuclear',' wind'],[' nuclear',' coal'],[' ccgt',' wind']])