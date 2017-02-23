import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sys
import time
try:
    import oceanobs.observatory_dev as observatory
except ImportError:
    import observatory_dev as observatory


class EMSOdevAPI:

    def __init__(self, login=None, password=None):
        # Instance variables
        self.login = None
        self.password = None
        self.observatories = []
        self.instruments = []
        self.parameters = []
        self.observations = []
        self.observatory_name = None
        self.instrument_name = None
        self.parameter_name = None
        self.data = pd.DataFrame()

        if login is not None:
            self.login = login
            self.password = password

    def read_observatories(self):
        """
        Look for observatories and save them into a list in self.observatories
        :return: int with the status code of the answer (200 means that everything is ok).
        """
        # Cleaning the list of instruments and parameters to select. If you are here, the instruments and the parameters
        # should be re-serched.
        self.instruments = []
        self.parameters = []

        r = requests.get('http://api.emsodev.eu/observatories', auth=(self.login, self.password))
        if r.status_code != 200:
            return r.status_code
        answer = r.json()
        self.observatories = []
        for station in answer:
            self.observatories.append(station['name'])
        return r.status_code

    def read_instruments(self):
        """
        Look for instruments of an observatory and save them into a list in self.observatories.
        :return r.status_code: int with the status code of the answer (200 means that everything is ok).
        """
        self.parameters = []
        r = requests.get('http://api.emsodev.eu/observatories/{}/instruments'.format(self.observatory_name),
                         auth=(self.login, self.password))
        # Error code
        if r.status_code != 200:
            return r.status_code
        answer = r.json()
        # Add the instrumets to the list of instruments
        self.instruments = []
        for instrument in answer['instruments']:
            self.instruments.append(instrument['name'])
        return r.status_code

    def read_parameters(self):
        """
        Look for the parameters that the instrument can measure.
        :return: int with the status code of the answer (200 means that everything is ok).
        """
        r = requests.get('http://api.emsodev.eu/observatories/{}/instruments/{}/parameters'.format(
            self.observatory_name, self.instrument_name), auth=(self.login, self.password))
        if r.status_code != 200:
            return r.status_code
        answer = r.json()
        self.parameters = []
        for parameter in answer['parameters']:
            self.parameters.append(parameter['name'])
        return r.status_code

    def read_data(self, start_date='1d-ago', end_date=""):
        """
        Download data from the paramer/instrument/observatory.
        :param start_date: Time that you want to start to have data.
        :return: int with the status code of the answer (200 means that everything is ok).
        """
        def format_data():
            """
            Creation of the data dataframe with the oceanobs standard.
            """
            data_param = pd.DataFrame()
            if self.parameter_name == "sea_water_temperature":
                data_param = pd.DataFrame({'temp': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                               self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['temp_qc'] = 0
            elif self.parameter_name == "sea_water_pressure":
                data_param = pd.DataFrame({'pres': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                               self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['pres_qc'] = 0
            elif self.parameter_name == "turbidity":
                data_param = pd.DataFrame({'tur': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['tur_qc'] = 0
            elif self.parameter_name == "oxygen_saturation":
                data_param = pd.DataFrame({'oxy': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['oxy_qc'] = 0
            elif self.parameter_name == "dissolved_oxygen":
                data_param = pd.DataFrame({'oxy': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['oxy_qc'] = 0
            elif self.parameter_name == "salinity":
                data_param = pd.DataFrame({'sal': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['sal_qc'] = 0
            elif self.parameter_name == "depth":
                data_param = pd.DataFrame({'depth': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                                self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['depth_qc'] = 0
            elif self.parameter_name == "conductivity":
                data_param = pd.DataFrame({'cond': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                               self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['cond_qc'] = 0
            elif self.parameter_name == "sound_velocity":
                data_param = pd.DataFrame({'sovel': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                                self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param['time_qc'] = 0
                data_param['sovel_qc'] = 0

            self.data = self.data.append(data_param)

        if end_date == "":
            r = requests.get('http://api.emsodev.eu/observatories/{}/instruments/{}/parameters/{}?startDate={}'.format(
                self.observatory_name, self.instrument_name, self.parameter_name, start_date),
                auth=(self.login, self.password))
        else:
            r = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments/{}/parameters/{}?startDate={}?endDate={}'.format(
                    self.observatory_name, self.instrument_name, self.parameter_name, start_date, end_date),
                auth=(self.login, self.password))
        if r.status_code != 200:
            return r.status_code
        answer = r.json()
        self.observations = []
        for observation in answer['observations']:
            self.observations.append((observation['phenomenonTime'], observation['value']))
        format_data()
        return r.status_code

    def save_as_pickle(self, directory=""):
        """
        Save data in the oceanobs standard (two pandas dataframes).
        The metadata will be saved as metadata_[date].pkl and data will be saved as data_[date].pkl.
        :param directory: Directory where the data is saved
        :return:
        """
        def create_metadata_dataframe():
            """
            Creation of the metadada file
            :return: Pandas dataframe with the metadata.
            """
            metadata_cr = pd.DataFrame({'platform_code': [self.observatory_name],
                                        'wmo_platform_code': [" "],
                                        'institution': ["UPC - CSIC"],
                                        'type': ["Mooring time series"]})
            return metadata_cr

        # Creation of the metadata
        metadata = create_metadata_dataframe()
        # Directory management
        if len(directory) > 0 and directory[-1] != "\\":
            directory += "\\"
        save_time = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        # Save metadata
        path_metadata = directory + "metadata_emsodev_{}.pkl".format(save_time)
        metadata.to_pickle(path_metadata)
        # Save data
        path_data = directory + "data_emsodev_{}.pkl".format(save_time)
        self.data.to_pickle(path_data)


def tui(login=None, password=None):
    """
    Text-based User Interface to download EMSO data.
    :param login: Login of the API.
    :param password: Password of the API
    :return:
    """
    def input_login_password():
        login_f = input("Login: ")
        password_f = input("Password: ")
        return login_f, password_f

    def input_observatories():
        """
        Ask to the user to select an observatory or exit.
        :return choise_ob: Choise of the user
        """
        print("Observatories:")
        # Print the list of observatories and the exit option.
        for num_ob, station in enumerate(api.observatories):
            print("{}. {}".format(num_ob, station))
        print("z. Exit")
        # If there is just one observatory, there is nothing to select.
        if len(api.observatories) > 1:
            choise_ob = input("Enter the number of the station: ")
            # Change the choise to int if it is not z.
            if choise_ob != "z":
                choise_ob = int(choise_ob)
        else:
            choise_ob = 0
        return choise_ob

    def input_instruments():
        """
        Ask to the user for the instrument
        :return choise: Option that the user entered.
        """
        print("Instruments:")
        # Print the list of instruments, back and exit
        for num_ins, instrument in enumerate(api.instruments):
            print("{}. {}".format(num_ins, instrument))
        print("b. Back")
        print("z. Exit")
        # If there is just 1 instrument, there is nothing to select
        if len(api.instruments) > 1:
            choise_ins = input("Enter the number of the instrument: ")
            # Cast to int if it is a number
            if choise_ins != "z" and choise_ins != "b":
                choise_ins = int(choise_ins)
        else:
            choise_ins = 0
        return choise_ins

    def input_parameters():
        """
        Ask to the user for the number of the parameter that he/she want to use
        :return choise_param: Option of the user
        """
        print("Parameters:")
        # Print the list of parameters, back and exit
        for num_param, parameter in enumerate(api.parameters):
            print("{}. {}".format(num_param, parameter))
        print("b. Back")
        print("z. Exit")
        # Ask for the parameter
        choise_param = input("Enter the number of the parameter: ")
        # Cast to int if the choise is a number
        if choise_param != "z" and choise_param != "b":
            choise_param = int(choise_param)
        return choise_param

    def input_dates():
        start_date = input("Enter the start date (dd/MM/yyyy hh:mm:ss): ")
        if start_date == "":
            start_date = "13/02/2017 15:00:00"
        try:
            start_date = str(int(time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S").timetuple())))
        except ValueError:
            print("Error: {}".format(ValueError))
            input_dates()
        stop_date = input("Enter the stop date (dd/MM/yyyy hh:mm:ss): ")
        if stop_date != "":
            try:
                stop_date = str(time.mktime(datetime.datetime.strptime(stop_date, "%d/%m/%Y %H:%M:%S").timetuple()))
            except ValueError:
                print("Error: {}".format(ValueError))
                input_dates()
        download_data(start_date, stop_date)

    def search_observatories():
        """
        Search for the observatories of EMSO via the EMSOdev API
        :return:
        """
        # Cleaning the list of instruments and parameters to select. If you are here, the instruments and the parameters
        # should be re-serched.
        api.instruments = []
        api.parameters = []
        # We do this just one time
        if len(api.observatories) == 0:
            print("Searching for observatories...")
            code = api.read_observatories()
            # Error response code
            if code != 200:
                print("Error: Impossible to connect. Status code: {}".format(code))
                sys.exit()
        # Ask to the user wich observatory want to use
        choise = input_observatories()
        # Process choise of the user
        if choise == "z":
            # Save data and exit
            if api.data.size > 0:
                api.save_as_pickle()
            sys.exit()
        api.observatory_name = api.observatories[choise]
        # Now the observatory is selected. Continue searching for the instruments
        search_instruments()

    def search_instruments():
        """
        Search for the instruments of a observatory
        """
        # We clean the parameters list
        api.parameters = []
        # We will do this just if the observatory is changed and the list of instruments is empty
        if len(api.instruments) == 0:
            # Search for instruments
            print("Searching for instruments in {}...".format(api.observatory_name))
            code = api.read_instruments()
            # Error code
            if code != 200:
                print("Error: Impossible to connect. Status code: {}".format(code))
                return
        # Ask to the user for the number of the instrumet
        choise = input_instruments()
        # Process choise
        if choise == "z":
            # Save and exit
            if api.data.size > 0:
                api.save_as_pickle()
            sys.exit()
        elif choise == "b":
            # Go back to search observatories
            search_observatories()
        # Save the selected instrument
        api.instrument_name = api.instruments[choise]
        # Now, let's go to select the parameter
        search_parameters()

    def search_parameters():
        """
        Search for the parameter that the user want to download.
        :return:
        """
        # We are going to do this only one time
        if len(api.parameters) == 0:
            # Search for the parameters
            print("Searching for parameters in {}...".format(api.instrument_name))
            code = api.read_parameters()
            if code != 200:
                print("Error: Impossible to connect. Status code: {}".format(code))
                return
        # Ask to the user for the parameter
        choise = input_parameters()
        # Process the choise
        if choise == "z":
            # Saveand exit
            if api.data.size > 0:
                api.save_as_pickle()
            sys.exit()
        # Go back, the search isntruments
        elif choise == "b":
            search_instruments()
        # Save the parameter name
        api.parameter_name = api.parameters[choise]
        # Ask for the interval of dates
        input_dates()

    def download_data(start_date, stop_date):
        # Downloading data
        print("Downloading data...")
        code = api.read_data(start_date, stop_date)
        if code != 200:
            print("Error: Impossible to connect. Status code: {}".format(code))
            return
        print("Done.")
        print("Result:")
        print(api.data.head())
        search_parameters()

    print("If you are here is because you want to download EMSO data.")

    # Ask for login and password
    if login is None:
        login, password = input_login_password()
    api = EMSOdevAPI(login, password)

    search_observatories()


class EMSO(observatory.Observatory):

    def __init__(self):
        """
        Constructor of class
        """
        # Instance variables
        self.data = None
        self.metadata = None
        self.dialog = None

    def open(self, path_data, path_metadata):
        """
        Open EMSO files. Now, we just can open pikle files.
        :param path_data: Path where data is.
        :param path_metadata: Path where metadata is.
        """
        self.dialog = None
        try:
            self.data = pd.read_pickle(path_data)
            self.metadata = pd.read_pickle(path_metadata)
        except e:
            self.dialog = "Error: {}".format(e)

    @staticmethod
    def how_to_download_data(language='ENG'):
        """
        Returns a string text explaining how to download OBSEA data with the selected language. Now, we just have
        English.
        :param language: Idioma con el que quieres la explicacion
        :type language: str
        :return: Explicacion
        :rtype: str
        """
        tutorial = ""
        if language == 'ENG':
            tutorial = "Usa directamente la API de EMSOdev o la GUI de oceanobs."
        return tutorial

if __name__ == '__main__':

    ''' TUI TO DOWNLOAD DATA '''
    tui(login='emsodev', password='Emsodev2017')

    ''' EXEMPLE OF CLASS EMSO '''

    ''' LOADING DATA FROM PKL FILE '''
    path_data = "data_emsodev_20170221100859.pkl"
    path_metadata = "metadata_emsodev_20170221100859.pkl"
    ob = EMSO()
    ob.data = pd.read_pickle(path_data)
    ob.metadata = pd.read_pickle(path_metadata)

    ''' INFO '''
    print("METADATA INFORMATION")
    print(ob.info_metadata())
    print("DATA INFORMATION")
    print(ob.info_data())
    print("DATA MEANING")
    print(ob.info_parameters())

    ''' BUTTERWORTH FILTER'''
    ob.butterworth_filter('pres')
    if ob.dialog:
        print(ob.dialog)
        sys.exit()

    ''' PLOTS '''
    ob.plt_pres()
    plt.show()

    print("END")
