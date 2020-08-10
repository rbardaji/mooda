""" Implementation of WaterFrame.resample(rule, method='mean') """
import pandas as pd

def resample(self, rule, method='mean', inplace=True):
    """
    Convenience method for frequency conversion and sampling of time series of the WaterFrame
    object. Warning: if WaterFrame.data contains MultiIndex, those indexes will disappear, obtaining a single 'TIME'
    index.

    Parameters
    ----------
        rule: str
            The offset string or object representing target conversion.
            You can find all of the resample options here:
            http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        method: "mean", "max", "min", optional, (method = "mean")
            Save the new value with the mean(), max() or min() function.
        inplace: bool
            If True, resample in place and return 'True', If False, return a new WaterFrame.

    Returns
    -------
        new_wf: WaterFrame
    """
    if isinstance(self.data.index,
        pd.MultiIndex) and 'DEPTH' in self.data.index.names:
    
        # pd.Grouper allows you to specify a "groupby instruction for a target
        # object".
        # Ref: https://stackoverflow.com/questions/15799162/resampling-within-a-pandas-multiindex
        level_values = self.data.index.get_level_values

        if method == "mean":
            data = (
                self.data.groupby(
                    [level_values(0)] +  # 0 is 'DEPTH'
                    [pd.Grouper(freq=rule, level='TIME')]).mean())
        elif method == "max":
            data = (
                self.data.groupby(
                    [level_values(0)] +  # 0 is 'DEPTH'
                    [pd.Grouper(freq=rule, level='TIME')]).max())
        elif method == "min":
            data = (
                self.data.groupby(
                    [level_values(0)] +  # 0 is 'DEPTH'
                    [pd.Grouper(freq=rule, level='TIME')]).min())
    else:
        # Legacy
        if method == "mean":
            data = self.data.resample(rule, level='TIME').mean()
        elif method == "max":
            data = self.data.resample(rule, level='TIME').max()
        elif method == "min":
            data = self.data.resample(rule, level='TIME').min()

    # Change "_QC" values to 0
    for key in self.data.keys():
        if "_QC" in key:
            data[key] = 0

    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf
