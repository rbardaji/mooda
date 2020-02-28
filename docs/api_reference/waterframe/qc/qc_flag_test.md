# WaterFrame.qc_flat_test(*parameters*=*None*, *window*=*3*, *flag*=*4*, *inplace*=*True*)

## Reference

It detects if there are equal consecutive values in the time series.

### Parameters

* parameters: Parameter to apply the test. (str, list of str)
* window: Size of the moving window of values to calculate the mean. If it is 0, the function calculates the optimal window. (int)
* flag: Flag value to write in on the fail test values. (int)
* inplace: If True, it changes the flags in place and returns True. Otherwhise it returns an other WaterFrame. (bool)

### Returns

* new_wf: WaterFrame

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md
import matplotlib.pyplot as plt

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

wf.qc_flat_test()
```

Return to [mooda.WaterFrame](../waterframe.md).
