""" Implementation of WaterFrame.min(parameter_name) """


def min(self, parameter_min):
    """
    It returns the minimum value of a parameter and the value's indexes.

    Parameters
    ----------
        parameter_min: str
            Name of the parameter.

    Returns
    -------
        min_dict: dict
            Dictionary with the following format:
            {
                '<name of index 1>': <value of index 1>,
                '<name of index n>': <value of index n>,
                'name of parameter': < min value of parameter>
            }
    """

    df = self.data[parameter_min]
    df = df.reset_index()

    min_dict = df.loc[df[parameter_min] == df[parameter_min].min()].to_dict('record')[0]

    return min_dict
