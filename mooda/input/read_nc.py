""" Implementation of a function to read a generic NetCDF file """
import xarray as xr
from ..waterframe import WaterFrame

def read_nc(path, decode_times=True):
    """
    Read data form NetCDF file and create a WaterFrame.

    Parameters
    ----------
        path: str
            Path of the NetCDF file.
        decode_times : bool, optional
            If True, decode times encoded in the standard NetCDF datetime format 
            into datetime objects. Otherwise, leave them encoded as numbers. 
    
    Returns
    -------
        wf: WaterFrame
    """
    # Create WaterFrame
    wf = WaterFrame()

    # Open file with xarrat
    ds = xr.open_dataset(path, decode_times=decode_times)

    # Save ds into a WaterFrame
    wf.metadata = dict(ds.attrs)
    wf.data = ds.to_dataframe()
    for variable in ds.variables:
        wf.vocabulary[variable] = dict(ds[variable].attrs)

    return wf
