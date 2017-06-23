import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import sys
import time
import pickle
try:
    import oceanobs.observatory as observatory
except ImportError:
    import observatory as observatory


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
        self.egim = pd.DataFrame()

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
        Look for instruments of an observatory and save them into a list in self.instruments.
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
        Look for the parameters that the instrument can measure and save them into a list in self.parameters.
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

    def read_data(self, start_date='01/04/2017', end_date=""):
        """
        Download data from the parameter/instrument/observatory. It saves the downloaded data into self.data with the
        oceanobs format. It creates the metadata variable and save it into self.metadata.
        :param start_date: Time that you want to start to have data.
        :param end_date: Time that you want to end to have data.
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
                data_param = observatory.qc(data_param)
                try:
                    del self.data['temp']
                    del self.data['temp_qc']
                except KeyError:
                    pass
            elif self.parameter_name == "sea_water_pressure":
                data_param = pd.DataFrame({'pres': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                               self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "turbidity":
                data_param = pd.DataFrame({'tur': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "oxygen_saturation":
                data_param = pd.DataFrame({'oxy': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "dissolved_oxygen":
                data_param = pd.DataFrame({'oxy': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "salinity":
                data_param = pd.DataFrame({'sal': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                              self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "depth":
                data_param = pd.DataFrame({'depth': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                                self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "conductivity":
                data_param = pd.DataFrame({'cond': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                               self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "sound_velocity":
                data_param = pd.DataFrame({'sovel': [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                                self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
                data_param = observatory.qc(data_param)
            elif self.parameter_name == "voltage":
                data_param = pd.DataFrame({'egim_voltage': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "waterInstrusion":
                data_param = pd.DataFrame({'egim_water_intrusion': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "energy":
                data_param = pd.DataFrame({'egim_current': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot1_current":
                data_param = pd.DataFrame({'egim_slot1_current': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot2_current":
                data_param = pd.DataFrame({'egim_slot2_current': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot3_current":
                data_param = pd.DataFrame({'egim_slot3_current': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot4_current":
                data_param = pd.DataFrame({'egim_slot4_current': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot5_current":
                data_param = pd.DataFrame({'egim_slot5_current': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot1_SD_capacity":
                data_param = pd.DataFrame({'egim_slot1_sd_capacity': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot2_SD_capacity":
                data_param = pd.DataFrame({'egim_slot2_sd_capacity': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot3_SD_capacity":
                data_param = pd.DataFrame({'egim_slot3_sd_capacity': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot4_SD_capacity":
                data_param = pd.DataFrame({'egim_slot4_sd_capacity': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot5_SD_capacity":
                data_param = pd.DataFrame({'egim_slot5_sd_capacity': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot1_temperature":
                data_param = pd.DataFrame({'egim_slot1_temperature': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot2_temperature":
                data_param = pd.DataFrame({'egim_slot2_temperature': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot3_temperature":
                data_param = pd.DataFrame({'egim_slot3_temperature': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot4_temperature":
                data_param = pd.DataFrame({'egim_slot4_temperature': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot5_temperature":
                data_param = pd.DataFrame({'egim_slot5_temperature': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot1_pressure":
                data_param = pd.DataFrame({'egim_slot1_pressure': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot2_pressure":
                data_param = pd.DataFrame({'egim_slot2_pressure': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot3_pressure":
                data_param = pd.DataFrame({'egim_slot3_pressure': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot4_pressure":
                data_param = pd.DataFrame({'egim_slot4_pressure': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')
            elif self.parameter_name == "EGIM_slot5_pressure":
                data_param = pd.DataFrame({'egim_slot5_pressure': [x[1] for x in self.observations],
                                           'time': [x[0] for x in self.observations]})
                data_param.set_index('time', inplace=True)
                data_param.index = pd.to_datetime(data_param.index, unit='s')

            if any("egim" in s for s in data_param.keys()):
                # We have read egim parameters
                self.egim = pd.concat([self.egim, data_param], axis=1)
            else:
                self.data = pd.concat([self.data, data_param], axis=1)
                # Adding time_qc
                try:
                    del self.data['time_qc']
                except KeyError:
                    pass
                self.data['time_qc'] = 0

        if end_date == "":
            r = requests.get('http://api.emsodev.eu/observatories/{}/instruments/{}/parameters/{}?startDate={}'.format(
                self.observatory_name, self.instrument_name, self.parameter_name, start_date),
                auth=(self.login, self.password))
        else:
            r = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments/{}/parameters/{}?startDate={}&endDate={}'.format(
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
        """
        def create_metadata_dataframe():
            """
            Creation of the metadada file
            :return: Pandas dataframe with the metadata.
            """
            metadata_cr = pd.DataFrame({'platform_code': [self.observatory_name],
                                        'wmo_platform_code': [" "],
                                        'institution': ["UPC - CSIC"],
                                        'type': ["Underwater lab"]})
            return metadata_cr

        # Creation of the metadata
        metadata = create_metadata_dataframe()
        # Directory management
        if len(directory) > 0 and directory[-1] != "\\":
            directory += "\\"
        save_time = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        # Saving the objects
        with open(directory + "emsodev_{}.pkl".format(save_time), 'wb') as fi:
            pickle.dump([metadata, self.data, self.egim], fi)


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
        print("a. All")
        print("b. Back")
        print("z. Exit")
        # Ask for the parameter
        choise_param = input("Enter the number of the parameter: ")
        # Cast to int if the choise is a number
        if choise_param != "z" and choise_param != "b" and choise_param != "a":
            choise_param = int(choise_param)
        return choise_param

    def input_dates():
        start_date = input("Enter the start date (dd/MM/yyyy): ")
        if start_date == "":
            start_date = "09/04/2017"
        stop_date = input("Enter the stop date (dd/MM/yyyy): ")
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
            # Save and exit
            if api.data.size > 0:
                api.save_as_pickle()
            sys.exit()
        # Go back, the search isntruments
        elif choise == "b":
            search_instruments()
        elif choise == "a":
            first_time = True
            for parameter in api.parameters:
                api.parameter_name = parameter
                # Ask for time
                if first_time:
                    start_date = input("Enter the start date (dd/MM/yyyy): ")
                    if start_date == "":
                        start_date = "15/04/2017"
                    stop_date = input("Enter the stop date (dd/MM/yyyy): ")
                    first_time = False
                # Download data
                print("Downloading data of {}".format(parameter))
                code = api.read_data(start_date, stop_date)
                if code != 200:
                    print("Error: Impossible to connect. Status code: {}".format(code))
                    return
                print("Done.")
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
        print("Result (5 first values):")
        print(api.data.head())
        search_parameters()

    print("If you are here is because you want to download EMSO data.")

    # Ask for login and password
    if login is None:
        login, password = input_login_password()
    api = EMSOdevAPI(login, password)

    search_observatories()


