""" Implementation of mooda.iplot_location() """


def iplot_location(list_wf):
    """
    It creates a Plotly Figure with a map and a spot of the measurement location of the input
    WaterFrames.

    Parameters
    ----------
        list_wf: List of WaterFrames
            List of WaterFrames to be concatenated.

    Returns
    -------
        figure: dict
            Dictionary of Plotly figure
    """

    lat = [float(wf.metadata.get('geospatial_lat_min')) for wf in list_wf]
    lon = [float(wf.metadata.get('geospatial_lon_min')) for wf in list_wf]
    text = [wf.metadata.get('platform_code') for wf in list_wf]
    # Data creation
    data = [
        dict(
            type="scattergeo",
            lon=lon,
            lat=lat,
            mode='markers',
            marker=dict(
                size=16,
            ),
            text=text
        )
    ]

    # Configuration of the zoom
    if lat is not None and lon is not None:
        lataxis = dict(range=[min(lat)-9, max(lat)+9])
        lonaxis = dict(range=[min(lon)-16, max(lon)+16])
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
