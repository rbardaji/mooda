""" Implementation of WaterFrame.qc_flat_test(parameters=None, window=2, flag=4) """


def qc_flat_test(self, parameters=None, window=3, flag=4, inplace=True):
    """
    It detects if there are equal consecutive values in the time series.

    Parameters
    ----------
        parameters: string or list of strings, optional
        (parameters = None)
            Parameter to apply the test.
        window: int, optional (window = 3)
            Size of the moving window of values to calculate the mean.
            If it is 0, the function calculates the optimal window.
        flag: int, optional (flag = 4)
            Flag value to write in on the fail test values.
        inplace: bool
            If True, it changes the flags in place and returns True.
            Otherwhise it returns an other WaterFrame.

    Returns
    -------
        new_wf: WaterFrame
    """
    if parameters is None:
        parameters = self.parameters
    elif isinstance(parameters, str):
        parameters = [parameters]

    if window == 0:
        window = 2

    df_rolling = self.data.rolling(window).std()

    data = self.data.copy()

    for parameter in parameters:
        if '_QC' in parameter:
            return False
        else:
            data.loc[df_rolling[parameter] == 0, parameter + '_QC'] = flag

    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf
