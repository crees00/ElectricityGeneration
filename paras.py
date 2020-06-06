# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:37:50 2019

@author: Chris
"""

from bokeh.io import output_file, show
from bokeh.models.widgets import Paragraph, Div, PreText

#output_file("div.html")


para0 = """
<br><b>Introduction</b><br>
<br>
This project shows where the electricity used in the UK comes from. The data has been acquired from publicly available online sources, then processed and presented here.
<br><br>
The project aims to provide some real data showing the underlying trends in our electricity supply, with the opportunity to investigate for yourself. The project also aims to show the effects of two different new electricity generation projects: Hinkley Point C nuclear power station and the Swansea Bay Tidal Lagoon.
<br><br>
Once you've read the information below, click the tabs at the top to get started.
<br><br>
<b>Electricity Sources - What are they?</b>
<br><br>
Our electricity comes from a lot of different places. The key ones are shown in this project:
<br>
<br>Demand - How much electricity the UK needs.
<br>Nuclear - We have 8 operating nuclear power stations, with most of them built in the 1960s-1980s and scheduled for decomissioning in the coming years. Hinkley Point C is currently being built.
<br>Wind - A combination of offshore and onshore wind farms.
<br>Coal - Being phased out due to its highly polluting nature.
<br>CCGT - Combined Cycle Gas Turbine i.e. gas power stations. Burn the gas (think jet engine), turn a turbine, generate electricity. Waste heat generates steam which turns its own turbine, generating more electricity.
<br>Interconnectors(ICT) - There are big wires under the sea linking the UK with France, the Netherlands, Ireland and Belgium. If we're short, we can buy in electricity from abroad and vice versa.
<br>Pumped storage - There are reservoirs that can be pumped full of water when we have surplus electricity. They can then be emptied (through turbines) to meet short spikes in demand.
<br>Hydro - Small scale hydroelectric stations, mainly in Scotland.
<br>Biomass - Burning substances such as wood, sometimes in converted coal power plants.
<br><br><br>

<b>Units - what's a GW?</b>
<br><br>
The rate of generation/consumption of electrical energy is called power, measured in Watts (W) - amount of electrical energy per second. 
<br>
<br> 1kW = 1,000W
<br> 1MW = 1,000,000W
<br> 1GW = 1,000,000,000W
<br> 1TW = 1,000,000,000,000W.
<br><br>
The quantity of electrical energy generated/consumed is measured in [kilo/mega/giga/tera]Watt-Hours (Wh). For example, you can generate 10MWh of electrical energy by generating at a power of 1MW for 10hours, or 10MW for 1hour. 
<br><br>
Your electricity provider probably charges you per kWh (a 'unit' of electricity). All that matters is how many kWh of electricity you have used in the last month. It doesn't matter if you've used your 2kW kettle for 5 minutes to make some tea or left your 55" LG OLED TV on standby at 0.5W for a fortnight, you've used the same amount of electricity so you'll get the same bill. 
<br><br><br>

<b>Data Sources</b>
<br><br>
Data have been obtained through some publicly available online sources:
<br>
<br><i>Gov.uk National Statistics. Energy Trends: electricity.</i> This gives the per-quarter longer term trends.
<br>https://www.gov.uk/government/statistics/electricity-section-5-energy-trends
<br>
<br><i>Gridwatch</i> - This site collates data reported every 5 mins for the UK. Note: solar power is not accurately reported.
https://www.gov.uk/government/statistics/electricity-section-5-energy-trends
<br>
<br><i>Elexon</i> - This site is the official source of electricity generation data and was used to find the output for the three wind farms to compare with the Tidal Lagoon.
<br>https://www.bmreports.com/bmrs/?q=actgenration/actualgeneration
<br>
<br><i>Back of the envelope calculations on the proposed Swansea Bay Tidal Lagoon, T. A. Adcock, Oxford University</i> - Here, a sense check has been done on the power output numbers for the Lagoon, providing the expected average power output used in this project.
<br>http://users.ox.ac.uk/~spet1235/Swansea.pdf
<br><br>
<br><br><br><br>


 
"""

para1 = """
<br><b>Gridwatch Data</b><br>

