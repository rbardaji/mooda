# WaterFrame.from_netcdf(*self*, *path*)

Load and decode a dataset from a netcdf file. The compatible netCDF files are from the mooring-buoys of [EMODNET](http://www.emodnet-physics.eu/Map/), [JERICO](http://www.jerico-ri.eu/data-access/), [EMSO](http://emso.eu), and all time series with [NetCDF OceanSites](http://www.oceansites.org/data/) format.

Parameters | Description | Type
--- | --- | ---
path | Path to a netCDF file or an OpenDAP URL. File-like objects are opened with scipy.io.netcdf (only netCDF3 supported). | string or obj

Returns | Description | Type
--- | --- | ---
True/False | It indicates if the procedure was successful. | bool

Return to the [WaterFrame Index](index_waterframe.md).
