"""
Script to create a plotly grapth. The graph contains the limelines of TEMP of
different instrument of the EGIM deployed in OBSEA.
"""
import plotly
import plotly.graph_objs as go
from mooda import WaterFrame

# The files that conain TEMP are from CTD, Tsunameter and Oxymeter
path_location = r"WRITE YOUR PATH HERE"
path_ctd = path_location + r"\OS_OBSEA_2016120120170426_R_37-14998.nc"
path_oxymeter = path_location + r"\OS_OBSEA_2016120120170426_R_4381-606.nc"

# Load data into a WaterFrame
print("Loading data from CTD")
wf_ctd = WaterFrame()
wf_ctd.from_netcdf(path_ctd)
print("Done")
print("Loading data from the Oxymeter")
wf_oxymeter = WaterFrame()
wf_oxymeter.from_netcdf(path_oxymeter)
print("Done")

# Creation of a third Waterframe
wf_anal = WaterFrame()
wf_anal.concat(wf_ctd)
wf_anal.rename("TEMP", "CTD")
wf_anal.concat(wf_oxymeter)
wf_anal.rename("TEMP", "OXYMETER")

# Calculation of correlation between the TEMP parameters
print(wf_anal.corr("CTD", "OXYMETER"))

# Calculation of maximun difference
where, val = wf_anal.max_diff("CTD", "OXYMETER")
print("Maximun difference:", val, "at", where)

# Resample data hourly
print("Resampling data from CTD")
wf_ctd.resample("H")
print("Done")
print("Resampling data from Oxymenter")
wf_oxymeter.resample("H")
print("Done")

# Creation of traces for the plotly graph
data_ctd = go.Scatter(x=wf_ctd.data.index, y=wf_ctd.data['TEMP'],
                      name="From CTD")
data_oxymeter = go.Scatter(x=wf_oxymeter.data.index,
                           y=wf_oxymeter.data['TEMP'], name="From Oxymeter")

data = [data_ctd, data_oxymeter]

# Edit the layout
layout = dict(title='Sea water temperature averaged hourly',
              yaxis=dict(title='degrees Celsius'),
              )

plotly.offline.plot(
    {
     "data": data,
     "layout": layout,
    }, auto_open=True, filename=r"C:\Users\Raul\Google Drive\Work\EmsoDev\server\ejemplos web\megakit - mio\grapths\obsea\TEMP-OBSEA.html")
