"""
Script to create a plotly graph. The graph contains the limelines of TEMP of
different instrument of the EGIM deployed in OBSEA.
"""
import plotly
import plotly.graph_objs as go
from mooda import WaterFrame

# Path of files
# Where the files are:
path_location = r"C:\Users\rbard\Google Drive\Work\EmsoDev\server\ejemplos web\megakit - mio\data\obsea"
path_data = path_location + r"\OS_OBSEA_2016120120170426_R_37-14998.nc"
# Where to save the result:
save_location = r"C:\Users\rbard\Google Drive\Work\EmsoDev\server\ejemplos web\megakit - mio\graphs\obsea"
save_start = r"\CTD-"
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
    layout = dict(title=wf.meaning[parameter]['long_name'],
                  yaxis=dict(title=wf.meaning[parameter]['units']),
                  )

    plotly.offline.plot(
        {
         "data": data,
         "layout": layout,
         }, auto_open=True, filename=save_location+save_start+parameter+end_save)
    print("Done")