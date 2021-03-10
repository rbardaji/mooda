""" Implementation of WaterFrame.asal_temp2dens() """
import numpy as np
import gsw
import pandas as pd

def asal_temp2dens(self, asal_parameter='ASAL', temp_parameter='TEMP',
                   pres_parameter='PRES', inplace=True):
    """
    This function uses the gsw library.
    Adds the parameter Absolute Salinity (ASAL) from Practical Salinity (PSAL).
    Since PSAL is non-negative by definition, this function changes any
    negative input values of SP to be zero.

    Parameters
    ----------
        asal_parameter: str
            Parameter with valus of Absolute Salinity (g/kg)
        temp_parameter: str
            Parameter with temperature data (degree_C)
        pres_parameter: str
            Parameter with values of pressure (dBar)
        inplace: bool
            If inplace, changes will be applied on self

    Returns
    -------
        new_wf: WaterFrame
    """

    df_copy = self.data.copy()

    df_copy['DENS'] = gsw.density.rho(df_copy[asal_parameter],
                                          df_copy[temp_parameter],
                                          df_copy[pres_parameter])

    # Add QC
    df_copy['DENS_QC'] = 1
    # QC=0
    df_copy.loc[df_copy[f'{asal_parameter}_QC'] == 0, 'DENS_QC'] = 0
    df_copy.loc[df_copy[f'{temp_parameter}_QC'] == 0, 'DENS_QC'] = 0
    df_copy.loc[df_copy[f'{pres_parameter}_QC'] == 0, 'DENS_QC'] = 0
    # QC=4
    df_copy.loc[df_copy[f'{asal_parameter}_QC'] == 4, 'DENS_QC'] = 4
    df_copy.loc[df_copy[f'{temp_parameter}_QC'] == 4, 'DENS_QC'] = 4
    df_copy.loc[df_copy[f'{pres_parameter}_QC'] == 4, 'DENS_QC'] = 4

    new_wf = self.copy()
    new_wf.data = df_copy.copy()
    # Add vocabulary
    new_wf.vocabulary['DENS'] = {
        'long_name': 'In-situ density',
        'units': 'kg/m'}

    if inplace:
        self.data = df_copy.copy()
        self.vocabulary = new_wf.vocabulary.copy()

    return new_wf
