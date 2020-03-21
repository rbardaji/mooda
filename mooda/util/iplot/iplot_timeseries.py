""" Implementation of WaterFrame.iplot_timeseries() """
import numpy as np
import plotly.graph_objects as go


def iplot_timeseries(list_wf, parameter_to_plot):
    """
    It creates a Plotly figure with the time-series of the input parameter.

    Parameters
    ----------
        list_wf: List of WaterFrames
            List of WaterFrames to be concatenated.
        parameter_to_plot: str
            Parameters to plot.

    Returns
    -------
        figure: dict
            Plotly figure dictionary
    """
    data = []
    for wf in list_wf:
        # Extract data
        df = wf.data[parameter_to_plot].dropna().reset_index()
        df = df.groupby(['DEPTH', 'TIME'])[parameter_to_plot].mean()
        df = df.reset_index()
        df.set_index('TIME', inplace=True)
        # df.renane(columns={parameter_to_plot: wf.metadata.get('platform_code')}, inplace=True)

        data.append(
            go.Scatter(x=df.index, y=df[parameter_to_plot],
                       # fill="tozeroy",
                       name=wf.metadata.get('platform_code')))

    # Layout
    y_label = None

    try:
        title = list_wf[0].vocabulary[parameter_to_plot]['long_name']
    except KeyError:
        title = parameter_to_plot
    try:
        y_label = list_wf[0].vocabulary[parameter_to_plot]['units']
    except KeyError:
        pass

    min_value = np.nanmin(list_wf[-1].data[parameter_to_plot])
    max_value = np.nanmax(list_wf[0].data[parameter_to_plot])

    layout = {
        'title': title,
        'yaxis': {
            # 'range': [min_value, max_value],
            'title': y_label
        },
        'margin': {'l': 50, 'r': 10, 't': 45, 'b': 30}
    }

    figure = {"data": data, "layout": layout}

    return figure
