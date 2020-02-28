# WaterFrame.time_intervals(*parameter*, *frequency*)

## Reference

It returns the index (TIME) of intervals between NaNs.

### Parameters

* parameter: Column name of WaterFrame.data. (str)
* frequency: Theorical sample frequency. (DateOffset, Timedelta or str)

### Returns

* intervals: List of tuples with the start and end index (TIME) of each interval of data.. ([(str, str)])

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

print(f'Available parameters: {wf.parameters}')

parameter = 'TEMP'  # Temperature

print(f"Time intervals of {wf.vocabulary.get(parameter).get('long_name')} ",
      f"between gaps: {wf.time_intervals(parameter, 'H')}")
```

Output:

```shell
Data intervals of Sea temperature between gaps: [('2014-01-19 00:00:00', '2014-01-23 00:00:00'), ('2014-01-26 00:00:00', '2014-01-31 23:00:00')]
```

Return to [mooda.WaterFrame](../waterframe.md).
