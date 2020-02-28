""" Implementation of WaterFrame.use_only(*parameters*) """


def use_only(self, parameters_to_use, inplace=True):
    """
    It deletes all parameters except the input parameters.

    Parameters
    ----------
        parameters_to_use: list of str
            List of parameter names.
        inplace: bool
            If True, do operation inplace and return True.

    Returns
    -------
        new_wf: WaterFrame
            Result of the WaterFrame after the method application.
    """

    # Force to have a list in parameters
    if isinstance(parameters_to_use, str):
        parameters_to_use = [parameters_to_use]

    # Check if all parameters_to_use exist
    parameters_qc = []
    for parameter_to_use in parameters_to_use:
        if parameter_to_use not in self.parameters:
            raise KeyError(f"{parameter_to_use} is not a parameter of the WaterFrame.")
        else:
            parameters_qc.append(f"{parameter_to_use}_QC")
    parameters_to_use += parameters_qc

    if inplace:
        self.data = self.data[parameters_to_use]
        return True
    else:
        # Drop parameters and return a new WaterFrame
        new_wf = self.copy()
        new_wf.data = self.data[parameters_to_use]
        return new_wf
