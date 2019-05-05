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
import loadFollowingHex
import paras

from bokeh.io import curdoc
from bokeh.layouts import column,row
global output_folder
output_folder="C:/Users/Chris/Documents/Documents/Python2018/DataVisCW/Plots"
#output_file("C:/Users/Chris/Documents/Documents/Python2018/DataVisCW/Plots/panels"+nowtime()+".html")

tab0 = Panel(child= paras.introP,
             title = 'Intro')

tab1 = Panel(child=column(paras.squiggleP,
                          allTheSquiggles.layout),
             title='High res data')
tab2 = Panel(child=column(paras.ridgeP,
                          twinRidgePlot.layout), 
             title='Ridges')
tab3 = Panel(child = column(paras.govtP,
                            govtDataPlot.layout,
                            paras.govtPb), 
             title = 'Trends')
tab4 = Panel(child = column(paras.tidalvwindP,
                            tidalvwind.layout), 
             title = 'Tidal v wind')

tab5 = Panel(child = loadFollowingHex.layout, 
             title = 'Load Following')

tabs = Tabs(tabs=[tab0,tab1,tab2,tab3,tab4, tab5])

curdoc().add_root(tabs)
#show(tabs)
