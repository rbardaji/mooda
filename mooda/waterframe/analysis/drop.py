""" Implementation of WaterFrame.drop(parameters) """

def drop(self, parameters, inplace=True):
    """
    Remove input parameters from WaterFrame.data.

    Parameters
    ----------
        parameters: str, list of str
            Parameters of WaterFrame.data.
        inplace: bool
            If True, Drop in place and return 'True', If False, return a copy of the WaterFrame
            without the input parameters.

    Returns
    -------
        new_wf: WaterFrame
    """
    keys = []
    if isinstance(parameters, str):
        keys.append(parameters)
        keys.append(parameters + '_QC')
    elif isinstance(keys, list):
        for parameter in parameters:
            keys.append(parameter)
            keys.append(parameter + '_QC')

    if inplace:
        self.data.drop(keys, axis=1, inplace=True)
        for key in keys:
            self.vocabulary.pop(key)
        return True
    else:
        new_wf = self.copy()
        new_wf.vocabulary = self.vocabulary.copy()
        new_wf.metadata = self.metadata.copy()
        new_wf.data = self.data.drop(keys, axis=1)
        for key in keys:
            new_wf.vocabulary.pop(key)

        return new_wf
