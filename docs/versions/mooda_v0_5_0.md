# mooda v0.5.0

State: Work in progress.

In waterframe.py:

* range_test(): Range of DRYT added.
* drop(): Bug fixed.
* value2nan(): New method. It change the values of the parameters with an input QC flag to NaN.
* \_\_repr()\_\_: Min and max date info changed to min and max {Index name} info.

In ifig.py

* time_series(): Changed min() and max() to np.nanmin() and np.nanmax()
* profile(): New method. It creates a profile figure.

In access.seanadsun.py:

* In SeaAndSun.from_tob_to_waterframe(): Now it can open files with unicode incompatibilities.

In access.seabird.py:

* In SeaBird.from_cnv_to_waterframe(): Now it can open files with unicode incompatibilities.

New class: access.bedc.py, open NetCDF data from BODC.

* from_nc_to_waterframe(): New static method. It opens a NetCDF file from BODC and creates a WaterFrame.

Return to the [Versions Index](index_versions.md).
