"""
Script to create a plotly graph. The graph contains the limelines of TEMP of
different instrument of the EGIM deployed in OBSEA.
"""
import plotly
import plotly.graph_objs as go
from mooda import WaterFrame


# Path of files
# Where the files are:
path_location = r"YOUR PATH LOCATION"
path_data = path_location + r"\OS_OBSEA_2016120120170426_R_NTURTD-648.nc"
# Where to save the result:
save_location = r"YOUR PATH TO SAVE"
save_start = r"\TUR-"
end_save = r"-OBSEA.html"


# Load data into a WaterFrame
print("Loading data")
wf = WaterFrame()
wf.from_netcdf(path_data)
print("Done")
print(wf)

# Check parameters
parameters = wf.parameters()

# Resample data hourly
print("Resampling data")
wf.resample("H")
print("Done")

for parameter in parameters:
    print("Creation of", parameter, "graph")
    # Creation of traces for the plotly graph
    data = [go.Scatter(x=wf.data.index, y=wf.data[parameter])]

    # Edit the layout
    title = wf.meaning[parameter]['long_name']
    if isinstance(title, list):
        title_ = ""
        for part in title:
            title_ += part + " "
    else:
        title_ = title + " "
    title_ += "averaged hourly"
    layout = dict(title=title_,
                  yaxis=dict(title=wf.meaning[parameter]['units']),
                  )

    plotly.offline.plot({"data": data, "layout": layout, }, auto_open=True, 
                        filename=save_location+save_start+parameter+end_save)
    print("Done")
