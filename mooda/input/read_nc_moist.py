""" Implementation of md.read_nc_moist() """
from . import read_nc

def read_nc_moist(path, resample_rule=False):
    """
    Open a NetCDF file from MOIST.
    This method only works with the files generated from CTDs.

    Parameters
    ----------
        path: str
            Path of the NetCDF file.
        resample_rule: str
            Time resample method. Use resample_rule = False to do not resample.
            See DateOffset objects:
            https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html

    Returns
    -------
        wf: WaterFrame
    """

    def drop(wf_in):
        wf_in.data.reset_index(inplace=True)
        del wf_in.data['LATITUDE']
        del wf_in.data['LONGITUDE']
        for key in wf_in.data.keys():
            if 'SDN_' in key or 'SEADATANET_QC' in key or 'INST' in key:
                del wf_in.data[key]
        del wf_in.data['crs']
        del wf_in.data['MAXT']

        del wf_in.vocabulary['LATITUDE']
        del wf_in.vocabulary['LONGITUDE']
        for key in list(wf_in.vocabulary.keys()):
            if 'SDN_' in key or 'SEADATANET_QC' in key or 'INST' in key:
                del wf_in.vocabulary[key]
        del wf_in.vocabulary['crs']

        return wf_in

    def resample(wf_in, resample_rule_in):
        wf_in.data.set_index('TIME', inplace=True)
        wf_in.data = wf_in.data.resample(resample_rule_in).mean()
        return wf_in

    def set_index(wf_in):
        wf_in.data.reset_index(inplace=True)
        wf_in.data.set_index(['DEPTH', 'TIME'], inplace=True)
        return wf_in

    def rename(wf_in):

        wf_in.vocabulary['DEPTH']['ancillary_variables'] = 'DEPTH_QC'
        wf_in.vocabulary['TIME']['ancillary_variables'] = 'TIME_QC'

        wf_in.vocabulary['CNDC'] = wf_in.vocabulary.pop('conductivity')
        wf_in.vocabulary['CNDC']['ancillary_variables'] = 'CNDC_QC'

        wf_in.vocabulary['TEMP'] = wf_in.vocabulary.pop('temperature')
        wf_in.vocabulary['TEMP']['ancillary_variables'] = 'TEMP_QC'

        wf_in.vocabulary['PRES'] = wf_in.vocabulary.pop('pressure')
        wf_in.vocabulary['PRES']['ancillary_variables'] = 'PRES_QC'

        wf_in.data.rename(
            columns={
                'conductivity': 'CNDC',
                'temperature': 'TEMP',
                'pressure': 'PRES'
            }, inplace=True)
        
        wf_in.data['PRES_QC'] = 0
        wf_in.data['TEMP_QC'] = 0
        wf_in.data['CNDC_QC'] = 0
        wf_in.data['TIME_QC'] = 0
        wf_in.data['DEPTH_QC'] = 0

        return wf_in

    wf = read_nc(path)
    wf = drop(wf)
    if resample_rule:
        wf = resample(wf, resample_rule)
    wf = set_index(wf)
    wf = rename(wf)

    return wf
