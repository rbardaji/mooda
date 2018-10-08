"""
Script to create a plotly graph. The graph contains the limelines of TEMP of
different instrument of the EGIM deployed in OBSEA.
"""
import plotly
import plotly.graph_objs as go
from mooda import WaterFrame
from mooda.access import EGIM


# Path of files
# Where the files are:
path_location = r"C:\Users\rbard\Desktop\Azores EGIM Data"
path_data = path_location + r"\turbidity.csv"
path_data = r"C:\Users\rbard\Desktop\Azores EGIM Data\Oximeter.csv"
# Where to save the result:
save_location = r"C:\Users\rbard\Google Drive\Work\EmsoDev\server\www\html\graphs\azores"
save_start = r"\OXI-"
end_save = r"-AZORES.html"


# Load data into a WaterFrame
print("Loading data")
if path_data[-1] == 'c':
    wf = WaterFrame()
    wf.from_netcdf(path_data)
elif path_data[-1] == 'v':
    print(path_data)
    wf = EGIM.from_raw_csv(observatory="EMSO-Azores", path=path_data)
print("Done")
print(wf)

# Check parameters
parameters = wf.parameters()

# Resample data hourly
print("Resampling data")
wf.resample("H")
print("Done")

wf.slice_time(start="20170725000000", end="20180811000000")

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
