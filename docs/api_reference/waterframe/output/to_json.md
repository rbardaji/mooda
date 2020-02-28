# WaterFrame.to_json()

## Reference

Get a JSON with the WaterFrame information.

### Returns

* json_string: JSON. (str)

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

wf_json = wf.to_json()
print(f'{wf_json[: 50]}...') # Print the first 50 characters of the JSON
```

Output:

```shell
{"metadata": {"platform_code": "OBSEA", "platform_...
```

Return to [mooda.WaterFrame](../waterframe.md).