class EMSO(observatory.Observatory):

    def __init__(self, path_in=None):
        """
        Constructor of class.
        :param path_in: Path where data is.
        """
        # Instance variables
        self.data = None
        self.metadata = None
        self.dialog = None
        self.egim = None

        if path_in is not None:
            self.open(path_in)

    def open(self, path_in):
        """
        Open EMSO files. Now, we just can open pikle files.
        :param path_in: Path where data is.
        """
        self.dialog = None
        try:
            self.metadata, self.data, self.egim = pd.read_pickle(path_in)
        except TypeError as e:
            self.dialog = "Error: {}".format(str(e))

    """ Information """

    def info_egim(self):
        """
        Return some information about the selg.egim variable.
        :return: info of the egim
        :rtype: str
        """
        # Search for initial and final dates
        try:
            # Look for start and stop time
            start_time = self.egim.index.min()
            stop_time = self.egim.index.max()
            message = "- Start date: {}\n- End date: {}\n".format(start_time, stop_time)
            # Look for the parameters
            message += "- Parameters: \n"
            for key in self.egim.keys():
                # QC stadistics
                message += "\t- {}\n".format(key)
        except IndexError:
            message = "Error: No good data."
        return message[:-1]

    def stadistics_slots_current_consumptions(self):
        """
        Calculation of the Average, Max and Min current consumption of all the slots.
        :return:
        """
        message = ""
        # Obtain the necessary information of the egim
        try:
            egim_data = self.egim[['egim_slot5_current',
                                   'egim_slot4_current',
                                   'egim_slot3_current',
                                   'egim_slot2_current',
                                   'egim_slot1_current']]
        except AttributeError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 5 [mA]', 'Slot 4 [mA]', 'Slot 3 [mA]', 'Slot 2 [mA]', 'Slot 1 [mA]']
        message = egim_data.describe().ix[['mean', 'min', 'max']].astype(int).to_string()
        return message

    def stadistics_slots_temperature(self):
        """
        It calculates the mean, min, max and standar deviation of the temperature measured in all the EGIM slots.
        :return message: Mean, min, max and std of the temperature measured in all the EGIM slots.
        """
        message = ""
        # Obtain the necessary information of the egim
        try:
            egim_data = self.egim[['egim_slot1_temperature',
                                   'egim_slot2_temperature',
                                   'egim_slot3_temperature',
                                   'egim_slot4_temperature',
                                   'egim_slot5_temperature']]
        except AttributeError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 1 [degree Celsius]', 'Slot 2 [degree Celsius]', 'Slot 3 [degree Celsius]',
                             'Slot 4 [degree Celsius]', 'Slot 5 [degree Celsius]']
        message = egim_data.describe().ix[['mean', 'min', 'max', 'std']].round(2).to_string()
        return message

    def stadistics_slots_pressure(self):
        """
        It calculates the mean, min, max and standar deviation of the pressure measured in all the EGIM slots.
        :return message: Mean, min, max and std of the pressure measured in all the EGIM slots.
        """
        message = ""
        # Obtain the necessary information of the egim
        try:
            egim_data = self.egim[['egim_slot1_pressure',
                                   'egim_slot2_pressure',
                                   'egim_slot3_pressure',
                                   'egim_slot4_pressure',
                                   'egim_slot5_pressure']]
        except AttributeError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 1 [mBar]', 'Slot 2 [mBar]', 'Slot 3 [mBar]', 'Slot 4 [mBar]', 'Slot 5 [mBar]']
        message = egim_data.describe().ix[['mean', 'min', 'max', 'std']].round(2).to_string()
        return message

    """ Plot functions """

    def plt_egim_all(self):
        """
        Make all the graphs related to the engineering parameters of the EGIM.
        :return:
        """
        fig_dict = {}
        data_keys = self.egim.keys()

        if 'egim_current' in data_keys:
            fig_current = self.plt_egim_current()
            fig_dic['Current'] = fig_current
        if 'egim_voltage' in data_keys:
            fig_volt = self.plt_egim_voltage()
            fig_dict['Voltage'] = fig_volt
        if 'egim_slot1_sd_capacity' in data_keys:
            fig_sd = self.plt_egim_slot1_sd_capacity()
            fig_dict['Slot 1: SD capacity'] = fig_sd
        if 'egim_slot2_sd_capacity' in data_keys:
            fig_sd = self.plt_egim_slot2_sd_capacity()
            fig_dict['Slot 2: SD capacity'] = fig_sd
        if 'egim_slot3_sd_capacity' in data_keys:
            fig_sd = self.plt_egim_slot3_sd_capacity()
            fig_dict['Slot 3: SD capacity'] = fig_sd
        if 'egim_slot4_sd_capacity' in data_keys:
            fig_sd = self.plt_egim_slot4_sd_capacity()
            fig_dict['Slot 4: SD capacity'] = fig_sd
        if 'egim_slot5_sd_capacity' in data_keys:
            fig_sd = self.plt_egim_slot5_sd_capacity()
            fig_dict['Slot 5: SD capacity'] = fig_sd
        if 'egim_slot1_current' in data_keys:
            fig_amp = self.plt_egim_slot1_current()
            fig_dict['Slot 1: Current'] = fig_amp
        if 'egim_slot2_current' in data_keys:
            fig_amp = self.plt_egim_slot2_current()
            fig_dict['Slot 2: Current'] = fig_amp
        if 'egim_slot3_current' in data_keys:
            fig_amp = self.plt_egim_slot3_current()
            fig_dict['Slot 3: Current'] = fig_amp
        if 'egim_slot4_current' in data_keys:
            fig_amp = self.plt_egim_slot4_current()
            fig_dict['Slot 4: Current'] = fig_amp
        if 'egim_slot5_current' in data_keys:
            fig_amp = self.plt_egim_slot5_current()
            fig_dict['Slot 5: Current'] = fig_amp
        if 'egim_water_intrusion' in data_keys:
            fig_water = self.plt_egim_water_intrusion()
            fig_dict['Water intrusion'] = fig_water
        if 'egim_slot1_temperature' in data_keys:
            fig_tempe = self.plt_egim_slot1_temperature()
            fig_dict['Slot 1: Temperature'] = fig_tempe
        if 'egim_slot2_temperature' in data_keys:
            fig_tempe = self.plt_egim_slot2_temperature()
            fig_dict['Slot 2: Temperature'] = fig_tempe
        if 'egim_slot3_temperature' in data_keys:
            fig_tempe = self.plt_egim_slot3_temperature()
            fig_dict['Slot 3: Temperature'] = fig_tempe
        if 'egim_slot4_temperature' in data_keys:
            fig_tempe = self.plt_egim_slot4_temperature()
            fig_dict['Slot 4: Temperature'] = fig_tempe
        if 'egim_slot5_temperature' in data_keys:
            fig_tempe = self.plt_egim_slot5_temperature()
            fig_dict['Slot 5: Temperature'] = fig_tempe
        if 'egim_slot1_pressure' in data_keys:
            fig_pres = self.plt_egim_slot1_pressure()
            fig_dict['Slot 1: Pressure'] = fig_pres
        if 'egim_slot2_pressure' in data_keys:
            fig_pres = self.plt_egim_slot2_pressure()
            fig_dict['Slot 2: Pressure'] = fig_pres
        if 'egim_slot3_pressure' in data_keys:
            fig_pres = self.plt_egim_slot3_pressure()
            fig_dict['Slot 3: Pressure'] = fig_pres
        if 'egim_slot4_pressure' in data_keys:
            fig_pres = self.plt_egim_slot4_pressure()
            fig_dict['Slot 4: Pressure'] = fig_pres
        if 'egim_slot5_pressure' in data_keys:
            fig_pres = self.plt_egim_slot5_pressure()
            fig_dict['Slot 5: Pressure'] = fig_pres
        if 'egim_slot5_pressure' in data_keys:
            fig_energy = self.plt_egim_energy()
            fig_dict['Energy'] = fig_energy

        return fig_dict

    def plt_egim_voltage(self):
        """
        It creates a plot of the EGIM input voltage over time.
        :return: Figure
        """
        self.dialog = False
        fig_volt, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_voltage'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No voltage data."
        axes.set_title('Voltage of EGIM')
        axes.set_ylabel('mV')
        axes.set_xlabel('Time UTC')
        return fig_volt

    def plt_egim_slot4_sd_capacity(self):
        """
        It creates a plot with the SD remeanding capacity of the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_slot, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot4_sd_capacity'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No capacity data."
        axes.set_title('Slot 4: SD capacity')
        axes.set_ylabel('KBytes')
        axes.set_xlabel('Time UTC')
        return fig_slot

    def plt_egim_slot1_sd_capacity(self):
        """
        It creates a plot with the SD remeanding capacity of the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_slot, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot1_sd_capacity'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No capacity data."
        axes.set_title('Slot 1: SD capacity')
        axes.set_ylabel('KBytes')
        axes.set_xlabel('Time UTC')
        return fig_slot

    def plt_egim_slot2_sd_capacity(self):
        """
        It creates a plot with the SD remeanding capacity of the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_volt, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot2_sd_capacity'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No capacity data."
        axes.set_title('Slot 2: SD capacity')
        axes.set_ylabel('KBytes')
        axes.set_xlabel('Time UTC')
        return fig_volt

    def plt_egim_slot3_sd_capacity(self):
        """
        It creates a plot with the SD remeanding capacity of the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_volt, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot3_sd_capacity'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No capacity data."
        axes.set_title('Slot 3: SD capacity')
        axes.set_ylabel('KBytes')
        axes.set_xlabel('Time UTC')
        return fig_volt

    def plt_egim_slot5_sd_capacity(self):
        """
        It creates a plot with the SD remeanding capacity of the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_volt, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot5_sd_capacity'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No capacity data."
        axes.set_title('Slot 5: SD capacity')
        axes.set_ylabel('KBytes')
        axes.set_xlabel('Time UTC')
        return fig_volt

    def plt_egim_slot1_current(self):
        """
        It creates a plot with the current consumption of the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_amp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot1_current'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No slot1 current data."
        axes.set_title('Slot 1: Current')
        axes.set_ylabel('mA')
        axes.set_xlabel('Time UTC')
        return fig_amp

    def plt_egim_slot2_current(self):
        """
        It creates a plot with the current consumption of the slot 2 over time.
        :return: Figure
        """
        self.dialog = False
        fig_amp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot2_current'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No slot 2 current data."
        axes.set_title('Slot 2: Current')
        axes.set_ylabel('mA')
        axes.set_xlabel('Time UTC')
        return fig_amp

    def plt_egim_slot3_current(self):
        """
        It creates a plot with the current consumption of the slot 3 over time.
        :return: Figure
        """
        self.dialog = False
        fig_amp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot3_current'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No slot3 current data."
        axes.set_title('Slot 3: Current')
        axes.set_ylabel('mA')
        axes.set_xlabel('Time UTC')
        return fig_amp

    def plt_egim_slot4_current(self):
        """
        It creates a plot with the current consumption of the slot 4 over time.
        :return: Figure
        """
        self.dialog = False
        fig_amp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot4_current'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No slot4 current data."
        axes.set_title('Slot 4: Current')
        axes.set_ylabel('mA')
        axes.set_xlabel('Time UTC')
        return fig_amp

    def plt_egim_slot5_current(self):
        """
        It creates a plot with the current consumption of the slot 5 over time.
        :return: Figure
        """
        self.dialog = False
        fig_amp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot5_current'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No slot5 current data."
        axes.set_title('Slot 5: Current')
        axes.set_ylabel('mA')
        axes.set_xlabel('Time UTC')
        return fig_amp

    def plt_egim_water_intrusion(self):
        """
        It creates a plot with the water intrusion values over time. 0 means no water intrusion,
        1 means water intrusion.
        :return: Figure
        """
        self.dialog = False
        fig_water, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_water_intrusion'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No water intrusion data."
        axes.set_title('Water intrusion')
        axes.set_ylabel('1-Yes, 0-No')
        axes.set_xlabel('Time UTC')
        return fig_water

    def plt_egim_slot1_temperature(self):
        """
        It creates a plot with the temperature measured in the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_tempe, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot1_temperature'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 1: Temperature')
        axes.set_ylabel('Degree Celsius')
        axes.set_xlabel('Time UTC')
        return fig_tempe

    def plt_egim_slot2_temperature(self):
        """
        It creates a plot with the temperature measured in the slot 2 over time.
        :return: Figure
        """
        self.dialog = False
        fig_tempe, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot2_temperature'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 2: Temperature')
        axes.set_ylabel('Degree Celsius')
        axes.set_xlabel('Time UTC')
        return fig_tempe

    def plt_egim_slot3_temperature(self):
        """
        It creates a plot with the temperature measured in the slot 3 over time.
        :return: Figure
        """
        self.dialog = False
        fig_tempe, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot3_temperature'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 3: Temperature')
        axes.set_ylabel('Degree Celsius')
        axes.set_xlabel('Time UTC')
        return fig_tempe

    def plt_egim_slot4_temperature(self):
        """
        It creates a plot with the temperature measured in the slot 4 over time.
        :return: Figure
        """
        self.dialog = False
        fig_tempe, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot4_temperature'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 4: Temperature')
        axes.set_ylabel('Degree Celsius')
        axes.set_xlabel('Time UTC')
        return fig_tempe

    def plt_egim_slot5_temperature(self):
        """
        It creates a plot with the temperature measured in the slot 5 over time.
        :return: Figure
        """
        self.dialog = False
        fig_tempe, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot5_temperature'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 5: Temperature')
        axes.set_ylabel('Degree Celsius')
        axes.set_xlabel('Time UTC')
        return fig_tempe

    def plt_egim_slot1_pressure(self):
        """
        It creates a plot with the pressure measured in the slot 1 over time.
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot1_pressure'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 1: Pressure')
        axes.set_ylabel('PSI')
        axes.set_xlabel('Time UTC')
        return fig_pres

    def plt_egim_slot2_pressure(self):
        """
        It creates a plot with the pressure measured in the slot 2 over time.
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot2_pressure'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 2: Pressure')
        axes.set_ylabel('PSI')
        axes.set_xlabel('Time UTC')
        return fig_pres

    def plt_egim_slot3_pressure(self):
        """
        It creates a plot with the pressure measured in the slot 3 over time.
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot3_pressure'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 3: Pressure')
        axes.set_ylabel('PSI')
        axes.set_xlabel('Time UTC')
        return fig_pres

    def plt_egim_slot4_pressure(self):
        """
        It creates a plot with the pressure measured in the slot 4 over time.
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot4_pressure'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 4: Pressure')
        axes.set_ylabel('PSI')
        axes.set_xlabel('Time UTC')
        return fig_pres

    def plt_egim_slot5_pressure(self):
        """
        It creates a plot with the pressure measured in the slot 5 over time.
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            self.egim['egim_slot5_pressure'].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No temperature data."
        axes.set_title('Slot 5: Pressure')
        axes.set_ylabel('PSI')
        axes.set_xlabel('Time UTC')
        return fig_pres

    def plt_egim_current(self, average_time='H', accumulated=True):
        """
        Graph of the current consumption since the last reset of the EGIM vs time.
        :param average_time: Average time interval. It can be None. By default is Hourly.
        :param accumulated: True means to plot the current consumption accumulated since the last reset.
            False means to plot the time interval current consumption.
        :return: Figure
        """
        """
        INFO ABOUT HOW OFTEN:
        B       business day frequency
        C       custom business day frequency (experimental)
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency
        BM      business month end frequency
        CBM     custom business month end frequency
        MS      month start frequency
        BMS     business month start frequency
        CBMS    custom business month start frequency
        Q       quarter end frequency
        BQ      business quarter endfrequency
        QS      quarter start frequency
        BQS     business quarter start frequency
        A       year end frequency
        BA      business year end frequency
        AS      year start frequency
        BAS     business year start frequency
        BH      business hour frequency
        H       hourly frequency
        T       minutely frequency
        S       secondly frequency
        L       milliseonds
        U       microseconds
        N       nanoseconds
        """
        self.dialog = False
        # Preparing data
        try:
            egim_data = self.egim['egim_current']
        except KeyError:
            self.dialog = "Error: No energy data."
            return
        if average_time is not None:
            egim_data = egim_data.resample(average_time).mean()
        # Transform from mA to A
        egim_data /= 1000
        title = "Acomulated EGIM current consumption since last Reset"
        if not accumulated:
            title = "EGIM current consumption"
            egim_data_copy = egim_data.copy()
            for i in range(0, len(egim_data)):
                if i == 0:
                    egim_data.iloc[i] = np.nan
                    continue
                if egim_data_copy[i - 1] > 0:
                    dif_current = egim_data_copy[i] - egim_data_copy[i-1]
                    if dif_current > 0:
                        egim_data.iloc[i] = dif_current
                    else:
                        egim_data.iloc[i] = np.nan
                else:
                    egim_data.iloc[i] = np.nan
        # Plot
        fig_current, axes = plt.subplots(nrows=1, ncols=1)
        egim_data.plot(drawstyle="steps", ax=axes)
        axes.set_title(title)
        axes.set_ylabel('A')
        axes.set_xlabel('')
        return fig_current

    def plt_egim_slots_current_consumptions(self, time_interval='W'):
        """
        Creates a plot with the current consumption of all the slots and the input voltage of the egim.
        :param time_interval: Frequency to that we want the data.
        :type time_interval: str
        :return: figure
        """
        """
        INFO ABOUT HOW OFTEN:
        B       business day frequency
        C       custom business day frequency (experimental)
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency
        BM      business month end frequency
        CBM     custom business month end frequency
        MS      month start frequency
        BMS     business month start frequency
        CBMS    custom business month start frequency
        Q       quarter end frequency
        BQ      business quarter endfrequency
        QS      quarter start frequency
        BQS     business quarter start frequency
        A       year end frequency
        BA      business year end frequency
        AS      year start frequency
        BAS     business year start frequency
        BH      business hour frequency
        H       hourly frequency
        T       minutely frequency
        S       secondly frequency
        L       milliseonds
        U       microseconds
        N       nanoseconds
        """
        self.dialog = False

        # Extract data
        try:
            egim_data = self.egim[['egim_slot1_current',
                                   'egim_slot2_current',
                                   'egim_slot3_current',
                                   'egim_slot4_current',
                                   'egim_slot5_current',
                                   'egim_voltage']]
        except AttributeError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5', 'EGIM voltage']
        # print(egim_data.head())
        # Resampling
        try:
            egim_data = egim_data.resample(time_interval).mean()
        except AttributeError:
            self.dialog = "Error: Cannot resample becouse there is no data."
            return
        # Change the voltage prom mV to V
        egim_data['EGIM voltage'] /= 1000
        egim_data['EGIM voltage'] = egim_data['EGIM voltage'].round(3)
        del egim_data.index.name
        # Plot
        fig_slot_current, axes = plt.subplots(nrows=1, ncols=1)
        egim_data.plot(drawstyle="steps", secondary_y=['EGIM voltage'], style=['-', '-', '-', '-', '-', '--'],
                       linewidth=2, ax=axes)

        axes.set_xlabel("")
        axes.set_ylabel("Slot current [mA]")
        axes.right_ax.set_ylabel("Input voltage [V]")
        return fig_slot_current

    def plt_egim_slots_temperature(self, time_interval='W'):
        """
        Creates a plot with the temperature of all the slots of the EGIM.
        :param time_interval: Frequency to that we want the data.
        :type time_interval: str
        :return: figure
        """
        """
        INFO ABOUT HOW OFTEN:
        B       business day frequency
        C       custom business day frequency (experimental)
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency
        BM      business month end frequency
        CBM     custom business month end frequency
        MS      month start frequency
        BMS     business month start frequency
        CBMS    custom business month start frequency
        Q       quarter end frequency
        BQ      business quarter endfrequency
        QS      quarter start frequency
        BQS     business quarter start frequency
        A       year end frequency
        BA      business year end frequency
        AS      year start frequency
        BAS     business year start frequency
        BH      business hour frequency
        H       hourly frequency
        T       minutely frequency
        S       secondly frequency
        L       milliseonds
        U       microseconds
        N       nanoseconds
        """
        self.dialog = False
        # Extract data
        try:
            egim_data = self.egim[['egim_slot1_temperature',
                                   'egim_slot2_temperature',
                                   'egim_slot3_temperature',
                                   'egim_slot4_temperature',
                                   'egim_slot5_temperature']]
        except AttributeError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5']
        # Resampling
        try:
            egim_data = egim_data.resample(time_interval).mean()
        except AttributeError:
            self.dialog = "Error: Cannot resample becouse there is no data."
            return
        del egim_data.index.name
        # Plot
        fig_slot_temp, axes = plt.subplots(nrows=1, ncols=1)
        egim_data.plot(drawstyle="steps", linewidth=2, ax=axes)
        axes.set_xlabel("")
        axes.set_ylabel("$^\circ$C")
        axes.set_title("Temperature of slots")
        return fig_slot_temp

    def plt_egim_slots_pressure(self, time_interval='W'):
        """
        Creates a plot with the pressure of all the slots of the EGIM.
        :param time_interval: Frequency to that we want the data.
        :type time_interval: str
        :return: figure
        """
        """
        INFO ABOUT HOW OFTEN:
        B       business day frequency
        C       custom business day frequency (experimental)
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency
        BM      business month end frequency
        CBM     custom business month end frequency
        MS      month start frequency
        BMS     business month start frequency
        CBMS    custom business month start frequency
        Q       quarter end frequency
        BQ      business quarter endfrequency
        QS      quarter start frequency
        BQS     business quarter start frequency
        A       year end frequency
        BA      business year end frequency
        AS      year start frequency
        BAS     business year start frequency
        BH      business hour frequency
        H       hourly frequency
        T       minutely frequency
        S       secondly frequency
        L       milliseonds
        U       microseconds
        N       nanoseconds
        """
        self.dialog = False
        # Extract data
        try:
            egim_data = self.egim[['egim_slot1_pressure',
                                   'egim_slot2_pressure',
                                   'egim_slot3_pressure',
                                   'egim_slot4_pressure',
                                   'egim_slot5_pressure']]
        except AttributeError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5']
        # Resampling
        try:
            egim_data = egim_data.resample(time_interval).mean()
        except AttributeError:
            self.dialog = "Error: Cannot resample becouse there is no data."
            return
        del egim_data.index.name
        # Plot
        fig_slot_temp, axes = plt.subplots(nrows=1, ncols=1)
        egim_data.plot(drawstyle="steps", linewidth=2, ax=axes)
        axes.set_xlabel("")
        axes.set_ylabel("mBars")
        axes.set_title("Pressure of slots")
        return fig_slot_temp

    def plt_egim_slots_sd_capacity(self, time_interval='W'):
        """
        Creates a plot with the remaining sd capacity of all the slots of the EGIM.
        :param time_interval: Frequency to that we want the data.
        :type time_interval: str
        :return: figure
        """
        """
        INFO ABOUT HOW OFTEN:
        B       business day frequency
        C       custom business day frequency (experimental)
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency
        BM      business month end frequency
        CBM     custom business month end frequency
        MS      month start frequency
        BMS     business month start frequency
        CBMS    custom business month start frequency
        Q       quarter end frequency
        BQ      business quarter endfrequency
        QS      quarter start frequency
        BQS     business quarter start frequency
        A       year end frequency
        BA      business year end frequency
        AS      year start frequency
        BAS     business year start frequency
        BH      business hour frequency
        H       hourly frequency
        T       minutely frequency
        S       secondly frequency
        L       milliseonds
        U       microseconds
        N       nanoseconds
        """
        self.dialog = False
        # Extract data
        try:
            egim_data = self.egim[['egim_slot1_sd_capacity',
                                   'egim_slot2_sd_capacity',
                                   'egim_slot3_sd_capacity',
                                   'egim_slot4_sd_capacity',
                                   'egim_slot5_sd_capacity']]
        except KeyError:
            self.dialog = "Error: No EGIM data."
            return
        egim_data.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5']
        # Resampling
        try:
            egim_data = egim_data.resample(time_interval).mean()
        except AttributeError:
            self.dialog = "Error: Cannot resample becouse there is no data."
            return
        del egim_data.index.name
        # Plot
        fig_slots_sd, axes = plt.subplots(nrows=1, ncols=1)
        egim_data.plot(drawstyle="steps", linewidth=2, ax=axes)
        axes.set_xlabel("")
        axes.set_ylabel("kBytes")
        axes.set_title("Slot SD remaining capacity")
        return fig_slots_sd


