"""Module with the class IPlot, designed to create Plotly charts"""


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
