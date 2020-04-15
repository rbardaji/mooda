""" Implementation of WaterFrame.to_pkl(path) """
import pickle


def to_pkl(self, path_pkl=None):
    """
    Save the WaterFrame into a pickle file.

    Parameters
    ----------
        path_pkl: str
            Location of the pickle file. If path_pkl is None, the path will be the metadata['id'].

    Returns
    -------
        path_pkl: str
            Location of the pickle file.
    """
    if path_pkl is None:
        path_pkl = self.metadata['id'] + '.pkl'

    pickle.dump(self.__dict__, open(path_pkl, "wb"))
    return path_pkl
