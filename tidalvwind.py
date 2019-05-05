# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:37:19 2019

@author: Chris
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import plotly.plotly as py
import plotly.graph_objs as go
from ipywidgets import interact

from bokeh.io import output_file, show, output_notebook, curdoc, push_notebook
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, \
Legend, DatetimeTickFormatter, CrosshairTool
from bokeh.models.widgets import Select, Tabs, Panel, Slider, TextInput, DateRangeSlider, RangeSlider
from bokeh.models.glyphs import VBar
from bokeh.layouts import column, row
from bokeh.palettes import Category10, Category20, Inferno
import colorcet as cc
import seaborn as sns
from numpy import linspace
from scipy.stats.kde import gaussian_kde
import panels

import datetime
#%load_ext blackcellmagic
#%matplotlib inline


startDate = datetime.datetime(2019,3,9)
endDate = datetime.datetime(2019,4,10)
tidaldf = pd.DataFrame({'DateTime':pd.date_range(start=startDate,
                                          end = endDate,
                                          freq='0.5H',
                                         normalize=True)})

hrsIn1yr = 365*24
annualOutputQuoted = 572e9 # GWh
avgPowerQuoted = annualOutputQuoted/hrsIn1yr
avgPowerQuoted
avgPowerExpected = 36e6 # W
offshoreLF = 0.39
onshoreLF = 0.27
offshoreWindCapNeeded = avgPowerExpected / offshoreLF
offshoreWindCapNeeded/1e6
no7MWturbinesNeeded = offshoreWindCapNeeded/7e6 # The three UK offshore wind projects in construction have 7MW turbines - renewableuk.com
no7MWturbinesNeeded
genHrsPerDay = 12
powerWhenGenerating = avgPowerExpected*24/genHrsPerDay
powerWhenGenerating/1e6

tidaldf['Quantity (MW)'] = np.where((tidaldf.index%12) <(genHrsPerDay/2),
                            powerWhenGenerating/1e6,0)


######## WIND DATA ############################################

dudgDict, sherDict, burbDict={},{},{}

for i in range(1,97):
    df = pd.read_csv('windData/B1610 ('+str(i)+').csv',skiprows=1)
    newdf = df.groupby(['SP','Settlement Date']).sum()
    newdf['DateTime'] = pd.date_range(start=newdf.index[0][1],
                                          periods=len(newdf),
                                          freq='0.5H',
                                         normalize=True)
    if df.iloc[0,3][:5] == 'DDGNO':
        dudgDict[str(i)] = newdf
    elif df.iloc[0,3][:5] == 'SHRSO':
        sherDict[str(i)] = newdf
    elif df.iloc[0,3][:5] == 'BRBEO':
        burbDict[str(i)] = newdf
    else:
        print(df.iloc[0,3][:5],'not DDGNO or SHRSO')


dudgdf = pd.concat(dudgDict)
dudgdf.reset_index(inplace=True)
dudgdf.drop('level_0', axis=1, inplace=True)
dudgdf.sort_values(by='DateTime',axis=0, inplace=True)

sherdf = pd.concat(sherDict)
sherdf.reset_index(inplace=True)
sherdf.drop('level_0', axis=1, inplace=True)
sherdf.sort_values(by='DateTime',axis=0, inplace=True)
#sherdf

burbdf = pd.concat(burbDict)
burbdf.reset_index(inplace=True)
burbdf.drop('level_0', axis=1, inplace=True)
burbdf.sort_values(by='DateTime',axis=0, inplace=True)



def makeDateSubset(df, startDate = startDate, endDate = endDate):
    df1 = df.copy()
    return df1[(df1['DateTime']>startDate) & (df1['DateTime']<=endDate)].copy()

def calcEnergy(df, col = 'Quantity (MW)'):
    ''' Input = whole df.
    Takes subset, adds col and calculates energy in subset '''
    df2 = makeDateSubset(df)
    df2['Energy (GWh)'] = df2[col] * 0.5 * 1e-3
    return df2['Energy (GWh)'].sum()


