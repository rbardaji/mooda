""" Implementation of WaterFrame.max(parameter_max) """


def max(self, parameter_max):
    """
    It returns the maximum value of a parameter and the value's indexes.

    Parameters
    ----------
        parameter_max: str
            Name of the parameter.

    Returns
    -------
        max_dict: dict
            Dictionary with the following format:
            {
                '<name of index 1>': <value of index 1>,
                '<name of index n>': <value of index n>,
                'name of parameter': < maximum value of parameter>
            }
    """

    df = self.data[parameter_max]
    df = df.reset_index()

    max_dict = df.loc[df[parameter_max] == df[parameter_max].max()].to_dict('record')[0]

    return max_dict
