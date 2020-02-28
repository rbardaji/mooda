""" Implementation of mooda.read_pkl(path) """
import pickle
from .. import WaterFrame

def read_pkl(path_pkl):
    """
    Get a WaterFrame from a pickle file.

    Parameters
    ----------
        path_pkl: str
            Location of the pickle file.

    Returns
    -------
        wf_pkl: WaterFrame
    """
    wf_pkl = WaterFrame()

    pickle_dataset = pickle.load(open(path_pkl, "rb"))

    wf_pkl.data = pickle_dataset.get('data')
    wf_pkl.vocabulary = pickle_dataset.get('vocabulary')
    wf_pkl.metadata = pickle_dataset.get('metadata')

    return wf_pkl
