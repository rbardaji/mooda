"""
Module to open data from the cnv files from Sea-Bird CTD
"""
from datetime import datetime
import pandas as pd
from mooda import WaterFrame


class SeaBird:
    """
    Class to import cnv files from Sea-Bird.
    """

    @staticmethod
    def from_cnv_to_waterframe(path, qc_tests=False):
        """
        It reads a cnv file and parses its content into a WaterFrame.

        Parameters
        ----------
            path: str
                Path where the TOB files is.
            qc_tests: bool (optional, qc_tests=False)
                If true, it executes WaterFrame.qc().

        Returns
        -------
            wf: WaterFrame
        """

        # Read file
        lines = ""
        with open(path, encoding="utf8", errors='ignore') as handle:
            lines = handle.readlines()

        # Extract info from cnv
        metadata = {}
        meaning = {}
        data_start = None
        column_names = []
        for index, line in enumerate(lines):
            line_strip = line.strip()
            if line_strip.startswith('* Sea-Bird '):
                # Metadata model line
                # ex: "* Sea-Bird SBE25 Data File:"
                line_split = line_strip.split(' ')
                metadata['model'] = line_split[2]
            elif line_strip.startswith('* Software Version '):
                # Sw version line
                # ex: "* Software Version 1.59"
                line_split = line_strip.split(' ')
                metadata['software_version'] = line_split[3]
            elif line_strip.startswith('* Temperature SN = '):
                # ex: "* Temperature SN = 031485"
                line_split = line_strip.split(' ')
                metadata['temperature_sn'] = line_split[4]
            elif line_strip.startswith('* Conductivity SN = '):
                # ex: "* Conductivity SN = 041189"
                line_split = line_strip.split(' ')
                metadata['conductivity_sn'] = line_split[4]
            elif line_strip.startswith('* System UpLoad Time = '):
                # ex: "* System UpLoad Time = Mar 18 2019 10:37:17"
                line_split = line_strip.split('* System UpLoad Time = ')
                metadata['system_upLoad_time'] = line_split[1]
            elif line_strip.startswith('* battery type = '):
                # ex: "* battery type = ALKALINE"
                line_split = line_strip.split(' ')
                try:
                    metadata['battery_type'] = line_split[4]
                except IndexError:
                    pass
            elif line_strip.startswith('# name '):
                # ex: "# name 0 = scan: Scan Count"
                line_split = line_strip.split(' ')
                name = line_split[4][:-1]  # Remove last ":"
                if name == 'prSM':
                    column_names.append('PRES')
                    meaning['PRES'] = {
                        'long_name': 'Strain Gauge Pressure',
                        'units': 'db'
                    }
                elif name == 't090C':
                    column_names.append('TEMP')
                    meaning['TEMP'] = {
                        'long_name': 'Sea Water Temperature',
                        'units': 'deg C'
                    }
                elif name == 'sal00':
                    column_names.append('PSAL')
                    meaning['PSAL'] = {
                        'long_name': 'Partial Salinity',
                        'units': 'PSU'
                    }
                elif name == 'seaTurbMtr':
                    column_names.append('TUR4')
                    meaning['PSAL'] = {
                        'long_name': 'Turbidity',
                        'units': 'FTU'
                    }
                elif name == 'wetStar':
                    column_names.append('FLUO')
                    meaning['FLUO'] = {
                        'long_name': 'Fluorescence',
                        'units': 'mg/m^3'
                    }
                elif name == 'c0mS/cm':
                    column_names.append('CNDC')
                    meaning['CNDC'] = {
                        'long_name': 'Conductivity',
                        'units': 'mS/cm'
                    }
                else:
                    column_names.append(name)
            elif line_strip.startswith('# start_time = '):
                # ex: "# name 0 = scan: Scan Count"
                line_split = line_strip.split('# start_time = ')
                metadata['start_time'] = line_split[1]
            elif line_strip.startswith('*END*'):
                data_start = index + 1

        # Create dataframe
        df = pd.read_csv(path, sep=" ", skiprows=range(data_start), skipinitialspace=True,
                         header=None)
        df.columns = column_names

        # Creation of TIME index
        start = pd.to_datetime(metadata['start_time']).to_pydatetime()
        seconds = (start - datetime(1970, 1, 1)).total_seconds()
        df['TIME'] = pd.to_datetime(df['timeS'] + seconds, unit='s')
        df.set_index('TIME', inplace=True)

        # Delete non used columns
        del df['timeS']
        del df['scan']
        del df['flag']

        # Creation of wf
        wf = WaterFrame(df=df, metadata=metadata, meaning=meaning)

        if qc_tests:
            wf.qc()

        return wf
