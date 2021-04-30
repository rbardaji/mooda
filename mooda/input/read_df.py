from ..waterframe import WaterFrame

def read_df(df, index_time, index_depth=None, metadata={}, vocabulary={}):
    """
    Get a WaterFrame from a pandas DataFrame.

    Parameters
    ----------
        df: Pandas.DataFrame
        index_time: str
            Column with the TIME index
        index_depth: str
            Column with the DEPTH index. If index_depth is None, DEPTH = 0
        metadata: dict
        vocabulary: dict

    Returns
    -------
        wf: mooda.WaterFrame
    """

    _df = df.copy()

    _df.reset_index(inplace=True)

    wf = WaterFrame()

    wf.metadata = metadata
    wf.vocabulary = vocabulary

    if index_depth is None:
        _df['DEPTH'] = 0

    _df.rename(columns={index_time: 'TIME'}, inplace=True)

    # Add QC columns
    keys = _df.keys()
    for key in keys:
        if key.endswith('_QC'):
            continue
        if f'{key}_QC' in keys:
            continue
        else:
            _df[f'{key}_QC'] = 0

    # Reindex
    _df.set_index(['DEPTH', 'TIME'], drop=True, inplace=True)

    wf.data = _df

    return wf
