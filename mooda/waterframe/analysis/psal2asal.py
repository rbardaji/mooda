""" Implementation of WaterFrame.psal2asal() """
import numpy as np
import gsw
import pandas as pd

def psal2asal(self, psal_parameter='PSAL', pres_parameter='PRES', lon='auto',
              lat='auto', inplace=True):
    """
    This function uses the gsw library.
    Adds the parameter Absolute Salinity (ASAL) from Practical Salinity (PSAL).
    Since PSAL is non-negative by definition, this function changes any
    negative input values of SP to be zero.

    Parameters
    ----------
        psal_parameter: str
            Parameter with valus of Practical Salinity
        pres_parameter: str
            Parameter with values of pressure, in dBar
        lon: str
            Parameter with the values of the longitud, in degrees
            If lon is 'auto', the value of lon will be taken from the
            metadata['last_longitude_observation']
        lat: str
            Parameter with the values of the ñatitude, in degrees
            If lat is 'auto', the value of lon will be taken from the
            metadata['last_latitude_observation']

    Returns
    -------
        wf: WaterFrame
    """

    df_copy = self.data.copy()
    if lat == 'auto':
        lat_parameter = 'LATITUDE'
        df_copy['LATITUDE'] = float(self.metadata['last_latitude_observation'])
        df_copy['LATITUDE_QC'] = 1 
    else:
        lat_parameter = lat
    if lon == 'auto':
        lon_parameter = 'LONGITUDE'
        df_copy['LONGITUDE'] = float(self.metadata['last_longitude_observation'])
        df_copy['LONGITUDE_QC'] = 1
    else:
        lon_parameter = 'lon'

    df_copy['ASAL'] = gsw.SA_from_SP(df_copy[psal_parameter],
                                     df_copy[pres_parameter],
                                     df_copy[lon_parameter],
                                     df_copy[lat_parameter])

    # Add QC
    df_copy['ASAL_QC'] = 1
    # QC=0
    df_copy.loc[df_copy[f'{psal_parameter}_QC'] == 0, 'ASAL_QC'] = 0
    df_copy.loc[df_copy[f'{pres_parameter}_QC'] == 0, 'ASAL_QC'] = 0
    df_copy.loc[df_copy[f'{lon_parameter}_QC'] == 0, 'ASAL_QC'] = 0
    df_copy.loc[df_copy[f'{lat_parameter}_QC'] == 0, 'ASAL_QC'] = 0
    # QC=4
    df_copy.loc[df_copy[f'{psal_parameter}_QC'] == 4, 'ASAL_QC'] = 4
    df_copy.loc[df_copy[f'{pres_parameter}_QC'] == 4, 'ASAL_QC'] = 4
    df_copy.loc[df_copy[f'{lon_parameter}_QC'] == 4, 'ASAL_QC'] = 4
    df_copy.loc[df_copy[f'{lat_parameter}_QC'] == 4, 'ASAL_QC'] = 4

    # Delete lat and lon
    if lat == 'auto':
        del df_copy[f'{lat_parameter}_QC']
        del df_copy[lat_parameter]
    if lon == 'auto':
        del df_copy[f'{lon_parameter}_QC']
        del df_copy[lon_parameter]

    new_wf = self.copy()
    new_wf.data = df_copy.copy()
    # Add vocabulary
    new_wf.vocabulary['ASAL'] = {
        'long_name': 'Absolute Salinity',
        'units': 'g/kg'}

    if inplace:
        self.data = df_copy.copy()
        self.vocabulary = new_wf.vocabulary.copy()

    return new_wf