<br>Data have been recorded for the past eight years, showing the power output of the different sources of electricity in the UK, as well as the total demand. 
<br><br>These measurements have been taken at five minute intervals. The data are plotted below with a selection of tools to inspect further.
<br><br> Play with the controls to the side, as well as rolling over the plot itself.
<br><br><br><br>
"""

para2 = """
<br><b>Comparing the output of nuclear and wind</b><br>
<br>
This plot shows histograms of the power output for wind and nuclear for each five minute period of the last eight years. They are on the same scales, allowing direct comparison. The height of a bar shows the number of 5min periods when the source was generating electricity at that power output.
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
<br><b>Long term generation trends</b><br>
<br>
Here is the government's data for electricity generated since 1998. It gives the totals for each quarter.
<br><br>
Choose the sources you'd like to see using the buttons
<br><br>
See what the nuclear generation would have been if Hinkley Point C had been completed and generating throughout this period.
<br><br>
See how the 'all other' group would have been affected if the Swansea Bay Tidal Lagoon had been completed and generating throughout this period (you may need to zoom!)
<br><br>
If you don't know what Hinkley Point C and the Swansea Bay Tidal Lagoon are, see below the plot.
<br><br><br><br>
"""
para3b = """
Hinkley Point C is a major project to build a new 3.2GW nuclear power station in North Somerset. It is being undertaken by the French nuclear power company EDF, with some of the investment from China, to a total cost of around £20bn. This huge expense is being recouped through the UK government paying an agreed price for each unit of electricity generated (the 'strike price'). The plant is currently being built, expected to be operational in 2025.
<br><br>"""

para3c="""
Swansea Bay Tidal Lagoon is a proposed project that has been awaiting approval for many years. The project plans to build a large sea wall enclosing an area of Swansea Bay, creating a 'lagoon'. The lagoon is connected to the sea via some large turbines which generate electricity. When the tide comes in, the seawater flows through the turbines, filling up the lagoon. When the tide goes out, the lagoon empties, again spinning the turbines. It has widespread support in the Swansea area due to its construction providing significant work for the local people and its assumed green credentials. 
<br><br>
"""

para4 = """
<br><b>Comparing the tidal lagoon with three existing UK wind farms</b><br>
<br>
The output from three different offshore wind farms for the last few weeks (at time of writing) is shown here, together with a simplified version of the output from the lagoon. One of the key benefits of tidal energy is the fact that it is predictable. Therefore I have predicted it!
<br><br>
The three wind farms are:
<br> - Dudgeon - 402MW installed
<br> - Sheringham Shoal - 317MW installed
<br> - Burbo Bank Extension - 250MW installed
<br><br>
These wind farms have been selected as they have roughly the same quoted capacity and cost in the same ballpark as the lagoon. Offshore wind was considered the best source to compare with the lagoon. Although the time period was selected arbitrarily, the Capacity Factor (proportion of maximum possible available output actually generated) for each wind farm is in the 30-40% region, which is approximately their annual average. This time period is therefore representative of average conditions. 
<br><br>
The shape of the lagoon output would differ from that shown (the tides fluctuate throughout the lunar cycle, power output is dependent on how the lagoon is operated, such as when the gates are opened/closed etc.), but the overall quantities (in both graphs) do exactly reflect the expected output. The lagoon could instantaneously generate far more power than that plotted but that would cause the lagoon to be filled/emptied faster, so the power generated an hour later would be less and the total electrical energy for the tidal cycle would not be different.
<br><br><br><br>
"""

para5 = """
<br><b>Load Following</b><br>
<br>
Load following is an important consideration in the management of the UK electricity supply. As you can see from the other tabs, the demand fluctuates a great deal throughout the day, week and year. Electricity storage is a challenge so it is best to generate electricity when it is needed. Therefore our supply needs to 'follow' the demand - when there is a high demand, we need to generate more electricity.
<br><br>
The generation data at 5min intervals have been normalised so that the plots show the ranges of the sources and demand. Demand is always on the x-axis.
<br><br>
To the right, for example, there is no obvious correlation between the demand and wind supply in 2015 - this is expected as unfortunately the wind does not always decide to blow when the UK needs electricity.
<br><br>
Compare that to coal in 2012 - Here there is a clear link between coal generation and UK demand. The coal power stations were fired up when demand was high and slowed down when electricity was not needed.
<br><br>
<b>Some other trends to spot</b>
<br>
<br>- Nuclear just generates at full blast at all times, regardless of demand.
<br>- Coal use has decreased dramatically, with a lot of time in recent years outputting no/little electricity.
<br>- Biomass, pumped storage and the French interconnector tend to provide electricity at set 'levels'.
<br><br><br><br>
"""

introP = Div(text=para0, width=600, height=600)
squiggleP = Div(text=para1,width=400, height=240)
ridgeP = Div(text=para2, width=600, height=260)
govtP = Div(text=para3, width=600, height=300)
govtPb = Div(text=para3b, width=400, height=300)
govtPc = Div(text=para3c, width=400, height=300)
gap = Div(text="", width=50, height=300)
tidalvwindP = Div(text=para4, width=600, height=420)
LFP = Div(text=para5, width=600, height=380)
#show(p)