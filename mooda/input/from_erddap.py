from typing import OrderedDict
from erddapClient import ERDDAP_Tabledap
from ..waterframe import WaterFrame
from collections import OrderedDict

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

    # Build the query
    if variables is None:
        variables = list(remote.variables.keys())
    remote.setResultVariables(variables) 
    if constraints:
        remote.addConstraints(constraints)
    
    # pandas read_csv parameters for the erddap csv request.
    _rcsvkwargs = { **{ 'header' : 0, 
                        'names' : variables } , **rcsvkwargs }
    if 'time' in variables:
        _rcsvkwargs['parse_dates'] = True
        _rcsvkwargs['index_col'] = 'time'

    # actual erddap data request
    _df = remote.getDataFrame(**_rcsvkwargs)

    # waterframe params      
    _vocabulary = OrderedDict([ (key,val) for key, val in remote.variables.items() if key in variables ])
    wf = WaterFrame(df=_df,
                    metadata=remote.info,
                    vocabulary=_vocabulary)

    # TODO variable names should be standarized? Ej. time -> TIME , temperature -> TEMP , etc? 
    # TODO Should this method include arguments to request ERDDAP server side operations ? Ej. orderBy, orderByClosest, orderByMean, etc?

    return wf