""" Implementation of WaterFrame.info_vocabulary(keys=None) """


def info_vocabulary(self, keys=None):
    """
    It returns a formatted string with the vocabulary information.

    Parameters
    ----------
        keys: string or list of strings (optional)
            The return message will contain the information of the input keys.
            If keys is None, all keys will be added to the return message.

    Returns
    -------
        message: str
            Message with the vocabulary information.
    """

    if keys is None:
        keys = self.vocabulary.keys()

    message = ""
    for key, vocabulary_dict in self.vocabulary.items():
        if key in keys:
            message += "  - {}\n".format(key)
            for vocabulary_key, vocabulary_value in vocabulary_dict.items():
                if str(vocabulary_value).strip() != "":
                    message += "    - {}: {}\n".format(vocabulary_key, vocabulary_value)

    return message[:-1]
