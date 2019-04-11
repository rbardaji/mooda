"""
Module to open data from the TOB files of Sea And Sun CTDs
"""
from mooda import WaterFrame
import pandas as pd
import re


class SeaAndSun:
    """
    Class to import TOB files from Sea And Sun.
    """

    @staticmethod
    def from_tob_to_waterframe(path, qc_tests=False):
        """
        It reads a TOB file and parses its content into a WaterFrame.

        Parameters
        ----------
            path: str
                Path where the TOB files is.
            qc_tests: bool (optional, qc_tests=False)
                If true, it executes WaterFrame.qc().

        Retuns
        ------
            wf: WaterFrame
        """
        # Find the number of line where starts data and column names
        # Read file
        lines = ""
        with open(path) as handle:
            lines = handle.readlines()

        data_start = None
        column_names = []
        for index, line in enumerate(lines):
            line_strip = line.strip()
            if line_strip.startswith('; Datasets'):
                # Column line
                line_split = line_strip.split(' ')
                column_names = [
                    column for column in line_split if column not in [';', '', 'Datasets']]
            elif line_strip.startswith('1 '):
                data_start = index
                break

        # Change name of columns and find date and time positions
        parameters = ['TIME']
        date_column = None
        time_column = None
        for index, name in enumerate(column_names):
            if name == 'Vbatt':
                parameters.append('BATT')
            elif name == 'Press':
                parameters.append('PRES')
            elif name == 'Temp':
                parameters.append('TEMP')
            elif name == 'SALIN':
                parameters.append('PSAL')
            elif name == 'Cond':
                parameters.append('CNDC')
            elif name == 'IntD':
                date_column = index + 1
            elif name == 'IntT':
                time_column = index + 1

        # Create dataframe
        df = pd.read_csv(path, sep=" ", skiprows=range(data_start), skipinitialspace=True,
                         header=None, parse_dates=[[date_column, time_column]])
        del df[0]
        df.columns = parameters
        df.set_index('TIME', inplace=True)

        # Creation of wf
        wf = WaterFrame(df=df)

        # Adding meaning
        for parameter in wf.parameters():
            if parameter == 'BATT':
                wf.meaning['BATT'] = {
                    'long_name': 'Remaining battery',
                    'units': 'Volt'}
            elif parameter == 'PRES':
                wf.meaning['PRES'] = {
                    'long_name': 'Sea water pressure',
                    'units': 'dBar'}
            elif parameter == 'TEMP':
                wf.meaning['TEMP'] = {
                    'long_name': 'Sea water temperature',
                    'units': 'degree Celsius'}
            elif parameter == 'TEMP':
                wf.meaning['CNDC'] = {
                    'long_name': 'Sea water conductivity',
                    'units': 'mS/cm'}
            elif parameter == 'TEMP':
                wf.meaning['PSAL'] = {
                    'long_name': 'Partial Salinity',
                    'units': 'PSU'}
        return wf
