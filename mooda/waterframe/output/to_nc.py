""" Function to be imported in a WaterFrame. It save the WaterFrame into a NetCDF file. """
from xarray import Dataset


def to_nc(self, path, nc_format="NETCDF4"):
    """
    It saves the WaterFrame into a NetCDF.

    Parameters
    ----------
        path: str
            Path to save the NetCDF.
        nc_format: str
            Specify the NetCDF format (NETCDF3_64BIT, NETCDF4).

    Returns
    -------
        True: bool
            If the internal functions of this method do not raise any error, the return is always
            True.
    """

    # Sometimes the metadata contains a list of str.
    # It can crash the creation of the NetCDF3_64Bits.
    # We are going to change the list of str to str
    metadata_netcdf = self.metadata.copy()
    for key, value in metadata_netcdf.items():
        if isinstance(value, list):
            metadata_netcdf[key] = ', '.join(value)

    # Multiindex is not alloud yet in to_netcdf of xarray
    df = self.data.reset_index()
    df.set_index('TIME', inplace=True)

    # Creation of an xarray dataset
    ds = Dataset(data_vars=df, attrs=metadata_netcdf)
    for key in self.parameters:
        try:
            ds[key].attrs = self.vocabulary[key]
        except KeyError:  # Variable without vocabulary
            pass

    # Creation of the nc file
    ds.to_netcdf(path, format=nc_format)

    return True
