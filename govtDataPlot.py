# -*- coding: utf-8 -*-
"""
Created on Wed May  1 12:46:49 2019

@author: Chris
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.io import output_file, show, output_notebook, curdoc
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, Legend, CrosshairTool
from bokeh.models.widgets import Select
from bokeh.models import CheckboxGroup, RadioGroup, Toggle, CheckboxButtonGroup, Button
from bokeh.layouts import column, row
from bokeh.palettes import Category10, Category20, Inferno
import colorcet as cc
import seaborn as sns
from numpy import linspace
from scipy.stats.kde import gaussian_kde
import panels

import datetime

# Read in data to get supply values from different electricity sources ############
data4 = pd.read_csv('5.1SuppliedQuarterly.csv', index_col=0, parse_dates=True, skiprows=4, header=[0,1])
data4.drop('Year',1, level=0,inplace=True)
data4.dropna(axis=1, thresh=1, inplace=True)

data5 = data4.transpose()
data5.index.set_names(['Year','Quarter'])

data51 = data5.reset_index()
data51
data51['Year'] = data51.apply(lambda row: int(row['level_0']), axis=1)
data51['Quarter'] = data51.apply(lambda row: int(str(row['level_1'])[0]), axis=1)
data51['Date'] = data51.apply(lambda row: datetime.datetime(row['Year'],(3*(row['Quarter'])-2),1), axis=1)

data52 = data51.drop('- of which, Offshore',axis=1)
otherCols = ['Oil','Hydro (natural flow) ','Bioenergy',
             'Pumped storage (net supply)', 'Other fuels','Net imports']
data52['All other'] = data52[otherCols].sum(axis=1)

# Read in data to get demand values ########################################
# 5.2 has units of GWh
data6 = pd.read_csv('5.2SupplyVsDemandQuarterly.csv', index_col=0, parse_dates=True, skiprows=3, header=[0,1], skip_blank_lines=True)
data6.drop('Supply',0, inplace=True)
data6.dropna(axis=1, thresh=1, inplace=True)
data6.dropna(axis=0, thresh=1, inplace=True)

data61 = data6.transpose()
data61 = data61['Total demand'].reset_index().copy()
data61['Quarter'] = data61.apply(lambda row: int(str(row['level_1'])[0]), axis=1)
data61['Date'] = data61.apply(lambda row: datetime.datetime(int(row['Year']),(3*(row['Quarter'])-2),1), axis=1)
data61['Demand'] = data61['Total demand']/1000

# Merge two into one dataFrame ##############################################
sourcesAndDemand = pd.merge(data52,data61.drop(['Year','level_1','Quarter','Total demand'],axis=1),how='outer',on='Date')
sourcesAndDemand
sourcesAndDemand.rename(index=str, 
                        columns={'Total all generating companies':'Total generated'},
                        inplace=True)

# Calculate output from Hinkley Point C #####################################
HPCpower = 3.26e9 * 0.9 # W assuming 90% capacity factor
secsInQuarter = 60*60*24*365.25/4
HPCjoulesInQuarter = HPCpower * secsInQuarter 
HPCTWhInQuarter = HPCjoulesInQuarter / (3600*1e12)
print(HPCTWhInQuarter)
sourcesAndDemand['Nuclear with HPC'] = sourcesAndDemand['Nuclear'] + HPCTWhInQuarter

# Calculate output from tidal lagoon #########################################
# Assume 36MW average power from tidal lagoon
lagoonPower = 36e6
lagoonTWhInQuarter = lagoonPower * secsInQuarter / (3600*1e12)
print(lagoonTWhInQuarter)
sourcesAndDemand['All other - including lagoon'] = sourcesAndDemand['All other']+lagoonTWhInQuarter

ylist = list(set(sourcesAndDemand.columns)-set(['level_0', 'level_1', 
       'Year', 'Quarter', 'Date'])-set(otherCols))
#zlist = [item[1:].lower() for item in ylist]

showcols = ['Demand','Nuclear','Wind and Solar']


def nowtime():
    now=datetime.datetime.now()
    return "".join([str(i) for i in (now.day,0,now.month,now.year,now.hour,now.minute)])



# Now have energy sources plus demand - time to plot them ###########################################

if panels.output_folder != None:
    output_file(panels.output_folder+"/SourcesDemandLine"+nowtime()+".html")
fig = figure(plot_width=700, plot_height=500,
             title='Total electricity demand/supply each quarter since 1998, TWh',
            x_axis_type='datetime', toolbar_location="above",
            tools='pan,box_zoom,wheel_zoom,reset',
            active_scroll='wheel_zoom')
fig.toolbar.logo=None
dataSource = ColumnDataSource(sourcesAndDemand)

legend=[]
dictOfLines={}

def showLines(showcols = showcols):
    for line in ylist:
        if line in showcols:
            dictOfLines[line].visible = True
        else:
            dictOfLines[line].visible = False

for colRef,line in enumerate(ylist,1):
    lines = fig.line(x='Date', y=line, source=dataSource, 
                     color = Category20[(len(ylist)+1)][colRef],
                    line_width=3) 
    dictOfLines[line]=lines
    legend.append((str(ylist[colRef-1])+' ',[lines]))
    hover = HoverTool(tooltips =[(ylist[colRef-1],'@{'+line+'}{( 0,0)} TWh')], 
                                 renderers=[lines], toggleable=False, 
                                 mode='vline')
    fig.add_tools(hover)
    #tips2 = 
    #hover2 = HoverTool(tooltips =tips2, 
     #                     formatters={' timestamp': 'datetime'},
    #                      renderers=[lines], toggleable=False,
    #                     mode='vline')
    #    fig.add_tools(hover2)
#    if line in showcols:
#        dictOfLines[line].visible = True
#    else:
#        dictOfLines[line].visible = False
showLines()        
    
#legend = Legend(items=legend, location='center')
#fig.add_layout(legend, 'right')
#fig.legend.click_policy="hide"
fig.add_tools(CrosshairTool(dimensions='height'))  

fig.outline_line_color = None
fig.background_fill_color = "#efefef"

fig.xaxis.minor_tick_line_color = 'black'

#fig.axis.major_tick_line_color = None
fig.axis.axis_line_color = 'black'
fig.yaxis.axis_label = 'Total electricity Demand/Supply in Quarter (TWh)'
fig.y_range.start=0
fig.xaxis[0].ticker.desired_num_ticks = 10
fig.yaxis.axis_label_text_font_style = "bold"


lagoon, HPC = False,False
ylistb = list(set(ylist)-set(['Nuclear with HPC','All other - including lagoon']))
showrefs = [ylistb.index(item) for item in showcols]
checkbuttons = CheckboxButtonGroup(labels=ylistb, active=showrefs,
                                   button_type = 'default')
def checkboxCallback(active):
    global showcols
    showcols=[]
    print(active)
    for activeItem in active:
        showcols.append(ylistb[activeItem])
    if 'Nuclear' not in showcols:
        try: showcols.remove('Nuclear with HPC')
        except: None
    elif HPC and ('Nuclear with HPC' not in showcols):
        showcols.append('Nuclear with HPC')
    
    if 'All other' not in showcols:
        try: showcols.remove('All other - including lagoon')
        except: None
    elif lagoon and ('All other - including lagoon' not in showcols):
        showcols.append('All other - including lagoon')
    
    showLines(showcols)

checkbuttons.on_click(checkboxCallback)


HPCButton = Toggle(label='Add Hinkley Point C', button_type = 'default')
def addHPC(clicked):
    global HPC
    HPC = clicked
    if HPC and ('Nuclear' not in showcols):
        showcols.append('Nuclear')
    if HPC:
        showcols.append('Nuclear with HPC')
        HPCButton.button_type='success'
    elif 'Nuclear with HPC' in showcols:
        showcols.remove('Nuclear with HPC')
    if not HPC:
        HPCButton.button_type = 'default'
    showLines(showcols)
HPCButton.on_click(addHPC)

lagoonButton = Toggle(label = 'Add tidal lagoon', button_type = 'default')
def addLagoon(clicked):
    global lagoon
    lagoon = clicked
    if clicked:
        lagoonButton.button_type = 'success'
        if 'All other' not in showcols:
            showcols.append('All other')
        showcols.append('All other - including lagoon')
    else:
        lagoonButton.button_type = 'default'
        try: showcols.remove('All other - including lagoon')
        except: None
    showLines(showcols)
lagoonButton.on_click(addLagoon)
    
axisButton = Button(label='Update y-axis', button_type = 'primary')
def updateAxis():
    newMax=0
    for colname in showcols:
        print(colname)
        if sourcesAndDemand[colname].max() > newMax:
            newMax = sourcesAndDemand[colname].max()
        print(newMax)
    print(newMax)
    fig.y_range.update()#Range1d(0,newMax))
    fig.y_range.start=0
    fig.y_range.end=10*newMax//10+10
axisButton.on_click(updateAxis)


layout=row(column(checkbuttons,HPCButton, lagoonButton,axisButton),fig)
#curdoc().add_root(layout)
#show(layout)