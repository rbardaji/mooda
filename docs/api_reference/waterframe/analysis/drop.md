# WaterFrame.drop(*parameters*, *inplace*=*True*)

## Reference

Remove input parameters from WaterFrame.data.

### Parameters

* parameters: Parameters of WaterFrame.data. (str, list of str)
* inplace: Drop in place and return 'True' or return a copy of the WaterFrame without the input parameters. (bool)

### Returns

* new_wf: WaterFrame

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

print(f'Available parameters: {wf.parameters}')

parameters_to_drop = ['TEMP', 'PSAL']
wf.drop(parameters_to_drop)

print(f'Available parameters after drop {parameters_to_drop}: {wf.parameters}')
```

Output:

```shell
Available parameters: ['DEPH', 'ATMS', 'CNDC', 'DRYT', 'PRES', 'PSAL', 'SVEL', 'TEMP', 'WDIR', 'WSPD']
Available parameters after drop ['TEMP', 'PSAL']: ['DEPH', 'ATMS', 'CNDC', 'DRYT', 'PRES', 'SVEL', 'WDIR', 'WSPD']
```

Return to [mooda.WaterFrame](../waterframe.md).
