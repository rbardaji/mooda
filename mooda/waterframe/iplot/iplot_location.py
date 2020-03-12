""" Implementation of WaterFrame.iplot_location() """


def iplot_location(self):
    """
    It creates a Plotly Figure with a map and a spot of the measurement location of the WaterFrame.

    Returns
    -------
        figure: dict
            Dictionary of Plotly figure
    """

    lat = self.metadata.get('geospatial_lat_min')
    lon = self.metadata.get('geospatial_lon_min')
    text = self.metadata.get('platform_code')
    # Data creation
    data = [
        dict(
            type="scattergeo",
            lon=[lon],
            lat=[lat],
            mode='markers',
            marker=dict(
                size=16,
            ),
            text=text
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
