# WaterFrame.\_\_init\_\_(*path*=*None*)

It creates the following instance variables:

* WaterFrame.data: A pandas DataFrame that contains the measurement values of the time series.
* WaterFrame.metadata: It is a dictionary that contains the metadata information of the time series.
* WaterFrame.meaning:s  It is a dictionary that contains the meaning of the keys of data (i.e. "TEMP": "Seawater temperature").

If there is a path to a NetCDF file, it loads the data from the file.

Parameters | Description | Type
--- | --- | ---
path | Path to a [NetCDF](http://www.oceansites.org/data/) file. | string
