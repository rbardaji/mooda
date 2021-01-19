from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from ..waterframe import WaterFrame
from ..util import EMSO

def from_emso(user: str, password: str, platform_code: str, parameters: List[str]=[],
              start_time: str='', end_time: str='', depth_min: float=None, depth_max: float=None,
              resample: str=None) -> WaterFrame:
    """
    Get a WaterFrame with the data of the EMSO API (api.emso.eu).

    Parameters
    ----------
        user: str
            Login for the EMSO ERIC API.
        password: str
            Password for the EMSO ERIC API.
        platform_code: str
            Data filtered by platform_code
        parameters: List[str]
            List of parameters to get data
        start_time: str
            First date of the measurement
        end_time: str
            Last date of the measurement
        depth_min: float
            Minimum depth of the measurement
        depth_max: float
            Maximum depth of the measurement
        resample: str
            Resample rule
    
    Returns
    -------
        wf: WaterFrame object
    """
    # Login to EMSO
    emso = EMSO(user=user, password=password)

    # Get metadata    
    metadata_list = emso.get_metadata(platform_codes=[platform_code])
    
    # Get data
    complete_data = DataFrame()
    for parameter in parameters:
        data_list = emso.get_data(platform_codes=[platform_code], parameters=[parameter],
                                  start_time=start_time, end_time=end_time, depth_min=depth_min,
                                  depth_max=depth_max)

        data = pd.DataFrame(data_list)

        data = data.rename(
            columns = {
                'time': 'TIME',
                'time_qc': 'TIME_QC',
                'value': parameter,
                'value_qc': f'{parameter}_QC',
                'depth': 'DEPTH',
                'depth_qc': 'DEPTH_QC' 
            })

        del data['parameter']
        del data['metadata_id']
        del data['platform_code']
        del data['institution']
        del data['area']
        del data['long_name']
        del data['units']
        del data['location']
        del data['location_qc']

        data.set_index(['DEPTH', 'TIME'], inplace=True)

        if resample:
            # Make a copy of data and reset the variable data
            df = data.reset_index()
            df.set_index(['TIME'], inplace=True)
            data = DataFrame()

            # Group by depth
            for depth, df_depth in df.groupby('DEPTH'):
                df_depth.sort_index(inplace=True)
                df_depth.resample(resample, inplace=True)

                # Add depth, reindex and append to data
                df_depth['DEPTH'] = depth
                df_depth.set_index(['DEPTH', 'TIME'], inplace=True)
                data.append(df_depth)

        complete_data.append(data)
        
    wf = WaterFrame()
    if metadata_list:
        wf.metadata = metadata_list[0]
    wf.data = complete_data

    return wf