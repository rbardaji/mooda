""" Implementation of WaterFrame.iplot_timeseries() """
import numpy as np
import plotly.graph_objects as go


def iplot_timeseries(self, parameters_to_plot=None, mode='lines', marker_line_width=0,
                     marker_size=4, marker_color=None, marker_colorscale='Viridis'):
    """
    It creates a Plotly figure with the time-series of the input parameters.

    Parameters
    ----------
        parameters_to_plot: str or list (optional, parameters_to_plot=None)
            Parameters to plot.
        mode: str (optional, mode='lines')
            Plotting points (makers), lines or lines and points (lines+markers).
        marker_line_width: float (optional, marker_line_width=0)
            Width of the line arround the marker.
        marker_size: float (optional, marker_size=4)
            Size of the marker.
        marker_color: str (optional, marker_color=None)
            Parameter name. Change the color of the marker related to a parameter.
        marker_colorscale: str (optional, marker_colorscale='Viridis')
            Color scale of markers. Options: Blackbody, Bluered, Blues, Earth, Electric, Greens,
            Greys, Hot, Jet, Picnic, Portland, Rainbow, RdBu, Reds, Viridis, YlGnBu, YlOrRd
    Returns
    -------
        figure: dict
            Plotly figure dictionary
    """

    # Show color scale
    showscale = False

    if parameters_to_plot is None:
        parameters_to_plot = self.parameters
    elif isinstance(parameters_to_plot, str):
        parameters_to_plot = [parameters_to_plot]

    parameters_and_colors = parameters_to_plot.copy()
    if marker_color is not None:
        parameters_and_colors.append(marker_color)

    # Extract data
    df = self.data[parameters_and_colors].dropna().reset_index()
    df = df.groupby(['DEPTH', 'TIME'])[parameters_and_colors].mean()
    df.reset_index(inplace=True)
    df.set_index('TIME', inplace=True)

    if marker_color is not None:
        marker_color = df[marker_color]
        showscale = True

    data = [go.Scattergl(
        x=df.index,
        y=df[parameter],
        fill="tozeroy",
        mode=mode,
        marker_line_width=marker_line_width,
        marker_size=marker_size,
        marker_color=marker_color,
        marker_showscale=showscale,
        marker_colorscale=marker_colorscale,
        name=parameter)
            for parameter in parameters_to_plot]

    # Layout
    y_label = None
    if len(parameters_to_plot) == 1:
        try:
            title = self.vocabulary[parameters_to_plot[0]]['long_name']
        except KeyError:
            title = parameters_to_plot[0]
        try:
            y_label = self.vocabulary[parameters_to_plot[0]]['units']
        except KeyError:
            pass
    else:
        title = "_".join(parameters_to_plot)
    min_value = None
    max_value = None
    for parameter in parameters_to_plot:

        _min = np.nanmin(self.data[parameters_to_plot])
        _max = np.nanmax(self.data[parameters_to_plot])

        if min_value is None or _min < min_value:
            min_value = _min

        if max_value is None or _max > max_value:
            max_value = _max

    layout = {
        'title': title,
        'yaxis': {
            'range': [min_value, max_value],
            'title': y_label
        },
        'margin': {'l': 50, 'r': 10, 't': 45, 'b': 30}
    }

    figure = {"data": data, "layout": layout}

    return figure
