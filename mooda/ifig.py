"""Module with the class IPlot, designed to create Plotly charts"""
import plotly.graph_objs as go
import pandas as pd


class IFig:
    """ It contains methods to create Plotly charts from WaterFrames"""

    def __init__(self, wf):
        """
        Constructor of the class.

        Parameters
        ----------
            wf: WaterFrame
        """
        self.wf = wf

        # Check if wf is multiindex and change to single index
        if isinstance(self.wf.data.index, pd.core.index.MultiIndex):
            self.wf.data.reset_index(inplace=True)
            self.wf.data.set_index('TIME', inplace=True)

    def site_map(self):
        """
        It creates a chart with a map with the coordinates of the site. It looks for the coordinates
        in the metadata information.

        Returns
        -------
            figure: dict
                Plotly Figure dictionary.
        """
        coordinates = self.wf.get_coordinates()

        # For now we are going to plot the minimum coordinates. It will change in the future.
        lat = coordinates[0][0]
        lon = coordinates[0][1]

        # Data creation
        data = [
            dict(
                type="scattergeo",
                lon=[lon],
                lat=[lat],
                mode='markers',
            )
        ]

        # Configuration of the zoom
        if lat is not None and lon is not None:
            lataxis = dict(range=[float(lat)-9, float(lat)+9])
            lonaxis = dict(range=[float(lon)-16, float(lon)+16])
        else:
            lataxis = None
            lonaxis = None

        layout = dict(
            geo=dict(
                lakecolor="rgb(255, 255, 255)",
                resolution=50,
                showcoastlines=True,
                showland=True,
                landcolor="rgb(229, 229, 229)",
                countrycolor="rgb(255, 255, 255)",
                coastlinecolor="rgb(255, 255, 255)",
                lataxis=lataxis,
                lonaxis=lonaxis
            ),
            margin=dict(l=10, r=10, t=0, b=0),
        )

        figure = dict(data=data, layout=layout)
        return figure

    def time_series(self, parameters=None):
        """
        It creates a Plotly time-series figure.

        Parameters
        ----------
            parameters: str or list (optional, parameters=None)
                Parameters to plot.

        Returns
        -------
            figure: dict
                Plotly figure dictionary
        """
        figure = {'data': None, 'layout': None}

        # Check parameters
        if parameters is None:
            parameters = self.wf.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return figure

        data = [go.Scatter(x=self.wf.data.index, y=self.wf[parameter], fill="tozeroy",
                           name=parameter) for parameter in parameters]

        # Layout
        y_label = None
        if len(parameters) == 1:
            try:
                title = self.wf.meaning[parameters[0]]['long_name']
            except KeyError:
                title = parameters[0]
            try:
                y_label = self.wf.meaning[parameters[0]]['units']
            except KeyError:
                pass
        else:
            title = "_".join(parameters)
        min_value = None
        max_value = None
        for parameter in parameters:

            _min = min(self.wf[parameter])
            _max = max(self.wf[parameter])

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

    @staticmethod
    def site_map_from_waterframe(waterframe):
        """
        It creates a chart with a map with the coordinates of the site. It looks for the coordinates
        in the metadata information.

        Parameters
        ----------
            wf: WaterFrame

        Returns
        -------
            figure: dict
                Plotly Figure dictionary.
        """
        coordinates = waterframe.get_coordinates()

        # For now we are going to plot the minimum coordinates. It will change in the future.
        lat = coordinates[0][0]
        lon = coordinates[0][1]

        # Data creation
        data = [
            dict(
                type="scattergeo",
                lon=[lon],
                lat=[lat],
                mode='markers',
            )
        ]

        # Configuration of the zoom
        if lat is not None and lon is not None:
            lataxis = dict(range=[float(lat)-8.5, float(lat)+8.5])
            lonaxis = dict(range=[float(lon)-16, float(lon)+16])
        else:
            lataxis = None
            lonaxis = None

        layout = dict(
            geo=dict(
                lakecolor="rgb(255, 255, 255)",
                resolution=50,
                showcoastlines=True,
                showland=True,
                landcolor="rgb(229, 229, 229)",
                countrycolor="rgb(255, 255, 255)",
                coastlinecolor="rgb(255, 255, 255)",
                lataxis=lataxis,
                lonaxis=lonaxis
            ),
            margin=dict(l=10, r=10, t=0, b=0),
        )

        figure = dict(data=data, layout=layout)
        return figure

    @staticmethod
    def site_map_from_coordinates(lat, lon, text):
        """
        It returns a figure of a map with a scatter of the input information.
        """
        # Data creation
        data = [
            dict(
                type="scattergeo",
                lon=lon,
                lat=lat,
                text=text,
                mode='markers',
            )
        ]

        # Configuration of the zoom
        lataxis = dict(range=[min(lat)-9, max(lat)+9])
        lonaxis = dict(range=[min(lon)-15, max(lon)+15])

        layout = dict(
            geo=dict(
                lakecolor="rgb(255, 255, 255)",
                resolution=50,
                showcoastlines=True,
                showland=True,
                landcolor="rgb(229, 229, 229)",
                countrycolor="rgb(255, 255, 255)",
                coastlinecolor="rgb(255, 255, 255)",
                lataxis=lataxis,
                lonaxis=lonaxis
            ),
            margin=dict(l=10, r=10, t=0, b=0),
        )

        figure = dict(data=data, layout=layout)
        return figure

    @staticmethod
    def time_series_from_waterframe(waterframe, parameters=None):
        """
        It creates a Plotly time-series figure.

        Parameters
        ----------
            waterframe: WaterFrame
            parameters: str or list (optional, parameters=None)
                Parameters to plot.

        Returns
        -------
            figure: dict
                Plotly figure dictionary
        """

        figure = {'data': None, 'layout': None}

        # Check parameters
        if parameters is None:
            parameters = waterframe.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return figure

        data = [go.Scatter(x=waterframe.data.index, y=waterframe[parameter], fill="tozeroy",
                           name=parameter) for parameter in parameters]

        # Layout
        y_label = None
        if len(parameters) == 1:
            try:
                title = waterframe.meaning[parameters[0]]['long_name']
            except KeyError:
                title = parameters[0]
            try:
                y_label = waterframe.meaning[parameters[0]]['units']
            except KeyError:
                pass
        else:
            title = "_".join(parameters)
        min_value = None
        max_value = None
        for parameter in parameters:

            _min = min(waterframe[parameter])
            _max = max(waterframe[parameter])

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
            'margin': {'l': 50, 'r': 1, 't': 45, 'b': 30}
        }

        figure = {"data": data, "layout": layout}

        return figure
