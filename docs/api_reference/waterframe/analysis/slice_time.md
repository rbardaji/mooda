# WaterFrame.slice_time(*start*=*None*, *end*=*None*, *inplace*=*True*)

## Reference

Delete data outside the time interval.

### Parameters

* start: Start time interval with format 'YYYYMMDDhhmmss'. (str)
* end: End time interval with format 'YYYYMMDDhhmmss'. (str)
* inplace: If inplace is True, changes will be applied on self.data and returns True. Otherwhise, it returs the new WaterFrame. (bool)

### Returns

* new_wf: (WaterFrame)

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

wf.slice_time("20140120000000", "20140121000000")

print(wf.data['TEMP'].head()) # Print the first five values of TEMP
```

Output:

```shell
TIME
2014-01-19    13.222084
2014-01-20    13.378334
2014-01-21    13.381667
2014-01-22    13.727917
2014-01-23          NaN
Freq: D, Name: TEMP, dtype: float64
```

Return to [mooda.WaterFrame](../waterframe.md).
