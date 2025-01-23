# mooda.read_nc(*path*)

## Reference

Read data form NetCDF file and create a WaterFrame.

### Parameters

* path: Path of the NetCDF file (str).

### Returns

* wf: WaterFrame

## Example

To reproduce the example, download the NetCDF file [here](docs/api_reference/input/read_nc.md) and save it as `example.nc` in the same pyhon script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc(path_netcdf)
print(wf)
```

Output:

```
Memory usage: 10.546 MBytes
Parameters:
  - CNDC: Electrical conductivity(S m-1)
    - Min value: 1335876.0
      - TIME: 2013-08-22 03:00:01
    - Max value: 1440466.0
      - TIME: 2013-09-20 01:30:01
    - Mean value: 1377554.1720595956
  - PRES: Sea pressure(dbar)
    - Min value: 540746.0
      - TIME: 2014-04-21 19:15:01
    - Max value: 543880.0
      - TIME: 2013-09-28 18:15:01
    - Mean value: 541994.744552376
  - PSAL: Practical salinity(PSU)
    - Min value: 31.4469523288697
      - TIME: 2013-09-22 03:45:01
    - Max value: 33.43121973422811
      - TIME: 2013-09-22 07:45:01
    - Mean value: 32.45014425234326
```

Return to [API reference](../index_api_reference.md).
