# ElectricityGeneration

Analysing the electricity generation of the UK from various sources

Before running:
One data source is too large to be held on GitHub (csv file ~100MB)
To download it, go to https://www.gridwatch.templar.co.uk/download.php and press 'download', ensuring that all sources are selected (they are by default).
Store the resulting 'gridwatch.csv' file in the same location as the code to run.

to run:

bokeh serve --show --port 5001 panels.py

On windows, to close the port use 
netstat -n -a -o
to find the PID of the process with port 5001, then kill the process

All other relevant csv files should be in this repo. They are stored here because they either do not have direct links online or have been modified to a format suitable to be read.