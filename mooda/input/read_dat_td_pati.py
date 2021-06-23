"""
This method allows to read data from the DIY DT used by the Pati Cientific
"""
import pandas as pd

from ..waterframe import WaterFrame


def read_dat_td_pati(filename):
    """
    This method allows to read data from the DIY DT used by the Pati Cientific.

    Parameters
    ----------
        filename: str
            Location of the '.DAT' file
    
    Reurns
    ------
        wf: WaterFrame
    """

    # Vocabulary
    vocabulary = {
        'TIME': {
            'standard_name': 'time',
            'units': 'number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT)',
            'axis': 'T',
            'long_name': 'time of measurement',
            'valid_min': -9223372036854775808,
            'valid_max': 9223372036854775808,
            'qc_indicator': 'excellent',
            'processing_level': 'Ranges applied, bad data flagged',
            'uncertainty': 'nan',
            'comment': 'Time is going be visualized as YYYY/MM/DD hh:mm:ss'
        },
        'TIME_QC': {
            'long_name': 'quality flag for TIME',
            'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
            'flag_meanings': [
                'unknown',
                'good_data',
                'probably_good_data',
                'potentially_correctable_bad_data',
                'bad_data',
                'nominal_value',
                'interpolated_value',
                'missing_value']   
        },
        'DEPTH': {
            'standard_name': 'depth',
            'units': 'meters',
            'positive': 'down',
            'axis': 'Z',
            'reference': 'sea_level',
            'coordinate_reference_frame': 'urn:ogc:def:crs:EPSG::5831',
            'long_name': 'Depth of measurement',
            '_FillValue': 'nan',
            'valid_min': -10,
            'valid_max': 12000,
            'qc_indicator': 'excellent',
            'processing_level': 'Ranges applied, bad data flagged',
            'uncertainty': 'nan',
            'comment': 'Depth calculated from the sea surface'
        },
        'DEPTH_QC': {
            'long_name': 'quality flag for DEPTH',
            'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
            'flag_meanings': [
                'unknown',
                'good_data',
                'probably_good_data',
                'potentially_correctable_bad_data',
                'bad_data',
                'nominal_value',
                'interpolated_value',
                'missing_value'
            ]
        },
        'TEMP': {
            'standard_name': 'water_temperature',
            'units': 'degree_C',
            '_FillValue': 'nan',
            'coordinates': [
                'DEPTH'
                'TIME'
            ],
            'long_name': 'Water temperature',
            'qc_indicator': 'excelent',
            'processing_level': 'Ranges applied, bad data flagged',
            'valid_min': 0,
            'valid_max': 40,
            'comment': 'n/a',
            'ancillary_variables': 'TEMP_QC',
            'history': 'n/a',
            'uncertainty': 0.05,
            'accuracy': 0.35,
            'precision': 0.1,
            'resolution': 0.01,
            'cell_methods': {
                'TIME': 'point',
                'DEPTH': 'point'
            },
            'DM_indicator': 'D',
            'reference_scale': 'n/a',
            'sensor_model': 'PT-100',
            'sensor_orientation': 'downward'
        },
        'TEMP_QC': {
            'long_name': 'quality flag for TEMP',
            'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
            'flag_meanings': [
                'unknown',
                'good_data',
                'probably_good_data',
                'potentially_correctable_bad_data',
                'bad_data',
                'nominal_value',
                'interpolated_value',
                'missing_value'
            ]
        },
        'PRES': {
            'standard_name': 'water_pressure',
            'units': 'dBar',
            '_FillValue': 'nan',
            'coordinates': [
                'DEPTH'
                'TIME'
            ],
            'long_name': 'Water pressure',
            'qc_indicator': 'excelent',
            'processing_level': 'Ranges applied, bad data flagged',
            'valid_min': 0,
            'valid_max': 40,
            'comment': 'n/a',
            'ancillary_variables': 'PRES_QC',
            'cell_methods': {
                'TIME': 'point',
                'DEPTH': 'point'
            },
            'DM_indicator': 'D',
            'sensor_orientation': 'downward'
        },
        'PRES_QC': {
            'long_name': 'quality flag for TEMP',
            'flag_values': [0, 1, 2, 3, 4, 7, 8, 9],
            'flag_meanings': [
                'unknown',
                'good_data',
                'probably_good_data',
                'potentially_correctable_bad_data',
                'bad_data',
                'nominal_value',
                'interpolated_value',
                'missing_value'
            ]
        }
    }

    # Data
    df = pd.read_csv(filename, skiprows=[0, 1], parse_dates=[['data','hora']])

    df.rename(columns={'data_hora': 'TIME', 'pressio': 'PRES', 't_ms5837': 'TEMP'}, inplace=True)
    del df[' t_tsys01']
    del df['num_mostres']

    df['DEPTH'] = 0
    df['DEPTH_QC'] = 0
    df['TIME_QC'] = 0
    df['PRES_QC'] = 0
    df['TEMP_QC'] = 0

    df.set_index(['DEPTH', 'TIME'], inplace=True)

    wf = WaterFrame()
    wf.data = df
    wf.vocabulary = vocabulary
    
    wf.pres2depth()

    return wf
