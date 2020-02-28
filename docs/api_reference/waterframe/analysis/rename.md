# WaterFrame.rename(*actual_name*, *new_name*, *inplace*=*True*)

## Reference

It renames a parameter.

### Parameters

* actual_name: Actual name of a parameter. (str)
* new_name: New name of the parameter. (str)
* inplace: If True, the rename is in place and returns True. (bool)

### Returns

* new_wf: WaterFrame with the renamed parameters. (WaterFrame)

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

print(f"WaterFrame original parameters: {(', ').join(wf.parameters)}")

wf.rename(actual_name='TEMP', new_name='TEMP-OBSEA', inplace=True)

print(f"WaterFrame renamed parameters: {(', ').join(wf.parameters)}")
```

Output:

```shell
WaterFrame original parameters: PRES, TEMP, CNDC
WaterFrame renamed parameters: PRES, TEMP-OBSEA, CNDC
```

Return to [mooda.WaterFrame](../waterframe.md).
