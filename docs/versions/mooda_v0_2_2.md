# mooda v0.2.2

State: Work in progress.

In waterframe.py:

* qcbarplot(): Legend changed.
* to_csv(): We have changed the way to save the metadata within the file. We have added an exception that was produced with the Pangea metadata.
* to_netcdf(): Some metadata contains lists of str. This is not compatible with the NETCDF3_64BITS format. We have changed the phrase lists by separate sentences by ",".

Return to the [Versions Index](index_versions.md).