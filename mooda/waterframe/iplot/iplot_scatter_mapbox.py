""" Implementation of wf.iplot_scatter_mapbox """
import plotly.express as px


def iplot_scatter_mapbox(self, mapbox_token, color, lat='LATITUDE',
                         lon='LONGITUDE', range_color='auto', title='auto',
                         animation_frame=None, zoom=14.5, labels=None, **kwds):
    """
    It uses plotly.express.scatter_mapbox().
    It creates a map with a point in each coordinate of the parameter of the
    color argument

    Parameters
    ----------
        mapbox_token: str
            Token of mapbox
        color: str
            Parameter to be pointed on the map.
        lat: str
            Parameter with the latitude.
        lon: str
            Paramter with the longutude.
        range_color: List[float] or 'auto'
            Range of values for the color scale.
            If color_scale is 'auto', the range is the min and max of the color
            parameter.
        title: str
            Title of the figure.
            If title is 'auto'
        animation_frame: str or None
            Parameter to create an animated graph 
        zoom: float
            Initial Zoom value
        **kwds: arguments from plotly.express.scatter_mapbox()
    
    Returns
    -------
        fig:
    """
    # Connect plotly express with your mapbox token
    px.set_mapbox_access_token(mapbox_token)

    if animation_frame:
        df = self.data.reset_index()
        animation_frame = df[animation_frame].astype(str)
    if range_color == 'auto':
        range_color = [min(self.data[color]), max(self.data[color])]
    if title == 'auto':
        title = self.metadata.get('title', '')

    fig = px.scatter_mapbox(self.data, lat=lat, lon=lon, color=color,
                            zoom=zoom, animation_frame=animation_frame,
                            range_color=range_color, title=title, labels=labels,
                            **kwds)

    return fig
