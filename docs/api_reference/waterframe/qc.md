# WaterFrame.qc(*self*, *parameters*=*None*, *window*=*0*, *threshold*=*3*, *bad_flag*=*4*, *good_flag*=*1*)

Auto QC process. It is the same that:

    self.reset_flag(parameters)
    self.range_test(parameters, flag=bad_flag)
    self.spike_test(parameters, window=window, threshold=threshold, flag=bad_flag)
    self.flat_test(parameters, window=window, flag=bad_flag)
    self.flag2flag(parameters, original_flag=0, translated_flag=good_flag)

## Parameters

    parameters: string, list of strings optional (parameters = None)
        Key of self.data to apply the test.
    window: int, optional (window = 0)
        Size of the moving window of values to calculate the mean.
        If it is 0, the function calculates the optimal window.
    threshold: int, optional (threshold = 3)
        The z-score at which the algorithm signals.
    bad_flag: int, optional (flag = 4)
        Flag value to write in on the fail values.
    good_flag: int, optional (flag = 1)
        Flag value to write in on the good values.

## Returns

    True/False: bool
        The operation is (not) successful.

Return to the [WaterFrame Index](index_waterframe.md).
