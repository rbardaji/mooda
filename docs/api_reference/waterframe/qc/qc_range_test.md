# WaterFrame.qc_range_test(*parameters*=*None*, *limits*=*None*, *flag*=*4*, *inplace*=*True*)

## Reference

Check if the values of a parameter are out of range.

### Parameters

* parameters: Parameter to apply the test. (str, list of str)
* limits: (Min value, max value) of the range of correct values. (tuple or list)
* flag: Flag value to write in on the fail test values. (int)
* inplace: If True, it changes the flags in place and returns True. Otherwhise it returns an other WaterFrame. (bool)

### Returns

* new_wf: WaterFrame

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

ok = wf.qc_range_test()

if ok:
    print("Range test applied.")
```

Output:

```shell
Range test applied.
```

Return to [mooda.WaterFrame](../waterframe.md).
