# wf.iplot_location()

## Reference

It creates a Plotly Figure with a map and a spot of the measurement location of the WaterFrame.

### Returns

* figure: Dictionary of Plotly figure. (dict)

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc).

```python
import mooda as md
import plotly.graph_objects as go

path_netcdf = "MO_TS_MO_OBSEA_201401.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

fig = wf.iplot_location()
go.Figure(fig).show()
```

Output:

[OBSEA location map example](../html_waterframe/obsea-location-example.html)

Return to [mooda.WaterFrame](../waterframe.md).
