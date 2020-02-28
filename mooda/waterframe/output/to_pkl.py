""" Implementation of WaterFrame.to_pkl(path) """
import pickle


def to_pkl(self, path_pkl):
    """
    Save the WaterFrame into a pickle file.

    Parameters
    ----------
        path_pkl: str
            Location of the pickle file.

    Returns
    -------
        True: bool
            Allways returns true, otherwise it raises an error.
    """
    

    pickle.dump(self.__dict__, open(path_pkl, "wb"))
    return True
