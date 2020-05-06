# mooda.read_nc_moist(path, resample_rule=False)

## Reference

Open a NetCDF file from [MOIST](http://www.moist.it/sites/western_ionian_sea/2).
This method only works with the files generated from CTDs.

### Parameters

* path: Path of the NetCDF file. (str)
* resample_rule: Time resample method. Use resample_rule = False to do not resample. See DateOffset objects [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html). (str)
            
### Returns

* wf: WaterFrame

Return to [API reference](../index_api_reference.md)
