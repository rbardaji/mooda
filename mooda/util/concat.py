""" Implementation of WaterFrame.concat(waterframe) """
import pandas as pd


def concat(list_wf):
    """
    The concat function does all of the heavy lifting of performing concatenation operations between
    a list of WaterFrames.

    Parameters
    ----------
        list_wf: List of WaterFrames
            List of WaterFrames to be concatenated.

    Returns
    -------
        wf_one: WaterFrame
            WaterFrame with input data, metadata, and vocabulary concatenated.
    """
    for index, wf in enumerate(list_wf):
        if index == 0:
            wf_one = wf.copy()
        else:
            # Check if waterframes are from the same platform
            if wf.metadata.get('platform_name') == wf_one.metadata.get('platform_name'):

                # Same metadata, just change the coverage times
                start_wf = wf.metadata.get('time_coverage_start')
                end_wf = wf.metadata.get('time_coverage_end')

                start_wf_one = wf_one.metadata.get('time_coverage_start')
                end_wf_one = wf_one.metadata.get('time_coverage_end')

                if start_wf < start_wf_one:
                    wf_one.metadata['time_coverage_start'] = start_wf
                if end_wf > end_wf_one:
                    wf_one.metadata['time_coverage_end'] = end_wf

                # Concat data
                wf_one.data = pd.concat([wf_one.data, wf.data])
            else:
                raise NotImplementedError("All WaterFrames must be from the same 'platform_name'")

    return wf_one
