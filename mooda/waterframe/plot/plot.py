""" Implementation of WaterFrame.plot(**kwds)"""


def plot(self, **kwds):
    """
    It calls the pandas DataFrame.plot() method.

    Parameters
    ----------
        **kwds: arguments
            pandas plot() arguments.

    Returns
    -------
        axes : matplotlib.axes.Axes or numpy.ndarray of them
    """
    axes = self.data.plot(**kwds)
    return axes
