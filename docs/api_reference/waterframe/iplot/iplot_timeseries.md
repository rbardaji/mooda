# wf.iplot_timeseries(*parameters_to_plot*=*None*)

## Reference

It creates a Plotly figure with the time-series of the input parameters.

### Returns

* figure: Dictionary of Plotly figure. (dict)

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc).

```python
import mooda as md
import plotly.graph_objects as go

path_netcdf = "MO_TS_MO_OBSEA_201401.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

fig = wf.iplot_timeseries('TEMP')
go.Figure(fig).show(filename='ex.html')
```

Output:

[Interactive time-series plot example](../html_waterframe/iplot-timeseries-example.html)

Return to [mooda.WaterFrame](../waterframe.md).
