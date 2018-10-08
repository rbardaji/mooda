"""
Script to create a plotly graph. The graph contains the limelines of TEMP of
different instrument of the EGIM deployed in OBSEA.
"""
import plotly
import plotly.graph_objs as go
from mooda import WaterFrame
from mooda.access import EGIM

# The files that contain TEMP are from CTD, Tsunameter and Oxymeter
path_location = r""
path_ctd = path_location + r"\CTD.csv"
path_oximeter = path_location + r"\Oximeter.csv"

output_file = r""

# Load data into a WaterFrame
print("Loading data from CTD")
wf_ctd = EGIM.from_raw_csv("EMSO-Azores", path_ctd)
print("Done")
print("Loading data from the Oximeter")
wf_oxymeter = EGIM.from_raw_csv("EMSO-Azores", path_oximeter)
print("Done")

# Creation of a third Waterframe
print("Creation of an other WaterFrame")
wf_anal = WaterFrame()
print("Concat CTD")
wf_anal.concat(wf_ctd)
print("Done")
print("Rename parameters")
wf_anal.rename("TEMP", "CTD")
print("Done")
print("Concat Oximeter")
wf_anal.concat(wf_oxymeter)
print("Done")
print("Rename parameters")
wf_anal.rename("TEMP", "OXYMETER")
print("Done")

# Calculation of correlation between the TEMP parameters
print(wf_anal.corr("CTD", "OXYMETER"))

# Calculation of maximun difference
where, val = wf_anal.max_diff("CTD", "OXYMETER")
print("Maximun difference:", val, "at", where)

# Resample data hourly
print("Resampling data from CTD")
wf_ctd.resample("H")
print("Done")
print("Resampling data from Oximenter")
wf_oxymeter.resample("H")
print("Done")

# Slice
wf_ctd.slice_time(start="20170720000000", end="20180809000000")
wf_oxymeter.slice_time(start="20170720000000", end="20180809000000")

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
    }, auto_open=True, filename=output_file)
