# mooda.emso.get_data(*depth_max*=*None*, *depth_min*=*None*, *depth_qcs*=*[]*, *end_time*=*''*, *metadata_ids*=*[]*, *size*=*10*, *sort*=*'desc'*, *parameters*=*[]*, platform_codes:List[str]=[], start_time:str='', *time_qcs*=*[]*, *value_qcs*=*[]*)

## Reference

Get data from the EMSO ERIC API.

### Parameters

* depth_max: Maximun depth of the measurement (int)
* depth_min: Minimum depth of the measurement (int)
* depth_qcs: List of QC values accepted for the depth_qc field (List[int])
* end_time: Maximum date of the measurement (str)
* metadata_ids: List of accepted 'metadata_id' (List[str])
* size: Number of values to be returned (int)
* sort: Options -> 'asc' or 'desc'. Get the first or last (in time) measurements (str)
* parameters: List of accepted 'parameter' (List[str])
* platform_codes: List of accepted 'platform_code' (List[str])
* start_time: Minimun date of the meassurement (str)
* time_qcs: List of accepted values for the field time_qc (List[int])
* value_qcs: List of accepted values for the field of value_qc (List[int])

### Returns

* data_list: The data (List[dict])

### Example

```python
import mooda as md
import pprint  # For nice printing

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

metadatas = emso.get_metadata()
for metadata in metadatas:      
    pprint.pprint(metadata)
```

Output:

```
{'area': 'Mediterranean',
 'depth': '2367.294921875',
 'depth_qc': 0,
 'institution': 'MIO UMR7294 CNRS / OSU Pytheas',
 'location': {'lat': '42.793', 'lon': '6.038'},
...
...
...
 'time': '2020-11-09 23:31:10',
 'time_qc': 0,
 'units': 'dbar',
 'value': '2195.3310546875',
 'value_qc': 0}
```

Return to [Index](../../index_api_reference.md).
