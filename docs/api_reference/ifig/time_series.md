# time_series(*self*, *parameters*=*None*)

It creates a Plotly time-series figure.

## Parameters

    parameters: str or list (optional, parameters=None)
        Parameters to plot.

## Returns

    figure: dict
        Plotly figure dictionary.

## Example

```python
"""Example code"""
from plotly.offline import plot
from mooda import WaterFrame
from mooda.ifig import IFig

# I downloaded the NetCDF file from
# http://193.144.35.225/emso_sites/data/obsea/OS_OBSEA_2016120120170426_R_37-14998.nc
NC_FILE = r"path to the netcdf"

def example():
    wf = WaterFrame(NC_FILE)

    ifig = IFig(wf)
    figure = ifig.time_series('TEMP')

    plot(figure)


example()

```
