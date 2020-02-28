"""
Implementation of WaterFrame.plot_hist(parameter=None, mean_line=False, **kwds)
"""

def plot_hist(self, parameters=None, mean_line=False, **kwds):
    """
    Make a histogram of the WaterFrame's.
    A histogram is a representation of the distribution of data.
    This function calls pandas.DataFrame.hist(), on each parameter of the
    WaterFrame, resulting in one histogram per parameter.

    Parameters
    ----------
        parameters: str, list of str, optional (parameters=None)
            keys of self.data to plot. If parameters=None, it will plot all
            parameters.
        mean_line: bool, optional (mean_line=False)
                It draws a line representing the average of the values.
        **kwds:
            All other plotting keyword arguments to be passed to
            DataFrame.hist().
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.hist.html
    Returns
    -------
        ax: matplotlib.AxesSubplot
            Axes of the plot.
    """

    if parameters is None:
        parameters = list(self.parameters)

    if isinstance(parameters, str):
        parameters = [parameters]

    axes = self.data.hist(column=parameters, **kwds)
    parameter_counter = 0
    try:
        for ax in axes:
            ax.set_xlabel("Values")
            ax.set_ylabel("Frequency")
            if mean_line is True:
                if parameter_counter < len(parameters):
                    x_mean = self.mean(parameters[parameter_counter])
                    ax.axvline(x_mean, color='k',
                                linestyle='dashed',
                                linewidth=1)

                    parameter_counter += 1
    except AttributeError:

        # Creation of the mean line
        parameter_counter = 0
        for irow in range(len(axes)):
            for icol in range(len(axes[irow])):
                if parameter_counter < len(parameters):
                    axes[irow, icol].set_xlabel("Values")
                    axes[irow, icol].set_ylabel("Frequency")
                    if mean_line is True:
                        x_mean = self.data[axes[irow, icol].get_title()].mean()
                        axes[irow, icol].axvline(x_mean, color='k',
                                                    linestyle='dashed',
                                                    linewidth=1)
                    parameter_counter += 1

    return axes
