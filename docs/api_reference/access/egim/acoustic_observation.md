# EGIM.acoustic_observation(*self*, *observatory*, *instrument*, *date*, *hour_minute*)

Gets an Acoustic file for a specific EGIM instrument of an EGIM Observatory.

Parameters | Description | Type
--- | --- | ---
observatory | EGIM observatory name. | str
instrument | Instrument name. | str
date | Date of Acoustic file. The date format is dd/MM/yyyy. | str
hour_minute | Hour and Minute of an Acoustic file. The Hour Minute format is HHMM. | str

Returns | Description | Type
--- | --- | ---
(statusCode, text) | ([Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), text of the acoustic file) | (int, str)

Return to the [EGIM Index](index_egim.md).
