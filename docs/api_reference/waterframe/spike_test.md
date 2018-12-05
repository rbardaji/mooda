# WaterFrame.spike_test(*parameters*, *window*=*0*, *threshold*=*3*, *flag*=*4*)

It checks if there is any spike in the time series.

## Parameters

    parameters: string or list of strings, optional
    (parameters = None)
        key of self.data to apply the test.
    window: int, optional (window = 0)
        Size of the moving window of values to calculate the mean.
        If it is 0, the function calculates the optimal window.
    threshold: int, optional (threshold = 3)
        The z-score at which the algorithm signals.
    flag: int, optional (flag = 4)
        Flag value to write in on the fail values.

## Returns

    True/False: bool
        It indicates if the process is (not) successful.

Return to the [WaterFrame Index](index_waterframe.md).