def download_metadata_egim(start="24/04/2017", path_egim = r""):

    api = EMSOdevAPI(login='', password='')
    api.observatory_name = "EMSODEV-EGIM-node00001"
    api.instrument_name = "0e5f248e-9e90-465f-91a0-f674b1d4eb3a"
    api.read_parameters()

    for parameter in api.parameters:
        print("Downloading {}...".format(parameter))
        api.parameter_name = parameter
        api.read_data(start_date=start)
    print("Result (5 first values):")
    print(api.egim.head())

    api.save_as_pickle(path_egim)


def download_temp(start="24/04/2017"):

    api = EMSOdevAPI(login='', password='')
    api.observatory_name = "EMSODEV-EGIM-node00001"
    api.parameter_name = "sea_water_temperature"
    instrument_list = ["SBE54-0049", "4381-606", "37-14998", "Workhorse_ADCP_21582"]
    path_list = [r"C:\Users\rbard\Google Drive\Work\Data\EMSO\EGIM1\SBE54-0049",
                 r"C:\Users\rbard\Google Drive\Work\Data\EMSO\EGIM1\4381-606",
                 r"C:\Users\rbard\Google Drive\Work\Data\EMSO\EGIM1\37-14998",
                 r"C:\Users\rbard\Google Drive\Work\Data\EMSO\EGIM1\Workhorse_ADCP_21582"]

    for instrument, path in zip(instrument_list, path_list):
        print("Instrument: {}".format(instrument))
        api.instrument_name = instrument
        api.read_data(start_date=start)
        api.save_as_pickle(path)


