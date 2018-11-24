# WaterFrame.qc(*key*="all", *window*=*3*, *threshold*=*3*, *bad_flag*=*4*, *good_flag*=*1*)

Auto QC process.

Parameters | Description | Type
--- | --- | ---
key | key of self.data to apply the test. If key is all, the test will be applied to all keys | str
window | Size of the moving window of values to calculate the mean. If it is 0, the function calculates the optimal window. | int
threshold | Flag value to write in on the fail values. | int
bad_flag | key of self.data to apply the test. | str
good_flag | Flag value to write in on the good values. | int
