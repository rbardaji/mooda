# WaterFrame.to_nc(*path*, *nc_format*=*"NETCDF4"*)

## Reference

It saves the WaterFrame into a NetCDF.

### Parameters

* path: Path to save the NetCDF (str).
* nc_format: Specify the NetCDF format (NETCDF3_64BIT, ‘NETCDF3_CLASSIC’, NETCDF4, NETCDF4_CLASSIC) (str).
  * NETCDF4: Data is stored in an HDF5 file, using netCDF4 API features.
  * NETCDF4_CLASSIC: Data is stored in an HDF5 file, using only netCDF 3 compatible API features.
  * NETCDF3_64BIT: 64-bit offset version of the netCDF 3 file format, which fully supports 2+ GB files, but is only compatible with clients linked against netCDF version 3.6.0 or later.
  * NETCDF3_CLASSIC: The classic netCDF 3 file format. It does not handle 2+ GB files very well.

### Returns

* True: If the internal functions of this method do not raise any error, the return is always true (bool).

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

# Print parameters
print(f"WaterFrame original parameters: {(', ').join(wf.parameters)}")
# Delete all parameters except 'TEMP'
wf2 = wf.use_only('TEMP', inplace=False)
print(f"New WaterFrame parameters: {(', ').join(wf.parameters)}")


# Save the new wf into a NetCDF with the name "example_TEMP.nc"
wf2.to_nc("example_TEMP.nc")
print("NetCDF created.")
```

Output:

```shell
WaterFrame original parameters: DEPH, ATMS, CNDC, DRYT, PRES, PSAL, SVEL, TEMP, WDIR, WSPD
New WaterFrame parameters: DEPH, ATMS, CNDC, DRYT, PRES, PSAL, SVEL, TEMP, WDIR, WSPD
NetCDF created.
```

Return to [mooda.WaterFrame](../waterframe.md).
