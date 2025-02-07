# mooda.read_nc(*path*)

## Reference

Read data form NetCDF file and create a WaterFrame.

### Parameters

* path: Path of the NetCDF file (str).

### Returns

* wf: WaterFrame

## Example

To reproduce the example, download the NetCDF file [here](https://github.com/rbardaji/mooda/blob/14f4fd776d30a6a2e3f7bc0920996dee2b8a0cb3/docs/examples/data/TEMP.nc) and save it as `example.nc` in the same pyhon script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc(path_netcdf)
print(wf)
```

Output:

```
Memory usage: 2.648 MBytes
Parameters:
  - TEMP: water temperature (degree_Celsius)
    - Min value: -2147483647.0
      - TIME: 2023-04-30 22:00:00
      - DEPTH: -3.0
    - Max value: 29.1200008392334
      - TIME: 2023-08-20 13:00:00
      - DEPTH: nan
    - Mean value: -120947890.73436177
```

Return to [API reference](../index_api_reference.md).
