"""
It creates a plotly grantt graph from data of NetCDF files.
The graph shows the intervals of time where there are data.
With the grantt graph users can see where are the gaps.
"""
import glob
import plotly
import plotly.figure_factory as ff
from mooda import WaterFrame

# Path of files
# Where the files are:
path_location = r"WRITE HERE THE LOCATION PATH"
# Where to save the result:
save_location = r"WRITE HERE THE PATH TO SAVE THE GRAPH"

path_files = glob.glob(path_location)

df = []
for path_file in path_files:

    # Load data into a WaterFrame
    print("Loading data")
    wf = WaterFrame()
    wf.from_netcdf(path_file)
    print("Done")
    print(wf)

    # Resample data hourly
    print("Resampling data")
    wf.resample("H")
    print("Done")

    # Obtain one of the parameters
    parameter = wf.parameters()[0]

    intervals = wf.datetime_intervals(parameter)

    if "R_4381-606" in path_file:
        instrument = "Turbidimeter"
    elif "R_37-14998" in path_file:
        instrument = "CTD"
    elif "NTURTD-64" in path_file:
        instrument = "Oximeter"
    elif "SBE54-0049" in path_file:
        instrument = "Tsunameter"

    for start, end in intervals:
        df.append(dict(Task=instrument, Start=start, Finish=end,
                       Resource=instrument))

fig = ff.create_gantt(df, group_tasks=True, title="Data intervals", width=780,
                      height=380)
plotly.offline.plot(fig, filename=save_location)
