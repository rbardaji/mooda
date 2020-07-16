# wf.iplot(*y*, *x*=*'TIME'*, *color*=*'auto'*, *plot_type*=*'scatter'*, *marginal_x*=*'histogram'*, *marginal_y*=*'box'* *trendline*=*'ols'*)

## Reference

Get a figure using plotly.express.

### Parameters

* y: Y axes of the plot. Column of self.data to plot. (str)
* x: X axes of the plot. It can be an index or a column of self.data. (str)
* color: Column of self.data, auto or None. Colors of the dots of the scatter. (str)
* plot_type: Type of plot figure to make. Options: *scatter*. (str)
* marginal_x: Additional graph on top x axes. Options: *None*, *rug*, *histogram*, *violin*, *box*. (str)
* marginal_y: Additional graph on right y axes. Options: *None*, *rug*, *histogram*, *violin*, *box*. (str)
* trendline: Activate the trendline. Options: *None*, *[ols](https://en.wikipedia.org/wiki/Ordinary_least_squares)*, *[lowess](https://en.wikipedia.org/wiki/Local_regression)*. (str)
* filename: Path and name of the file to save the figure in html. (str)

### Returns

* fig: Plotly figure.

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201402.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201402.nc).

```python
import mooda as md


path_netcdf = "MO_TS_MO_OBSEA_201402.nc"  # Path of the NetCDF file
wf = md.read_nc_emodnet(path_netcdf)

fig = wf.iplot('TEMP')
fig.show()
```

Output:

![iplot example][iplot-example]

*Note: The script makes an interactive charts. The image shown in this example have been generated by saving the interactive images in a PNG file.*

Return to [mooda.WaterFrame](../waterframe.md).

[iplot-example]: ../img_waterframe/iplot-example.png