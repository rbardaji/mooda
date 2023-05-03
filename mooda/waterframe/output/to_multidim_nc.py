""" Function to be imported in a WaterFrame. It save the WaterFrame into a multidimensional NetCDF file. """
from xarray import Dataset
import netCDF4 as nc
import pandas as pd
import numpy as np


def to_multidim_nc(self, path, dimensions: list,  time_key="TIME", compression=True, fill_value=-99999):
    """
    It saves the WaterFrame into a multidimensional NetCDF using NetCDF4 library

    Parameters
    ----------
        path: str
            Path to save the NetCDF. If path is None, the filename will be metadata['id'].
        dimensions: list
            List of the variable names to be stored as dimensions
        time_key: str
            Name of the time column
        compression: str
            If True, use zlib compression
        fill_value: str
                Fill value


    Returns
    -------
        path: str
            Path where the file is placed.
    """

    # Make sure that time is the last entry in the multiindex
    if time_key in dimensions:
        dimensions.remove(time_key)
        dimensions.append(time_key)

    df = self.data  # Access the DataFrame within the waterframe
    df = df.reset_index()

    index_df = df[dimensions].copy()  # create a dataframe with only the variables that will be used as indexes
    multiindex = pd.MultiIndex.from_frame(index_df)  # create a multiindex from the dataframe

    # Arrange other variables into a dict
    data = {col: df[col].values for col in df.columns if col not in dimensions}

    # Create a dataframe with multiindex
    data_df = pd.DataFrame(data, index=multiindex)

    dimensions = tuple(dimensions)

    with nc.Dataset(path, "w", format="NETCDF4") as ncfile:
        for dimension in dimensions:
            data = index_df[dimension].values
            values = np.unique(data)  # fixed-length dimension
            if dimension == time_key:
                # convert timestamp to float
                index_df[time_key] = pd.to_datetime(index_df[time_key])
                times = index_df[time_key].dt.to_pydatetime()
                values = nc.date2num(times, "seconds since 1970-01-01", calendar="standard")

            ncfile.createDimension(dimension, len(values))  # create dimension
            if type(values[0]) == str:  # Some dimension may be a string (e.g. sesnor_id)
                var = ncfile.createVariable(dimension, str, (dimension,), fill_value=fill_value, zlib=compression)
            else:
                var = ncfile.createVariable(dimension, 'f8', (dimension,), fill_value=fill_value, zlib=compression)

            var[:] = values  # assign dimension values
            # add all dimension metadata

            for key, value in self.vocabulary[dimension].items():
                if type(value) == list:
                    values = [str(v) for v in value]
                    value = join_attr.join(values)
                var.setncattr(key, value)

        for varname in data_df.columns:
            values = data_df[varname].to_numpy()  # assign values to the variable
            if varname.endswith("_QC"):
                # Store Quality Control as unsigned bytes
                var = ncfile.createVariable(varname, "u1", dimensions, fill_value=fill_value, zlib=compression)
                var[:] = values.astype(np.int8)
            else:
                var = ncfile.createVariable(varname, 'float', dimensions, fill_value=fill_value, zlib=compression)
                var[:] = values

            # Adding metadata
            for key, value in self.vocabulary[varname].items():
                if type(value) == list:
                    values = [str(v) for v in value]
                    value = join_attr.join(values)
                var.setncattr(key, value)

        # Set global attibutes
        for key, value in self.metadata.items():
            if type(value) == list:
                values = [str(v) for v in value]
                value = join_attr.join(values)
            ncfile.setncattr(key, value)
    return path