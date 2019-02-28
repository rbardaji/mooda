"""Module to read data from a Hobo instrument file.
Initial work from Carlos Rodero Garcia ()
"""
from io import StringIO
import csv
import re
import pandas as pd
from mooda import WaterFrame


class Hobo:
    """Class to import Hobo data from a csv file"""

    SN_REGEX = re.compile(r'(?:LGR S/N: |Serial Number:)(\d+)')

    @staticmethod
    def _find_units(header):
        """
        Internal function to find the units value from the header of a HOBO csv file.

        Parameters
        ----------
            header: str
                Header of one parameter.

        Returns
        -------
            units: str
                Units of the parameter.
        """
        header_units = header.split(",", 2)[1].strip()
        units = header_units.split(" ")[0].strip()
        return units

    @staticmethod
    def _find_name(header):
        """
        Infernal function. It looks for the label of the parameter in the header.

        Parameters
        ----------
            header: str
                Header of one parameter.

        Returns
        -------
            name: str
                Label of the parameter.
        """
        header_name = header.rsplit(",", 1)[1].strip(" )")
        if header_name.split(":")[0].strip() == "LBL":
            name = header_name.split(":")[1].strip()
        else:
            name = header.split(",", 1)[0].strip()
        return name

    @staticmethod
    def _find_long_name(header):
        """
        Infernal function. It looks for the long name of the parameter in the header.

        Parameters
        ----------
            header: str
                Header of one parameter.

        Returns
        -------
            long_name: str
                Long name of the parameter.
        """
        long_name = header.split(",", 1)[0].strip()
        return long_name

    @staticmethod
    def from_csv_to_waterframe(path, qc_tests=False):
        """
        It creates a WaterFrame form data of the csv file of a hobo logger.

        Parameters
        ----------
            path: str
                Path where the csv is located.
            qc_tests: bool (optional)
                Make the QC test of the WaterFrame before return it.

        Returns
        -------
            wf: WaterFrame
                WaterFrame with the data and metadata of the source csv file.
        """

        wf = WaterFrame()

        with open(path, encoding='utf-8-sig') as f_hobo:

            # Find title
            title = next(f_hobo)
            # Get title, we supposes that the title is in the first line and it is something like
            # ['"Título de trazado', ' test_lab"']
            wf.metadata['title'] = title.strip().split(":")[1].strip(" \"")

            # Find headers
            header = next(f_hobo)
            # Get serial number
            sn_match = Hobo.SN_REGEX.search(header)
            if sn_match:
                wf.metadata['sn'] = sn_match.groups()[0]

            # Find and set column names for headers
            headers = next(csv.reader(StringIO(header)))
            timestamp_position = None
            for i, header in enumerate(headers):
                # Find the column of the timestamp
                if 'Date Time' in header or 'Fecha Tiempo' in header:
                    timestamp_position = i
                    continue

                # Find the temperature
                temp_vocabulary = ['High Res. Temp.', 'High-Res Temp', 'Temp,', 'Temp.',
                                   'Temperature']
                if any(word in header for word in temp_vocabulary):
                    wf.meaning[header] = {
                        'long_name': Hobo._find_long_name(header),
                        'units': Hobo._find_units(header),
                        'name': 'temp'
                    }
                    continue

                # Find pressure
                if 'Pres abs,' in header:
                    wf.meaning[header] = {
                        'long_name': Hobo._find_long_name(header),
                        'units': Hobo._find_units(header),
                        'name': 'press'
                    }
                    continue

                # Find rh
                if 'RH,' in header:
                    wf.meaning[header] = {
                        'long_name': Hobo._find_long_name(header),
                        'units': Hobo._find_units(header),
                        'name': 'rh'
                    }
                    continue

                # Find battery
                if 'Batt, V' in header:
                    wf.meaning[header] = {
                        'long_name': Hobo._find_long_name(header),
                        'units': Hobo._find_units(header),
                        'name': 'batt'
                    }
                    continue

            if timestamp_position:
                wf.from_csv(path=f_hobo, names=headers, index_col=timestamp_position)

                # Rename columns
                for parameter in wf.parameters():
                    renamed = False
                    for key, value in wf.meaning.items():
                        if key == parameter:
                            wf.rename(parameter, value['name'])
                            renamed = True
                            break
                    if not renamed:
                        wf.drop(parameter)
                # Rename index to TIME
                wf.data.set_index(pd.DatetimeIndex(wf.data.index), inplace=True)
                wf.data.index.names = ['TIME']

                if qc_tests:
                    wf.qc()
            else:
                raise ValueError("Not possible to read the structure of the csv file.")
        return wf
