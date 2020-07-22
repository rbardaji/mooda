""" Implementation of WaterFrame.qc_spike_test(parameters=None, window=0, threshold=3, flag=4)"""
import numpy as np


def qc_spike_test(self, parameters=None, window=0, threshold=3.5, influence=0.5, flag=4,
                  inplace=True):
    """
    Based on:
    https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data

    Algorithm based on the principle of dispersion: if a new datapoint is a given x number of
    standard deviations away from some moving mean, the algorithm signals (also called z-score).
    The algorithm is very robust because it constructs a separate moving mean and deviation, such
    that signals do not corrupt the threshold. Future signals are therefore identified with
    approximately the same accuracy, regardless of the amount of previous signals.
    
    For example, a window of 5 will use the last 5 observations to smooth
    the data. A threshold of 3.5 will signal if a datapoint is 3.5 standard deviations away
    from the moving mean. And an influence of 0.5 gives signals half of the influence that normal
    datapoints have. Likewise, an influence of 0 ignores signals completely for recalculating the
    new threshold. An influence of 0 is therefore the most robust option (but assumes stationarity);
    putting the influence option at 1 is least robust. For non-stationary data, the influence
    option should therefore be put somewhere between 0 and 1.

    Parameters
    ----------
        parameters: string or list of strings, optional
        (parameters = None)
            key of self.data to apply the test.
        window: int, optional (window = 0)
            The lag of the moving window.
            Minimun value = 3.
            If it is 0, the window is the 10% of the length of data with a maximum value of 100.
        threshold: float, optional (threshold = 3.5)
            The z-score at which the algorithm signals.
        influence: float, optional (influence = 0.5)
            The influence (between 0 and 1) of new signals on the mean and standard deviation.
        flag: int, optional (flag = 4)
            Flag value to write on the signal values.
        inplace: bool
            If True, it changes the flags in place and returns True.
            Otherwhise it returns an other WaterFrame.

    Returns
    -------
        new_wf: WaterFrame.
    """

    def thresholding_algo(y, lag, threshold, influence, signals, flag):
        filteredY = np.array(y)
        avgFilter = [0]*len(y)
        stdFilter = [0]*len(y)
        avgFilter[lag - 1] = np.mean(y[0:lag])
        stdFilter[lag - 1] = np.std(y[0:lag])
        for i in range(lag, len(y)):
            if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
                signals[i] = flag

                filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
                avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
                stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
            else:
                filteredY[i] = y[i]
                avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
                stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

        return np.asarray(signals)

    if parameters is None:
        parameters = self.parameters
    elif isinstance(parameters, str):
        parameters = [parameters]

    data = self.data.copy()

    for parameter in parameters:
        # Auto calculation of window
        if window == 0:
            window = round(len(data[parameter])*5/100)  # 5% of len
            if window < 3:
                window = 3
            elif window > 100:
                window = 100

        df = data[[parameter, f'{parameter}_QC']].reset_index()
        df.set_index('TIME', inplace=True)

        try:
            for depth, df_depth in df.groupby('DEPTH'):
                df_depth.sort_index(inplace=True)

                y = df_depth[parameter].values
                signals = df_depth[f'{parameter}_QC'].values

                # Run algo with settings from above
                result = thresholding_algo(y, lag=window, threshold=threshold,
                                        influence=influence, signals=signals,
                                        flag=4)
                
                data.loc[(depth,), f'{parameter}_QC'] = result
        except KeyError:
            # No Depth
            y = df[parameter].values
            signals = df[f'{parameter}_QC'].values

            # Run algo with settings from above
            result = thresholding_algo(y, lag=window, threshold=threshold,
                                    influence=influence, signals=signals,
                                    flag=4)
            
            data[f'{parameter}_QC'] = result
    
    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf

    return True
