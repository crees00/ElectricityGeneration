# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:37:50 2019

@author: Chris
"""

from bokeh.io import output_file, show
from bokeh.models.widgets import Paragraph, Div, PreText

#output_file("div.html")


para0 = """
<br>
This project shows where the electricity in the UK comes from. The data has been acquired from publicly available online sources, then processed and presented here.
<br><br>
The project aims to provide some real data showing the underlying trends in our electricity supply, with the opportunity to investigate for yourself. The project also aims to show the effects of two different new electricity generation projects: Hinkley Point C nuclear power station and the Swansea Bay Tidal Lagoon.
<br><br>
Hinkley Point C is a major new build project in North Somerset. It is being undertaken by the French nuclear power company EDF, with some of the investment from China, to a total cost of around £20bn. This huge expense is being recouped through the UK government paying an agreed price for each unit of electricity generated (the 'strike price'). The plant is currently being built, expected to be operational in 2025.
<br><br>
Swansea Bay Tidal Lagoon is a proposed project that has been awaiting approval for many years. The project plans to build a large sea wall enclosing an area of Swansea Bay, creating a 'lagoon'. The lagoon is connected to the sea via some large turbines which generate electricity. When the tide comes in, the seawater flows through the turbines, filling up the lagoon. When the tide goes out, the lagoon empties, again spinning the turbines. It has widespread support in the Swansea area due to its construction providing significant work for the local people and its assumed green credentials. 
<br><br>
Units
<br><br>





Now it's your turn - click the tabs at the top to explore the data for yourself


 
"""

para1 = """
<br>Data have been recorded for the past eight years, showing the power output of the different sources of electricity in the UK, as well as the total demand. 
<br><br>These measurements have been taken at five minute intervals. The data are plotted below with a selection of tools to inspect further.
<br><br> Press the buttons to the side, as well as rolling over the plot itself.
<br><br><br><br>
"""

para2 = """
This plot shows histograms of the power output for wind and nuclear over the years. They are on the same scales, so each block of the same height indicates the same amount of time generating exactly that amount of power.
<br><br>
Some key trends:
<br><br>
- Wind power capacity has increased from below 3.5GW to over
12GW
<br>
- Nuclear power generation is in general decline
<br>
- Nuclear power generation is far more consistent - over the last few years, it can be predicted relatively accurately within a 2GW range
<br>
- Wind generation is spread evenly over a large range
<br> 
- Nuclear power generation has hardly ever dipped below 5GW in the last 8 years
<br><br><br><br>
"""

para3 = """
Here is the government's data for electricity generated since 1998. It gives the totals for each quarter, providing some smoothing to the graph.
<br><br>
Choose the sources you'd like to see using the buttons
<br><br>
See what the nuclear generation would have been if Hinkley Point C had been completed and generating throughout this period.
<br><br>
See how the 'all other' group would have been affected if the Swansea Bay Tidal Lagoon had been completed and generating throughout this period (you may need to zoom!)
<br><br><br><br>
"""

para4 = """
The output from three different offshore wind farms for the last few weeks (at time of writing) is shown here, together with a simplified version of the output from the lagoon. One of the key benefits of tidal energy is the fact that it is predictable. Therefore I have predicted it!
<br><br>
The three wind farms are:
<br> - Dudgeon - 402MW installed
<br> - Sheringham Shoal - 317MW installed
<br> - Burbo Bank Extension - 250MW installed
<br><br>
These wind farms have been selected as they have roughly the same quoted capacity and cost in the same ballpark as the lagoon. Offshore wind was considered the best source to compare with the lagoon. 
<br><br>
The shape of the lagoon output would differ slightly from this, but the overall quantities (in both graphs) do exactly reflect the expected output. The lagoon could instantaneously generate far more power than that plotted but that would cause the lagoon to be filled/emptied faster, so the power generated an hour later would be less and the total electrical energy for the tidal cycle would not be different.
<br><br><br><br>
"""



introP = Div(text=para0, width=600, height=600)
squiggleP = Div(text=para1,width=400, height=400)
ridgeP = Div(text=para2, width=600, height=400)
govtP = Div(text=para3, width=600, height=400)
tidalvwindP = Div(text=para4, width=600, height=400)

#show(p)