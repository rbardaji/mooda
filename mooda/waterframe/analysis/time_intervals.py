""" Implementation of WaterFrame.data_intervals(parameter) """


def time_intervals(self, parameter, frequency):
    """
    It returns the index (TIME) of intervals between NaNs.

    Parameters
    ----------
        parameter: str
            Column name of WaterFrame.data.
        frequency: DateOffset, Timedelta or str
            Theorical sample frequency.

    Returns
    -------
        intervals: [(str, str)]
            List of tuples with the start and end index (TIME) of each interval of
            data.
    """
    # Creation of the DataFrame with the required info
    df = self.data.copy()

    df.reset_index(inplace=True)
    df.set_index('TIME', inplace=True)
    df.sort_index(inplace=True)

    # print(df[parameter]['2014-01-19 00:00:00'])
    df = df.resample(frequency).mean()

    # Creation of a timeseries with the positions of null values
    ts = df[parameter].isnull()

    # Check where are the intervals
    intervals = []
    in_interval = False
    end = None
    for index, value in ts.items():
        end = index.strftime('%Y-%m-%d %H:%M:%S')
        if in_interval is False and value is False:
            in_interval = True
            start = index.strftime('%Y-%m-%d %H:%M:%S')
        elif in_interval is True and value is True:
            in_interval = False
            intervals.append((start, end))
    if in_interval is True:
        intervals.append((start, end))

    return intervals
