# EGIM.to_csv(*self*, *observatory*, *data*, *path*, *qc_tests*=*True*, *only_qc*=*True*)

From mooda v0.2.0.

It is a static method. It creates a csv file following the OceanSites standard.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
data | Data to be saved into a csv file. | Pandas dataframe, WaterFrame
path | Path to save the csv file | str
qc_tests | It indicates if QC test should be passed. | bool
only_qc | It indicates to save only values with QC = 1. | bool

Returns | Description | Type
--- | --- | ---
True | Operation successful. | bool

Return to the [EGIM Index](index_egim.md).
