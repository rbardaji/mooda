# EGIM.to_netcdf(*self*, *observatory*, *instrument*, *data*, *path*, *qc_tests*=*True*, *only_qc*=*True*)

From mooda v0.2.0.

It creates a netCDF file following the [OceanSites](http://archimer.ifremer.fr/doc/00250/36149/34703.pdf) standard.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
instrument | Instrument name. | str
data | Data to be saved into a netCDF file. | Pandas dataframe, WaterFrame
path | Path to save the netCDF file | str
qc_tests | It indicates if QC test should be passed. | bool
only_qc | It indicates to save only values with QC = 1. | bool

Returns | Description | Type
--- | --- | ---
True | Operation successful. | bool

Return to the [EGIM Index](index_egim.md).
