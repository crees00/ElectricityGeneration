# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:37:19 2019

@author: Chris
"""

import numpy as np
import pandas as pd
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, \
Legend, DatetimeTickFormatter, CrosshairTool
from bokeh.models.widgets import Select, Tabs, Panel, Slider, TextInput, DateRangeSlider, RangeSlider
from bokeh.models.glyphs import VBar
from bokeh.layouts import column, row
from bokeh.palettes import Category10, Category20, Inferno
import datetime
#%load_ext blackcellmagic
#%matplotlib inline

# Take in wind data and generate tidal data ################################
# Calculate electricity generation #########################################
# Plot both on linked charts ###############################################

# Range of dates that wind data is for
startDate = datetime.datetime(2019,3,9)
endDate = datetime.datetime(2019,4,10)
tidaldf = pd.DataFrame({'DateTime':pd.date_range(start=startDate,
                                          end = endDate,
                                          freq='0.5H',
                                         normalize=True)})

hrsIn1yr = 365*24
annualOutputQuoted = 572e9 # GWh
avgPowerQuoted = annualOutputQuoted/hrsIn1yr
avgPowerExpected = 36e6 # W
genHrsPerDay = 12
powerWhenGenerating = avgPowerExpected*24/genHrsPerDay
powerWhenGenerating/1e6
# Set tidal lagoon to generate four times per day(24hrs) - in, out, in, out
tidaldf['Quantity (MW)'] = np.where((tidaldf.index%6) <(genHrsPerDay/4),
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

nameList= ['Tidal','Dudgeon',"Sher'm Shoal",'BBE']# To look nice

ylist=['tidal','dudg','sher','burb']# Column names
#if panels.output_folder != None:
#    output_file(panels.output_folder+nowtime()+".html")
fig = figure(plot_width=600, plot_height=550,
             title='Power at 30min intervals, MW',
            x_axis_type='datetime', toolbar_location="above",
            tools='wheel_zoom,box_zoom,pan,reset',
            active_drag='box_zoom')
fig.toolbar.logo=None
barfig = figure(plot_width=300, plot_height=550,
             title='Electricity generated in period, GWh',
             toolbar_location=None,
               x_range=nameList)

# Initial values
timeRange=10
startDay = 7

global dataSource
dataSource = ColumnDataSource(condf)

def updateLineCDS(startDay=startDay, timeRange=timeRange):
    '''When time window is updated, update the CDS for the line chart
    so that the chart updates.
    Called within both callback functions'''
    global start
    global end
    start = startDate + datetime.timedelta(days=startDay)
    end = start + datetime.timedelta(days=timeRange)
    dataSource.data.update(ColumnDataSource(
            data=makeDateSubset(condf, startDate=start, endDate=end)).data)
    
updateLineCDS()

# Calculate energy and make up colorList so that both plots have same colours
y,colorList= [],[]
for colRef,bar in enumerate(ylist,1):
    y.append(calcEnergy(condf,bar))
    colorList.append(Category10[(len(ylist)+2)][colRef])
barDict = dict(x=nameList, top=y, col = colorList,
               names=nameList)

barDS = ColumnDataSource((barDict))

# Initial line plot 
for colRef,line in enumerate(ylist,1):
    lines = fig.line(x='DateTime', y=line, source=dataSource, 
                 color = Category10[(len(ylist)+2)][colRef],
                line_width=2) 
# Initial bar plot
bars = VBar(x='x', top='top',width=0.5,
            line_color='col',
           fill_color='col',
           name='names')
barfig.add_glyph(barDS, bars)

# Adjust line plot
fig.outline_line_color = None
fig.background_fill_color = "#efefef"
fig.xaxis.formatter = DatetimeTickFormatter(days = [ '%a%e-%b'])
fig.xaxis.minor_tick_line_color = 'black'
fig.axis.axis_line_color = 'black'
fig.y_range.start=0
barfig.y_range.start=0

numDays = (endDate-startDate).days

def updateBarCDS(start,end):
    '''When the time window is updated, update the CDS for the bar chart so 
    that the bar chart updates.
    Called within both callback functions'''
    y=[]
    for bar in ylist:
        y.append(calcEnergy(makeDateSubset(condf, startDate=start, endDate=end),bar))
    barDict = dict(x=nameList, top=y,col = colorList)
    barDS.data.update(ColumnDataSource(data=barDict).data)


# Set up widgets - two sliders to adjust the time window
startDaySlider = Slider(start=1, end=numDays-7, value=timeRange,
     step=1, title='Start day')
def startDayCallback(attr, old, new):
    '''Slider to set the first day of the time window shown'''
    global startDay 
    startDay = startDaySlider.value
    updateLineCDS(startDay=startDay, timeRange=timeRange)
    updateBarCDS(start,end)
startDaySlider.on_change('value', startDayCallback)

dateRangeSlider = Slider(start=7, end=numDays, value=startDay,
     step=1, title='Time window')
def dateRangeCallback(attr, old, new):
    '''Slider to set the time range shown i.e. the width of the 
    time window'''
    global timeRange
    timeRange = dateRangeSlider.value
    updateLineCDS(startDay=startDay, timeRange=timeRange)
    updateBarCDS(start,end)
dateRangeSlider.on_change('value', dateRangeCallback)

layout = column(startDaySlider, dateRangeSlider, row(fig,barfig))
#curdoc().add_root(layout)
#show(layout)

