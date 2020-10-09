import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def iplot_scatter(self, y, x='TIME', trendline=None, marginal_x=None, marginal_y='histogram',
                  color='auto', symbol='DEPTH', range_y='auto', **kwds):
    """
    It uses plotly.express.scatter.
    Each data point is represented as a marker point, whose location is given by the x and y columns
    of self.data.

    Parameters
    ----------
        y: str
            Y axis, column or index of data.
        x: str
            X axis, column or index of data.
        trendline: str
            Options:
                None
                'ols': Ordinary Least Squares regression line will be drawn for each
                    discrete-color/symbol group.
                'ols_np': Ordinary Least Squares regression line will be drawn for each
                    discrete-color/symbol group.
                    Line generated with numpy.polyfit with all values of y axes.
                'lowess': Locally Weighted Scatterplot Smoothing line will be drawn for each
                    discrete-color/symbol group.
        marginal_x: str
            If set, a horizontal subplot is drawn above the main plot, visualizing the
            x-distribution.
            Options: None, 'rug', 'box', 'violin', or 'histogram'.
        marginal_y: str
            If set, a horizontal subplot is drawn above the main plot, visualizing the
            y-distribution.
            Options: None, 'rug', 'box', 'violin', or 'histogram'.
        color: str
            Name of a column or index of data. Values from this column are used to assign color to
            marks. If color = 'auto', color = QC column of y.
        symbol: str
            Name of a column or index of data. Values from this column are used to assign symbols to
            marks.
        range_y: list
            [min value, max value] of y axes. If range_y = 'auto', range is generated between the
            min and max values of y axes +- 5%.
        **kwds: keywords
            plotly express scatter keywords.

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """
    df = pd.DataFrame()
    _df = self.data.reset_index()

    df[y] = _df[y]
    df[x] = _df[x]

    # Range Y calculation
    y_min = min(df[y].values)
    y_max = max(df[y].values)
    y_percent = (y_max - y_min) / 100

    if range_y == 'auto':
        range_y = [y_min - 5* y_percent, y_max + 5* y_percent]

    if color == 'auto':
        color = f'{y}_QC'
        df[color] = _df[color].astype('str')
    elif color:
        df[color] = _df[color]
    
    if symbol == 'DEPTH':
        df[symbol] = _df[symbol].astype('str')
    elif symbol:
        df[symbol] = _df[symbol]

    # Save memory
    del _df

    # Dropna
    df.dropna(inplace=True)

    # Sort index TIME
    df.set_index('TIME', inplace=True)
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)

    fig = px.scatter(
        df[100:150], x=x, y=y, trendline=trendline, marginal_x=marginal_x, marginal_y=marginal_y,
        color=color, symbol=symbol, range_y=range_y, **kwds)

    return fig
