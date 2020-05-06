# wf.iplot_timeseries(*parameters_to_plot*=*None*, *mode*=*'lines'* *marker_line_width*=*0*, *marker_size*=*4*, *marker_color*=*None*, *marker_colorscale*=*'Viridis'*)

## Reference

It creates a Plotly figure with the time-series of the input parameters.

### Parameters

* parameters_to_plot: Parameters to plot. (str or list)
* mode: Plotting points (makers), lines or lines and points (lines+markers). (str)
* marker_line_width: Width of the line arround the marker. (float)
* marker_size: Size of the marker. (float)
* marker_color: Parameter name. Change the color of the marker related to a parameter. (str)
* marker_colorscale: Color scale of markers. Options: Blackbody, Bluered, Blues,Earth, Electric, Greens, Greys, Hot, Jet, Picnic, Portland, Rainbow, RdBu, Reds, Viridis, YlGnBu, YlOrRd. (str)

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
