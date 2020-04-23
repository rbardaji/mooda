""" Implementation fo WaterFrame.to_nc() """


def to_csv(self, path=None):
    """
    Create a CSV file with the WaterFrame data.
    The metadata and vocabulary will be placed in the first lines of the file with a # as first
    character of the line.

    Parameters
    ----------
        path: str
            Location and filename of the csv file.
            If path is None, the filename will be the
            metadata['id'].
    
    Returns
    -------
        path: str
            Location and filename of the csv file.
    """

    filename = path
    if path is None:
        filename = self.metadata['id'] + '.csv'

    with open(filename, 'w') as f:
        f.write('# METADATA\n')
        for key, value in self.metadata.items():
            if value != '':
               f.write(f'# {key}: {value}\n')
        f.write('\n')
        f.write('# VOCABULARY\n')
        for key, definition in self.vocabulary.items():
            f.write(f'# {key}:\n')
            for key_definition, value_definition in definition.items():
               f.write(f'#   - {key_definition}: {value_definition}\n')
        f.write('\n')

    # Save data in a csv
    self.data.to_csv(filename, mode='a')

    return filename
