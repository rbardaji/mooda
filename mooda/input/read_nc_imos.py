"""
Implementation of a function to read NetCDF files from Integrated Marine Observing System (IMOS)
"""
import xarray as xr
from ..waterframe import WaterFrame


def read_nc_imos(path, clean_data=True):
    """
    Open a NetCDF file from Integrated Marine Observing System (IMOS). All QC flags are 0.

    Parameters
    ----------
        path: str
            Path of the NetCDF file.
        clean_data: bool
            It deletes variables with _burst_min, _burst_max, _burst_sd, _num_obs, TIMESERIES and
            NOMINAL_DEPTH in name.

    Returns
    -------
        wf: WaterFrame
    """
    def drop(ds_in, clean_data_in):
        """Drop some parameters of the dataset.

        Parameters
        ----------
            ds_in: xarray.Dataset
                Input dataset.
            clean_data_in: bool
                It indicates if "_DM" variables should be deleted.
        Returns
        -------
            ds_out: xarray.Dataset
                Output dataset
        """

        ds_out = ds_in
        if clean_data_in:

            for key in ds_in.variables.keys():
                # This id / elif / elif can be just one if... I know...
                if key == 'TIMESERIES' or key == 'NOMINAL_DEPTH':
                    ds_out = ds_out.drop(key)
                elif '_burst_min' in key or '_burst_max' in key or '_burst_sd' in key:
                    ds_out = ds_out.drop(key)
                elif '_num_obs' in key:
                    ds_out = ds_out.drop(key)

        return ds_out

    # Create WaterFrame
    wf = WaterFrame()

    # Open file with xarrat
    ds = xr.open_dataset(path)
    ds = drop(ds, clean_data)
    # Save ds into a WaterFrame
    wf.metadata = dict(ds.attrs)
    wf.data = ds.to_dataframe()
    for key in wf.data.keys():
        wf.data[f'{key}_QC'] = 0
    for variable in ds.variables:
        wf.vocabulary[variable] = dict(ds[variable].attrs)

    return wf
