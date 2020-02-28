# WaterFrame.min(*parameter*)

## Reference

It returns the minimum value of a parameter and the value's indexes.

### Parameters

*  parameter_min: Name of the parameter (str)
            
### Returns

* min_dict: Dictionary with the following format:
```python
{
    '<name of index 1>': <value of index 1>,
    '<name of index n>': <value of index n>,
    'name of parameter': <min value of parameter>
}
```

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same pyhon script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)
min_temp = wf.min('TEMP')

print(f"Minimum value of temperature: {min_temp['TEMP']}")
print("At:")
for key, value in min_temp.items():
    if key == 'TEMP':
        continue
    else:
        print(f"  - {key}: {value}")
```

Output:

```
Minimum value of temperature: 20.0500009523239
At:
  - DEPTH: 1
  - POSITION: 0
  - TIME: 2014-10-30 12:00:00
```

Return to [mooda.WaterFrame](../waterframe.md).
