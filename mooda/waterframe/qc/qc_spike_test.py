""" Implementation of WaterFrame.qc_spike_test(parameters=None, window=0, threshold=3, flag=4)"""
import numpy as np


def qc_spike_test(self, parameters=None, window=0, threshold=3, flag=4, inplace=True):
    """
    It checks if there is any spike in the time series.

    Parameters
    ----------
        parameters: string or list of strings, optional
        (parameters = None)
            key of self.data to apply the test.
        window: int, optional (window = 0)
            Size of the moving window of values to calculate the mean.
            If it is 0, the function calculates the optimal window.
        threshold: int, optional (threshold = 3)
            Maximum deference between the average of the moving window and the analyzed value
        flag: int, optional (flag = 4)
            Flag value to write in on the fail values.
        inplace: bool
            If True, it changes the flags in place and returns True.
            Otherwhise it returns an other WaterFrame.

    Returns
    -------
        new_wf: WaterFrame.
    """

    if parameters is None:
        parameters = self.parameters
    elif isinstance(parameters, str):
        parameters = [parameters]

    data = self.data.copy()

    for parameter in parameters:
        # Auto calculation of window
        if window == 0:
            window = int(len(data[parameter])/100)
            if window < 3:
                window = 3
            elif window > 100:
                window = 100

        signals = data[parameter].rolling(window=window, center=True).mean().fillna(method='bfill')
        difference = np.abs(data[parameter] - signals)
        outlier_idx = difference > threshold
        data.loc[outlier_idx, parameter + '_QC'] = flag
    
    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf

    return True
