# WaterFrame.qc_syntax_test()

## Reference

It checks whether the object data contains all the QC columns required to pass the rest of the tests.

### Returns

* success: The test has been successfully passed. (bool)
            
## Example

To reproduce the example, download the NetCDF file [here](../../../examples/data/MO_TS_MO_OBSEA_201402.nc) and save it as `MO_TS_MO_OBSEA_201402.nc` in the same python script folder.

```python
import mooda as md
import matplotlib.pyplot as plt

path = "MO_TS_MO_OBSEA_201402.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

ok = wf.qc_syntax_test()

if ok:
    print('The syntaxis of the data is correct')
else:
    print('The syntaxis of the data is not correct')
```

Output:

```
The syntaxis of the data is correct
```
Return to [mooda.WaterFrame](../waterframe.md).
