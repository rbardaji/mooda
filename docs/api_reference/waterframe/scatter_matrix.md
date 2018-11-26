# WaterFrame.scatter_matrix(*keys*, *ax*=*None*)

Draw a matrix of scatter plots.

Parameters | Description | Type
--- | --- | ---
key | keys of self.data to plot. | list of str
ax | It is used to add the plot to an input axes object. | matplotlib.axes

Keys must contain different words. Example:

* keys = ['VAVH', 'VCMX'] is ok.
* keys = ['VAVH', 'VAVH'] is not ok.

Returns | Description | Type
--- | --- | ---
ax | New axes of the plot. | matplotlib.AxesSubplot

Return to the [WaterFrame Index](index_waterframe.md).
