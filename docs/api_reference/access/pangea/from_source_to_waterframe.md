# Pangea.from_source_to_waterframe(*id_data*=*None*, *data*=*None*, *metadata*=*None*)

It is a static method.

It creates a mooda.WaterFrame object with data from www.pangea.de.

## Parameters

    id_data: int (optional, id_data=None)
        Id if the dataset of pangea to use.
    data: pandas.DataFrame (optional, data=None)
        DataFrame to include into the WaterFrame.
    metadata: dict (optional, metadata=None)
        Metadata to include into the WaterFrame.

## Returns

    wf_pangea: mooda.WaterFrame
        WaterFrame object.

Return to the [Pangea Index](index_pangea.md).
