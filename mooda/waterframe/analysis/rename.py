""" Implementation of WaterFrame.rename(actual_name, new_name) """


def rename(self, actual_name, new_name, inplace=True):
    """
    It renames a parameter.

    Parameters
    ----------
        actual_name: str
            Actual name of a parameter.
        new_name: str
            New name of the parameter.
        inplace: bool
            If True, the rename is inplace and returns True

    Returns
    -------
        new_wf: WaterFrame
            WaterFrame with the renamed parameters.
    """

    new_data = self.data.rename(
        columns={actual_name: new_name, f'{actual_name}_QC': f'{new_name}_QC'},
        inplace=inplace)

    if inplace:
        new_wf = True
    else:
        new_wf = self.copy()
        new_wf.data = new_data

    return new_wf
