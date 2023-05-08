""" Implementation of a function to read a generic NetCDF file """
import xarray as xr
from ..waterframe import WaterFrame

def read_nc(path, decode_times=True, time_key="TIME"):
    """
    Read data form NetCDF file and create a WaterFrame.

    Parameters
    ----------
        path: str
            Path of the NetCDF file.
        decode_times : bool, optional
            If True, decode times encoded in the standard NetCDF datetime format
            into datetime objects. Otherwise, leave them encoded as numbers.
        time_key:
            time variable, defaults to "TIME"

    Returns
    -------
        wf: WaterFrame
    """
    # Create WaterFrame
    wf = WaterFrame()

    time_units = ""
    if decode_times:
        # decode_times in xarray.open_dataset will erase the unit field from TIME, so store it before it is removed
        ds = xr.open_dataset(path, decode_times=False)
        if  time_key in ds.variables and "units" in ds[time_units].attrs.keys():
            time_units = ds[time_key].attrs["units"]
        ds.close()

    # Open file with xarray
    ds = xr.open_dataset(path, decode_times=decode_times)

    # Save ds into a WaterFrame
    wf.metadata = dict(ds.attrs)
    wf.data = ds.to_dataframe()
    for variable in ds.variables:
        wf.vocabulary[variable] = dict(ds[variable].attrs)

    if time_units:
        wf.vocabulary[time_key]["units"] = time_units

    return wf
