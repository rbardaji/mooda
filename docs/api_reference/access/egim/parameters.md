# EGIM.parameters(*self*, *observatory*, *instrument*)

Get the list of EGIM parameters for a specific EGIM instrument of an EGIM Observatory.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
instrument | Instrument name. | str

Returns | Description | Type
--- | --- | ---
(statusCode, parameterList) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), list of parameters) | (int, list of dictionaries)

parameterList contains dictionaries as follow:

```python
parameter = dict()
parameter['name'] = 'name of the parameter'
parameter['uom'] = 'units of measurement'
```

Return to the [EGIM Index](index_egim.md).
