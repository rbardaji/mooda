""" Implementation of WaterFrame.corr(parameter1, parameter2, method='pearson', min_periods=1) """


def corr(self, parameter1, parameter2, method='pearson', min_periods=1):
    """
    Compute pairwise correlation of data columns of parameter1 and parameter2, excluding NA/null
    values.

    Parameters
    ----------
        parameter1: str
            Key name of the column 1 to correlate.
        parameter2: str
            Key name of the column 2 to correlate.
        method: {‘pearson’, ‘kendall’, ‘spearman’}
            pearson : standard correlation coefficient
            kendall : Kendall Tau correlation coefficient
            spearman : Spearman rank correlation
        min_periods : int, optional
            Minimum number of observations required per pair of columns to
            have a valid result. Currently only available for pearson and
            spearman correlation
    Returns
    -------
        correlation_number: float
    """
    correlation_number = self.data[
        parameter1].corr(self.data[parameter2], method=method, min_periods=min_periods)
    return correlation_number
