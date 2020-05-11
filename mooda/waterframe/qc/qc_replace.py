""" Implementation of wf.qc_replace() """

def qc_replace(self, parameters=None, to_replace=0, value=1, inplace=True):
    """
    Replace the values of QC from the input parameters.

    Parameters
    ----------
        parameters: None, str or list of str.
            List of parameters to change the values of QC. Ex: ['TEMP', 'PSAL'].
        to_replace: int
            QC value to replace.
        value: int
            Value to replace any values matching to_replace with.
        inplace: bool
            If inplace, makes changes inplace and returns True.
            Otherwhise, returns a new WaterFrame.
    
    Returns
    -------
        new_wf: WaterFrame
    """

    if parameters is None:
        parameters = self.parameters
    elif isinstance(parameters, str):
        parameters = [parameters]

    data = self.data.copy()

    for parameter in parameters:
        data[f'{parameter}_QC'].replace(to_replace=to_replace, value=value, inplace=True)

    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf