""" Implementation of WaterFrame.pres2depth() """
import numpy as np

def pres2depth(self, add_nominal_depth=True, density='sea-water', inplace=True):
    """
    It creates the DEPTH index of the WaterFrame from the PRES column.

    Parameters
    ----------
        add_nominal_depth: bool
            Returns a WaterFrame with an extra parameter called 'NOMINAL_DEPTH'
            that contains the previous 'DEPTH' values.
        density: str
            Options: 'sea-water', 'fresh-water', '<a number in Kg/m^3>'

    Returns
    -------
        min_dict: dict
            Dictionary with the following format:
            {
                '<name of index 1>': <value of index 1>,
                '<name of index n>': <value of index n>,
                'name of parameter': < min value of parameter>
            }
            If min_dict is None, all the values of the parameter are NaN.
    """

    df_copy = self.data.copy()

    df_copy = df_copy.reset_index()

    # Add QC flags from PRES
    df_copy['DEPTH_QC'] = df_copy['PRES_QC']

    if add_nominal_depth:
        df_copy['NOMINAL_DEPTH'] = df_copy['DEPTH']
        df_copy['NOMINAL_DEPTH_QC'] = df_copy['DEPTH_QC']

    # Calculation of DEPTH
    if isinstance(density, str):
        if density == 'sea-water':
            dens = 1.114293
        elif density == 'fresh-water':
            dens = 1.11135
        else:
            dens = float(density)
    else:
        # Supose to be a number
        dens = density

    df_copy['DEPTH'] = df_copy['PRES'] / dens
    df_copy.set_index(['TIME', 'DEPTH'], inplace=True)
    
    wf_copy = self.copy()
    wf_copy.data = df_copy.copy()

    if inplace:
        self.data = df_copy.copy()

    return wf_copy