dudgdf2 = dudgdf.rename(columns={'Quantity (MW)':'dudg'})
sherdf2 = sherdf.rename(columns={'Quantity (MW)':'sher'})
burbdf2 = burbdf.rename(columns={'Quantity (MW)':'burb'})
tidaldf2 = tidaldf.rename(columns={'Quantity (MW)':'tidal'})
condf = pd.merge(tidaldf2,sherdf2,how='outer',on='DateTime', )
condf.sort_values(by='DateTime',axis=0, inplace=True)
condf = pd.merge(condf,burbdf2, how='outer',on='DateTime')
condf.sort_values(by='DateTime',axis=0, inplace=True)
condf = pd.merge(condf,dudgdf2, how='outer', on='DateTime')
condf.sort_values(by='DateTime',axis=0, inplace=True)
condf.drop(['SP_x', 'Settlement Date_x', 'SP_y','Settlement Date_y', 'SP', 'Settlement Date'],inplace=True,axis=1)



########### PLOT ###############################################

# Plot demand IN ONE WEEK with Bokeh

ylist=['tidal','dudg','sher','burb']
if panels.output_folder != None:
    output_file(panels.output_folder+nowtime()+".html")
fig = figure(plot_width=600, plot_height=550,
             title='Power at 30min intervals, MW',
            x_axis_type='datetime', toolbar_location="above",
            tools='wheel_zoom,pan,reset',
            active_scroll='wheel_zoom')
fig.toolbar.logo=None
barfig = figure(plot_width=300, plot_height=550,
             title='Electricity generated in period, GWh',
             toolbar_location=None,
               x_range=ylist)

# Initial values
timeRange=10
startDay = 7

global dataSource
dataSource = ColumnDataSource(condf)

def updateLineCDS(startDay=startDay, timeRange=timeRange):
    global start
    global end
    start = startDate + datetime.timedelta(days=startDay)
    end = start + datetime.timedelta(days=timeRange)
    dataSource.data.update(ColumnDataSource(
            data=makeDateSubset(condf, startDate=start, endDate=end)).data)

updateLineCDS()

y,colorList= [],[]

for colRef,bar in enumerate(ylist,1):
    y.append(calcEnergy(condf,bar))
    colorList.append(Category10[(len(ylist)+2)][colRef])
    
barDict = dict(x=ylist, top=y, col = colorList,
               names=['Tidal','Dudgeon','Sheringham\n Shoal','Burbo Bank\n Extension'])

barDS = ColumnDataSource((barDict))


for colRef,line in enumerate(ylist,1):
    lines = fig.line(x='DateTime', y=line, source=dataSource, 
                 color = Category10[(len(ylist)+2)][colRef],
                line_width=2) 

bars = VBar(x='x', top='top',width=0.5,
            line_color='col',
           fill_color='col',
           name='names')
barfig.add_glyph(barDS, bars)

fig.outline_line_color = None
fig.background_fill_color = "#efefef"

fig.xaxis.formatter = DatetimeTickFormatter(days = [ '%a%e-%b'])
fig.xaxis.minor_tick_line_color = 'black'

#fig.axis.major_tick_line_color = None
fig.axis.axis_line_color = 'black'
fig.y_range.start=0
barfig.y_range.start=0
#fig.yaxis.axis_label = 'Total electricity supplied in Quarter (TWh)'

numDays = (endDate-startDate).days

def updateBarCDS(start,end):
    y=[]
    for bar in ylist:
        y.append(calcEnergy(makeDateSubset(condf, startDate=start, endDate=end),bar))
    barDict = dict(x=ylist, top=y,col = colorList)
    barDS.data.update(ColumnDataSource(data=barDict).data)



startDaySlider = Slider(start=1, end=numDays-7, value=timeRange,
     step=1, title='Start day')
def startDayCallback(attr, old, new):
    global startDay 
    startDay = startDaySlider.value
    updateLineCDS(startDay=startDay, timeRange=timeRange)
    updateBarCDS(start,end)
startDaySlider.on_change('value', startDayCallback)

dateRangeSlider = Slider(start=7, end=numDays, value=startDay,
     step=1, title='Time window')
def dateRangeCallback(attr, old, new):
    global timeRange
    timeRange = dateRangeSlider.value
    updateLineCDS(startDay=startDay, timeRange=timeRange)
    updateBarCDS(start,end)
dateRangeSlider.on_change('value', dateRangeCallback)

layout = column(startDaySlider, dateRangeSlider, row(fig,barfig))
#curdoc().add_root(layout)
#show(layout)

