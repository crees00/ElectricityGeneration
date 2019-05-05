# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:27:19 2019

@author: Chris
"""
# netstat -a -o -n

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

data161 = getData.data161.copy()


# Plot demand IN ONE DAY/WEEK/MONTH with Bokeh

dataLength = 'week'
#if panels.output_folder != None:
#    output_file(panels.output_folder+"/AllTheSquiggles"+nowtime()+".html")
fig = figure(plot_width=800, plot_height=500,
             title='UK electricity sources and demand, recorded at 5min intervals',
            x_axis_type='datetime', toolbar_location="above",
            tools='wheel_zoom,pan,box_zoom,reset',
            active_drag='box_zoom')
fig.toolbar.logo=None
pts = len(data161)


daySlot = 24*12 # number of data points (5min periods) in 24hrs
weekSlot = 7*daySlot
monthSlot = 30*daySlot

lastDay = datetime.datetime(2019,(data161['Month']).iloc[pts-1],(data161['Day']).iloc[pts-1]-1)
print(lastDay)
rangeEnd = pts-monthSlot

def updateToolTips(dataLength=dataLength):
    tooltips = []#('Demand','@{ demand}{( 0,0)}MW')]
    if dataLength == 'month':
        slot, space = monthSlot, 1
        tooltips.insert(0,('Time','@{ timestamp}{%H:%M}'))
        tooltips.insert(1,('Date','@{ timestamp}{%a %e-%b}'))
    elif dataLength == 'week':
        slot,space = weekSlot, 1
        tooltips.insert(0,('Time','@{ timestamp}{%H:%M}'))
        tooltips.insert(1,('Date','@{ timestamp}{%a %e-%b}'))
    elif dataLength == 'day':
        slot,space = daySlot, 1
        tooltips.insert(0,('Time','@{ timestamp}{%H:%M}'))
    return tooltips, slot, space

tooltips,slot,space = updateToolTips()
dataSource = ColumnDataSource(data161.iloc[-slot::space,:])

# Choose columns to have as options in the plot
zlist = ['Demand','Nuclear','Wind','Coal','CCGT','Solar','Pumped','Hydro',
         'Biomass','Oil','French_ICT'] 
ylist = [' '+z.lower() for z in zlist]
showcols = ylist[:3]
dictOfLines={}

# Plot ALL of the lines and put in dictionary to set their visibility on update
for colRef,line in enumerate(ylist,1):
    if line in dataSource.column_names:
        lines = fig.line(x=' timestamp', y=line, source=dataSource, 
                         color = Category20[(len(ylist)+2)][colRef],
                        line_width=2) 
        dictOfLines[line]=lines
        #legend.append((str(ylist[colRef-1])+' ',[lines]))
        tips2 = [(zlist[colRef-1],'@{'+line+'}{( 0,0)}MW')]
        if line == ' demand':
            tips2 = list(set(tips2+tooltips))
        hover2 = HoverTool(tooltips =tips2, 
                          formatters={' timestamp': 'datetime'},
                          renderers=[lines], toggleable=False,
                         mode='vline')
        fig.add_tools(hover2)
        if line in showcols:
            dictOfLines[line].visible = True
        else:
            dictOfLines[line].visible = False
        
startPt = rangeEnd

def update(Demand, Nuclear, Wind, Coal, CCGT, Solar, French_ICT,timerange='month',startPt=rangeEnd):
    tooltips,slot,space = updateToolTips(timerange)
    showcols=[]
   # print(locals())
    newMax=0
    data161subset = data161.iloc[startPt:startPt+slot:space,:]
    for colname in zlist:
        if (colname in locals().keys())and locals()[colname]==True:
       #     print(colname, locDict161[colname])
            showcols.append(' '+colname.lower())
            if data161subset[showcols[-1]].max() > newMax:
                newMax = data161subset[showcols[-1]].max()
     
    dataSource.data.update(ColumnDataSource(data161subset).data)
   # print(newMax)
    for colRef,line in enumerate(ylist,1):
        if line in dataSource.column_names:
            if line in showcols:
                dictOfLines[line].visible = True
            else:
                dictOfLines[line].visible = False
    fig.y_range.update()#Range1d(0,newMax))
    fig.y_range.start=0
    fig.y_range.end=1000*newMax//1000+1000

fig.add_tools(CrosshairTool(dimensions='height'))  
fig.outline_line_color = None
fig.background_fill_color = "#efefef"


fig.y_range=Range1d(0, data161.iloc[-slot::space,:][' demand'].max())

fig.xaxis.minor_tick_line_color = 'black'
fig.xaxis.formatter = DatetimeTickFormatter(days = [ '%a %e-%b %Y'], hours=['%R'])

#fig.axis.major_tick_line_color = None
fig.axis.axis_line_color = 'black'
#fig.yaxis.axis_label = 'Total electricity supplied in Quarter (TWh)'



# Slider to change time window shown 
slider = Slider(start=1, end=rangeEnd, value=rangeEnd,
     step=daySlot, title='Date selection', show_value=False)
def callback(attr, old, new):
     global startPt
     startPt = slider.value
     print(startPt)
     data161subset = data161.iloc[startPt:startPt+slot:space,:]
     dataSource.data.update(ColumnDataSource(data161subset).data)
slider.on_change('value', callback)

# Radio buttons to choose time scale
radioLabels = ['day','week','month']
radio = RadioGroup(labels=radioLabels,active=1)
def radioCallback(active):
    timerange = radioLabels[active]
    print(timerange)
    global slot
    global space
    tooltips,slot, space = updateToolTips(timerange)
    data161subset = data161.iloc[startPt:startPt+slot:space,:]
    dataSource.data.update(ColumnDataSource(data161subset).data)
radio.on_click(radioCallback)

# Buttons to choose which sources are shown
checkbuttons = CheckboxButtonGroup(labels=zlist, active=[0,1,2])
def checkboxCallback(active):
    global showcols
    showcols=[]
    print(active)
    for activeItem in active:
        showcols.append(' '+zlist[activeItem].lower())
    print(showcols)
    for colRef,line in enumerate(ylist,1):
        if line in showcols:
            dictOfLines[line].visible = True
        else:
            dictOfLines[line].visible = False
checkbuttons.on_click(checkboxCallback)

# Button to update axis
axisButton = Button(label='Update y-axis', button_type='primary')
def updateAxis():
    newMax=0
    data161subset = data161.iloc[startPt:startPt+slot:space,:]
    for colname in showcols:
        print(colname)
        if data161subset[colname].max() > newMax:
            newMax = data161subset[colname].max()
        print(newMax)
    print(newMax)
    fig.y_range.update()#Range1d(0,newMax))
    fig.y_range.start=0
    fig.y_range.end=1000*newMax//1000+1000
axisButton.on_click(updateAxis)

    
# Arrange plots and widgets in layouts
layout = row(column(slider,radio,checkbuttons,axisButton), fig)
#curdoc().add_root(layout)
