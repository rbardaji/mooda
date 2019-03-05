# time_series_from_waterframe(*waterframe*, *parameters*=*None*)

It creates a Plotly time-series figure.

## Parameters

    waterframe: WaterFrame
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
    wf.resample('W')

    figure = IFig.time_series_from_waterframe(wf, 'TEMP')

    plot(figure)


example()

```
