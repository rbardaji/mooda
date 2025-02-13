""" Implementation of mooda.iplot_location() """
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from sklearn.linear_model import LinearRegression
import random

def iplot_line(wf_list, y, x='TIME', color='auto', range_y='auto',
               line_shape='spline', rangeslider_visible=False,
               line_group='DEPTH', resample=None, view_maxmin=True, trend=False,
               **kwds):
    """
    It uses plotly.express.line.
    Each data point is represented as a marker point, whose location is given by the x and y columns
    of self.data.

    Parameters
    ----------
        wf_list: List(WaterFrame)
            List of WaterFrame objects.
        y: str List[str]
            Y axes, columns of data (max 4 columns).
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
        resample: str
            Get the plot with resample data. If resample, color = 'DEPTH
            and each y is represented with a different simbol
        view_maxmin: bool
            Show the max and min values if data is resampled.
        trend: bool
            Show a linear regression of the trace.
        **kwds: keywords
            plotly express scatter keywords.

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """

     # Load all simbols
    raw_symbols = SymbolValidator().values
    symbols = []
    for i in range(1,len(raw_symbols),8):
        symbols.append(raw_symbols[i])

    list_y = []
    if isinstance(y, str):
        list_y = [y]
    else:
        list_y = y
    
    # Color configuration
    # fillcolor_list = [
    #     'rgba(0,100,80,0.2)',
    #     'rgba(0,176,246,0.2)',
    #     'rgba(231,107,243,0.2)',
    #     'rgba(240,184,48,0.2)',
    #     'rgba(245,71,26,0.2)',
    #     'rgba(227,245,65,0.2)',
    #     'rgba(0,0,0,0.2)',
    #     'rgba(94,86,245,0.2)',
    #     'rgba(157,49,245,0.2)',
    #     'rgba(255,0,0,0.2)',
    #     'rgba(0,255,0,0.2)',
    #     'rgba(0,0,255,0.2)',
    #     'rgba(0,100,100,0.2)']
    # line_color_list = [
    #     'rgb(0,100,80)',
    #     'rgb(0,176,246)',
    #     'rgb(231,107,243)',
    #     'rgb(240,184,48)',
    #     'rgb(245,71,26)',
    #     'rgb(227,245,65)',
    #     'rgb(0,0,0)',
    #     'rgb(94,86,245)',
    #     'rgb(157,49,245)',
    #     'rgb(255,0,0)',
    #     'rgba(0,255,0,0.2)',
    #     'rgba(0,0,255,0.2)',
    #     'rgba(0,100,100,0.2)']

    fillcolor_list = [
        'rgba(51,0,0,0.2)',
        'rgba(102,51,0,0.2)',
        'rgba(153,153,0,0.2)',
        'rgba(102,204,0,0.2)',
        'rgba(0,255,0,0.2)',
        'rgba(51,255,153,0.2)',
        'rgba(102,255,255,0.2)',
        'rgba(153,204,255,0.2)',
        'rgba(204,204,255,0.2)',
        'rgba(204,153,255,0.2)',
        'rgba(255,102,255,0.2)',
        'rgba(255,51,153,0.2)',
        'rgba(128,128,128,0.2)',
        'rgba(204,0,102,0.2)',
        'rgba(153,0,153,0.2)',
        'rgba(51,0,102,0.2)',
        'rgba(0,0,51,0.2)',
        'rgba(0,51,102,0.2)',
        'rgba(0,153,153,0.2)',
        'rgba(0,204,102,0.2)',
        'rgba(153,255,51,0.2)',
        'rgba(255,255,102,0.2)',
        'rgba(255,204,153,0.2)',
        'rgba(255,204,204,0.2)',
        'rgba(255,0,0,0.2)',
        'rgba(255,153,51,0.2)',
        'rgba(255,255,102,0.2)',
        'rgba(204,255,153,0.2)',
        'rgba(204,255,204,0.2)',
        'rgba(153,255,204,0.2)',
        'rgba(102,255,255,0.2)',
        'rgba(51,153,255,0.2)',
        'rgba(0,0,255,0.2)',
        'rgba(153,0,153,0.2)',
        'rgba(102,0,51,0.2)',
        'rgba(0,0,0,0.2)',]

    line_color_list = [
        'rgb(51,0,0)',
        'rgb(102,51,0)',
        'rgb(153,153,0)',
        'rgb(102,204,0)',
        'rgb(0,255,0)',
        'rgb(51,255,153)',
        'rgb(102,255,255)',
        'rgb(153,204,255)',
        'rgb(204,204,255)',
        'rgb(204,153,255)',
        'rgb(255,102,255)',
        'rgb(255,51,153)',
        'rgb(128,128,128)',
        'rgb(204,0,102)',
        'rgb(153,0,153)',
        'rgb(51,0,102)',
        'rgb(0,0,51)',
        'rgb(0,51,102)',
        'rgb(0,153,153)',
        'rgb(0,204,102)',
        'rgb(153,255,51)',
        'rgb(255,255,102)',
        'rgb(255,204,153)',
        'rgb(255,204,204)',
        'rgb(255,0,0)',
        'rgb(255,153,51)',
        'rgb(255,255,102)',
        'rgb(204,255,153)',
        'rgb(204,255,204)',
        'rgb(153,255,204)',
        'rgb(102,255,255)',
        'rgb(51,153,255)',
        'rgb(0,0,255)',
        'rgb(153,0,153)',
        'rgb(102,0,51)',
        'rgb(0,0,0)',]

    fig = go.Figure()

    for num_wf, wf in enumerate(wf_list):
        dash='solid'
        if num_wf == 1:
            dash = 'dash'
        elif num_wf == 2:
            dash = 'dot'
        elif num_wf > 2:
            dash = 'dashdot'


        _df = wf.data.reset_index()

        for y_num, one_y in enumerate(list_y):

            # yaxis config
            yaxis = 0
            if y_num == 0:
                yaxis = 'y'
            elif y_num == 1:
                yaxis = 'y2'
            elif y_num == 2:
                yaxis = 'y3'
            elif y_num == 3:
                yaxis = 'y4'
            else:
                raise 'Error, cannot add more than 4 "y" parameters'

            df = pd.DataFrame()
            df[one_y] = _df[one_y]
            df[f'{one_y}_QC'] = _df[f'{one_y}_QC']

            df[x] = _df[x]

            if 'DEPTH' in _df.keys():
                df['DEPTH'] = _df['DEPTH']

            # Range Y calculation
            y_min = min(df[one_y].values)
            y_max = max(df[one_y].values)
            y_percent = (y_max - y_min) / 100

            if range_y == 'auto':
                range_y = [y_min - 5* y_percent, y_max + 5* y_percent]

            # Dropna
            df.dropna(inplace=True)


            if 'DEPTH' in df.keys() and 'TIME' in df.keys():
                # Sort by TIME AND DEPTH
                df.sort_values(['DEPTH', 'TIME'], inplace=True)
            elif 'TIME' in df.keys():
                df.sort_values(['TIME'], inplace=True)

            if resample:
                color = 'DEPTH'

            if color == 'DEPTH':
                df[color] = df[color].astype('str')
            elif color == 'auto':
                color = f'{one_y}_QC'

            if resample:

                df_agg = df.groupby(
                    ['DEPTH'] + [pd.Grouper(freq=resample, key='TIME')]).agg(
                        {one_y: ['mean', 'max', 'min']})

                df_agg.reset_index(inplace=True)
                df_agg['mean'] = df_agg[one_y]['mean']
                df_agg['max'] = df_agg[one_y]['max']
                df_agg['min'] = df_agg[one_y]['min']           

                for color_comt, (depth, df_depth) in enumerate(df_agg.groupby('DEPTH')):
                    
                    # Create color
                    r_color = random.randint(0, 255)
                    g_color = random.randint(0, 255)
                    b_color = random.randint(0, 255)

                    df_depth.set_index('TIME', inplace=True)
                    df_depth['values_from_start'] = (df_depth.index - df_depth.index[0]).days
                    df_depth.reset_index(inplace=True)

                    x_time = df_depth['TIME']
                    x_days = df_depth['values_from_start']
                    x_rev = x_time[::-1]
                    y_mean = df_depth['mean']
                    y_max = df_depth['max']
                    y_min = df_depth['min']
                    y_min = y_min[::-1]

                    if trend:
                        reg = LinearRegression().fit(np.vstack(x_days), y_mean)
                        bestfit = reg.predict(np.vstack(x_days))

                        fig.add_trace(go.Scatter(
                            x=x_time,
                            y=bestfit,
                            name=f'trend-{wf.metadata["platform_code"]}-{one_y}-{depth}',
                            # line_shape=line_shape,
                            mode='lines+markers',
                            yaxis=yaxis,
                            marker_symbol=symbols[y_num],
                            line=dict(dash=dash)
                        ))

                    if view_maxmin:
                        fig.add_trace(go.Scatter(
                            x=pd.concat([x_time, x_rev]),
                            y=pd.concat([y_max, y_min]),
                            fill='toself',
                            # fillcolor=fillcolor_list[selected_color],
                            fillcolor=f'rgba({r_color},{g_color},{b_color},0.2)',
                            line_color='rgba(255,255,255,0)',
                            showlegend=True,
                            name=f'{wf.metadata["platform_code"]}-{one_y}-{depth}-MaxMin',
                            line_shape=line_shape,
                            yaxis=yaxis,
                            line=dict(dash=dash)
                        ))

                    fig.add_trace(go.Scatter(
                        x=x_time, y=y_mean,
                        # line_color=line_color_list[selected_color],
                        line_color=f'rgb({r_color},{g_color},{b_color})',
                        name=f'{wf.metadata["platform_code"]}-{one_y}-{depth}',
                        line_shape=line_shape,
                        yaxis=yaxis,
                        marker_symbol=symbols[y_num],
                        line=dict(dash=dash)))

                    fig.update_traces(mode='lines+markers')

                    # Update yaxis
                    fig.update_layout(xaxis=dict(title='Time'))
                    try:
                        if y_num == 0:
                            fig.update_layout(
                                yaxis=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})"))
                        elif y_num == 1:
                            fig.update_layout(
                                yaxis2=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})",
                                    side="right",
                                    overlaying="y"))
                        elif y_num == 2:
                            fig.update_layout(
                                xaxis=dict(
                                    domain=[0.07, 1],
                                    title='Time'
                                ))
                            fig.update_layout(
                                yaxis3=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})",
                                    overlaying="y",
                                    side="left",
                                    position=0))
                        elif y_num == 3:
                            fig.update_layout(
                                xaxis=dict(
                                    domain=[0.07, 0.93],
                                    title='Time'
                                ))
                            fig.update_layout(
                                yaxis4=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})",
                                    overlaying="y",
                                    side="right",
                                    position=1))
                    except:
                        pass

                # Add 'Depth' to legend
                fig.update_layout(legend_title={'text': 'Platform Code - Parameter - Depth (m)'})
            else:

                for color_comt, (depth, df_depth) in enumerate(df.groupby('DEPTH')):
                    
                    # Create color
                    r_color = random.randint(0, 255)
                    g_color = random.randint(0, 255)
                    b_color = random.randint(0, 255)

                    df_depth.set_index('TIME', inplace=True)
                    df_depth['values_from_start'] = (df_depth.index - df_depth.index[0]).days
                    df_depth.reset_index(inplace=True)

                    x_time = df_depth['TIME']
                    x_days = df_depth['values_from_start']
                    y_plot = df_depth[one_y]

                    if trend:
                        reg = LinearRegression().fit(np.vstack(x_days), y_plot)
                        bestfit = reg.predict(np.vstack(x_days))

                        fig.add_trace(go.Scatter(
                            x=x_time,
                            y=bestfit,
                            name=f'trend-{wf.metadata["platform_code"]}-{one_y}-{depth}',
                            # line_shape=line_shape,
                            mode='lines+markers',
                            yaxis=yaxis,
                            marker_symbol=symbols[y_num],
                            line=dict(dash=dash)
                        ))

                    fig.add_trace(go.Scatter(
                        x=x_time, y=y_plot,
                        line_color=f'rgb({r_color},{g_color},{b_color})',
                        name=f'{wf.metadata["platform_code"]}-{one_y}-{depth}',
                        line_shape=line_shape,
                        yaxis=yaxis,
                        marker_symbol=symbols[y_num],
                        line=dict(dash=dash)))

                    fig.update_traces(mode='lines+markers')

                    # Update yaxis
                    fig.update_layout(xaxis=dict(title='Time'))
                    try:
                        if y_num == 0:
                            fig.update_layout(
                                yaxis=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})"))
                        elif y_num == 1:
                            fig.update_layout(
                                yaxis2=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})",
                                    side="right",
                                    overlaying="y"))
                        elif y_num == 2:
                            fig.update_layout(
                                xaxis=dict(
                                    domain=[0.07, 1],
                                    title='Time'
                                ))
                            fig.update_layout(
                                yaxis3=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})",
                                    overlaying="y",
                                    side="left",
                                    position=0))
                        elif y_num == 3:
                            fig.update_layout(
                                xaxis=dict(
                                    domain=[0.07, 0.93],
                                    title='Time'
                                ))
                            fig.update_layout(
                                yaxis4=dict(
                                    title=f"{one_y} - {wf.vocabulary[one_y]['long_name']} ({wf.vocabulary[one_y]['units']})",
                                    overlaying="y",
                                    side="right",
                                    position=1))
                    except:
                        pass

                # Add 'Depth' to legend
                fig.update_layout(legend_title={'text': 'Platform Code - Parameter - Depth (m)'})

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

    return fig