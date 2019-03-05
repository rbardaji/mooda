# IFig.site_map_from_waterframe(*wf*)

From mooda >= 0.3.

It is a static method.

It creates a chart with a map with the coordinates of the site. It looks for the coordinates in the metadata information.

## Parameters

    waterframe: WaterFrame

## Returns

    figure: dict
        Plotly Figure dictionary.

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

    figure = IFig.site_map_from_waterframe(wf)

    plot(figure)


example()

```