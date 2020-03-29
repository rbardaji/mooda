# mooda.md5(*file_path*, *save_dm5*=*True*, *md5_path*=*None*)

## Reference

It generates the MD5 code of the input file. It saves the code into a file if it save_md5 is True. It saves the code into the text file of 'md5_path'. If md5_path is None, the name of the file is the same as the input file with the md5 extension.

### Parameters

* file_path: Path of the file to make the MD5. (str)
* save_md5: If save_md5 is True, it creates a file with the MD5. (bool)
* md5_path: Path of the MD5 file. If md5_path is None, the name of the file is the same as the input file with the md5 extension. (path)

### Returns

* haser: MD5 code. (str)

### Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201402.nc](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA_201402.nc).

```python
import mooda as md


md5_string = md.md5("MO_TS_MO_OBSEA_201402.nc")
print(md5_string)
```

Output:

```shell
aff8d84c53f38e5525fd312f38d1e4cf
```

*Note: The script also makes a file called MO_TS_MO_OBSEA_201402.md5 with the MD5 code.*

Return to [mooda.WaterFrame](../index_api_reference.md).
