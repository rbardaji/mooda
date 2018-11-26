# EGIM.observation(*observatory*, *instrument*, *parameter*, *startDate*=*None*, *endDate*=*None*, *limit*=*None*)

Gets the time-series of a specific EGIM parameter in a certain  time range or  the last X (limit) values for an EGIM instrument of an EGIM observatory.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
instrument | Instrument name. | str
parameter | Parameter name. | str
startDate | Beginning date for the time series range. The date format is dd/MM/yyyy. If the start time is not supplied, we are going to use 'limit'. | str
endDate | End date for the time series range. The date format is dd/MM/yyyy. If the end time is not supplied, the current time will be used. | str
limit | The last x-measurements. | str

Returns | Description | Type
--- | --- | ---
(statusCode, data) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), list of DataFrame) | (int, list with dict of parameters)
