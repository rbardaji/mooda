""" Implementation of a function to get a WaterFrame object from a JSON. """
import json
import pandas as pd


def read_json(self, json_string):
    """
    It gets a WaterFrame object from a JSON.

    Parameters
    ----------
        json_string: str
            String that contains a JSON.

    Returns
    -------
        done: bool
            True if the operation is successful.
    """

    done = False
    try:
        big_dict = json.loads(json_string)

        keys = big_dict.keys()
        if "metadata" in keys:
            self.metadata = big_dict["metadata"].copy()
        if "vocabulary" in keys:
            self.meaning = big_dict["vocabulary"].copy()
        if "data" in keys:
            self.data = pd.read_json(big_dict["data"])
        else:
            self.data = pd.read_json(big_dict)

        done = True
    except ValueError:
        pass
    return done
