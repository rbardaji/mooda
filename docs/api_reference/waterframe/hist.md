# WaterFrame.hist(*parameter*=*None*, *mean_line*=*False*, *\*\*kwds*)

Make a histogram of the WaterFrame's.

A histogram is a representation of the distribution of data. This function calls DataFrame.hist(), on each parameter of the WaterFrame, resulting in one histogram per parameter.

Parameters | Description | Type
--- | --- | ---
parameter | keys of self.data to plot. If parameter=None, it will plot all
                parameters. | str or list of str or None
mean_line | It draws a line representing the average of the dataset. | bool
**kwds | All other plotting keyword arguments to be passed to DataFrame.hist(). <https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.hist.html> | --

Returns | Description | Type
--- | --- | ---
axes | New axes of the plot. | matplotlib.AxesSubplot or numpy.ndarray of them

Return to the [WaterFrame Index](index_waterframe.md).