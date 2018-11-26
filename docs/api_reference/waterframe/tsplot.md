# WaterFrame.tsplot(*keys*=*None*, *rolling*=*None*, *ax*=*None*, *average_time*=*None*, *secondary_y*=*False*, *color*=*None*)

Plot time series.

Parameters | Description | Type
--- | --- | ---
keys | keys of *self.data* to plot. If None, all parameters of the WaterFrame will be traced. | list of str
rolling | Size of the moving window. It is the number of observations used for calculating the statistic. | int
ax | It is used to add the plot to an input axes object. | matplotlib.axes object
average_time | It calculates an average value of a time interval. You can find all of the resample options [here](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases). | matplotlib.axes object
secondary_y | Plot on the secondary y-axis. | bool
color | Color of the traces. Any matplotlib color can be possible. | str or list of str

Returns | Description | Type
--- | --- | ---
ax | New axes of the plot. | matplotlib.AxesSubplot

Return to the [WaterFrame Index](index_waterframe.md).
