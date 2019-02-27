"""
Module to open data from the txt files of LICOR datalogs
Initial work: Carlos Rodero, https://github.com/Carlos-Rodero/licor-python
"""
import itertools
import pandas as pd
from mooda import WaterFrame


class Licor:
    """
    Class to import Licor data from a txt file.
    It just contains a static method: from_text_to_waterframe(...)
    """

    @staticmethod
    def from_txt_to_waterframe(sensor_model, path, qc_tests=False):
        """
        Parameters
        ----------
            model: str
                Model of the sensor.
            path: str
                Path of the txt file.
            qc_tests: bool (optional)
                It indicates if QC test should be passed.

        Returns
        -------
            wf: WaterFrame
        """
        # Creation of a WaterFrame
        wf = WaterFrame()
        metadata = {}

        # The arguments of pandas.read_csv could change depending on the
        # source.
        if sensor_model == "LI-192":
            # lines to skip (int) at the start of the file.
            skiprows = 6
            # format_time = '%d/%m/%Y %H:%M:%S'

            # Add metadata info
            with open(path, encoding='utf-8-sig') as txtfile:
                # Read 2 first lines from csv
                for row in itertools.islice(txtfile, 1, 6):
                    # Delete return carriage from row
                    row = ''.join(row.splitlines())
                    # Split row by "\t" and remove empty strings returned in
                    # split()
                    parts = row.split(":")
                    if "Timestamp" not in parts[0]:
                        metadata[parts[0]] = parts[1].strip()

            # Load metadata to waterframe
            wf.metadata = metadata

            # Load data from table into a DataFrame
            df = pd.read_table(path, delim_whitespace=True, skiprows=skiprows,
                               low_memory=False)
            df['Ns'] = pd.to_numeric(df['Nanoseconds'], errors='coerce')/1000000000
            df['Input1'] = pd.to_numeric(df['Input1'], errors='coerce')

            # Create the time index. Convert "Nanoseconds" to seconds, add to
            # column "Seconds"
            # and convert to datetime
            df['Seconds_total'] = df['Ns'] + pd.to_numeric(df['Seconds'],
                                                           errors='coerce')
            df['TIME'] = pd.to_datetime(df['Seconds_total'], unit='s',
                                        errors='coerce')
            df.set_index(df['TIME'], inplace=True)
            df.drop(['DATAH', 'Record', 'Seconds', 'Nanoseconds', 'Ns',
                     'Seconds_total', 'TIME', 'MULT_1', 'CHK'], inplace=True,
                    axis=1)

            # Add DataFrame into the WaterFrame
            wf.data = df.copy()

            # Change parameter names and add QC columns
            for key in wf.data.keys():
                if key == "Input1":
                    wf.data.rename(columns={"Input1": "PPFD"}, inplace=True)
                    wf.data["PPFD_QC"] = 0
                    wf.meaning['PPFD'] = {"long_name":
                                          "Photosynthetic Photon Flux Density",
                                          "units": "µMol/M^2S"}

            # resample to seconds
            wf.resample('S')

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

        else:
            raise ValueError("model not found or implemented")

        return wf
