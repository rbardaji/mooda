""" Implementation of WaterFrame.slice_time(start=None, end=None) """
import pandas as pd
import datetime


def slice_time(self, start=None, end=None, inplace=True):
    """
    Delete data outside the time interval.

    Parameters
    ----------
        start: str, timestamp, optional (start=None)
            Start time interval with format 'YYYYMMDDhhmmss' or timestamp.
        end: str, timestamp, optional (end=None)
            End time interval with format 'YYYYMMDDhhmmss' or timestamp.
        inplace: bool
            If inplace is True, changes will be applied on self.data and returns True.
            Otherwhise, it returs the new WaterFrame

    Returns
    -------
        new_wf: WaterFrame
    """
    start_time = None
    end_time = None
    if start:
        start_time = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
    if end:
        end_time = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')
    
    # data = self.data.sort_index(level='TIME')
    data = self.data.sort_index()

    idx = pd.IndexSlice
    data = data.loc[idx[:, :, start_time:end_time], :]

    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf
