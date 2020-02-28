""" Implementation of WaterFrame.copy() """
from copy import deepcopy


def copy(self):
    """
    It returns a copy of the WaterFrame.

    Returns
    -------
        new_wf: WaterFrame
            A copy of the WaterFrame.
    """
    new_wf = deepcopy(self)
    return new_wf
