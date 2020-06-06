# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:02:42 2019

@author: Chris
"""

import numpy as np
import pandas as pd
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource, Select,FixedTicker, PrintfTickFormatter, \
Legend, DatetimeTickFormatter, CrosshairTool, LabelSet, Label,NumeralTickFormatter
from bokeh.models.widgets import Select, Tabs, Panel, Slider, TextInput, DateRangeSlider, RangeSlider
import colorcet as cc
from numpy import linspace
import datetime

### Make twin ridge plot - nuclear & wind histograms #####################

# Prepare the data
data12 = pd.read_csv('gridwatch.csv', index_col=1,skip_blank_lines=True, header=[0], parse_dates=True)
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

#if panels.output_folder != None:
#    output_file=(panels.output_folder+"/twinridgeplot"+nowtime()+".html")

def ridge(category, data, scale=800):
    return list(zip([category]*len(data), scale*data))

# Prepare for ridge plot
years = data122['Year'].unique()
print(len(cc.coolwarm))
print(len(years))
lim1 = int(255-(len(years)*10))
lim2 = int(10*len(years))
palette1 =[cc.coolwarm[i*10+lim1] for i in range(len(years)+1)]
palette2 =[cc.coolwarm[lim2-i*10] for i in range(len(years)+1)]
xmin,xmax,num = 0,max(data122[[' nuclear',' wind']].max()),500
x = linspace(xmin,xmax,num)
xnew = list(x)
xnew.insert(0,xmin - (xmax-xmin)/num)
xnew.append(xmax + (xmax-xmin)/num)

# Set up figure
p = figure(plot_width=900,y_range=[str(year) for year in reversed(years)], 
            x_range=(-5, xmax),#,toolbar_location=None)
           title = 'Histogram showing power output for each 5min interval throughout the year',
           tools='pan,box_zoom,box_zoom,wheel_zoom,reset',
           active_drag='box_zoom')

p.toolbar.logo=None
p.xaxis.axis_label = 'Power output (MW)'
p.outline_line_color = None
p.background_fill_color = "#efefef"
p.xaxis.ticker = FixedTicker(ticks=list(range(0, xmax,1000)))
p.ygrid.grid_line_color = None
p.xgrid.grid_line_color = "#dddddd"
p.xgrid.ticker = p.xaxis[0].ticker
p.axis.minor_tick_line_color = None
p.axis.major_tick_line_color = None
p.axis.axis_line_color = None
p.xaxis.formatter=NumeralTickFormatter(format="0,000")
p.xaxis.axis_label_text_font_style = "bold"
p.yaxis.axis_label_text_font_style = "bold"
p.xaxis.major_label_text_font_size = '12pt'
p.yaxis.major_label_text_font_size = '10pt' 
p.y_range.range_padding = 0.1

# Make the histograms and plot for nuclear and wind for each year
for i, year in enumerate(reversed(years)):
    print(i)
    hist, edges = np.histogram(data122[data122['Year']==year].loc[:,' nuclear'].reset_index(drop=True),
                               density=True, bins=200, range=(0,xmax))
    hist2, edges2 = np.histogram(data122[data122['Year']==year].loc[:,' wind'].reset_index(drop=True),
                               density=True, bins=200, range=(0,xmax))
    scaler = 1/ (1000*np.max([np.max(hist),np.max(hist2)]))
    y = ridge(str(year), hist)#*scaler)
    y2 = ridge(str(year), hist2)#*scaler)

    p.quad(top=y, bottom=((str(year),0),)*len(y), left=edges[:-1], right=edges[1:],
           fill_color=palette1[9-i], line_color=palette1[9-i], alpha=0.5, legend='Nuclear')
    p.quad(top=y2, bottom=((str(year),0),)*len(y2), left=edges[:-1], right=edges[1:],
           fill_color=palette2[9-i], line_color=palette2[9-i], alpha=0.5, legend='Wind')


#label=Label(x=9500, y=6.5, x_units='data', 
#            text='Maximum nuclear generation\n9.4GW', 
#            render_mode='css')
      #border_line_color='black', border_line_alpha=1.0,
      #background_fill_color='white', background_fill_alpha=0.3)
#p.add_layout(label)
layout = p
#show(p)
