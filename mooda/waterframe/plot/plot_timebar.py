""" Implementation of WaterFrame.plot_bar(key, ax=None, average_time=None)"""
import datetime

def plot_timebar(self, keys, ax=None, time_interval_mean=None,  ylim='auto'):
    """
    Make a bar plot of the input keys.
    The bars are positioned at x with date/time. Their dimensions are given by height.

    Parameters
    ----------
        keys: list of str
                keys of self.data to plot.
        ax: matplotlib.axes object, optional (ax = None)
            It is used to add the plot to an input axes object.
        time_interval_mean: str, optional (time_interval_mean = None)
            It calculates an average value of a time interval. You can find
            all of the resample options here:
            https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
        ylim: 2-tuple/list, None, 'auto'
            Y axis limit. If ylim = 'auto'
    Returns
    -------
        ax: matplotlib.AxesSubplot
            Axes of the plot.
    """

    def format_year(x):
        return datetime.datetime.\
            strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y')

    def format_day(x):
        return datetime.datetime.\
            strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    # Extract data
    df = self.data[keys].dropna().reset_index().set_index('TIME')
    df.index.rename("Date", inplace=True)

    # Delete DEPTH, we are not going to use it in this case
    if 'DEPTH' in df.keys():
        del df['DEPTH']

    # Resample data
    if time_interval_mean is None:
        pass
    else:
        df = df.resample(time_interval_mean).mean()

    # Get min and max values for ylim
    if ylim == 'auto':
        # df.min() returns a Series or DataFrame with the min of each column
        y_min = min(df.min().values)
        y_max = max(df.max().values)
        y_percent = (y_max - y_min) / 100
        ylim = (y_min - 5 * y_percent, y_max + 5 * y_percent)

    if isinstance(keys, list):
        ax = df[keys].plot.bar(ax=ax, legend=True, ylim=ylim)
    else:
        ax = df[keys].plot.bar(ax=ax, ylim=ylim)
        # Write axes
        try:
            ax.set_ylabel(self.vocabulary[keys]['units'])
        except KeyError:
            print("Warning: We don't know the units of", keys,
                    "Please, add info into self.meaning[", keys, "['units']")

        if time_interval_mean == 'A':
            ax.set_xticklabels([format_year(x.get_text())
                                for x in ax.get_xticklabels()], rotation=60)
        elif time_interval_mean == 'D':
            ax.set_xticklabels([format_day(x.get_text())
                                for x in ax.get_xticklabels()], rotation=60)
        elif time_interval_mean == 'M':
            ax.set_xticklabels([format_day(x.get_text())
                                for x in ax.get_xticklabels()], rotation=60)

    return ax
