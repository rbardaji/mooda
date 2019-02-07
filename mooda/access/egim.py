""" Module to access to the Data Management Portal of EMSO Eric"""
# pylint: disable=C0302
import ast
import datetime
from io import StringIO
import warnings
import requests
import pandas as pd
import xarray as xr
from mooda import WaterFrame


class EGIM:
    """Class to download EGIM data from the EMSODEV DMP."""

    METADATA_00001 = {'site_code': 'OBSEA',
                      'platform_code': 'prototype1',
                      'data_mode': 'D',
                      'title': ('Test dataset from EMSODEV shallow water test '
                                'side'),
                      'summary': ('Test dataset from EMSODEV shallow water '
                                  'test side in the Mediterranean Sea'),
                      'naming_authority': 'UPC-CSIC',
                      'source': 'subsurface mooring',
                      'institution': 'EMSO',
                      'project': 'EMSODEV',
                      'keywords_vocabulary': 'GCMD Science Keywords',
                      'comment': 'Test data',
                      'geospatial_lat_min': '41.182',
                      'geospatial_lat_max': '41.182',
                      'geospatial_lat_units': 'degree_north',
                      'geospatial_lon_min': '1.752',
                      'geospatial_lon_mX': '1.752',
                      'geospatial_lon_units': 'degree_east',
                      'geospatial_vertical_min': '17.841',
                      'geospatial_vertical_max': '19.879',
                      'geospatial_vertical_positive': 'down',
                      'geospatial_vertical_units': 'meter',
                      'time_coverage_start': '2017-01-27T09:28:57Z',
                      'time_coverage_end': '2017-04-24T07:11:24Z',
                      'time_coverage_duration': '',
                      'time_coverage_resolution': 'PT30S',
                      'cmd_data_type': 'Station',
                      'data_type': 'OceanSITES time-series data',
                      'format_version': '1.3',
                      'publisher_name': '',
                      'publisher_email': '',
                      'publisher_url': '',
                      'references': ('http://www.oceansites.org, '
                                     'http://emso.eu'),
                      'data_assembly_center': '',
                      'update_interval': 'void',
                      'license': ('Follows CLIVAR (Climate Variability and '
                                  'Predictability) standards, cf. '
                                  'http://www.clivar.org/data/data_policy.php '
                                  'Data available free of charge. User '
                                  'assumes all risk for use of data. Uer must '
                                  'display citation in any publication or '
                                  'product using data. User must contact PI '
                                  'prior to any commercial use of data.'),
                      'citation': ('These data were collected and made freely '
                                   'available by the EMSODEV project.'),
                      'acknowledgement': ('This work benefited from the H2020 '
                                          'INFRADEV-3-2015 EMSODEV Project '
                                          'n°676555.'),
                      'date_created':
                      datetime.datetime.utcnow().isoformat()[:-6]+'Z',
                      'date_modified':
                      datetime.datetime.utcnow().isoformat()[:-6]+'Z',
                      'history': 'Data collected and processed with MOODA',
                      'processing_level': 'Ranges applied, bad data flagged',
                      'QC_indicator': 'excellent',
                      'contributor_name': 'EMSODEV project',
                      'contributor_role': 'consortium',
                      'contributor_email': ''}

    METADATA_AZORES = {'site_code': 'Azores',
                       'platform_code': 'EMSO-Azores',
                       'data_mode': 'D',
                       'title': 'Data from EGIM in the EMSO Site Azores',
                       'summary': ('This dataset contains pressure data '
                                   'acquired between July 2017 and August '
                                   '2018 on EMSO-Azores observatory by the '
                                   'EGIM. The pressure is one of the 7 core '
                                   'parameters monitored by the EGIM, EMSO '
                                   'Generic Instrumental Module. The EGIM '
                                   'prototype was deployed at Lucky Strike '
                                   'hydrothermal vent site, 25 m south west of'
                                   ' the active edifice Tour Eiffel, to '
                                   'monitor local hydrodynamic variability and'
                                   ' complement the data obtained by the '
                                   'numerous sensors set on this site: '
                                   'oceanographic mooring deployed south of '
                                   'the vent field, the multidisciplinary '
                                   'Seamon East node, autonomous current '
                                   'meters, array of temperature probes.'),
                       'naming_authority': '',
                       'source': 'subsurface mooring',
                       'institution': 'Ifremer, CNRS, IPGP',
                       'project': 'EMSODEV',
                       'keywords_vocabulary': 'GCMD Science Keywords',
                       'comment': 'Test data',
                       'geospatial_lat_min': '37.289433',
                       'geospatial_lat_max': '37.289433',
                       'geospatial_lat_units': 'degree_north',
                       'geospatial_lon_min': '-32.277567',
                       'geospatial_lon_mX': '-32.277567',
                       'geospatial_lon_units': 'degree_east',
                       'geospatial_vertical_min': '17.841',
                       'geospatial_vertical_max': '19.879',
                       'geospatial_vertical_positive': 'down',
                       'geospatial_vertical_units': 'meter',
                       'time_coverage_start': '2017-07-01T00:00:00Z',
                       'time_coverage_end': '2018-08-31T00:00:00Z',
                       'time_coverage_duration': '',
                       'time_coverage_resolution': 'PT30S',
                       'cmd_data_type': 'Station',
                       'data_type': 'OceanSITES time-series data',
                       'format_version': '1.3',
                       'publisher_name': '',
                       'publisher_email': '',
                       'publisher_url': '',
                       'references': ('http://www.oceansites.org, '
                                      'http://emso.eu'),
                       'data_assembly_center': '',
                       'update_interval': 'void',
                       'license': ('https://creativecommons.org/'
                                   'licenses/by/4.0/'),
                       'citation': ('These data were collected and made freely'
                                    ' available by the EMSODEV project.'),
                       'acknowledgement': ('This work benefited from the H2020'
                                           ' INFRADEV-3-2015 EMSODEV Project '
                                           'n°676555.'),
                       'date_created':
                       datetime.datetime.utcnow().isoformat()[:-6]+'Z',
                       'date_modified':
                       datetime.datetime.utcnow().isoformat()[:-6]+'Z',
                       'history': 'Data collected and processed with MOODA',
                       'processing_level': 'Ranges applied, bad data flagged',
                       'QC_indicator': 'excellent',
                       'contributor_name': 'EMSODEV project',
                       'contributor_role': 'consortium',
                       'contributor_email': ''}

    METADATA_ADCP_21582 = {'sensor_model': 'TELEDYNE RDI Workhorse monitor',
                           'sensor_manufactured': 'TELEDYNE RD INSTRUMENTS',
                           'sensor_reference': 'Workhorse_ADCP_21582',
                           'sensor_serial_number': '21582',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_icListen_1636 = {'sensor_model': 'OceanSonics icListen SB60L-ETH',
                              'sensor_manufactured': 'Ocean Sonics',
                              'sensor_reference': 'icListen-1636',
                              'sensor_serial_number': '1636',
                              'sensor_mount':
                              'mounted_on_seafloor_structure_riser',
                              'sensor_orientation': 'downward',
                              }

    METADATA_TEMP_SBE37 = {'standard_name': 'sea_water_temperature',
                           'units': 'degree_Celsius',
                           'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                           'long_name': ' Temperature of the water column',
                           'QC_indicator': 'Good data',
                           'processing_level': ('Ranges applied, bad data '
                                                'flagged'),
                           'valid_min': '-5.f',
                           'valid_max': '45.f',
                           'ancillary_variables': 'TEMP_QC',
                           'history': '',
                           'uncertainty': '0.002f',
                           'accuracy': '0.002f',
                           'precision': '0.002f',
                           'resolution': '0.002f',
                           'cell_methods': ('TIME: mean DEPTH: point '
                                            'LATITUDE: point LONGITUDE: '
                                            'point'),
                           'DM_indicator': 'D',
                           'reference_scale': 'ITS-90',
                           'sensor_model': 'SBE37-SIP-P7000-RS232',
                           'sensor_manufactured': 'Sea-Bird Scientific',
                           'sensor_reference': '37-14998',
                           'sensor_serial_number': '14998',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_TEMP_AADI4381 = {'standard_name': 'sea_water_temperature',
                              'units': 'degree_Celsius',
                              'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                              'long_name': 'Temperature of the water column',
                              'QC_indicator': 'Good data',
                              'processing_level': ('Ranges applied, bad data '
                                                   'flagged'),
                              'valid_min': '-5.f',
                              'valid_max': '40.f',
                              'ancillary_variables': 'TEMP_QC',
                              'history': '',
                              'uncertainty': '0.03f',
                              'accuracy': '0.03f',
                              'precision': '0.03f',
                              'resolution': '0.01f',
                              'cell_methods': ('TIME: mean DEPTH: point '
                                               'LATITUDE: point LONGITUDE: '
                                               'point'),
                              'DM_indicator': 'D',
                              'reference_scale': 'ITS-90',
                              'sensor_model': 'AADI-3005214831 DW4831',
                              'sensor_manufactured': ('Aanderaa Data '
                                                      'Instruments AS'),
                              'sensor_reference': '4381-606',
                              'sensor_serial_number': '606',
                              'sensor_mount':
                              'mounted_on_seafloor_structure_riser',
                              'sensor_orientation': 'downward',
                              }

    METADATA_TEMP_QC = {'long_name': 'quality flag for sea water temperature',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_PSAL_SBE37 = {'standard_name': 'sea_water_practical_salinity',
                           'units': 'PSU',
                           'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                           'long_name': 'Salinity of the water column',
                           'QC_indicator': 'Good data',
                           'processing_level': ('Ranges applied, bad data '
                                                'flagged'),
                           'valid_min': '33.f',
                           'valid_max': '37.f',
                           'ancillary_variables': 'PSAL_QC',
                           'history': '',
                           'uncertainty': '',
                           'accuracy': '',
                           'precision': '',
                           'resolution': '',
                           'cell_methods': ('TIME: mean DEPTH: point '
                                            'LATITUDE: point LONGITUDE: '
                                            'point'),
                           'DM_indicator': 'D',
                           'reference_scale': '',
                           'sensor_model': 'SBE37-SIP-P7000-RS232',
                           'sensor_manufactured': 'Sea-Bird Scientific',
                           'sensor_reference': '37-14998',
                           'sensor_serial_number': '14998',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_PSAL_QC = {'long_name': 'quality flag for sea water practical salinity',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_CNDC_SBE37 = {'standard_name':
                           'sea_water_electrical_conductivity',
                           'units': 'S/m',
                           'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                           'long_name': 'Electrical conductivity of the water column',
                           'QC_indicator': 'Good data',
                           'processing_level': 'Ranges applied, bad data flagged',
                           'valid_min': '0.f',
                           'valid_max': '7.f',
                           'ancillary_variables': 'CNDC_QC',
                           'history': '',
                           'uncertainty': '0.0003f',
                           'accuracy': '0.0003f',
                           'precision': '0.0003f',
                           'resolution': '0.0003f',
                           'cell_methods': ('TIME: mean DEPTH: point '
                                            'LATITUDE: point LONGITUDE: '
                                            'point'),
                           'DM_indicator': 'D',
                           'reference_scale': '',
                           'sensor_model': 'SBE37-SIP-P7000-RS232',
                           'sensor_manufactured': 'Sea-Bird Scientific',
                           'sensor_reference': '37-14998',
                           'sensor_serial_number': '14998',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_CNDC_QC = {'long_name': ('quality flag for sea water electrical '
                                      'conductivity'),
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_MPMN_SBE37 = {'standard_name': 'depth',
                           'units': 'meters',
                           'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                           'long_name': 'Moored instrument depth',
                           'QC_indicator': 'Good data',
                           'processing_level': ('Ranges applied, bad data '
                                                'flagged'),
                           'valid_min': '0.f',
                           'valid_max': '7000.f',
                           'ancillary_variables': 'MPMN_QC',
                           'history': '',
                           'uncertainty': '',
                           'accuracy': '',
                           'precision': '',
                           'resolution': '',
                           'cell_methods': ('TIME: mean DEPTH: point '
                                            'LATITUDE: point LONGITUDE: '
                                            'point'),
                           'DM_indicator': 'D',
                           'reference_scale': '',
                           'sensor_model': 'SBE37-SIP-P7000-RS232',
                           'sensor_manufactured': 'Sea-Bird Scientific',
                           'sensor_reference': '37-14998',
                           'sensor_serial_number': '14998',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_MPMN_QC = {'long_name': 'quality flag for instrument depth',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_SVEL_SBE37 = {'standard_name': 'sea_water_sound_velocity',
                           'units': 'meters/second',
                           'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                           'long_name': 'Sound velocity of the water column',
                           'QC_indicator': 'Good data',
                           'processing_level': 'Ranges applied, bad data flagged',
                           'valid_min': '',
                           'valid_max': '',
                           'ancillary_variables': 'SVEL_QC',
                           'history': '',
                           'uncertainty': '',
                           'accuracy': '',
                           'precision': '',
                           'resolution': '',
                           'cell_methods': ('TIME: mean DEPTH: point '
                                            'LATITUDE: point LONGITUDE: '
                                            'point'),
                           'DM_indicator': 'D',
                           'reference_scale': '',
                           'sensor_model': 'SBE37-SIP-P7000-RS232',
                           'sensor_manufactured': 'Sea-Bird Scientific',
                           'sensor_reference': '37-14998',
                           'sensor_serial_number': '14998',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_SVEL_QC = {'long_name': ('quality flag for sea water sound '
                                      'velocity'),
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_PRES_SBE54 = {'standard_name': 'sea_water_pressure',
                           'units': 'psia',
                           'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                           'long_name': 'Pressure of water',
                           'QC_indicator': 'Good data',
                           'processing_level': ('Ranges applied, bad data '
                                                'flagged'),
                           'valid_min': '0.f',
                           'valid_max': '10000.f',
                           'ancillary_variables': 'PRES_QC',
                           'history': '',
                           'uncertainty': '0.0011f',
                           'accuracy': '0.0011f',
                           'precision': '0.0011f',
                           'resolution': '0.0011f',
                           'cell_methods': ('TIME: mean DEPTH: point '
                                            'LATITUDE: point LONGITUDE: '
                                            'point'),
                           'DM_indicator': 'D',
                           'reference_scale': '',
                           'sensor_model': 'SBE54-0049',
                           'sensor_manufactured': 'Sea-Bird Scientific',
                           'sensor_reference': '54-0049',
                           'sensor_serial_number': '0049',
                           'sensor_mount':
                           'mounted_on_seafloor_structure_riser',
                           'sensor_orientation': 'downward',
                           }

    METADATA_PRES_QC = {'long_name': 'quality flag for sea water pressure',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_TUR4_NTURTD = {'standard_name': 'turbidity',
                            'units': 'NTU',
                            'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                            'long_name': 'Turbidity of water',
                            'QC_indicator': 'Good data',
                            'processing_level': ('Ranges applied, bad data '
                                                 'flagged'),
                            'valid_min': '',
                            'valid_max': '',
                            'ancillary_variables': 'TUR4_QC',
                            'history': '',
                            'uncertainty': '',
                            'accuracy': '',
                            'precision': '',
                            'resolution': '',
                            'cell_methods': ('TIME: mean DEPTH: point '
                                             'LATITUDE: point LONGITUDE: '
                                             'point'),
                            'DM_indicator': 'D',
                            'reference_scale': '',
                            'sensor_model': 'WETlabs ECO NTUrtd',
                            'sensor_manufactured': 'Sea-Bird Scientific',
                            'sensor_reference': 'NTURTD-648',
                            'sensor_serial_number': '648',
                            'sensor_mount':
                            'mounted_on_seafloor_structure_riser',
                            'sensor_orientation': 'horizontal',
                            }

    METADATA_TUR4_QC = {'long_name': 'quality flag for sea water turbidity',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_OSAT_AADI4381 = {'standard_name': 'oxygen_saturation',
                              'units': '%',
                              'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                              'long_name': 'oxygen saturation of water',
                              'QC_indicator': 'Good data',
                              'processing_level': ('Ranges applied, bad data '
                                                   'flagged'),
                              'valid_min': '0.f',
                              'valid_max': '100.f',
                              'ancillary_variables': 'OSAT_QC',
                              'history': '',
                              'uncertainty': '5f',
                              'accuracy': '5f',
                              'precision': '5f',
                              'resolution': '0.4f',
                              'cell_methods': ('TIME: mean DEPTH: point '
                                               'LATITUDE: point LONGITUDE: '
                                               'point'),
                              'DM_indicator': 'D',
                              'reference_scale': '',
                              'sensor_model': 'AADI-3005214831 DW4831',
                              'sensor_manufactured': ('Aanderaa Data '
                                                      'Instruments AS'),
                              'sensor_reference': '4381-606',
                              'sensor_serial_number': '606',
                              'sensor_mount':
                              'mounted_on_seafloor_structure_riser',
                              'sensor_orientation': 'downward',
                              }

    METADATA_OSAT_QC = {'long_name': 'quality flag for oxygen saturation',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    METADATA_DOX2_AADI4381 = {'standard_name': 'dissolbed_oxygen',
                              'units': 'microMols / liter',
                              'coordinates': 'TIME DEPTH LATITUDE LONGITUDE',
                              'long_name': 'moles of oxygen per unit mass',
                              'QC_indicator': 'Good data',
                              'processing_level': ('Ranges applied, bad data '
                                                   'flagged'),
                              'valid_min': '0.f',
                              'valid_max': '500.f',
                              'ancillary_variables': 'DOX2_QC',
                              'history': '',
                              'uncertainty': '8f',
                              'accuracy': '8f',
                              'precision': '8f',
                              'resolution': '2.5f',
                              'cell_methods': ('TIME: mean DEPTH: point '
                                               'LATITUDE: point LONGITUDE: '
                                               'point'),
                              'DM_indicator': 'D',
                              'reference_scale': '',
                              'sensor_model': 'AADI-3005214831 DW4831',
                              'sensor_manufactured': ('Aanderaa Data '
                                                      'Instruments AS'),
                              'sensor_reference': '4381-606',
                              'sensor_serial_number': '606',
                              'sensor_mount':
                              'mounted_on_seafloor_structure_riser',
                              'sensor_orientation': 'downward',
                              }

    METADATA_DOX2_QC = {'long_name': 'quality flag for dissolved oxygen',
                        'flag_values': '0, 1, 2, 3, 4, 7, 8, 9',
                        'flag_meanings': ('unknown good_data '
                                          'probably_good_data '
                                          'potentially_correctable_bad_data '
                                          'bad_data nominal_value '
                                          'interpolated_value missing_value'),
                        }

    def __init__(self, login=None, password=None):
        """
        It creates the instance variables login and password to use the DMP
        API.

        Parameters
        ----------
            login: str
                Login of the EMSODEV DMP API.
            password: str
                Password of the EMSODEV DMP API.
        """
        self.login = login
        self.password = password

    def observatories(self):
        """
        It represents the EGIM observatories accessible through the EMSODEV
        DMP API.

        Returns
        -------
            (statusCode, observatoryList): (int, list of str)
                (Status code answer of the API, list with names of
                observatories).
        """
        try:
            response = requests.get('http://api.emsodev.eu/observatories',
                                    auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if response.status_code == 200:
            answer = response.json()
            observatory_list = [observatory['name'] for observatory in answer]
            return response.status_code, observatory_list
        else:
            return response.status_code, None

    def instruments(self, observatory):
        """
        It represents the instruments deployed in an EGIM observatory.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.

        Returns
        -------
            (statusCode, instrumentList): (int, list of dict{"name": "string",
            "sensorLongName": "string", "sensorType": "string",
            "sn": "string"})
                (Status code answer of the API, list with dictionaries of
                available instruments)
        """
        try:
            response = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments'.format(
                    observatory), auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if response.status_code == 200:
            answer = response.json()
            instrument_list = answer['instruments']
            return response.status_code, instrument_list
        else:
            return response.status_code, None

    def metadata(self, observatory, instrument):
        """
        Get EGIM observatory instrument resource.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name.

        Return
        ------
            (statusCode, metadataList): (int, list of dict{{"instrumentName":
            "string", "metadataList": [{"metadata": "string","validityDate":
            "string"}]}})
                (Status code answer of the API, list with dictionaries of
                metadata).
        """
        try:
            response = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments/{}'.format(
                    observatory, instrument), auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if response.status_code == 200:
            answer = response.json()
            # The DMP API do not response with a JSON well formated.
            # We are going to fix their error with the following lines.
            metadata_dict = dict(answer['metadataList'][0])
            metadata_dict = metadata_dict['metadata']
            metadata_dict = metadata_dict.replace('{E', '{\'E')
            metadata_dict = metadata_dict.replace('=', '\':\'')
            metadata_dict = metadata_dict.replace(', ', '\', \'')
            metadata_dict = metadata_dict.split(", 'InstrumentPosition'")[0]
            metadata_dict += "}"
            metadata_dict = ast.literal_eval(metadata_dict)
            return response.status_code, metadata_dict
        else:
            return response.status_code, None

    def parameters(self, observatory, instrument):
        """
        Get the list of EGIM parameters for a specific EGIM instrument of an
        EGIM Observatory.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name

        Returns
        -------
            (statusCode, parameterList): (int, list of dict{"name": "string",
            "uom": "string"})
                (Status code answer of the API, list of dict of parameters)
        """
        try:
            response = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments/{}/'
                'parameters'.format(observatory, instrument),
                auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if response.status_code == 200:
            answer = response.json()
            parameter_list = answer['parameters']
            return response.status_code, parameter_list
        else:
            return response.status_code, None

    def observation(self, observatory, instrument, parameter, start_date=None,
                    end_date=None, limit=None):
        """
        Gets the time-series of a specific EGIM parameter in a certain time
        range or  the last X (limit) values for an EGIM instrument of an EGIM
        observatory.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name.
            parameter: str
                Parameter name.
            start_date: str, optional (start_date = None)
                Beginning date for the time series range. The date format is
                dd/MM/yyyy.
                If the start time is not supplied, we are going to use 'limit'.
            end_date: str
                End date for the time series range. The date format is
                dd/MM/yyyy.
                If the end time is not supplied, the current time will be used.
            limit: str
                The last x-measurements.
        Returns
        -------
            (statusCode, data): (int, list of Dataframe)
                (Status code answer of the API, list with dict of parameters)
        """

        # Query definition
        query = ''
        if limit is None:
            limit = 0
        else:
            limit = int(limit)
        if limit > 0:
            query = 'http://api.emsodev.eu/observatories' + \
                    '/{}/instruments/{}/parameters/{}/limit/{}'.format(
                        observatory, instrument, parameter, limit)
        else:
            if start_date and end_date:
                query = 'http://api.emsodev.eu/observatories' + \
                        '/{}/instruments'.format(observatory) + \
                        '/{}/parameters/{}?startDate={}&endDate={}'.\
                    format(instrument, parameter, start_date,
                           end_date)
            elif start_date:
                query = 'http://api.emsodev.eu/observatories' + \
                        '/{}/instruments/{}/parameters/{}?startDate={}'.\
                        format(observatory, instrument, parameter, start_date)
        try:
            response = requests.get(query, auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if response.status_code == 200:
            answer = response.json()
            observations = []
            for observation in answer['observations']:
                observations.append((observation['phenomenonTime'],
                                     observation['value']))
            # Format data
            df = pd.DataFrame({parameter: [x[1] for x in observations],  # pylint: disable: C0103
                               'time': [x[0] for x in observations]})
            # Changing the time values to a datatime
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.rename(columns={"time": "TIME"}, inplace=True)
            df.set_index('TIME', inplace=True)

            return response.status_code, df
        else:
            return response.status_code, None

    def acoustic_date(self, observatory, instrument):
        """
        Gets the date list of available acoustic files observed by a specific
        EGIM instrument of an EGIM Observatory.

        Parameters
        ----------
        observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name.
        Returns
        -------
            (statusCode, dateList): (int, list of dict{})
                (Status code answer of the API, list with dict of dates)
        """
        try:
            response = requests.get('http://api.emsodev.eu/observatories' +
                                    '/{}/instruments/{}/acousticfiledate'.format(
                                        observatory, instrument),
                                    auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if response.status_code == 200:
            answer = response.json()
            dateList = answer['acousticObservationDate']
            return response.status_code, dateList
        else:
            return response.status_code, None

    def acoustic_observation(self, observatory, instrument, date, hour_minute):
        """
        Gets an Acoustic file for a specific EGIM instrument of an EGIM
        Observatory.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name.
            date: str
                Date of Acoustic file. The date format is dd/MM/yyyy.
            hour_minute: str
                Hour and Minute of an Acoustic file. The Hour Minute format is
                HHMM.
        Returns
        -------
            (statusCode, text): (int, str)
                (Status code answer of the API, text of the acoustic file)
        """
        try:
            r = requests.get(
                'http://api.emsodev.eu/observatories' +
                '/{}/instruments/{}/acousticfile?date={}&hourMinute={}'.format(
                    observatory, instrument, date, hour_minute), auth=(
                        self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:

            # Write metadata
            metadata = {}
            lines = r.text.split("\n")
            for i, line in enumerate(lines):
                print(i, line)
                if i in [0, 1, 9, 10, 17, 18]:
                    continue
                if i == 28:
                    break
                parts = line.split("\t")
                metadata[parts[0]] = parts[1]

            # Write data
            data_ = StringIO(r.text.split("Data:")[1])
            data = pd.read_csv(data_, sep='\t')

            # Changing the time values to a datatime
            data['Time'] = pd.to_datetime(data['Time'])
            data.rename(columns={"Time": "TIME"}, inplace=True)
            data.set_index('TIME', inplace=True)

            return r.status_code, data, metadata
        else:
            return r.status_code, None

    @staticmethod
    def to_waterframe(data, metadata):
        """
        It creates a WaterFrame object from the input variables.

        Parameters
        ----------
            data: Pandas DataFrame
                Pandas DataFrame with data without WaterFrame format.
            metadata: dict
                Dictionary with metadata information.
        Returns
        -------
            wf: WaterFrame
                Data and metadata formated in a WaterFrame Object.
        """

        # Delete columns without data
        for key in data.keys():
            if data[key].empty:
                del data[key]

        wf = WaterFrame()
        wf.data = data

        # Change names
        for key in data.keys():
            if key == "depth":
                wf.data.rename(columns={"depth": "MPMN"}, inplace=True)
                wf.data["MPMN_QC"] = 0
                wf.meaning['MPMN'] = {"long_name": "depth", "units": "meters"}
            elif key == "salinity":
                wf.data.rename(columns={"salinity": "PSAL"}, inplace=True)
                wf.data["PSAL_QC"] = 0
                wf.meaning['PSAL'] = {
                    "long_name": "sea_water_practical_salinity",
                    "units": "PSU"}
            elif key == "conductivity":
                wf.data.rename(columns={"conductivity": "CNDC"}, inplace=True)
                wf.data["CNDC_QC"] = 0
                wf.meaning['CNDC'] = {
                    "long_name": "sea_water_electrical_conductivity",
                    "units": "S/m"}
            elif key == "sea_water_temperature":
                wf.data.rename(columns={"sea_water_temperature": "TEMP"},
                               inplace=True)
                wf.data["TEMP_QC"] = 0
                wf.meaning['TEMP'] = {"long_name": "sea_water_temperature",
                                      "units": "degree Celsius"}
            elif key == "sound_velocity":
                wf.data.rename(columns={"sound_velocity": "SVEL"},
                               inplace=True)
                wf.data["SVEL_QC"] = 0
                wf.meaning['SVEL'] = {"long_name": "sound_velocity",
                                      "units": "m/s"}
            elif key == "oxygen_saturation":
                wf.data.rename(columns={"oxygen_saturation": "OSAT"},
                               inplace=True)
                wf.data["OSAT_QC"] = 0
                wf.meaning['OSAT'] = {"long_name": "oxygen_saturation",
                                      "units": "%"}
            elif key == "dissolved_oxygen":
                wf.data.rename(columns={"dissolved_oxygen": "DOX2"},
                               inplace=True)
                wf.data["DOX2_QC"] = 0
                wf.meaning['DOX2'] = {
                    "long_name": "moles_of_oxygen_per_unit_mass",
                    "units": "uM/l"}
            elif key == "turbidity":
                wf.data.rename(columns={"turbidity": "TUR4"}, inplace=True)
                wf.data["TUR4_QC"] = 0
                wf.meaning['TUR4'] = {"long_name": "turbidity", "units": "NTU"}
            elif key == "sea_water_pressure":
                wf.data.rename(columns={"sea_water_pressure": "PRES"},
                               inplace=True)
                wf.data["PRES_QC"] = 0
                wf.meaning['PRES'] = {"long_name": "sea_water_pressure",
                                      "units": "PSI"}
            elif "N_S_sea_water_speed" in key:
                # Obtain the Bin number
                bin_number = key.split("_")[0].split("n")[1]
                wf.data.rename(columns={key: "VCUR{}".format(bin_number)},
                               inplace=True)
                wf.data["VCUR{}_QC".format(bin_number)] = 0
                wf.meaning['VCUR{}'.format(bin_number)] = {
                    "long_name": "northward_sea_water_velocity ",
                    "units": "mm/s"}
            elif "E_W_sea_water_speed" in key:
                # Obtain the Bin number
                bin_number = key.split("_")[0].split("n")[1]
                wf.data.rename(columns={key: "UCUR{}".format(bin_number)},
                               inplace=True)
                wf.data["UCUR{}_QC".format(bin_number)] = 0
                wf.meaning['UCUR{}'.format(bin_number)] = {
                    "long_name": "eastward_sea_water_velocity",
                    "units": "mm/s"}
            elif "error_sea_water_speed" in key:
                # Obtain the Bin number
                bin_number = key.split("_")[0].split("n")[1]
                wf.data.rename(columns={key: "error_sea_water_speed{}".format(
                    bin_number)}, inplace=True)
                wf.data["error_sea_water_speed{}_QC".format(bin_number)] = 0
                wf.meaning['error_sea_water_speed{}'.format(bin_number)] = {
                    "long_name": "error_sea_water_speed",
                    "units": "mm/s"}
            elif "vert_sea_water_speed" in key:
                # Obtain the Bin number
                bin_number = key.split("_")[0].split("n")[1]
                wf.data.rename(columns={key: "VCSP{}".format(bin_number)},
                               inplace=True)
                wf.data["VCSP{}_QC".format(bin_number)] = 0
                wf.meaning['VCSP{}'.format(bin_number)] = {
                    "long_name": "vert_sea_water_speed",
                    "units": "mm/s"}
            elif key == "pitch":
                wf.data.rename(columns={"pitch": "pitch"}, inplace=True)
                wf.data["pitch_QC"] = 0
                wf.meaning['pitch'] = {"long_name": "pitch",
                                       "units": "degrees"}
            elif key == "heading_of_device":
                wf.data.rename(columns={"heading_of_device": "heading"},
                               inplace=True)
                wf.data["heading_QC"] = 0
                wf.meaning['heading'] = {"long_name": "heading_of_device",
                                         "units": "degrees"}
            elif key == "roll":
                wf.data.rename(columns={"roll": "roll"}, inplace=True)
                wf.data["roll_QC"] = 0
                wf.meaning['roll'] = {"long_name": "roll", "units": "degrees"}
            elif "EGIM" in key and "SD_capacity" in key:
                # Obtain the Slot number
                slot_number = key.split("_")[1].split("t")[1]
                wf.data.rename(columns={key: "SD{}".format(slot_number)},
                               inplace=True)
                wf.data["SD{}_QC".format(slot_number)] = 0
                wf.meaning["SD{}".format(slot_number)] = {
                    "long_name": "slot_SD_capacity", "units": "kBytes"}
            elif "EGIM" in key and "_current" in key:
                # Obtain the Slot number
                slot_number = key.split("_")[1].split("t")[1]
                wf.data.rename(columns={key: "current{}".format(slot_number)},
                               inplace=True)
                wf.data["current{}_QC".format(slot_number)] = 0
                wf.meaning["current{}".format(slot_number)] = {
                    "long_name": "slot_current", "units": "mA"}
            elif key == "waterInstrusion":
                wf.data.rename(columns={"waterInstrusion": "leak"},
                               inplace=True)
                wf.data["leak_QC"] = 0
                wf.meaning['leak'] = {"long_name": "WaterIntrusion",
                                      "units": "bool"}
            elif "EGIM" in key and "_temperature" in key:
                # Obtain the Slot number
                slot_number = key.split("_")[1].split("t")[1]
                wf.data.rename(columns={key: "temperature{}".format(
                    slot_number)}, inplace=True)
                wf.data["temperature{}_QC".format(slot_number)] = 0
                wf.meaning["temperature{}".format(slot_number)] = {
                    "long_name": "EGIM_slot_temperature",
                    "units": "degree Celsius"}
            elif "EGIM" in key and "_pressure" in key:
                # Obtain the Slot number
                slot_number = key.split("_")[1].split("t")[1]
                wf.data.rename(columns={key: "pressure{}".format(slot_number)},
                               inplace=True)
                wf.data["pressure{}_QC".format(slot_number)] = 0
                wf.meaning["pressure{}".format(slot_number)] = {
                    "long_name": "EGIM_slot_pressure", "units": "mBars"}
            elif key == "voltage":
                wf.data.rename(columns={"voltage": "voltage"}, inplace=True)
                wf.data["voltage_QC"] = 0
                wf.meaning['voltage'] = {"long_name": "Incoming EGIM voltage",
                                         "units": "volts"}
            elif key == "energy":
                wf.data.rename(columns={"energy": "energy"}, inplace=True)
                wf.data["energy_QC"] = 0
                wf.meaning['energy'] = {"long_name": "Energy consumption",
                                        "units": "mAh"}
            elif key == "Comment":
                del wf.data["Comment"]
            elif key == "Temperature [C]":
                wf.data.rename(columns={"Temperature [C]": "TEMP"},
                               inplace=True)
                wf.data["TEMP_QC"] = 0
                wf.meaning['TEMP'] = {"long_name": "sea_water_temperature",
                                      "units": "degree Celsius"}
            elif key == "Humidity [%]":
                wf.data.rename(columns={"Humidity [%]": "RELH"}, inplace=True)
                wf.data["RELH_QC"] = 0
                wf.meaning['RELH'] = {"long_name": "RELH", "units": "%"}
            elif key == "Sequence #":
                wf.data.rename(columns={"Sequence #": "Sequence"},
                               inplace=True)
                wf.meaning['Sequence'] = {"long_name": "Sequence number",
                                          "units": "#"}
            elif key == "Data Points":
                wf.data.rename(columns={"Data Points": "Data Points"},
                               inplace=True)
                wf.meaning['Data Points'] = {"long_name": "Data Points",
                                             "units": "#"}

        wf.metadata = metadata

        return wf

    @staticmethod
    def to_netcdf(observatory, instrument, data, path,  qc_tests=True,
                  only_qc1=False):
        """It creates a netCDF3 file following the OceanSites standard.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name.
            data: Pandas dataframe, WaterFrame
                Data to be saved into a netCDF file.
            path: str
                Path to save the netCDF file.
            qc_tests: bool (optional, qc_tests=True)
                It indicates if QC test should be passed.
            only_qc1: bool (optional, only_qc1=True)
                It indicates to save only values with QC = 1.

        Returns
        -------
            True: bool
                Operation successful.

        """
        # Choose observatory metadata
        if observatory == 'EMSODEV-EGIM-node00001':
            metadata = EGIM.METADATA_00001

        # Creation of WaterFrame
        if type(data).__name__ == 'WaterFrame':
            wf = data
        else:
            wf = EGIM.to_waterframe(data, metadata)

        if qc_tests:
            # Creation of QC Flags following OceanSites recomendation
            for parameter in wf.parameters():
                # Reset QC Flags to 0
                wf.reset_flag(parameters=parameter, flag=0)
                # Flat test
                wf.flat_test(parameters=parameter, window=0, flag=4)
                # Spike test
                wf.spike_test(parameters=parameter, window=0, threshold=3, flag=4)
                # Range test
                wf.range_test(parameters=parameter, flag=4)
                # Change flags from 0 to 1
                wf.flag2flag(parameters=parameter, original_flag=0, translated_flag=1)
        if only_qc1:
            wf.use_only(flags=1)

        # Creation of an xarray dataset
        ds = xr.Dataset(data_vars=wf.data, attrs=metadata)

        # Creation of attr of dataset parameters
        for key in wf.data.keys():
            if key == 'TEMP':
                if observatory == 'EMSODEV-EGIM-node00001':
                    if instrument == '37-14998':
                        attr = EGIM.METADATA_TEMP_SBE37
                    elif instrument == '4381-606':
                        attr = EGIM.METADATA_TEMP_AADI4381
            if key == 'PSAL':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_PSAL_SBE37
            if key == 'SVEL':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_SVEL_SBE37
            if key == 'CNDC':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_CNDC_SBE37
            if key == 'MPMN':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_MPMN_SBE37
            if key == 'PRES':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_PRES_SBE54
            if key == 'TUR4':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_TUR4_NTURTD
            if key == 'OSAT':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_OSAT_AADI4381
            if key == 'DOX2':
                if observatory == 'EMSODEV-EGIM-node00001':
                    attr = EGIM.METADATA_DOX2_AADI4381
            if key == 'TEMP_QC':
                attr = EGIM.METADATA_TEMP_QC
            if key == 'PSAL_QC':
                attr = EGIM.METADATA_PSAL_QC
            if key == 'SVEL_QC':
                attr = EGIM.METADATA_SVEL_QC
            if key == 'CNDC_QC':
                attr = EGIM.METADATA_CNDC_QC
            if key == 'MPMN_QC':
                attr = EGIM.METADATA_MPMN_QC
            if key == 'PRES_QC':
                attr = EGIM.METADATA_PRES_QC
            if key == 'TUR4_QC':
                attr = EGIM.METADATA_TUR4_QC
            if key == 'OSAT_QC':
                attr = EGIM.METADATA_OSAT_QC
            if key == 'DOX2_QC':
                attr = EGIM.METADATA_DOX2_QC
            # Add the attrs to the variable
            ds[key].attrs = attr

        # Creation of the nc file
        ds.to_netcdf(path, format="NETCDF3_64BIT")

        return True

    @staticmethod
    def to_csv(observatory, data, path, qc_tests=True, only_qc1=False):
        """It creates a CSV file following the OceanSites standard.

        Parameters
        ----------
            observatory: str
                EGIM observatory name.
            instrument: str
                Instrument name.
            data: Pandas dataframe, WaterFrame
                Data to be saved into a netCDF file.
            path: str
                Path to save the CSV file.
            qc_tests: bool (optional, qc_tests=True)
                It indicates if QC test should be passed.
            only_qc1: bool (optional, only_qc1=True)
                It indicates to save only values with QC = 1

        Returns
        -------
            True: bool
                Operation successful.
        """
        # Choose observatory metadata
        if observatory == 'EMSODEV-EGIM-node00001':
            metadata = EGIM.METADATA_00001

        # Creation of WaterFrame
        if type(data).__name__ == 'WaterFrame':
            wf = data
        else:
            wf = EGIM.to_waterframe(data, metadata)

        if qc_tests:
            # Creation of QC Flags following OceanSites recomendation
            for parameter in wf.parameters():
                # Reset QC Flags to 0
                wf.reset_flag(parameters=parameter, flag=0)
                # Flat test
                wf.flat_test(parameters=parameter, window=0, flag=4)
                # Spike test
                wf.spike_test(parameters=parameter, window=0, threshold=3, flag=4)
                # Range test
                wf.range_test(parameters=parameter, flag=4)
                # Change flags from 0 to 1
                wf.flag2flag(parameters=parameter, original_flag=0, translated_flag=1)
        if only_qc1:
            wf.use_only(flags=1)

        # Metadata text creation
        metadata_text = "# Global attributes;Value"
        for key, value in metadata.items():
            metadata_text += "# " + str(key) + ";" + str(value) + "\n"

        # Creation of the csv file of the data
        wf.data.to_csv(path, sep=";", header=True)

        # Adding the metadata to the file
        with open(path, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(metadata_text.rstrip('\r\n') + '\n\n\n\n' + content)

        return True

    @staticmethod
    def from_raw_csv(observatory, path, qc_tests=False):
        """ It opens a csv file that contains data from an EGIM instrument.

        Parameters
        ----------
            observatory: str
                Name of the observatory. For now, only "EMSO-Azores" is
                possible.
                Write "EMSO-Azores" if the node is "EMSO-Azores" and source
                files are from: www.seanoe.org
            path: str
                Path where the file is.
            qc_tests: bool (optional)
                It indicates if QC test should be passed.

        Returns
        -------
            wf: WaterFrame
        """
        # Creation of a WaterFrame
        wf = WaterFrame()

        # The arguments of pandas.read_csv could change depending on the
        # source.
        sep = ","  # Delimiter to use.
        header = None  # Row number(s) to use as the column names, and the
        # start of the data.
        skiprows = None  # Line numbers to skip (0-indexed) or number of
        # lines to skip (int) at the start of the file.
        if observatory == "EMSO-Azores":
            sep = ";"
            header = 1
            skiprows = [2]
            format_time = '%d/%m/%Y %H:%M:%S'

            # Add metadata info
            wf.metadata = EGIM.METADATA_AZORES.copy()
        else:
            warnings.warn("EGIM cannot open the CSV because it does not know the observatory.")
            return
        # Load data from CSV into a DataFrame
        df = pd.read_csv(path, sep=sep, header=header, skiprows=skiprows)
        columns = df.columns.tolist()  # get the columns
        cols_to_use = columns[:len(columns)-1]  # drop the last one
        df = pd.read_csv(path, sep=sep, header=header, skiprows=skiprows,
                         usecols=cols_to_use)

        # Create the time index
        df['TIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'],
                                    format=format_time)
        df.set_index(pd.DatetimeIndex(df['TIME']), inplace=True)
        df.drop(['DATE', 'TIME'], inplace=True, axis=1)

        # Add QC columns
        for parameter in df.keys():
            df["{}_QC".format(parameter)] = 0

        # Add DataFrame into the WaterFrame
        wf.data = df.copy()

        # Change column names and add meanings
        for parameter in wf.parameters():
            if parameter == "TEMPERATURE":
                info = {'long_name': EGIM.METADATA_TEMP_SBE37['long_name'],
                        'units': EGIM.METADATA_TEMP_SBE37['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("TEMPERATURE", "TEMP")
            elif parameter == "CONDUCTIVITY":
                info = {'long_name': EGIM.METADATA_CNDC_SBE37['long_name'],
                        'units': EGIM.METADATA_CNDC_SBE37['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("CONDUCTIVITY", "CNDC")
            elif parameter == "PRESSION":
                info = {'long_name': EGIM.METADATA_MPMN_SBE37['long_name'],
                        'units': EGIM.METADATA_MPMN_SBE37['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("PRESSION", "MPMN")
            elif parameter == "SALINITY":
                info = {'long_name': EGIM.METADATA_PSAL_SBE37['long_name'],
                        'units': EGIM.METADATA_PSAL_SBE37['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("SALINITY", "PSAL")
            elif parameter == "SOUND SPEED":
                info = {'long_name': EGIM.METADATA_SVEL_SBE37['long_name'],
                        'units': EGIM.METADATA_SVEL_SBE37['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("SOUND SPEED", "SVEL")
            elif parameter == "OXYGEN":
                info = {'long_name': EGIM.METADATA_DOX2_AADI4381['long_name'],
                        'units': EGIM.METADATA_DOX2_AADI4381['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("OXYGEN", "DOX2")
            elif parameter == "SATURATION":
                info = {'long_name': EGIM.METADATA_OSAT_AADI4381['long_name'],
                        'units': EGIM.METADATA_OSAT_AADI4381['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("SATURATION", "OSAT")
            elif parameter == "NTU_SIGNAL_2":
                info = {'long_name': EGIM.METADATA_TUR4_NTURTD['long_name'],
                        'units': EGIM.METADATA_TUR4_NTURTD['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("NTU_SIGNAL_2", "TUR4")
            elif parameter == "PRESSURE":
                info = {'long_name': EGIM.METADATA_PRES_SBE54['long_name'],
                        'units': EGIM.METADATA_PRES_SBE54['units']}
                wf.meaning[parameter] = info.copy()
                wf.rename("PRESSURE", "PRES")
            else:
                # Delete the parameter
                wf.drop(parameter)

        # Creation of QC Flags following OceanSites recomendation
        if qc_tests:
            # Reset QC Flags to 0
            wf.reset_flag(flag=0)
            # Flat test
            wf.flat_test(window=0, flag=4)
            # Spike test
            wf.spike_test(window=0, threshold=3, flag=4)
            # Range test
            wf.range_test(flag=4)
            # Change flags from 0 to 1
            wf.flag2flag(original_flag=0, translated_flag=1)

        return wf
