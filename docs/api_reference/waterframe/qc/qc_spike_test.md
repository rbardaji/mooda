# WaterFrame.qc_spike_test(*parameters*=*None*, *window*=*0*, *threshold*=*3*, *flag*=*4*, *inplace*=*True*)

## Reference

Based on [peak signal detection in realtime timeseries data](https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data).

Algorithm based on the principle of dispersion: if a new datapoint is a given x number of standard deviations away from some moving mean, the algorithm signals (also called z-score). The algorithm is very robust because it constructs a separate moving mean and deviation, such that signals do not corrupt the threshold. Future signals are therefore identified with approximately the same accuracy, regardless of the amount of previous signals.
    
For example, a window of 5 will use the last 5 observations to smooth the data. A threshold of 3.5 will signal if a datapoint is 3.5 standard deviations away from the moving mean. And an influence of 0.5 gives signals half of the influence that normal datapoints have. Likewise, an influence of 0 ignores signals completely for recalculating the new threshold. An influence of 0 is therefore the most robust option (but assumes stationarity); putting the influence option at 1 is least robust. For non-stationary data, the influence option should therefore be put somewhere between 0 and 1.

### Parameters

* parameters: Key of self.data to apply the test. (string or list of strings)
* window: The lag of the moving window. Minimun value = 3. If it is 0, the window is the 10% of the length of data with a maximum value of 100. (int)
* threshold: The z-score at which the algorithm signals. (float)
* influence: The influence (between 0 and 1) of new signals on the mean and standard deviation. (float)
* flag: Flag value to write on the signal values. (int)
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