if __name__ == '__main__':
    import matplotlib.style as style
    style.use('ggplot')

    ''' DOWNLOAS METADATA OF EGIM'''
    # download_metadata_egim(start="24/04/2017")

    ''' TUI TO DOWNLOAD DATA '''
    tui()

    ''' DOWNLOAD TEMPERATURES '''
    # download_temp(start="01/04/2017")

    ''' EXEMPLE OF CLASS EMSO '''
    ''' LOADING DATA FROM PKL FILE '''
    path_file = r"C:\Users\Raul\Google Drive\Work\Data\EMSO\EGIM1\egim\emsodev_20170426092349.pkl"
    # path_file = r"C:\Users\rbard\Google Drive\Work\Data\EMSO\EGIM1\37-14998\allCTD_20170415\emsodev_20170526140054.pkl"
    ob = EMSO(path_file)

    ''' INFO '''
    # print("METADATA INFORMATION")
    # print(ob.info_metadata())
    # print("DATA INFORMATION")
    # print(ob.info_data())
    # print("DATA MEANING")
    # print(ob.info_parameters())
    # print("EGIM INFORMATION")
    print(ob.info_egim())
    # print(ob.stadistics_slots_current_consumptions())
    # print(ob.stadistics_slots_temperature())
    # print("GAPS")
    # print(ob.find_gaps())

    ''' BUTTERWORTH FILTER'''
    # ob.butterworth_filter('pres')
    # if ob.dialog:
    #     print(ob.dialog)
    #     sys.exit()

    ''' PLOTS '''
    # ob.plt_all()
    # ob.plt_egim_all()
    # ob.plt_egim_slots_current_consumptions('H')
    # ob.plt_egim_slots_temperature('H')
    # ob.plt_egim_slots_pressure('W')
    ob.plt_egim_slots_sd_capacity('W')
    ob.plt_egim_current(average_time='D', accumulated=False)
    plt.show()

    print("END")
