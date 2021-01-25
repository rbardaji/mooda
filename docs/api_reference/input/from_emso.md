# mooda.from_emso(*platform_code*, *parameters*=*[]*, *start_time*=*''*, *end_time*=*''*, *depth_min*=None, *depth_max*=None, *user*=*''*, *password*=*''*, *size*=*10*)

## Reference

Get a WaterFrame with the data of the EMSO API (api.emso.eu).

### Parameters

* user: Login for the EMSO ERIC API (str)
* password: Password for the EMSO ERIC API (str)
* platform_code: Data filtered by platform_code (str)
* parameters: List of parameters to get data (List[str])
* start_time: First date of the measurement (str)
* end_time: Last date of the measurement (str)
* depth_min: Minimum depth of the measurement (float)
* depth_max: Maximum depth of the measurement (float)
* size: Number of values (int)

### Returns

wf: WaterFrame

## Example

```python
import mooda as md

wf = md.from_emso(platform_code='ANTARES', parameters=['TEMP'],
                  start_time='2013-01-01 00:00:00',
                  end_time='2014-01-01 00:00:00', size=80000)

print(wf)
```

Output:

```
Memory usage: 11.776 KBytes
Parameters:
  - TEMP: Parameter without meaning
    - Min value: 13.232633813222249
      - DEPTH: 2193.0
      - TIME: 2013-04-20 00:00:00
    - Max value: 13.358148854188245
      - DEPTH: 2303.0
      - TIME: 2013-07-17 00:00:00
    - Mean value: 13.264398355267707
```

Return to [API reference](../index_api_reference.md).
