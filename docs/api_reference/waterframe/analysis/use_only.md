# WaterFrame.use_only(*parameters_to_use*, *inplace*=*True*)

## Reference

It deletes all parameters except the input parameters.

### Parameters

* parameters_to_use: List of parameter names to keep (list or str).
* inplace: If True, do operation inplace and return True (bool). 

### Returns

* new_qf: WaterFrame after the method is applied (WaterFrame).

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same pyhon script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

# Print parameters
print(f"WaterFrame original parameters: {(', ').join(wf.parameters)}")
# Delete all parameters except 'TEMP'
wf2 = wf.use_only('TEMP', inplace=False)
print(f"New WaterFrame parameters: {(', ').join(wf2.parameters)}")
```

Output:

```
WaterFrame original parameters: PRES, TEMP, CNDC
New WaterFrame parameters: TEMP
```

Return to [mooda.WaterFrame](../waterframe.md).
