import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


class PlotMap:
    """
    It contains functions related to the management of maps.
    It creates an instance variable called 'm' that is a Basemap object.
    We are going to use and modify 'm' in all functions.
    """
    def __init__(self, ):
        self.m = Basemap()

    def map_world(self, res='l'):
        """
        It creates a map of the world and saves into 'm'.

        Parameters
        ----------
            res: str, 'l', 'i', 'h', 'f', optional (res = 'l')
                Resolution of boundary database to use. Can be c (crude),
                l (low), i (intermediate), h (high), f (full) or None. If None,
                no boundary data will be read in (and class methods such as
                drawcoastlines will raise an if invoked). Higher res datasets
                are much slower to draw.
        """
        self.m = Basemap(projection='mill', resolution=res)
        # Draw the coastal lines
        self.m.drawcoastlines()
        # Fill the continents with black
        self.m.fillcontinents(color='K')

    def map_mediterranean(self, res='l'):
        """
        It creates a map of the Mediterranean.

        Parameters
        ----------
            res: str, 'l', 'i', 'h', 'f', optional (res = 'l')
                Resolution of boundary database to use. Can be c (crude),
                l (low), i (intermediate), h (high), f (full) or None. If None,
                no boundary data will be read in (and class methods such as
                drawcoastlines will raise an if invoked). Higher res datasets
                are much slower to draw.
        """
        self.m = Basemap(projection='mill', resolution=res, llcrnrlat=30,
                         llcrnrlon=-13, urcrnrlat=47, urcrnrlon=38)
        # Draw the coastal lines
        self.m.drawcoastlines()
        # Fill the continents with black
        self.m.fillcontinents(color='K')

    def add_point(self, lon, lat, color='blue', label=None):
        """
        It adds points to the map.

        Parameters
        ----------
            lon: float
                Longitude.
            lat: float
                Latitude.
            color: str
                Color of the point.
            label: str
                Text to write in the point.
        """
        x, y = self.m(float(lon), float(lat))
        self.m.plot(x, y, color=color, marker='o', markersize=7)
        if label is not None:
            plt.text(x+10000, y+5000, label)
