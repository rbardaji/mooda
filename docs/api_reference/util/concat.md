# mooda.concat(*list_wf*)

## Reference

The concat function does all of the heavy lifting of performing concatenation operations between a list of WaterFrames.

### Parameters

* list_wf: List of WaterFrames to be concatenated. (List of WaterFrames)

### Returns

* wf_one: WaterFrame with input data, metadata, and vocabulary concatenated. (WaterFrame)

## Example

To reproduce the example, download the NetCDF files [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA_201401.nc) and [MO_TS_MO_OBSEA_201402.nc](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA_201402.nc).

```python
import mooda as md

path_obsea_january = "MO_TS_MO_OBSEA_201401.nc"
path_obsea_february = "MO_TS_MO_OBSEA_201402.nc"

wf_january = md.read_nc_emodnet(path_obsea_january)
wf_february = md.read_nc_emodnet(path_obsea_february)

print('Range time from wf_january:',
      f"{wf_january.metadata.get('time_coverage_start')} -",
      f"{wf_january.metadata.get('time_coverage_end')}")
print('Range time from wf_february: ',
      f"{wf_february.metadata.get('time_coverage_start')} -",
      f"{wf_february.metadata.get('time_coverage_end')}")

wf_january_february = md.concat([wf_january, wf_february])

print('Range time from wf_january_february:',
      f"{wf_january_february.metadata.get('time_coverage_start')} -",
      f"{wf_january_february.metadata.get('time_coverage_end')}")
```

Output:

```shell
Range time from wf_january: 2014-01-19T00:00:00Z - 2014-01-31T23:00:00Z
Range time from wf_february:  2014-02-01T00:00:00Z - 2014-02-28T23:00:00Z
Range time from wf_january_february: 2014-01-19T00:00:00Z - 2014-02-28T23:00:00Z
```

Return to [mooda.WaterFrame](../index_api_reference.md).
