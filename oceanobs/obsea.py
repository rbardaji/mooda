# -*- coding: cp850 -*
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
try:
    import oceanobs.observatory as observatory
except ImportError:
    import observatory


class OBSEA(observatory.Observatory):
    """
    Clase para analizar los datos de OBSEA (www.obsea.edu)
    """
    def __init__(self, path=None):
        """
        Constructor of class
        :param path: Path where data is
        :type path: str
        """
        if path is not None:
            self.open(path)

    def open(self, path):
        """
        Extract data from file or directory
        :param path: Path from the csv file or directory, or list of paths of csv files
        :type path: str of list of str
        """

        def qc():
            """
            QC flags creation. We are using the GLOBAL QCFF flags.
            Flags are added to the data frame.
            Flag - Meaning
            0 - no quality control
            1 - value seems correct
            2 - value appears inconsistent with other values
            3 - value seems doubtful
            4 - value seems erroneous
            5 - value was modified
            6 - flagged land test
            7 - nominal_value
            8 - interpolated value
            9 - value missing
            """

            def qc_init():
                """
                Start with the QC flags. Writing "0" to all flags.
                Indicate that, for the moment, no data has qc.
                """
                self.data['time_qc'] = 0
                data_keys = self.data.keys()
                if 'temp' in data_keys:
                    self.data['temp_qc'] = 0
                if 'atemp' in data_keys:
                    self.data['atemp_qc'] = 0
                if 'cond' in data_keys:
                    self.data['cond_qc'] = 0
                if 'sal' in data_keys:
                    self.data['sal_qc'] = 0
                if 'sovel' in data_keys:
                    self.data['sovel_qc'] = 0
                if 'pres' in data_keys:
                    self.data['pres_qc'] = 0
                if 'atm' in data_keys:
                    self.data['atm_qc'] = 0
                if 'wis' in data_keys:
                    self.data['wis_qc'] = 0
                if 'wid' in data_keys:
                    self.data['wid_qc'] = 0
                if 'ph' in data_keys:
                    self.data['ph_qc'] = 0

            def qc_missing_values():
                """
                First level of qc. Look for missing values. Writing "9" to the flag.
                """
                data_keys = self.data.keys()
                if 'temp_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['temp']), 'temp_qc'] = 9
                if 'sal_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['sal']), 'sal_qc'] = 9
                if 'cond_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['cond']), 'cond_qc'] = 9
                if 'sovel_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['sovel']), 'sovel_qc'] = 9
                if 'pres_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['pres']), 'pres_qc'] = 9
                if 'atm_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['atm']), 'atm_qc'] = 9
                if 'wis_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['wisp']), 'wisp_qc'] = 9
                if 'wid_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['widi']), 'widi_qc'] = 9
                if 'atemp_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['atemp']), 'atemp_qc'] = 9
                if 'ph_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['ph']), 'ph_qc'] = 9

            def qc_impossible_values():
                """
                Second level of qc. Find the data that seems erroneous. Writing "4" to the flag.
                This test applies only where conditions can be further qualified. In this case, specific ranges for
                observations from the Mediterranean (OBSEA) further restrict what are considered sensible values.
                """
                data_keys = self.data.keys()
                if 'time_qc' in data_keys:
                    # Year greater than 2008
                    self.data.ix[self.data.index < datetime.datetime(2008, 1, 1), 'time_qc'] = 4
                if 'temp_qc' in data_keys:
                    # Sea Water Temperature in range 10øC to 28øC
                    self.data.ix[self.data['temp'] < 10.0, 'temp_qc'] = 4
                    self.data.ix[self.data['temp'] > 28.0, 'temp_qc'] = 4
                if 'sal_qc' in data_keys:
                    # Salinity in range 35 to 39
                    self.data.ix[self.data['sal'] < 35.0, 'sal_qc'] = 4
                    self.data.ix[self.data['sal'] > 39.0, 'sal_qc'] = 4
                if 'cond_qc' in data_keys:
                    # Conductivity in range 3.5S/m to 6.5S/m
                    self.data.ix[self.data['cond'] < 3.5, 'cond_qc'] = 4
                    self.data.ix[self.data['cond'] > 6.5, 'cond_qc'] = 4
                if 'sovel_qc' in data_keys:
                    # Sound velocity in range 1480m/s to 1550m/s
                    self.data.ix[self.data['sovel'] < 1480.0, 'sovel_qc'] = 4
                    self.data.ix[self.data['sovel'] > 1550.0, 'sovel_qc'] = 4
                if 'pres_qc' in data_keys:
                    # Pressure in range 18 dbar to 21 dbar
                    self.data.ix[self.data['pres'] < 18.0, 'pres_qc'] = 4
                    self.data.ix[self.data['pres'] > 21.0, 'pres_qc'] = 4
                if 'atm_qc' in data_keys:
                    # Sea level air pressure in range 850hPa to 1060hPa (mbar)
                    self.data.ix[self.data['atm'] < 0.850, 'atm_qc'] = 4
                    self.data.ix[self.data['atm'] > 1.060, 'atm_qc'] = 4
                if 'wis_qc' in data_keys:
                    # Wind speed in range 0m/s to 60m/s
                    self.data.ix[self.data['wisp'] < 0.0, 'wisp_qc'] = 4
                    self.data.ix[self.data['wisp'] > 60.0, 'wisp_qc'] = 4
                if 'wid_qc' in data_keys:
                    # Wind Direction in range 0ø to 360ø
                    self.data.ix[self.data['widi'] < 0.0, 'widi_qc'] = 4
                    self.data.ix[self.data['widi'] > 360.0, 'widi_qc'] = 4
                if 'atemp_qc' in data_keys:
                    # Air Temperature in range -10øC + 40øC
                    self.data.ix[self.data['atemp'] < -10.0, 'atemp_qc'] = 4
                    self.data.ix[self.data['atemp'] > 40.0, 'atemp_qc'] = 4

            def qc_spyke_test():
                """
                Third level of qc. Find the data that appears inconsistent with other values. Writing "2" to the flag.
                A large difference between sequential measurements, where one measurement is quite different from adjacent
                ones, is a spike in both size and gradient. The test does not consider the differences in depth, but assumes
                a sampling that adequately reproduces the temperature and salinity changes with depth. The algorithm is
                used on both the temperature and salinity instruments:
                    Test value = |V2 ? (V3 + V1)/2| ? |(V3 ? V1) / 2|
                where V2 is the measurement being tested as a spike, and V1 and V3 are the values above and below.
                """
                def spyke_formula(v1, v2, v3):
                    """
                    This is the formula we have to use for the spyke test
                    :param v2: Measurement being tested
                    :param v1: Before measurement
                    :param v3: Next measurement
                    :return: Test value
                    """
                    test_val = np.abs(v2 - (v2 + v1) / 2) - np.abs((v3 - v1) / 2)
                    return test_val

                data_keys = self.data.keys()
                if 'temp_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['temp_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.1øC for sampling interval of less
                        # than 1 minute
                        test_value = spyke_formula(self.data['temp'][i - 1], self.data['temp'][i],
                                                   self.data['temp'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.1:
                            self.data.set_value(self.data.index[i], 'temp_qc', 2)
                if 'cond_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['cond_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.1 for sampling interval of less
                        # than 1 minute
                        test_value = spyke_formula(self.data['cond'][i - 1], self.data['cond'][i],
                                                   self.data['cond'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.1:
                            self.data.set_value(self.data.index[i], 'cond_qc', 2)
                if 'sal_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['sal_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.5 for sampling interval of less
                        # than 1 minute
                        test_value = spyke_formula(self.data['sal'][i - 1], self.data['sal'][i],
                                                   self.data['sal'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.5:
                            self.data.set_value(self.data.index[i], 'sal_qc', 2)
                if 'pres_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['pres_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 1.0 for sampling interval of less
                        # than 1 minute
                        test_value = spyke_formula(self.data['pres'][i - 1], self.data['pres'][i],
                                                   self.data['pres'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 1.0:
                            self.data.set_value(self.data.index[i], 'pres_qc', 2)
                if 'atm_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['atm_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 5.0 for sampling interval of less
                        # than 1 minute
                        test_value = spyke_formula(self.data['atm'][i - 1], self.data['atm'][i],
                                                   self.data['atm'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 5.0:
                            self.data.set_value(self.data.index[i], 'atm_qc', 2)
                if 'atemp_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['atemp_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.2 for sampling interval of less
                        # than 1 minute
                        test_value = spyke_formula(self.data['atemp'][i - 1], self.data['atemp'][i],
                                                   self.data['atemp'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.2:
                            self.data.set_value(self.data.index[i], 'atemp_qc', 2)

            def qc_gradient_test():
                """
                Fourth level of qc. Find the data that appears inconsistent with other values. Writing "2" to the flag.
                This test is failed when the difference between vertically adjacent measurements is too steep.
                The test does not consider the differences in depth, but assumes a sampling that adequately reproduces the
                temperature and salinity changes with depth:
                    Test value = | V2 ? (V3 + V1)/2 |
                where V2 is the measurement being tested as a spike, and V1 and V3 are the values above and below.
                """
                def gradient_formula(v1, v2, v3):
                    """
                    This is the formula we have to use for the gradient test
                    :param v2: Measurement being tested
                    :param v1: Before measurement
                    :param v3: Next measurement
                    :return: Test value
                    """
                    test_val = np.abs(v2 - (v3 + v1) / 2)
                    return test_val

                data_keys = self.data.keys()
                if 'temp_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['temp_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.2øC for sampling interval of less
                        # than 1 minute
                        test_value = gradient_formula(self.data['temp'][i - 1], self.data['temp'][i],
                                                      self.data['temp'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.2:
                            self.data.set_value(self.data.index[i], 'temp_qc', 2)
                if 'cond_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['cond_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.2 for sampling interval of less
                        # than 1 minute
                        test_value = gradient_formula(self.data['cond'][i - 1], self.data['cond'][i],
                                                      self.data['cond'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.2:
                            self.data.set_value(self.data.index[i], 'cond_qc', 2)
                if 'sal_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['sal_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 1 for sampling interval of less
                        # than 1 minute
                        test_value = gradient_formula(self.data['sal'][i - 1], self.data['sal'][i],
                                                      self.data['sal'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 1:
                            self.data.set_value(self.data.index[i], 'sal_qc', 2)
                if 'pres_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['pres_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 2.0 for sampling interval of less
                        # than 1 minute
                        test_value = gradient_formula(self.data['pres'][i - 1], self.data['pres'][i],
                                                      self.data['pres'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 2.0:
                            self.data.set_value(self.data.index[i], 'pres_qc', 2)
                if 'atm_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['atm_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 10.0 for sampling interval of less
                        # than 1 minute
                        test_value = gradient_formula(self.data['atm'][i - 1], self.data['atm'][i],
                                                      self.data['atm'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 10.0:
                            self.data.set_value(self.data.index[i], 'atm_qc', 2)
                if 'atemp_qc' in data_keys:
                    for i in range(len(self.data.index)):
                        if i == 0 or i == len(self.data.index) - 1 or self.data['atemp_qc'][i] == 4:
                            continue
                        # Value appears inconsistent when the test value exceeds 0.4 for sampling interval of less
                        # than 1 minute
                        test_value = gradient_formula(self.data['atemp'][i - 1], self.data['atemp'][i],
                                                      self.data['atemp'][i + 1])
                        if (self.data.index[i + 1] - self.data.index[i - 1]).total_seconds() < 60 and test_value > 0.4:
                            self.data.set_value(self.data.index[i], 'atemp_qc', 2)

            def qc_good_data():
                """
                Final level of qc. Find data that seems correct. Writing "2" to the flag.
                Data was not flagged previously in "qc_impossible_values()", "qc_spyke_test()" and "qc_gradient_test()".
                """
                data_keys = self.data.keys()
                if 'time_qc' in data_keys:
                    self.data.ix[self.data['time_qc'] == 0, 'time_qc'] = 1
                if 'temp_qc' in data_keys:
                    self.data.ix[self.data['temp_qc'] == 0, 'temp_qc'] = 1
                if 'air_temp_qc' in data_keys:
                    self.data.ix[self.data['air_temp_qc'] == 0, 'air_temp_qc'] = 1
                if 'cond_qc' in data_keys:
                    self.data.ix[self.data['cond_qc'] == 0, 'cond_qc'] = 1
                if 'sal_qc' in data_keys:
                    self.data.ix[self.data['sal_qc'] == 0, 'sal_qc'] = 1
                if 'sovel_qc' in data_keys:
                    self.data.ix[self.data['sovel_qc'] == 0, 'sovel_qc'] = 1
                if 'pres_qc' in data_keys:
                    self.data.ix[self.data['pres_qc'] == 0, 'pres_qc'] = 1
                if 'atm_qc' in data_keys:
                    self.data.ix[self.data['atm_qc'] == 0, 'atm_qc'] = 1
                if 'wisp_qc' in data_keys:
                    self.data.ix[self.data['wisp_qc'] == 0, 'wisp_qc'] = 1
                if 'widi_qc' in data_keys:
                    self.data.ix[self.data['widi_qc'] == 0, 'widi_qc'] = 1
                if 'atemp_qc' in data_keys:
                    self.data.ix[self.data['atemp_qc'] == 0, 'atemp_qc'] = 1
                if 'ph_qc' in data_keys:
                    self.data.ix[self.data['ph_qc'] == 0, 'ph_qc'] = 1

            qc_init()
            qc_missing_values()
            qc_impossible_values()
            qc_spyke_test()
            qc_gradient_test()
            qc_good_data()

        def open_csv(path_csv):
            """
            Extract data from csv file
            :param path_csv: Path from the csv file
            :type path_csv: str
            """

            def data_format():
                """
                Change the actual names of the data by the standard names defined in oceanobs.
                """
                # Changing the index name
                self.data.index.rename(name='time', inplace=True)
                # Changing the name of the data
                data_keys = self.data.keys()
                if 'temperatura' in data_keys:
                    self.data.rename(columns={'temperatura': 'temp'}, inplace=True)
                if 'airTemperatue' in data_keys:
                    self.data.rename(columns={'airTemperatue': 'atemp'}, inplace=True)
                if 'conductividat' in data_keys:
                    self.data.rename(columns={'conductividat': 'cond'}, inplace=True)
                if 'salinitat' in data_keys:
                    self.data.rename(columns={'salinitat': 'sal'}, inplace=True)
                if 'velocitat_so' in data_keys:
                    self.data.rename(columns={'velocitat_so': 'sovel'}, inplace=True)
                if 'pressio' in data_keys:
                    self.data.rename(columns={'pressio': 'pres'}, inplace=True)
                if 'pressure' in data_keys:
                    self.data.rename(columns={'pressure': 'atm'}, inplace=True)
                if 'windSpeed' in data_keys:
                    self.data.rename(columns={'windSpeed': 'wisp'}, inplace=True)
                if 'windDirection' in data_keys:
                    self.data.rename(columns={'windDirection': 'widi'}, inplace=True)
                if 'ph_calcul' in data_keys:
                    self.data.rename(columns={'ph_calcul': 'ph'}, inplace=True)

            self.dialog = False
            # Extract data from csv file
            try:
                self.data = pd.read_csv(path_csv, sep='\t', parse_dates=['date_sistema'], index_col=0)
            except ValueError:
                self.data = pd.read_csv(path_csv, sep='\t', parse_dates=['date_time'], index_col=0)
            except FileNotFoundError as error:
                self.dialog = error
            except OSError:
                self.dialog = "Error: File = '{}' does not exist.".format(path)
            # Look for any error
            if self.dialog:
                return
            # Convert data to numeric
            self.data = self.data.apply(pd.to_numeric, args=('coerce',))
            # Format data with our standard
            data_format()

        def create_metadata():
            """
            Creation of the metadada file
            """
            self.metadata = pd.DataFrame({'platform_code': ["OBSEA"],
                                          'wmo_platform_code': ["INSITU MED NRT OBSERVATIONS 013 035"],
                                          'institution': ["UPC - Universitat Politecnica de Catalunya - Spain"],
                                          'type': ["Mooring time series"]})

        def open_list(path_list):
            """
            Read all the data of the list of paths
            :param path_list: List of paths
            :return:
            """
            big_data = pd.DataFrame()
            for one_path in path_list:
                _filename, file_extension = os.path.splitext(one_path)
                if file_extension == ".txt":
                    open_csv(one_path)
                    # Convert data to numeric
                    self.data = self.data.apply(pd.to_numeric, args=('coerce',))
                    # Add to big data
                    big_data = big_data.append(self.data)
            self.data = big_data
            # qc creation
            qc()
            # Copy of the data for future resets
            self.data_original = self.data.copy()

        def listdir_fullpath(d):
            return [os.path.join(d, f) for f in os.listdir(d)]

        self.dialog = False
        # Know if it is a string or a list
        if isinstance(path, str):
            # It is a string
            # Know if path is a file or a directory
            if os.path.isfile(path):
                # Path is a file
                open_csv(path)
                # qc creation
                qc()
                # Copy of the data for future resets
                self.data_original = self.data.copy()
            elif os.path.isdir(path):
                # Path is a directory
                path_lst = listdir_fullpath(path)
                open_list(path_lst)
            else:
                self.dialog = "Error: {} does not exist.".format(path)
        elif isinstance(path, list):
            # It is a list
            open_list(path)
        # Create metadata
        create_metadata()

    @staticmethod
    def how_to_download_data(lenguage='CAT'):
        """
        Explicacion de como descargar datos.
        :param lenguage: Idioma con el que quieres la explicacion
        :type lenguage: str
        :return: Explicacion
        :rtype: str
        """
        tutorial = ""
        if lenguage == 'CAT':
            tutorial = ("1. Abans de tot s'ha de seleccionar el per¡ode de temps (From-to).\n"
                        "2. DesprŠs es prem el boto Update Plot perquŠ s'actualitzi la grfica.\n"
                        "3. I per exportar les dades s'ha de pr‚mer el boto Generate Data.\n"
                        "A partir d'ara hi ha dues maneres per fer l'exportaciÂ¢ (dos quadres):\n"
                        "\ti. El primer quadre permet exportar nom‚s un parmetre i el que es fa es un promig de les"
                        " dades depenent del per¡ode (de hores si el per¡ode menor de 24 hores,  de dies si es menor "
                        "de 7 dies etc...).\n"
                        "\tii.  El segon quadre si que permet seleccionar m‚s d'un parmetre i tambÂ‚ permet fixar la "
                        "temporitzaciÂ¢ (cada 10 o 30 min). Aquesta opci¢ no es descarrega el fitxer directament com "
                        "la opci¢ 1 sin¢ que el descarrega via FTP, per aix• quan es prem el link download via FTP "
                        "(Raw data) es visualitza en vermell el proc‚s que s'ha de seguir per obtenir el fitxer.")
        return tutorial

if __name__ == '__main__':
    import sys
    from matplotlib import style
    style.use('ggplot')

    print("Example of class OBSEA")

    # Path de los datos
    # path_data = r"C:\Users\rbard\OneDrive\Data\obsea\buoy\buoy.txt"
    path_data = r"C:\Users\rbard\OneDrive\Data\obsea\obsea\ctd1_short.txt"
    # path_data = r"C:\Users\rbard\OneDrive\Data\obsea\obsea\ctd2.txt"
    # path_data = r"C:\Users\rbard\OneDrive\Data\obsea\obsea"
    print("Data path: {}".format(path_data))

    print("Loading data, please wait.")
    ob = OBSEA(path_data)
    if ob.dialog:
        print(ob.dialog)
        sys.exit()
    else:
        print("Done.")

    print("DATA INFO:")
    print("Platform code: {}".format(ob.metadata['platform_code'][0]))
    print("WMO platform code: {}".format(ob.metadata['wmo_platform_code'][0]))
    print("Institution: {}".format(ob.metadata['institution'][0]))
    print("Type: {}".format(ob.metadata['type'][0]))

    print(ob.data)

    # print("Resampling weekly frequency.")
    # ob.resample_data('W')
    # if ob.dialog:
    #     print(ob.dialog)
    #     sys.exit()
    # else:
    #     print("Done.")

    # Plots
    print("Making plots.")
    ob.plt_all()
    ob.plt_qc()
    print("Done.")

    # Slicing
    # print("Slicing.")
    # start = '20160117000000'
    # stop = '20160131000000'
    # print("Start: {}/{}/{} {}:{}:{}, Stop: {}/{}/{} {}:{}:{}".format(start[:4], start[4:6], start[6:8], start[8:10],
    #                                                                  start[10:12],  start[12:], stop[:4], stop[4:6],
    #                                                                  stop[6:8], stop[8:10], stop[10:12],  stop[12:]))
    # ob.slicing(start, stop)
    # print("Done.")

    # print(ob.data)
    # print(ob.how_to_download_data())
    # print(ob.info_data())

    plt.show()
