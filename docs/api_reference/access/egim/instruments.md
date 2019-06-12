# EGIM.instruments(*self*, *observatory*)

It request the available instruments of a selected observatory to the EMSO DMP.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str

Returns | Description | Type
--- | --- | ---
(statusCode, instrumentList) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), list with dictionaries of available instruments) | (int, list of dictionaries)

instrumentList contains dictionaries as follow:

```python
instrument = dict()
instrument['name'] = 'name of the instrument'
instrument['sensorLongName'] = 'long name of the instrument'
instrument['sensorType'] = 'type of the instrument'
instrument['sn'] = 'Serial number of the instrument'
```

Return to the [EGIM Index](index_egim.md).
