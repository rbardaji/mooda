# WaterFrame.drop(*keys*, *flags*=*None*)

Remove input keys (and associated QC keys) from self.data.

Parameters | Description | Type
--- | --- | ---
key | keys of self.data to drop. | list of str
flags | Number of flag to drop. It can be None, int or a list of int. If it is None, column will be deleted. | list of int, , int, None

Returns | Description | Type
--- | --- | ---
True/False | It indicates if the process was successfully. | bool

Return to the [WaterFrame Index](index_waterframe.md).
