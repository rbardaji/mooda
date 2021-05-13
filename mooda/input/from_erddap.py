from erddapClient import ERDDAP_Tabledap
from collections import OrderedDict
from ..waterframe import WaterFrame

def from_erddap(server, dataset_id, variables=None, constraints=None, rcsvkwargs={}, auth=None):
    """
    Get a WaterFrame from an ERDDAP server tabledap dataset. 

    Parameters
    ----------
        server : The ERDDAP server URL        
        dataset_id : The dataset id to query
        variables : List of variables to get from ERDDAP server, it can be comma separated string or a list.
        constraints : Query constraints to appy to the ERDDAP query, this can be list or dictionary.
        read_csv_kwargs : Dictionary with the parameters to pass to the read_csv function that converts the ERDDAP response to pandas DataFrame
        auth : Tupple with username and password to authenticate to a protected ERDDAP server.
    """

    remote = ERDDAP_Tabledap(server, dataset_id, auth=auth)

    # Build the ERDDAP query
    if variables is None:
        variables = list(remote.variables.keys())
    remote.setResultVariables(variables) 
    if constraints:
        remote.addConstraints(constraints)
    
    # parameters for the pandas read_csv method, which its used in the getDataFrame method
    _rcsvkwargs = { **{ 'header' : 0, 
                        'names' : variables } , **rcsvkwargs }
    if 'time' in variables:
        _rcsvkwargs['parse_dates'] = ['time']

    # actual erddap data request
    _df = remote.getDataFrame(**_rcsvkwargs)
    # vocabulary subset from erddap
    _vocabulary = OrderedDict([ (key,val) for key, val in remote.variables.items() if key in variables ])

    # Handle index columns names
    for posible_depth_name in ['depth', 'altitude']:  # Special variable names in ERDDAP
        if posible_depth_name in variables:
            _df.rename(columns={posible_depth_name: 'DEPTH'}, inplace=True)
            break
    if not 'DEPTH' in _df.keys():
        _df['DEPTH'] = 0

    # time is a special variable in ERDDAP, it's always called time
    _df.rename(columns={'time': 'TIME'}, inplace=True) 

    # Add QC columns
    keys = _df.keys()
    for key in keys:
        if key.endswith('_QC'):
            continue
        if f'{key}_QC' in keys:
            continue
        else:
            _df[f'{key}_QC'] = 0

    # Set index
    _df.set_index(['DEPTH', 'TIME'], drop=True, inplace=True)

    # TODO variable names should be standarized? Ej. time -> TIME , temperature -> TEMP , etc? 
    # TODO Should this method include arguments to request ERDDAP server side operations ? Ej. orderBy, orderByClosest, orderByMean, etc?

    return WaterFrame(df=_df,
                      metadata=remote.info,
                      vocabulary=_vocabulary)
