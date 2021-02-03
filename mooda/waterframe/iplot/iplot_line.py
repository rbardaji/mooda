import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def iplot_line(self, y, x='TIME', marginal_x=None, marginal_y='histogram', color='auto',
               range_y='auto', line_shape='linear', rangeslider_visible=True, line_group='DEPTH',
               **kwds):
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
        rangeslider_visible: bool
            Show a time range slide on the bottom x axes.
        line_group: str or int or Series or array-like
            Either a name of a column in wf.data, or a pandas Series or array_like object.
            Values from this column or array_like are used to group rows of data_frame into lines.
        **kwds: keywords
            plotly express scatter keywords.

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """
    df = pd.DataFrame()
    _df = self.data.reset_index()

    df[y] = _df[y]
    df[f'{y}_QC'] = _df[f'{y}_QC']
    df[x] = _df[x]

    if 'DEPTH' in _df.keys():
        df['DEPTH'] = _df['DEPTH']

    # Range Y calculation
    y_min = min(df[y].values)
    y_max = max(df[y].values)
    y_percent = (y_max - y_min) / 100

    if range_y == 'auto':
        range_y = [y_min - 5* y_percent, y_max + 5* y_percent]

    # Save memory
    del _df

    # Dropna
    df.dropna(inplace=True)

    if 'DEPTH' in df.keys() and 'TIME' in df.keys():
        # Sort by TIME AND DEPTH
        df.sort_values(['DEPTH', 'TIME'], inplace=True)
    elif 'TIME' in df.keys():
        df.sort_values(['TIME'], inplace=True)

    if color == 'DEPTH':
        df[color] = df[color].astype('str')
    elif color == 'auto':
        color = f'{y}_QC'
    # elif color:
    #     df[color] = df[color]

    # # Set index TIME
    # df.set_index('TIME', inplace=True)
    # df.sort_index(inplace=True)
    # df.reset_index(inplace=True)

    fig = px.line(df, x=x, y=y, color=color, range_y=range_y,
                  line_shape=line_shape,
                  labels={
                      y: self.vocabulary[y].get('units', y)},
                  line_group=line_group,
                  **kwds)

    fig.update_xaxes(rangeslider_visible=rangeslider_visible)
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
    elif 'DEPTH' in color:
        fig.for_each_trace(
            lambda trace: trace.update(mode='lines+markers'))

    return fig
