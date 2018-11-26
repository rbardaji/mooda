# WaterFrame.resample(*rule*, *method*=*'mean'*)

Convenience method for frequency conversion and sampling of time series of the WaterFrame object.

Parameters | Description | Type
--- | --- | ---
rule | The offset string or object representing target conversion. You can find all of the resample options [here](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases) | str
method | Save the new value with the mean(), max() or min() function. | "mean", "max" or "min"

Returns | Description | Type
--- | --- | ---
True/False | It indicates if the process was successfully. | bool

Return to the [WaterFrame Index](index_waterframe.md).
