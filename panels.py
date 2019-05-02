# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:15:26 2019

@author: Chris
"""

from bokeh.models import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure
import allTheSquiggles
import tidalvwind
import twinRidgePlot
import govtDataPlot

from bokeh.io import curdoc
from bokeh.layouts import column,row

#output_file("C:/Users/Chris/Documents/Documents/Python2018/DataVisCW/Plots/panels"+nowtime()+".html")



tab1 = Panel(child=allTheSquiggles.layout, title='Squiggles')
tab2 = Panel(child=twinRidgePlot.layout, title='Ridges')
tab3 = Panel(child = govtDataPlot.layout, title = 'Trends')
tab4 = Panel(child = tidalvwind.layout, title = 'Tidal v wind')

tabs = Tabs(tabs=[tab1,tab2,tab3,tab4])

curdoc().add_root(tabs)