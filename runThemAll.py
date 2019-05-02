# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:28:18 2019

@author: Chris
"""

import allTheSquiggles
import tidalvwind
import twinRidgePlot
import govtDataPlot

from bokeh.io import curdoc
from bokeh.layouts import column,row

#squigglesLayout = row(column(allTheSquiggles.slider,
#                             allTheSquiggles.radio,
#                             allTheSquiggles.checkbuttons,
#                             allTheSquiggles.axisButton), allTheSquiggles.fig)
#
#tidalvwindLayout = column(tidalvwind.startDaySlider, 
#                          tidalvwind.dateRangeSlider, 
#                          row(tidalvwind.fig,
#                              tidalvwind.barfig))

allLayout = column(allTheSquiggles.layout,
                   twinRidgePlot.layout,
                   govtDataPlot.layout,
                   tidalvwind.layout)
curdoc().add_root(allLayout)
