# WaterFrame.to_pkl(*path*)

## Reference

It saves the WaterFrame into a pickle file.

### Parameters

* path: Path to save the pickle file (str).

### Returns

* True: If the internal functions of this method do not raise any error, the return is always true (bool).

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same pyhon script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

# Save the wf into a pickle file
wf.to_pkl("example.pkl")
print("Pickle created.")
```

Output:

```
Pickle created.
```

Return to [mooda.WaterFrame](../waterframe.md).
