# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:32:16 2019

@author: Chris
"""

import numpy as np
import pandas as pd

from bokeh.io import output_file, show, output_notebook, curdoc, push_notebook
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import HoverTool, Slider,ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, CrosshairTool, DatetimeTickFormatter, Range1d
from bokeh.layouts import column, row, gridplot, layout
from bokeh.models.widgets import Div
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
import paras
import writeLFdata
###########################################################################
# Creates hex plot
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

# If LF.csv is not in directory, make it and save it in directory
try:
    df = pd.read_csv('LF.csv')
    df.drop('Unnamed: 0',inplace=True, axis=1)
except:
    print('File LF.csv not found. Creating file\nThis may take a few minutes')
    df = writeLFdata.makecsv()

#if panels.output_folder != None:
#    output_file(panels.output_folder+"loadFollowingHex"+nowtime()+".html")

zlist = ['Nuclear','Coal','Hydro','Wind','CCGT','Biomass','Pumped','French_ICT']
ylist = [' '+z.lower()+str(2) for z in zlist]

# Make grid of plots ########################
figList = []
for y,year in enumerate(df['Year'].unique()):
    print(year)
    dfSubset = df[df['Year']==year]
    for i,source in enumerate(ylist):
        a = figure(title=zlist[i] + ' '+str(year), 
                   background_fill_color='#440154',
                   toolbar_location=None)
        a.grid.visible=False
        a.xaxis.major_tick_line_color = None 
        a.xaxis.minor_tick_line_color = None  
        a.yaxis.major_tick_line_color = None 
        a.yaxis.minor_tick_line_color = None 
        a.xaxis.major_label_text_font_size = '0pt'  
        a.yaxis.major_label_text_font_size = '0pt' 
        bins = hexbin(dfSubset[' demand2'],#[:10000],
                      dfSubset[source],#[:10000],
                      size=0.01)
        a.hex_tile(q="q", r="r", size=0.01, line_color=None, source=bins[1:],
           fill_color=linear_cmap('counts', 'Viridis256', 
                                  0, np.percentile(bins.counts,98)))
        # Adjust so that if source has zero output it still shows on plot
        if dfSubset[source].mean()==0:
            a.y_range.update()#Range1d(0,newMax))
            a.y_range.start=-0.01
            a.y_range.end=1

        if y == 0:
            figList.append([a])
        else:
            figList[i].append(a)

# Make example plot - Copy of code above #############################
b = figure(title='Wind 2015', 
                   plot_height=220, 
                   plot_width=220,
                   match_aspect=True, 
                   background_fill_color='#440154',
                   toolbar_location=None)
b.title.offset=0
b.min_border=0
b.sizing_mode='scale_both'
b.grid.visible=False
b.xaxis.major_tick_line_color = None 
b.xaxis.minor_tick_line_color = None  
b.yaxis.major_tick_line_color = None 
b.yaxis.minor_tick_line_color = None 
b.xaxis.axis_label = 'Min         Demand         Max'
b.yaxis.axis_label = 'Min        Wind          Max'
b.xaxis.axis_label_text_font_style = "bold"
b.yaxis.axis_label_text_font_style = "bold"
b.xaxis.major_label_text_font_size = '0pt'  
b.yaxis.major_label_text_font_size = '0pt'  
dfSubset = df[df['Year']==2015]
bins = hexbin(dfSubset[' demand2'],
              dfSubset[' wind2'],
              size=0.01)
b.hex_tile(q="q", r="r", size=0.01, line_color=None, source=bins[1:],
   fill_color=linear_cmap('counts', 'Viridis256', 
                          0, np.percentile(bins.counts,98)))

# Layout ###############################################################
# Show example plot:
#show(b)    
space = Div(text="",width=100, height=100)
grid1 = gridplot(children=figList, 
                           toolbar_location=None,
                           plot_width=120,
                           plot_height=120)
layout = layout([[paras.LFP,space,b],
                [grid1]])
#show(layout)