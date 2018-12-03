# WaterFrame.slice_time(*start*=*None*, *end*=*None*)

Delete data outside the time interval. If start or end is None, the slice will be from the beginning or to the final of the time series.

## Parameters

    start: str, timestamp, optional
        Start time interval with format 'YYYYMMDDhhmmss' or timestamp.
    end: str, timestamp, optional
        End time interval with format 'YYYYMMDDhhmmss' or timestamp.

## Returns

    True: bool
        The operation is successful.

Return to the [WaterFrame Index](index_waterframe.md).
