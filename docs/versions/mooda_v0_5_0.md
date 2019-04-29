# mooda v0.5.0

State: Work in progress.

In waterframe.py:

* range_test(): Range of DRYT added.
* drop(): Bug fixed.
* value2nan(): New method. It change the values of the parameters with an input QC flag to NaN.

In ifig.py

* time_series(): Changed min() and max() to np.nanmin() and np.nanmax()

In access.seanadsun.py:

* In SeaAndSun.from_tob_to_waterframe(): Now it can open files with unicede incompatibilities.

In access.seabird.py:

* In SeaBird.from_cnv_to_waterframe(): Now it can open files with unicede incompatibilities.

Return to the [Versions Index](index_versions.md).
