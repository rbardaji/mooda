# EGIM.instruments(*observatory*)

It represents the instruments deployed in an EGIM observatory.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str

Returns | Description | Type
--- | --- | ---
(statusCode, instrumentList) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), list with dictionaries of available instruments) | (int, list of dict{"name": "string", "sensorLongName": "string", "sensorType": "string", "sn": "string"})

Return to the [EGIM Index](index_egim.md).
