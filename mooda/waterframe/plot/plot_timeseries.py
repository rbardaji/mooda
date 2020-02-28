""" Implementation of WaterFrame.plot_timeseries(keys=None, rolling=None, ax=None,
average_time=None, secondary_y=False, color=None)"""


def plot_timeseries(self, parameters_to_plot=None, qc_flags=None, rolling_window=None, ax=None,
                    average_time=None, secondary_y=None, color=None):
    """
    Plot the input parameters with time on X and the parameters on Y. It calculates the
    standar deviation of a rolling window and plot it.

    Parameters
    ----------
        parameters_to_plot: list of str, str, optional (parameters_to_plot = None)
            Parameters of the WaterFrame to plot. If parameters_to_plot is None, all parameters
            will be ploted.
        qc_flags: list of int, optional (qc_flags = None)
            QC flags of the parameters to plot. If qc_flags in None, all QC flags will be used.
        rolling_window: int, optional (rolling_window = None)
            Size of the moving window. It is the number of observations
            used for calculating the statistic.
        ax: matplotlib.axes object, optional (ax = None)
            It is used to add the plot to an input axes object.
        average_time: str, optional (average_time = None)
            It calculates an average value of a time interval. You can find
            all of the resample options here:
            http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        secondary_y: bool, optional (secondary_y = False)
            Plot on the secondary y-axis.
        color: str or list of str, optional (color = None)
            Any matplotlib color. It will be applied to the traces.
    Returns
    -------
        ax: matplotlib.AxesSubplot
            Axes of the plot.
    """
    def make_plot(df_in, parameter_name, ax_in, color_in, rolling_in):
        """
        It makes the graph.

        Parameters
        ----------
            df_in: pandas.DataFrame
                It contains the info to plot.
            parameter_name: str
                Name of the parameter to plot.
            ax_in: matplotlib.axes
                Axes to add the plot.
            color_in: str
                Color of the line.
            rolling_in: int
                Size of the rolling window to calculate the mean and standar deviation.

        Returns
        -------
            ax_out: matplotlib.axes
                Axes with the plot.
        """
        # Calculation of the std and the mean
        roll = df_in[parameter_name].rolling(rolling_in, center=True)
        m = roll.agg(['mean', 'std'])
        # rename 'mean' column
        m.rename(columns={'mean': parameter_name}, inplace=True)
        m.dropna(inplace=True)
        ax_out = m[parameter_name].plot(ax=ax_in, secondary_y=secondary_y, legend=True,
                                        color=color_in)
        ax_out.fill_between(m.index, m[parameter_name] - m['std'], m[parameter_name] + m['std'],
                            alpha=.25, color=color_in)
        ax_out.legend([f"{parameter_name} at depth: {df_in['DEPTH'].mean()}"])
        # Write axes
        try:
            ax_out.set_ylabel(self.vocabulary[parameter_name]['units'])
        except KeyError:
            # No units
            pass

        return ax_out

    if parameters_to_plot is None:
        parameters_to_plot = self.parameters
    elif isinstance(parameters_to_plot, str):
        parameters_to_plot = [parameters_to_plot]

    # Extract data
    # Dropna is necessary?
    df = self.data[parameters_to_plot].dropna().reset_index()
    # df = self.data[parameters_to_plot].dropna().reset_index().set_index('TIME')
    df = df.groupby(['DEPTH', 'TIME'])[parameters_to_plot].mean()
    # print(df2)
    df.reset_index(inplace=True)
    df.set_index('TIME', inplace=True)

    for _, df_depth in df.groupby('DEPTH'):
        df_depth.index.rename("Date", inplace=True)
        df_depth.sort_index(inplace=True)

        # Resample data
        if average_time is None:
            pass
        else:
            df_depth = df_depth.resample(average_time).mean()

        # Calculation of the rolling value
        if rolling_window is None:
            if df_depth.size <= 100:
                rolling_window = 1
            elif df_depth.size <= 1000:
                rolling_window = df_depth.size//10
            elif df_depth.size <= 10000:
                rolling_window = df_depth.size // 100
            else:
                rolling_window = df_depth.size // 1000

        if color is None:
            for parameter_to_plot in parameters_to_plot:
                ax = make_plot(df_depth, parameter_to_plot, ax, color, rolling_window)
        else:
            for parameter_to_plot, color_to_plot in zip(parameters_to_plot, color):
                ax = make_plot(df_depth, parameter_to_plot, ax, color_to_plot, rolling_window)

    return ax
