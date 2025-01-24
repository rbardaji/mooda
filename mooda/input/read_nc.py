import xarray as xr
import pandas as pd
import numpy as np
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

    try:
        # Open file with xarray (decode times)
        ds = xr.open_dataset(path, decode_times=decode_times)
    except ValueError as e:
        print("Warning: Decoding 'TIME' failed. Opening dataset with decode_times=False.")
        ds = xr.open_dataset(path, decode_times=False)

        # Attempt to manually decode 'TIME' if it exists
        if "TIME" in ds.variables:
            try:
                time_values = ds["TIME"].values

                # Flatten if multidimensional
                if len(ds["TIME"].dims) > 1:
                    time_values = time_values.flatten()

                # Handle microseconds or milliseconds
                max_time_value = time_values.max()
                if max_time_value > 1e15:  # Likely in microseconds
                    print("TIME appears to be in microseconds, converting to milliseconds...")
                    time_values = time_values / 1000
                elif max_time_value > 1e12:  # Likely in milliseconds
                    print("TIME appears to be in milliseconds.")

                # Convert to datetime using numpy
                time_values = pd.to_datetime(
                    time_values.astype(np.float64), unit="ms", origin="unix"
                )

                # Assign the decoded 'TIME' back to the dataset
                ds = ds.assign_coords({"TIME": time_values})
            except Exception as e:
                print(f"Error decoding 'TIME': {e}")


    # Save dataset metadata and convert to DataFrame
    wf.metadata = dict(ds.attrs)
    wf.data = ds.to_dataframe()

    # Normalize column names to uppercase
    wf.data.columns = wf.data.columns.str.upper()

    # Rename columns ending with _SEADATANET_QC to _QC
    wf.data.rename(columns=lambda col: col.replace("_SEADATANET_QC", "_QC"), inplace=True)

    # Keywords to identify non-measurement columns
    non_measurement_keywords = ["QC", "ENTITY", "SIZE", "ID", "CODE", "URL", "LINK"]

    # Detect non-numeric constant columns and columns with suspicious names
    for col in wf.data.columns:
        if any(keyword in col for keyword in ["_QC", "LON", "LAT"]):
            continue
        unique_values = wf.data[col].unique()
        if (
            len(unique_values) == 1  # Column has only one unique value
            or (any(keyword in col for keyword in non_measurement_keywords) and col not in ["LATITUDE", "LONGITUDE"])
        ):
            # Save the unique value or mark as metadata
            wf.metadata[col] = unique_values[0] if len(unique_values) == 1 else "SUSPICIOUS_COLUMN"
            wf.data.drop(columns=[col], inplace=True)

    # Add missing "_QC" columns for numeric data
    for column in wf.data.select_dtypes(include=["float64", "int64", "float32", "int32"]).columns:
        if "_QC" in column:
            continue
        qc_column = f"{column}_QC"
        if qc_column not in wf.data.columns:
            wf.data[qc_column] = 0

    # Ensure TIME, DEPTH, LATITUDE, and LONGITUDE are indices if they exist
    index_columns = []
    for index_name in ["TIME", "DEPTH", "LATITUDE", "LONGITUDE"]:
        if index_name in wf.data.columns:
            index_columns.append(index_name)

    if index_columns:
        # Drop the original columns being set as indices
        wf.data.set_index(index_columns, inplace=True, drop=True)

    # Save variable attributes to the vocabulary
    for variable in ds.variables:
        wf.vocabulary[variable.upper()] = dict(ds[variable].attrs)

    return wf
