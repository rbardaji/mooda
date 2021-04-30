from stockstats import StockDataFrame
import plotly.graph_objects as go


def iplot_candlestick(self, parameter="", interval="", show_macd=False,
                      xaxis_rangeslider_visible=False, title="", **kargs):
    """
    It uses https://plotly.com/python/candlestick-charts/.

    The candlestick chart is a style of financial chart describing open, high,
    low and close for a given x coordinate (most likely time). The boxes
    represent the spread between the open and close values and the lines
    represent the spread between the low and high values. Sample points
    where the close value is higher (lower) then the open value are called
    increasing (decreasing). By default, increasing candles are drawn in
    green whereas decreasing are drawn in red.

    Parameters
    ----------
        parameter: str
            Parameter of self.data
        interval:
            Interval for the candlestick boxes
        show_macd: bool
            Show the MACD indicator (Moving Average Convergence Divergence)
    """

    df = self.data.copy()
    df.reset_index(inplace=True)
    df.set_index(['TIME'], inplace=True)

    if parameter and interval:

        df_min = df.resample(interval).min()
        df_max = df.resample(interval).max()
        df_open = df.resample(interval).first()
        df_close = df.resample(interval).last()
        
        df = df_min.copy()
        df['low'] = df_min[parameter].copy()
        df['high'] = df_max[parameter].copy()
        df['open'] = df_open[parameter].copy()
        df['close'] = df_close[parameter].copy()


    if show_macd:
        df = StockDataFrame.retype(df)

        df['macd'] = df.get('macd') # calculate MACD

    df['0'] = 0

    fig = go.Figure(
        data=[go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'])])

    if show_macd:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['0'],
                line = dict(color='black'),
                name='0',
                showlegend=False))

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['macd'],
                line=dict(color='blue'),
                name='macd'))

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['macds'],
                line=dict(color='orange'),
                name='macds'))

        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['macdh'],
                name='macdh'))

    fig.update_layout(
        xaxis_rangeslider_visible=xaxis_rangeslider_visible,
        title=title)

    return fig
