# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:15:26 2019

@author: Chris
"""

from bokeh.models import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure
import gridwatchLinePlot
import tidalvwind
import twinRidgePlot
import govtDataPlot
import loadFollowingHex
import paras

from bokeh.io import curdoc
from bokeh.layouts import column,row
output_folder="C:/Users/Chris/Documents/Documents/Python2018/DataVisCW/Plots"

##  Define the layout of the overall bokeh output #########################

tab0 = Panel(child= paras.introP,
             title = 'Info')

tab1 = Panel(child=column(paras.squiggleP,
                          gridwatchLinePlot.layout),
             title='Explore the data')
tab2 = Panel(child=column(paras.ridgeP,
                          twinRidgePlot.layout), 
             title='Nuclear vs Wind')
tab3 = Panel(child = column(paras.govtP,
                            govtDataPlot.layout,
                            row(paras.govtPb,
                                paras.gap,
                                paras.govtPc)), 
             title = 'Trends')
tab4 = Panel(child = column(paras.tidalvwindP,
                            tidalvwind.layout), 
             title = 'Tidal vs wind')

tab5 = Panel(child = loadFollowingHex.layout, 
             title = 'Load Following')

tabs = Tabs(tabs=[tab0,tab1,tab2,tab3,tab4, tab5])

curdoc().add_root(tabs)
#show(tabs)
