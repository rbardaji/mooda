# WaterFrame.flat_test(*parameters*=*None*, *window*=*3*, *flag*=*4*)

It detects if there are equal consecutive values in the time series.

## Parameters

    parameters: string or list of strings, optional (parameters = None)
        key of self.data to apply the test.
    window: int, optional (window = 1)
        Size of the moving window of values to calculate the mean.
        If it is 0, the function calculates the optimal window.
    flag: int, optional (flag = 4)
        Flag value to write in on the fail values.

## Returns

    True/False: bool
        It indicates if the process is (not) successful.

Return to the [WaterFrame Index](index_waterframe.md).