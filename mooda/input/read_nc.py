import numpy as np
import xarray as xr
from ..waterframe import WaterFrame


import numpy as np
import xarray as xr
from ..waterframe import WaterFrame


def read_nc(path, decode_times=True):
    """
    Read data from NetCDF file and create a WaterFrame.

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

    # Open file with xarray
    ds = xr.open_dataset(path, decode_times=decode_times)

    # Save dataset metadata and convert to DataFrame
    wf.metadata = dict(ds.attrs)
    wf.data = ds.to_dataframe()

    # Normalize column names to uppercase
    wf.data.columns = wf.data.columns.str.upper()

    # Keywords to identify non-measurement columns
    non_measurement_keywords = ["ENTITY", "SIZE", "ID", "CODE"]

    # Detect non-numeric constant columns and columns with suspicious names
    for col in wf.data.columns:
        unique_values = wf.data[col].unique()
        if (
            len(unique_values) == 1  # Column has only one unique value
            or any(keyword in col for keyword in non_measurement_keywords)  # Suspicious column name
        ) and "_QC" not in col:  # Ignore columns with "_QC"
            # Save the unique value or mark as metadata
            if len(unique_values) == 1:
                wf.metadata[col] = unique_values[0]
                wf.data.drop(columns=[col], inplace=True)

    # Add missing "_QC" columns only for numeric columns without "_QC"
    for column in wf.data.columns:
        if "_QC" not in column and np.issubdtype(wf.data[column].dtype, np.number):
            qc_column = f"{column}_QC"
            if qc_column not in wf.data.columns:
                # Add a placeholder QC column (default value: 0 for 'no quality control')
                wf.data[qc_column] = 0

    # Identify potential index columns
    index_columns = ["TIME", "DEPTH", "LATITUDE", "LONGITUDE"]
    present_indices = [col for col in index_columns if col in wf.data.columns]

    # Set indices if any are present
    if present_indices:
        wf.data.set_index(present_indices, inplace=True, drop=True)

    # Save variable attributes to the vocabulary
    for variable in ds.variables:
        wf.vocabulary[variable.upper()] = dict(ds[variable].attrs)

    return wf
