from erddapy import ERDDAP

# WORK IN PROGRESS

def from_erddap(server, dataset_id, variables=None, constraints=None):
    """
    Get a WaterFrame form an ERDDAP server.

    Parameters
    ----------
        server: str
            Server name.
    """

    protocol = 'tabledap'
    response = 'nc'

    e = ERDDAP(server, protocol, response)

    e.dataset_id = dataset_id
    e.variables = variables
    e.constraints = constraints

    ds = e.to_xarray(decode_times=False)

    return ds
