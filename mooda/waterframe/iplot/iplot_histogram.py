import plotly.express as px


def iplot_histogram(self, x='TIME', nbins=None, **kwds):
    """
    It uses plotly.express.histogram.
    Each data point is represented as a marker point, whose location is given by the x and y columns
    of self.data.

    Parameters
    ----------
        x: str
            X axes, column or index of data.
        nbins: int
            By default, the number of bins is chosen so that this number is comparable to the
            typical number of samples in a bin. This number can be customized, as well as the range of values.
        **kwds: keywords
            plotly express scatter keywords.

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """

    df = self.data.copy()

    fig = px.histogram(df, x=x, nbins=nbins)

    return fig
