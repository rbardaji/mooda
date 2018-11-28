# EGIM.parameters(*observatory*, *instrument*)

Get the list of EGIM parameters for a specific EGIM instrument of an EGIM Observatory.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
instrument | Instrument name. | str

Returns | Description | Type
--- | --- | ---
(statusCode, parameterList) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), list of dict of parameters) | (int, list of dict{"name": "string", "uom": "string"})

Return to the [EGIM Index](index_egim.md).
