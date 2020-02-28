# WaterFrame.qc_spike_test(*parameters*=*None*, *window*=*0*, *threshold*=*3*, *flag*=*4*, *inplace*=*True*)

## Reference

It checks if there is any spike in the time series.

### Parameters

* parameters: Parameter to apply the test. (str, list of str)
* window: Size of the moving window of values to calculate the mean. If it is 0, the function calculates the optimal window. (int)
* threshold: Maximum deference between the average of the moving window and the analyzed value. (int)
* flag: Flag value to write in on the fail test values. (int)
* inplace: If True, it changes the flags in place and returns True. Otherwhise it returns an other WaterFrame. (bool)

### Returns

* new_wf: WaterFrame

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path_netcdf = "MO_TS_MO_OBSEA_201401.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

ok = wf.qc_spike_test()

if ok:
    print('Spike test applied.')
```

Output:

```shell
Spike test applied.
```

Return to [mooda.WaterFrame](../waterframe.md).
