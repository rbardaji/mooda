from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from ..waterframe import WaterFrame
from ..util import EMSO

def from_emso(platform_code: str, parameters: List[str]=[], start_time: str='',
              end_time: str='', depth_min: float=None, depth_max: float=None,
              user: str='', password: str='', size: int=10, token: str=''
              ) -> WaterFrame:
    """
    Get a WaterFrame with the data of the EMSO API (api.emso.eu).

    Parameters
    ----------
        user: str
            Login for the EMSO ERIC API.
        password: str
            Password for the EMSO ERIC API.
        token: str
            Token for the EMSO ERIC API.
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
        size: int
            Number of values
    
    Returns
    -------
        wf: WaterFrame object
    """
    # Login to EMSO
    emso = EMSO(user=user, password=password, token=token)

    # Get metadata    
    metadata_list = emso.get_metadata(platform_codes=[platform_code])

    # Get data
    complete_data = DataFrame()
    for parameter in parameters:
        data_list = emso.get_data(platform_codes=[platform_code], parameters=[parameter],
                                  start_time=start_time, end_time=end_time, depth_min=depth_min,
                                  depth_max=depth_max, size=size, sort='asc')

        if data_list:
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

            data['TIME'] = pd.to_datetime(data['TIME'])
            data.set_index(['DEPTH', 'TIME'], inplace=True)
            data = data.astype(float)
            complete_data = complete_data.append(data)

    wf = WaterFrame()
    if metadata_list:
        wf.metadata = metadata_list[0]
    wf.data = complete_data.copy()
    for parameter in wf.parameters:
        for metadata_parameter in wf.metadata['parameters']:
            acronym = metadata_parameter.split('-')[0].strip()
            long_name = metadata_parameter.split('-')[1].strip().split('[')[0].strip()
            units = metadata_parameter.split('-')[1].strip().split('[')[1].strip().split(']')[0]
            if parameter == acronym:
                wf.vocabulary[acronym] = {'long_name': long_name, 'units': units}
                break

    return wf
