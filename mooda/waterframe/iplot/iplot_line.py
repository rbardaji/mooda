import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def iplot_line(self, y, x='TIME', marginal_x=None, marginal_y='histogram', color='DEPTH',
               range_y='auto', line_shape='spline', **kwds):
    """
    It uses plotly.express.line.
    Each data point is represented as a marker point, whose location is given by the x and y columns
    of self.data.

    Parameters
    ----------
        y: str
            Y axes, column or index of data.
        x: str
            X axes, column or index of data.
        color: str
            Name of a column or index of data. Values from this column are used to assign color to
            marks. If color = 'auto', color = QC column of y.
        range_y: list
            [min value, max value] of y axes. If range_y = 'auto', range is generated between the
            mina nd max values of y axes +- 5%.
        line_shape: str
            Line options: 'linear' 'spline', 'vhv', 'hvh', 'vh', 'hv'
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

    if color == 'DEPTH':
        df[color] = _df[color].astype('str')
    elif color:
        df[color] = _df[color]

    # Save memory
    del _df

    # Dropna
    df.dropna(inplace=True)

    # Sort index TIME
    df.set_index('TIME', inplace=True)
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)

    fig = px.line(df, x=x, y=y, color=color,
                  range_y=range_y,
                  line_shape=line_shape,
                  labels={
                      y: self.vocabulary[y].get('units', y)},
                  **kwds)

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(margin=dict(l=30, r=0, t=30, b=0))

    if 'QC' in color:
        fig.for_each_trace(
            lambda trace: trace.update(
                visible='legendonly',
                mode='markers',
                marker_color='red') if trace.name == 'Bad data' else (),
        )
        fig.for_each_trace(
            lambda trace: trace.update(
                mode='lines+markers',
                marker_color='blue',
                line_color='blue') if trace.name == 'Good data' else (),
        )

    return fig
