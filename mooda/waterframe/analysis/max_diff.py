""" Implementation of WaterFrame.max_diff(parameter1, parameter2) """


def max_diff(self, parameter1, parameter2):
    """
    It calculates the maximum difference between the values of two parameters.

    Parameters
    ----------
        parameter1: str
            Key name of column 1 to calculate the difference.
        parameter2: str
            Key name of column 2 to calculate the difference.

    Returns
    -------
        where: index
            The position (index) of WaterFrame.data.
        value: float
            Value of the maximum difference.
    """

    where = (self.data[parameter1] - self.data[parameter2]).abs().idxmax()
    value = (self.data[parameter1] - self.data[parameter2]).abs().max()

    return (where, value)
