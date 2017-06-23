# -*- coding: cp850 -*
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import time
import sys
try:
    import oceanobs.observatory as observatory
except ImportError:
    import observatory


class OBSEA(observatory.Observatory):
    """
    Class to open OBSEA data (www.obsea.edu)
    """
    def __init__(self, path=None):
        """
        Constructor of class
        :param path: Path where data is
        :type path: str
        """

        # Instance variables
        self.data = None
        self.dialog = None

        if path is not None:
            self.open(path)

    def open(self, path):
        """
        Extract data from file or directory
        :param path: Path from the csv file or directory, or list of paths of csv files
        :type path: str of list of str
        """

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
            self.data = observatory.qc(self.data)
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
                self.data = observatory.qc(self.data)
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


if __name__ == '__main__':
    from matplotlib import style
    style.use('ggplot')

    print("Example of class OBSEA")

    # Data path
    path_data = r"C:\Users\rbard\Google Drive\Work\Data\obsea\obsea\all 30 min\short.txt"
    print("Data path: {}".format(path_data))

    ''' KNOW HOW MANY TIME TAKES TO OPEN DATA '''
    # ob = OBSEA()
    # estimation = ob.estimation_time_to_open(path_data)
    # print("Estimation of time to open the file: {}".format(estimation))
    # print("Size: {} Bytes".format(sys.getsizeof(ob.data)))

    ''' LOADING DATA FROM PATH'''
    print("Loading data, please wait.")
    ob = OBSEA(path_data)
    if ob.dialog:
        print(ob.dialog)
        sys.exit()
    # Saving the data in a pkl file
    ob.data.to_pickle("data.pkl")
    ob.metadata.to_pickle("metadata.pkl")

    ''' LOADING DATA FROM PKL FILE '''
    # ob = OBSEA()
    # ob.data = pd.read_pickle(r"C:\Users\rbard\Google Drive\Work\Data\obsea\data_obsea.pkl")
    # ob.metadata = pd.read_pickle(r"C:\Users\rbard\Google Drive\Work\Data\obsea\metadata_obsea.pkl")

    ''' INFO '''
    print("METADATA INFORMATION")
    print(ob.info_metadata())
    print("DATA INFORMATION")
    print(ob.info_data())
    print("DATA MEANING")
    print(ob.info_parameters())

    ''' DELETING COLUMNS NOT NEEDED '''
    # print("Deleting data that we do not need.")
    # ob.delete_param('sal')

    ''' RESAMPLING '''
    print("Resampling to calendar day frequency.")
    ob.resample_data('M')
    if ob.dialog:
        print(ob.dialog)
        sys.exit()

    ''' Clear '''
    # ob.clear_bad_data()

    ''' Butterworth Filter'''
    # print("Applying Butterworth filter.")
    # ob.butterworth_filter('temp')
    # if ob.dialog:
    #     print(ob.dialog)
    #     sys.exit()
    # ob.butterworth_filter('atemp')
    # if ob.dialog:
    #     print(ob.dialog)
    #     sys.exit()

    ''' SLICING '''
    '''print("Slicing.")
    start = ""
    stop = ""
    print("Start: {}/{}/{} {}:{}:{}, Stop: {}/{}/{} {}:{}:{}".format(start[:4], start[4:6], start[6:8], start[8:10],
                                                                     start[10:12],  start[12:], stop[:4], stop[4:6],
                                                                     stop[6:8], stop[8:10], stop[10:12],  stop[12:]))
    ob.slicing(start, stop)
    print("Done.")'''

    ''' PLOTS '''
    print("Making plots.")
    # ob.plt_all()
    # ob.plt_multiparam_one_plot('temp','atemp')
    ob.plt_qc()
    print("Done.")
    plt.show()

    print("END")
