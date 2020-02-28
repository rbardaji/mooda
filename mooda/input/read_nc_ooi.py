""" Implementation of a function to read NetCDF files from Ocean Observatory Iniciative (OOI) """
import xarray as xr
from ..waterframe import WaterFrame


def read_nc_ooi(path, clean_data=True):
    """
    Open a NetCDF file from OOI. This function was tested with CTD files.
    Web - https://oceanobservatories.org

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

    def add_pres(key_in):
        """ Add parameter PRES """
        # Data
        wf.data.rename(columns={key_in: 'PRES'}, inplace=True)
        wf.data['PRES_QC'] = 0

        # vocabulary
        wf.vocabulary['PRES'] = {
            "standard_name": "sea_water_pressure",
            "long_name": "Sea pressure",
            "units": "dbar",
            "valid_min": "0.0",
            "valid_max": "12000.0"
        }

    def add_temp(key_in):
        """ Add parameter TEMP """
        # Data
        wf.data.rename(columns={key_in: 'TEMP'}, inplace=True)
        wf.data['TEMP_QC'] = 0

        # vocabulary
        wf.vocabulary['TEMP'] = {
            "valid_min": "-5.0",
            "valid_max": "35.0",
            "ancillary_variables": "TEMP_QC",
            "standard_name": "sea_water_temperature",
            "units": "degrees_C",
            "long_name": "Sea temperature"
        }

    def add_cndc(key_in):
        """ Add parameter CNDC """
        # Data
        wf.data.rename(columns={key_in: 'CNDC'}, inplace=True)
        wf.data['CNDC_QC'] = 0

        # vocabulary
        wf.vocabulary['CNDC'] = {
            "valid_min": "0.0",
            "valid_max": "7.0",
            "ancillary_variables": "CNDC_QC",
            "standard_name": "sea_water_electrical_conductivity",
            "units": "S m-1",
            "long_name": "Electrical conductivity"
        }

    def add_psal(key_in):
        """ Add parameter PSAL """
        # Data
        wf.data.rename(columns={key_in: 'PSAL'}, inplace=True)
        wf.data['PSAL_QC'] = 0

        # vocabulary
        wf.vocabulary['PSAL'] = {
            "valid_min": "0.0",
            "valid_max": "42.0",
            "ancillary_variables": "PSAL_QC",
            "standard_name": "sea_water_practical_salinity",
            "units": "PSU",
            "long_name": "Practical salinity"
        }

    # WaterFrame creation
    wf = WaterFrame(path)

    # Set index
    try:
        wf.data.rename(columns={'time': 'TIME'}, inplace=True)
        # Set index to TIME
        wf.data.set_index('TIME', inplace=True)
    except KeyError:
        pass

    keys = wf.data.keys()
    # OOI sometimes contains "ctmo", other no... extrange things.

    if any("ctdmo" in key_str for key_str in keys):
        for key in keys:

            # Only use columns with "ctmo" in the name
            # We are going to assign QC to 0, CHECK IT
            if key == "ctdmo_seawater_pressure":
                add_pres(key)
            elif key == "ctdmo_seawater_temperature":
                add_temp(key)
            elif key == "ctdmo_seawater_conductivity":
                add_cndc(key)
            else:
                del wf.data[key]
    elif any("ctdpf" in key_str for key_str in keys):
        for key in keys:

            # Only use columns with "ctmo" in the name
            # We are going to assign QC to 0, CHECK IT
            if key == "ctdpf_ckl_seawater_pressure":
                add_pres(key)
            elif key == "ctdpf_ckl_seawater_temperature":
                add_temp(key)
            elif key == "ctdpf_ckl_seawater_conductivity":
                add_cndc(key)
            else:
                del wf.data[key]
    else:
        for key in keys:
            if key == "pressure":
                add_pres(key)
            elif key == "temp":
                add_temp(key)
            elif key == "conductivity":
                add_cndc(key)
            elif key == "practical_salinity":
                add_psal(key)

    # Adding platform_code to metadata
    wf.metadata['platform_code'] = wf.metadata['node']
    return wf
