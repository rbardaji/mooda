import plotly.express as px


def iplot_histogram(self, parameter='', nbins=None, show_median=False, **kwds):
    """
    It uses plotly.express.histogram.
    Each data point is represented as a marker point, whose location is given by the x and y columns
    of self.data.

    Parameters
    ----------
        parameter: str
            x axes, column or index of data.
        nbins: int
            By default, the number of bins is chosen so that this number is comparable to the
            typical number of samples in a bin. This number can be customized, as well as the range of values.
        **kwds: keywords
            plotly express scatter keywords.

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """

    if parameter:
        _df = self.data.copy()
        _df.reset_index(inplace=True)
        df = _df[[parameter, 'TIME', 'DEPTH']].copy()

        fig = px.histogram(df, x=parameter, nbins=nbins, **kwds)

        if show_median:
            mean = df[parameter].mean()
            print(mean)
            text = dict(
                x=mean, y=0.95, xref='x', yref='paper',
                showarrow=False, xanchor='left', text=f'Mean: {mean:.3f}')
            shape = dict(
                x0=mean,
                x1=mean,
                y0=0, y1=1,
                xref='x',
                yref='paper',
                line_width=2)
            
            fig.update_layout(
                shapes=[shape],
                annotations=[text])
    else:

        fig = px.histogram(dnbins=nbins, **kwds)

    return fig
