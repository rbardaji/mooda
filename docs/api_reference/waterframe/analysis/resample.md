# WaterFrame.resample(rule, method='mean', inplace=True)

## Reference

Convenience method for frequency conversion and sampling of time series of the WaterFrame object. Warning: if WaterFrame.data contains MultiIndex, those indexes disappears, obtaining a single 'TIME' index.

### Parameters

* rule: The offset string or object representing [target conversion](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases) (str).
* method: "mean", "max", "min". Save the new value with the mean(), max() or min() function. (str)
* inplace: If True, resample in place and return 'True', If False, return a new WaterFrame. (bool)

### Returns

* new_wf: WaterFrame with the renamed parameters. (WaterFrame)

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

wf.resample('D')
print(wf.data['TEMP'].head()) # Print the first 5 values of TEMP
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
