# WaterFrame.flat_test(*key*, *window*=*3*, *flag*=*4*)

It detects no changes in values of time-series.

Parameters | Description | Type
--- | --- | ---
key | key of self.data to apply the test. | str
window | Size of the moving window of values to calculate the mean.If it is 0, the function calculates the optimal window. | int
flag | Flag value to write in on the fail values. | int

Returns | Description | Type
--- | --- | ---
outlier_idx | Array with the flags result of the test. | numpy array

Return to the [WaterFrame Index](index_waterframe.md).