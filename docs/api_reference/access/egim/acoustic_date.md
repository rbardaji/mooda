# EGIM.acoustic_date(*observatory*, *instrument*)

Gets the date list of available acoustic files observed by a specific EGIM instrument of an EGIM Observatory.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
instrument | Instrument name. | str

Returns | Description | Type
--- | --- | ---
(statusCode, data) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), list with dict of dates) | (int, list of dict{})
