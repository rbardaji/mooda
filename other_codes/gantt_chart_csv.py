"""
It creates a plotly grantt graph from data of CSV files.
The graph shows the intervals of time where there are data.
With the grantt graph users can see where are the gaps.
"""
import glob
import plotly
import plotly.figure_factory as ff
from mooda import WaterFrame
from mooda.access import EGIM

# Path of files
# Where the files are:
path_location = r""
# Where to save the result:
save_location = r""

path_files = glob.glob(path_location)
df = []
for path_file in path_files:

    if path_file[-1] != "v":
        continue

    # Load data into a WaterFrame
    print("Loading data")
    wf = EGIM.from_raw_csv("EMSO-Azores", path_file)
    print("Done")
    print(wf)

    # Resample data hourly
    print("Resampling data")
    wf.resample("H")
    print("Done")

    # Obtain one of the parameters
    parameter = wf.parameters()[0]

    intervals = wf.datetime_intervals(parameter)

    print(path_file)
    instrument = path_file.split(".")[-2].split("\\")[-1]

    for start, end in intervals:
        df.append(dict(Task=instrument, Start=start, Finish=end,
                       Resource=instrument))

fig = ff.create_gantt(df, group_tasks=True, title="Data intervals", width=700,
                      height=380)
fig['layout'].update(autosize=False, margin=dict(l=110))
plotly.offline.plot(fig, filename=save_location)
