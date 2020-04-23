# WaterFrame.to_csv(*path*=*None*)

## Reference

Create a CSV file with the WaterFrame data.
The metadata and vocabulary will be placed in the first lines of the file with a # as first character of the line.

### Parameters

* path: Location and filename of the csv file. If path is None, the filename will be the metadata['id']. (str)

### Returns

* path: Location and filename of the csv file.

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201402.nc](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA_201402.nc).

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201402.nc"
wf = md.read_nc_emodnet(path)

path_csv = wf.to_csv()

print(path_csv)
```

Output:

```shell
MO_TS_MO_OBSEA_201402.csv
```

Note: The example makes a CSV with the name and location of the output.

Return to [mooda.WaterFrame](../waterframe.md).
