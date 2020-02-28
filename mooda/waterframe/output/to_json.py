"""
Function to be imported in a WaterFrame. It creates a JSON with the WaterFrame information.
"""
import json


def to_json(self):
    """
    Get a JSON with the WaterFrame information.

    Returns
    -------
        json_string: str
            JSON string.
    """
    # Convert all dict values into str
    big_dict = {
        "metadata": dict(zip(self.metadata, map(str, self.metadata.values()))),
        "vocabulary": dict(zip(self.vocabulary, map(str, self.vocabulary.values()))),
        "data": self.data.to_json()
    }

    json_string = json.dumps(big_dict)

    return json_string
