""" Implementation of a function to read NetCDF files from EMODNET """
import xarray as xr
from ..waterframe import WaterFrame


def read_nc_emodnet(path, clean_data=True):
    """
    Open a NetCDF file from EMODNET physics. The file should be from a fixed point observatory due
    to this function delete the coordenates LATITUDE and LONGITUDE from the variables. If LATITUDE
    and LONGITUDE are not deleted, the pandas DataFrame is huge and your script will raise a
    MemoryError.

    Parameters
    ----------
        path: str
            Path of the NetCDF file.
        clean_data: bool
            It deletes variables with DC in name.

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
                Output dataset"""
        # Creation of a list with the variables to drop. We are going to
        # drop all variables with a "_DM" in the key name.
        vars2drop = [k for k in ds_in.variables.keys() if '_DM' in k]

        if clean_data_in:
            # Dropping the previous list and some other variables
            ds_out = ds_in.drop(vars2drop)
        else:
            ds_out = ds_in

        if 'LATITUDE' in ds_in.variables.keys():
            ds_out = ds_out.drop('LATITUDE')
        if 'LONGITUDE' in ds_in.variables.keys():
            ds_out = ds_out.drop('LONGITUDE')
        if 'POSITION_QC' in ds_in.variables.keys():
            ds_out = ds_out.drop('POSITION_QC')
        return ds_out

    # Create WaterFrame
    wf = WaterFrame()

    # Open file with xarrat
    ds = xr.open_dataset(path)
    ds = drop(ds, clean_data)
    # Save ds into a WaterFrame
    wf.metadata = dict(ds.attrs)
    wf.data = ds.to_dataframe()
    for variable in ds.variables:
        wf.vocabulary[variable] = dict(ds[variable].attrs)

    return wf
