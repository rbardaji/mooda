""" Implementation of WaterFrame.info_metadata(keys=None) """


def info_metadata(self, keys=None):
    """
    It returns a formatted string with the metadata information.

    Parameters
    ----------
        keys: string or list of strings (optional)
            Keys of WaterFrame.metadata

    Returns
    -------
        message: string
            Message with the metadata information.
    """

    if keys is None:
        keys = self.metadata.keys()

    message = ""
    for key, value in self.metadata.items():
        if key in keys and str(value).strip() != "":
            message += "  - {}: {}\n".format(key, value)

    return message[:-1]
