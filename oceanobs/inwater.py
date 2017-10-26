import gsw
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4 as Nc
import numpy as np
import pandas as pd
import pickle
import requests
from scipy import stats


class EGIM:
    """
    Class to download EGIM data from the EMSODEV DMP
    """

    def __init__(self, login=None, password=None, observatory=None, instrument=None, parameter=None, path=None,
                 start=None, end=""):

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

        self.wf = WaterFrame()

        if login is not None and password is not None:
            self.login = login
            self.password = password
            if observatory is not None and instrument is not None and parameter is not None and path is not None \
                    and start is not None:
                if isinstance(observatory, str):
                    if observatory == 'all':
                        self.load_observatories()
                    else:
                        self.observatories.append(observatory)
                else:
                    # It is a list
                    self.observatories += observatory
                if isinstance(instrument, str):
                    if instrument == 'all':
                        instruments = []
                        for observatory_ in self.observatories:
                            self.observatory_name = observatory_
                            self.load_instruments()
                            instruments += self.instruments
                        self.instruments = instruments
                    else:
                        self.instruments.append(instrument)
                else:
                    # It is a list
                    self.instruments += instrument
                if isinstance(parameter, str):
                    if parameter == "all":
                        parameters = []
                        for observatory_ in self.observatories:
                            self.observatory_name = observatory_
                            for instrument_ in self.instruments:
                                self.instrument_name = instrument_
                                self.load_parameters()
                                parameters += self.parameters
                        # It saves all the parameters in self.parameters, but remove duplicate strigs
                        self.parameters = list(set(parameters))
                    else:
                        self.parameters.append(parameter)
                else:
                    self.parameters += parameter
                self.auto_download(path, start, end)

    def load_observatories(self):
        """
        Look for observatories and save them into a list in self.observatories
        :return: int with the status code of the answer (200 means that everything is ok).
        """
        # Cleaning the list of instruments and parameters to select. If you are here, the instruments and the parameters
        # should be re-searched.
        self.instruments = []
        self.parameters = []
        try:
            r = requests.get('http://api.emsodev.eu/observatories', auth=(self.login, self.password))
        except requests.exceptions.ConnectionError:
            # print("Error: No internet connexion.")
            return 0
        if r.status_code != 200:
            return r.status_code
        answer = r.json()
        self.observatories = []
        for station in answer:
            self.observatories.append(station['name'])
        return r.status_code

    def load_instruments(self):
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
        # Add the intrument names to the list of instruments
        self.instruments = []
        for instrument in answer['instruments']:
            self.instruments.append(instrument['name'])
        return r.status_code

    def load_parameters(self):
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

    def load_data(self, start_date='01/04/2017', end_date=""):
        """
        Download data from the parameter/instrument/observatory.
        :param start_date: Time that you want to start to have data.
        :param end_date: Time that you want to end to have data.
        :return: int with the status code of the answer (200 means that everything is ok).
        """

        def metadata_creation():
            """
            It creates the wf.metadata dict.
            """
            self.wf.metadata['qc_manual'] = "OceanSITES User's Manual v1.2"
            self.wf.metadata['distribution_statement'] = "These data follow Copernicus standards; they are public " \
                                                         "and free of charge. User assumes all risk for use of data. " \
                                                         "User must display citation in any publication or product " \
                                                         "using data. User must contact PI prior to any commercial " \
                                                         "use of data."
            self.wf.metadata['references'] = "http://www.emsodev.eu/, http://www.emso-eu.org/"
            self.wf.metadata['cdm_data_type'] = "Time-series"
            self.wf.metadata['citation'] = "These data were collected and made freely available by the EMSODEV" \
                                           " project and the programs that contribute to it."
            self.wf.metadata['source'] = "Underwater observatory"
            self.wf.metadata['summary'] = self.wf.acronym
            self.wf.metadata['data_type'] = "OceanSITES time-series data"

        def format_data():
            """
            Creation of the data dataframe with the oceanobs standard.
            """

            def data_frame_creation(param_name, technical=False):
                """
                Creation of a pandas DataFrame with the input parameter
                :param param_name: Name of the parameter
                :param technical: Technical parameters does not need qc flags.
                """
                df = pd.DataFrame({param_name: [x[1] for x in self.observations], 'time': [x[0] for x in
                                                                                           self.observations]})
                # Changing the time values to a datatime
                df['time'] = pd.to_datetime(df['time'], unit='s')

                if not technical:
                    # Adding QC flag
                    df['time_qc'] = 0
                    # Adding latitude and longitude
                    if self.observatory_name == "EMSODEV-EGIM-node00001":
                        df['latitude'] = 41.185
                        df['longitude'] = 1.745
                    if "_" in param_name:
                        parts_in = param_name.split("_")
                        df["{}_qc_{}".format(parts_in[0], parts_in[1])] = 0
                    else:
                        df["{}_qc".format(param_name)] = 0
                    try:
                        self.wf.data = pd.merge(self.wf.data, df, how='outer', on=['time', 'time_qc', 'latitude',
                                                                                   'longitude'])
                    except KeyError:
                        self.wf.data = df
                else:
                    try:
                        self.wf.technical = pd.merge(self.wf.technical, df, how='outer', on="time")
                    except KeyError:
                        self.wf.technical = df

            def acronym_creation(key, long_name, standard_name, units):
                info = dict()
                info['long_name'] = long_name
                info['standard_name'] = standard_name
                info['units'] = units
                info['observatory'] = self.observatory_name
                info['instrument'] = self.instrument_name
                self.wf.acronym[key] = info

            # Data parameters
            if self.parameter_name == "sea_water_temperature":
                data_frame_creation("temp_{}".format(self.instrument_name.replace("_", "-")))
                acronym_creation(key="temp_{}".format(self.instrument_name.replace("_", "-")),
                                 long_name="Sea water temperature", standard_name="sea_water_temperature",
                                 units="degree Celsius")
            elif self.parameter_name == "sea_water_pressure":
                data_frame_creation("pres")
                acronym_creation(key="pres", long_name="Sea water pressure",
                                 standard_name="sea_water_pressure", units="dBar")
                # Change from PSI to dBar
                self.wf.data['pres'] *= 0.6804595706270282
            elif self.parameter_name == "turbidity":
                data_frame_creation('tur4')
                acronym_creation(key="tur4", long_name="Turbidity",
                                 standard_name="turbidity", units="NTU")
                # Change from mNTU to NTUs
                self.wf.data['tur4'] /= 100
            elif self.parameter_name == "oxygen_saturation":
                data_frame_creation('osat')
                acronym_creation(key="osat", long_name="Oxygen saturation", standard_name="oxygen_saturation",
                                 units="%")
            elif self.parameter_name == "dissolved_oxygen":
                data_frame_creation('dox1')
                acronym_creation(key="dox1", long_name="Dissolved oxygen", standard_name="dissolved_oxygen",
                                 units="mg/L")
            elif self.parameter_name == "salinity":
                data_frame_creation('psal')
                acronym_creation(key="psal", long_name="Sea water salinity", standard_name="salinity", units="PSU")
            elif self.parameter_name == "depth":
                data_frame_creation('depth')
                acronym_creation(key="depth", long_name="Depth", standard_name="depth", units="meters")
            elif self.parameter_name == "conductivity":
                data_frame_creation('cndc')
                acronym_creation(key="cndc", long_name="Sea water conductivity", standard_name="conductivity",
                                 units="Siemens/meter")
            elif self.parameter_name == "sound_velocity":
                data_frame_creation('svel')
                acronym_creation(key="svel", long_name="Sea water sound velocity", standard_name="sound_velocity",
                                 units="meters/seconds")
            elif "N_S_sea_water_speed" in self.parameter_name:
                # Extract the number of the Bin
                parts = self.parameter_name.split("_")  # parts[0] = BinXX
                important_parts = parts[0].split("n")  # important_parts[1] is the number
                data_frame_creation("nsct_bin{}".format(important_parts[1]))
                self.wf.data["nsct_bin{}".format(important_parts[1])] /= 1000
                acronym_creation(key="nsct_bin{}".format(important_parts[1]), long_name="South-north current component",
                                 standard_name="N_S_sea_water_speed", units="m/s")
            elif "E_W_sea_water_speed" in self.parameter_name:
                # Extract the number of the Bin
                parts = self.parameter_name.split("_")  # parts[0] = BinXX
                important_parts = parts[0].split("n")  # important_parts[1] is the number
                data_frame_creation("ewct_bin{}".format(important_parts[1]))
                self.wf.data["ewct_bin{}".format(important_parts[1])] /= 1000
                acronym_creation(key="ewct_bin{}".format(important_parts[1]), long_name="West-east current component",
                                 standard_name="E_W_sea_water_speed", units="m/s")
            elif "vert_sea_water_speed" in self.parameter_name:
                # Extract the number of the Bin
                parts = self.parameter_name.split("_")  # parts[0] = BinXX
                important_parts = parts[0].split("n")  # important_parts[1] is the number
                data_frame_creation("vcsp_bin{}".format(important_parts[1]))
                self.wf.data["vcsp_bin{}".format(important_parts[1])] /= 1000
                acronym_creation(key="vcsp_bin{}".format(important_parts[1]), long_name="Bottom-top current component",
                                 standard_name="vert_sea_water_speed", units="m/s")
            elif self.parameter_name == "heading_of_device":
                data_frame_creation("heading_adcp", technical=True)
                acronym_creation(key="heading_adcp", long_name="Heading of the ADCP", standard_name="heading",
                                 units="degrees")
            elif self.parameter_name == "pitch":
                data_frame_creation("pitch_adcp", technical=True)
                acronym_creation(key="pitch_adcp", long_name="Pitch of the ADCP", standard_name="pitch",
                                 units="degrees")
            elif self.parameter_name == "roll":
                data_frame_creation("roll_adcp", technical=True)
                acronym_creation(key="roll_adcp", long_name="Roll of the ADCP", standard_name="roll", units="degrees")
            # TODO: Program the same things with parameters such as "Bin1_error_sea_water_speed".

            # Egim parameters
            if self.parameter_name == "voltage":
                data_frame_creation("voltage", technical=True)
                # We transform from mV to V
                self.wf.technical['voltage'] /= 1000
                acronym_creation(key="voltage", long_name="Input voltage", standard_name="voltage", units="volts")
            elif self.parameter_name == "waterInstrusion":
                data_frame_creation("leak", technical=True)
                acronym_creation(key="leak", long_name="Water intrusion", standard_name="water_intrusion",
                                 units="0=No, 1=Yes")
            elif self.parameter_name == "energy":
                data_frame_creation("energy", technical=True)
                # We transform the current from mA to A
                self.wf.technical['energy'] /= 1000
                acronym_creation(key="energy", long_name="Accumulated current consumption",
                                 standard_name="current_consumption", units="A")
            elif "_current" in self.parameter_name:
                parts = self.parameter_name.split("_")  # EGIM_slotx_current, we want slotx
                data_frame_creation("current_{}".format(parts[1]), technical=True)
                acronym_creation(key="current_{}".format(parts[1]), long_name="Current Consumption of {}".
                                 format(parts[1]), standard_name="current_consumption", units="mA")
            elif "_SD_capacity" in self.parameter_name:
                parts = self.parameter_name.split("_")  # EGIM_slotx__SD_capacity, we want slotx
                data_frame_creation("sd_{}".format(parts[1]), technical=True)
                # Translate from Bytes to MBytes
                self.wf.technical["sd_{}".format(parts[1])] /= 1000000
                acronym_creation(key="sd_{}".format(parts[1]), long_name="SD remaining capacity of {}".
                                 format(parts[1]), standard_name="sd", units="MBytes")
            elif "_temperature" in self.parameter_name and "sea" not in self.parameter_name:
                # The not "sea" is to avoid sea_temperature_water
                parts = self.parameter_name.split("_")  # EGIM_slotx__temperature, we want slotx
                data_frame_creation("temperature_{}".format(parts[1]), technical=True)
                acronym_creation(key="temperature_{}".format(parts[1]), long_name="Temperature of {}".
                                 format(parts[1]), standard_name="temperature", units="degree_celsius")
            elif "_pressure" in self.parameter_name and "sea" not in self.parameter_name:
                # The not "sea" is to avoid sea_pressure_water
                parts = self.parameter_name.split("_")  # EGIM_slotx__pressure, we want slotx
                data_frame_creation("pressure_{}".format(parts[1]), technical=True)
                acronym_creation(key="pressure_{}".format(parts[1]), long_name="Pressure of {}".format(parts[1]),
                                 standard_name="pressure", units="dBar")

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

        if len(self.observations) > 0:
            format_data()
            metadata_creation()

        return r.status_code

    def auto_download(self, path_in, start_in, end_in=""):
        """
        Download all the data and save it into a pickle file.
        :param path_in: Path of the pickle file.
        :param start_in: Start time to download data.
        :param end_in: End time to download data.
        :return: true if ok, false if ko
        """
        for self.observatory_name in self.observatories:
            for self.instrument_name in self.instruments:
                for self.parameter_name in self.parameters:
                    print(self.observatory_name, self.instrument_name, self.parameter_name)
                    print(self.load_data(start_in, end_in))
        answer = self.wf.to_pickle(path_in)
        return answer

    def clean(self):
        """
        Clear data and technical variables.
        """
        self.wf.data = pd.DataFrame()
        self.wf.technical = pd.DataFrame()


class WaterFrame:
    """
    To complete...
    """

    def __init__(self, path=None):
        """
        Constructor
        """
        # Instance variables
        self.data = pd.DataFrame()  # pandas DataFrame with scientific measurements
        self.metadata = dict()  # dictionary with the metadata
        self.technical = pd.DataFrame()  # pandas DataFrame with instrument technical data
        self.acronym = dict()  # dictionary with the acronyms

        if path:
            if path[-1] == "c":
                self.from_netcdf(path)
            elif path[-1] == "l":
                self.from_pickle(path)
            elif path[-1] == "t":
                self.from_csv(path)

    def from_netcdf(self, path, parameter=None):
        """
        Load data from a NetCDF file. It extracts the data and the metadata of the file and saves them into a pandas
        DataFrame in self.data and self.metadata.
        :param path: Path where the NetCDF file is.
        :return: If there is any problem, it returns an str with the problem.
        """

        def read_metadata():
            """
            Save the NetCDF attributes into self.metadata
            """

            self.metadata = dict()

            # Read and save all the attributes
            for name in df.ncattrs():
                self.metadata[name] = getattr(df, name)
            self.metadata['summary'] = self.acronym

        def read_data(parameter):
            """
            Save the variables of the NetCDF file into self.data
            """

            # NetCDF variables without columns
            variables_without_columns = ["TIME", "TIME_QC", "LATITUDE", "LONGITUDE", "POSITION_QC", "GPS_LATITUDE",
                                         "GPS_LONGITUDE"]
            variables_not_saved = ["DC_REFERENCE", "DEPH", "DEPH_QC", "GPS_POSITION_QC", "POSITIONING_SYSTEM"]
            variables_no_depth = ["PRRT", "PRRT_QC", "WSPD", "WSPD_QC", "WSPE", "WSPE_QC", "WSPD", "WSPD_QC",
                                  "WSPE", "WSPE_QC", "WSPN", "WSPN_QC", "WTODIR", "WTODIR_QC", "RELH", "RELH_QC",
                                  "DRYT", "DRYT_QC", "SINC", "SINC_QC", "HOURLY_RAIN", "HOURLY_RAIN_QC", "ATMS",
                                  "ATMS_QC", "ATMP", "ATMP_QC", "DEWT", "DEWT_QC", "DRYT", "DRYT_QC", "GSPD", "GSPD_QC",
                                  "NRAD", "NRAD_QC", "VAVH", "VAVH_QC", "VDIR", "VDIR_QC", "VEMH", "VEMH_QC", "VGHS",
                                  "VGHS_QC", "VGTA", "VGTA_QC", "VHZA", "VHZA_QC", "VMDR", "VMDR_QC", "VTZM", "VTZM_QC",
                                  "WDIR", "WDIR_QC", "SWHT", "SWHT_QC"]

            # Reading the deph parameter
            try:
                depth = df.variables['DEPH'][:][0, :]
            except KeyError:
                return

            # Save the variables into the dictionary data
            data = dict()
            # Clean the dictionary of the acronyms
            self.acronym = dict()
            # print(df.variables)
            # print(df.variables['TEMP'])
            time = None
            for key in df.variables.keys():
                # print(key)
                if "_DM" in key:
                    continue
                if parameter is not None:
                    if key == "TIME":
                        pass
                    elif parameter not in key:
                        continue
                if key in variables_not_saved:
                    continue
                elif key in variables_without_columns:
                    # The time needs a conversion to be understood
                    if key == "TIME":
                        time = df.variables['TIME']
                        time = Nc.num2date(time[:], time.units)
                    else:
                        data[key.lower()] = df[key][:]
                else:
                    # Search the column number (i)
                    #print(key)
                    n_sensors = len(df[key][:][:][0])
                    for i in range(n_sensors):
                        #print(i, n_sensors)
                        for j in range(len(df[key][:][:, i])):
                            # This is to run the code faster. We try to find a value just 1000 times. If we do not
                            # find it, we break
                            if j == 50:
                                break
                            if df[key][:][:, i][j] != '--':
                                # Save the values
                                if (key in variables_no_depth) or ('--' in str(depth[i])):
                                    data[key.lower().replace("_t", "-t").replace("_r", "-r")] = df[key][:][:, i]
                                else:
                                    data["{}_{}".format(key.lower().replace("_t", "-t").replace("_r", "-r"),
                                                        depth[i])] = df[key][:][:, i]
                                # Save the acronym information
                                try:
                                    info = dict()
                                    # print(key)
                                    try:
                                        info['long_name'] = df.variables[key].long_name
                                    except AttributeError:
                                        try:
                                            info['long_name'] = df.variables[key].standard_name
                                        except AttributeError:
                                            pass
                                    # print(df.variables[key].long_name)
                                    try:
                                        info['standard_name'] = df.variables[key].standard_name
                                        # print(df.variables[key].standard_name)
                                        info['units'] = df.variables[key].units
                                        # print(df.variables[key].units)
                                        info['depth'] = "{} m".format(depth[i])
                                    except AttributeError:
                                        pass
                                    if key in variables_no_depth:
                                        self.acronym[key.lower().replace("_t", "-t").replace("_r", "-r")] = info
                                    else:
                                        self.acronym["{}_{}".format(key.lower().replace("_t", "-t").replace("_r", "-r"),
                                                                    depth[i])] = info
                                except AttributeError:
                                    pass
                                break

            # Sort the new names
            data_keys_sorted = sorted(data.keys(), key=lambda item: (
                float(item.split("_")[-1]) if item[-1].isdigit() else float('inf'), item))
            self.data = pd.DataFrame(data, index=time, columns=data_keys_sorted)

        try:
            # Open nc file
            df = Nc.Dataset(path)
        except OSError as error:
            return "Error loading NetCDF file ({}): {}".format(path, error)
        read_data(parameter)
        read_metadata()

    def from_csv(self, path):
        """
        It opens a CSV file and creates the save the values into the WaterFrame object.
        It just works with the CSV from OBSEA.
        :param path:  Path of the CDV file.
        :return: If there is any problem, it returns an str with the problem.
        """

        def data_format():
            """
            Write the correct name of index and keys of self.data
            """

            def acronym_creation(key, long_name, standard_name, units):
                info = dict()
                info['long_name'] = long_name
                info['standard_name'] = standard_name
                info['units'] = units
                self.acronym[key] = info

            # Changing the index name
            self.data.index.rename(name='time', inplace=True)
            data_keys = self.data.keys()
            if 'temperatura' in data_keys:
                self.data.rename(columns={'temperatura': 'temp_ctd'}, inplace=True)
                self.data['temp_qc_ctd'] = 0
                acronym_creation(key="temp_ctd", long_name="Sea water temperature",
                                 standard_name="sea_water_temperature", units="degree_celsius")
            if 'pressio' in data_keys:
                self.data.rename(columns={'pressio': 'pres_ctd'}, inplace=True)
                self.data['pres_qc_ctd'] = 0
                acronym_creation(key="pres_ctd", long_name="Sea water pressure", standard_name="sea_water_pressure",
                                 units="dBar")
            if 'salinitat' in data_keys:
                self.data.rename(columns={'salinitat': 'psal'}, inplace=True)
                self.data['psal_qc'] = 0
                acronym_creation(key="pres_ctd", long_name="Sea water practical salinity",
                                 standard_name="sea_water_practical_salinity", units="PSU")
                # TODO: We have to complete the rest of parameters The source names can change.

        try:
            self.data = pd.read_csv(path, sep='\t', parse_dates=['date_sistema'], index_col=0)
        except ValueError:
            try:
                self.data = pd.read_csv(path, sep='\t', parse_dates=['date_time'], index_col=0)
            except ValueError:
                return "Error: There are no data in {}.".format(path)
        except OSError as error:
            return "Error loading CSV file ({}): {}".format(path, error)
        # Transform all the values to numbers
        self.data = self.data.apply(pd.to_numeric, args=('coerce',))
        data_format()

    def from_pickle(self, path):
        """
        Upload the actual WaterFrame object to the object that is in the pickle file of the path
        :param path: Path of the pickle file.
        :return:
        """
        try:
            with open(path, "rb") as handle:
                pickle_temp = pickle.load(handle)
            self.data = pickle_temp.data
            try:
                self.data.set_index('time', inplace=True)
            except KeyError:
                # It means that self.data is empty
                pass
            self.metadata = pickle_temp.metadata
            self.technical = pickle_temp.technical
            try:
                self.technical.set_index('time', inplace=True)
            except KeyError:
                # It means that self.technical is empty
                pass
            self.acronym = pickle_temp.acronym
        except EOFError:
            return "Error loading pickle file {}. This is not a pickle file.".format(path)
        except FileNotFoundError:
            return "Error loading pickle file {}. File not found.".format(path)

    def add_netcdf(self, path):
        """
        Add data from a new NetCDF file.
        :param path: Path of the new NetCDF file.
        :return:
        """
        big_data = self.data.copy()
        self.from_netcdf(path)
        big_data = pd.concat([big_data, self.data])
        self.data = big_data.copy()

    def to_pickle(self, path):
        """
        Save a WaterFrame object to a pickle (serialize) object in the input path
        :param path: File path
        :return:
        """
        try:
            with open(path, 'wb') as handle:
                pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return "WaterFrame object saved in {}".format(path)
        except PermissionError:
            return "Error saving WaterFrame object in {}. Permission denied.".format(path)

    def plot(self, param, join=False, qc_flag=None):
        """
        It creates a figure.
        :param param: Acronym of the parameter to plot.
        :param join: Returns a figure with with the parameter at different depths
        :param qc_flag: Number of QC flag to plot.
        :return:
        """

        fig, axes = plt.subplots(nrows=1, ncols=1)

        # Init, just for warnings
        ax_in = None
        if not join:
            technical = False
            # Make of a pandas DataFrame only with the necessary information
            data = pd.DataFrame()
            # Init, just for warnings
            parameter_qc = ""
            parts = None
            #  Look for the parts of the parameter, split with a _
            try:
                parts = param.split("_")
                if len(parts) == 1:
                    parameter_qc = "{}_qc".format(param)
                else:
                    parameter_qc = "{}_qc_{}".format(parts[0], parts[1])
                data[param] = self.data[param].dropna()
                data[parameter_qc] = self.data[parameter_qc]
                if qc_flag is not None:
                    data = data[data[parameter_qc] == qc_flag]
            except KeyError:
                try:
                    data[param] = self.technical[param].dropna()
                    technical = True
                except KeyError:
                    return "Error plotting {}: Parameter does not exist.".format(param)
            if technical:
                # This is a technical plot
                ax_in = data.plot(linestyle='-', ax=axes)
                ax_in.set_ylabel(self.acronym[param]['units'])
                ax_in.set_title(self.acronym[param]['long_name'])
            else:
                # Split the DataFrame with the qc flags and append to a list
                first_time = True
                for qc_number in range(0, 10):
                    df = data[param][data[parameter_qc] == qc_number].dropna()
                    if len(df) > 0:
                        if first_time is False:
                            if qc_number == 1 or qc_number == 8:
                                ax_in = df.plot(ax=axes, label="QC Flag:{}".format(qc_number), linestyle='--',
                                                marker='o')
                            else:
                                ax_in = df.plot(ax=axes, label="QC Flag:{}".format(qc_number), linestyle='',
                                                marker='o')
                        else:
                            if qc_number == 1 or qc_number == 8:
                                ax_in = df.plot(ax=axes, label="QC Flag:{}".format(qc_number), linestyle='--',
                                                marker='o')
                            else:
                                ax_in = df.plot(ax=axes, label="QC Flag:{}".format(qc_number), linestyle='', marker='o')
                            first_time = False
                if first_time is False:
                    ax_in.set_ylabel(self.acronym[param]['units'])
                    ax_in.legend()
                    try:
                        if "bin" in parts[1]:
                            ax_in.set_title("{} in {}".format(self.acronym[param]['long_name'], parts[1]))
                        elif "-" in parts[1]:
                            ax_in.set_title("{} from sensor {}".format(self.acronym[param]['long_name'], parts[1]))
                        else:
                            ax_in.set_title("{} at {} meters".format(self.acronym[param]['long_name'], parts[1]))
                    except IndexError:
                        ax_in.set_title(self.acronym[param]['long_name'])
        else:
            # Make of a pandas DataFrame only with the necessary information
            first_time = True
            param_name = ""
            for key in self.data.keys():
                if "_qc" in key:
                    continue
                elif "_dm" in key:
                    continue
                elif param in key:
                    param_name = key
                    # Look for the parts of the parameter, separed with a _
                    parts = key.split("_")
                    if first_time:
                        try:
                            ax_in = self.data[key].dropna().plot(label=parts[1], marker='')
                        except IndexError:
                            ax_in = self.data[key].dropna().plot(label=key, marker='')
                        first_time = False
                    else:
                        ax_in = self.data[key].dropna().plot(ax=axes, label=parts[1], marker='')
            if not first_time:
                ax_in.set_title(self.acronym[param_name]['long_name'])
                ax_in.set_ylabel(self.acronym[param_name]['units'])
                if "bin" in param_name:
                    ax_in.legend(title="Bin")
                elif "-" in param_name:
                    ax_in.legend(title="Sensors")
                elif "Work" in param_name:
                    ax_in.legend(title="Sensors")
                elif "_" not in param_name:
                    ax_in.legend(title="Sensors")
                else:
                    ax_in.legend(title="Depth (m)")
        return fig

    def plot_ts(self, name_temp):
        """
        Graph of T-S.
        :param name_temp: Key of the *data* variable that contains the temperature values.
        :return: figure
        """
        try:
            temp = self.data[name_temp]
            salt = self.data['psal']
        except KeyError:
            return "Error: Not enough data."

        # Figure out boundaries (mins and maxs)
        smin = salt.min() - (0.01 * salt.min())
        smax = salt.max() + (0.01 * salt.max())
        tmin = temp.min() - (0.1 * temp.max())
        tmax = temp.max() + (0.1 * temp.max())

        # Calculate how many grid cells we need in the x and y dimensions
        xdim = round((smax - smin) / 0.1 + 1, 0)
        ydim = round((tmax - tmin) + 1, 0)

        # Create empty grid of zeros
        dens = np.zeros((np.int(ydim), np.int(xdim)))

        # Create temp and salt vectors of appropriate dimensions
        ti = np.linspace(1, ydim - 1, ydim) + tmin
        si = np.linspace(1, xdim - 1, xdim) * 0.1 + smin

        # Loop to fill in grid with densities
        for j in range(0, int(ydim)):
            for i in range(0, int(xdim)):
                dens[j, i] = gsw.rho(si[i], ti[j], 0)

        # Subtracts 1000 to convert to sigma-t
        dens -= 1000

        # Plot data ***********************************************
        fig_ts = plt.figure()
        ax1 = fig_ts.add_subplot(111)
        cs = plt.contour(si, ti, dens, linestyles='dashed', colors='k')
        plt.clabel(cs, fontsize=12, inline=1, fmt='%1.1f')  # Label every second level

        ax1.plot(salt, temp, 'or', markersize=9)

        ax1.set_xlabel('PSU')
        ax1.set_ylabel('ºC')
        ax1.set_title("T-S diagram")
        return fig_ts

    def predefined_plot(self, name, average_time='W'):
        """
        It creates a set of typical functions to make fixed plots.
        :param name:
        :param average_time:
        :return:
        """

        fig, axes = plt.subplots(nrows=1, ncols=1)

        if name == "current_slots":
            # obtain data
            try:
                df = self.technical[['current_slot1', 'current_slot2', 'current_slot3', 'current_slot4',
                                     'current_slot5', 'voltage']]
            except AttributeError:
                return "Error: No data to create the {} graph.".format(name)
            df.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5', 'Input voltage']
            # print(egim_data.head())
            # Resampling
            df = df.resample(average_time).mean()
            df['Input voltage'] = df['Input voltage'].round(3)
            del df.index.name
            # Plot
            ax = df.plot(ax=axes, drawstyle="steps", secondary_y=['Input voltage'],
                         style=['-', '-', '-', '-', '-', '--'], linewidth=2)

            ax.set_xlabel("")
            ax.set_ylabel("Slot current [mA]")
            ax.right_ax.set_ylabel("Input voltage [V]")
            return fig
        elif name == 'temperature':
            # Obtain data
            try:
                df = self.technical[['temperature_slot1', 'temperature_slot2', 'temperature_slot3', 'temperature_slot4',
                                     'temperature_slot5']]
            except AttributeError:
                return "Error: There are no data of temperature of slots."
            df.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5']
            # Resampling
            df = df.resample(average_time).mean()
            del df.index.name
            # Plot
            ax = df.plot(ax=axes, drawstyle="steps", linewidth=2)
            ax.set_xlabel("")
            ax.set_ylabel("$^\circ$C")
            ax.set_title("Temperature of slots")
            return fig
        elif name == 'sd':
            # obtain data
            try:
                df = self.technical[['sd_slot1', 'sd_slot2', 'sd_slot3', 'sd_slot4', 'sd_slot5']]
            except KeyError:
                return "Error: No SD data."
            df.columns = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5']
            # Resampling
            egim_data = df.resample(average_time).mean()
            del egim_data.index.name
            # Plot
            ax = df.plot(ax=axes, drawstyle="steps", linewidth=2)
            ax.set_xlabel("")
            ax.set_ylabel("MBytes")
            ax.set_title("Slot SD remaining capacity")
            return fig
        else:
            return "Error: No predefined plot with name: {}".format(name)

    def qc(self, param=None, influencer=0.7, threshold=6, multiplier=3):
        """
        It analyzes self.data and change the QC flags from 0 to the corresponding number.
        :param param: Name of the parameter to create the QC.
        :param threshold: A threshold of X will signal if a datapoint is X standard deviations away from the moving
        mean. It is used for the spike procedure.
        :param influencer: The influence (between 0 and 1) of new not good values on the mean and standard deviation,
        for the spike procedure.
        :param multiplier: The multiplier value to calculate the maximum value of the slope procedure.
        """

        def gap_test(parameter, qc_number = 4):
            """
            It detects missing values.
            :param parameter: Name of the parameter.
            :param qc_number: Number to write if the value it is flagged.
            :return:
            """
            parameter_qc = self.name_qc(parameter)

            self.data.ix[self.data[parameter].isnull(), parameter_qc] = qc_number

        def location_test(parameter, qc_number = 4):
            """
            All the values should have the location of the measures.
            :param qc_number: Number to write if the value it is flagged.
            """
            parameter_qc = self.name_qc(parameter)

            try:
                self.data.ix[self.data['latitude'].isnull(), parameter_qc] = qc_number
                self.data.ix[self.data['longitude'].isnull(), parameter_qc] = qc_number
            except KeyError:
                # There is no latitude or longitude values
                self.data[parameter_qc] = qc_number

        def range_test(parameter, qc_number = 4):
            """
            Check impossible values of a paramerer.
            :param parameter: Name of the parameter.
            :param qc_number: Number to write if the value it is flagged.
            """

            mediterranean_values = {
                'longitude':{'min': -5.625709, 'max': 35.560366},
                'latitude':{'min': 30.235617, 'max': 45.866313},
                'wdir':{'min': 0, 'max': 360}, # Wind from direction relative true north
                'swdr':{'min': 0, 'max': 360}, # SWELL DIRECTION REL TRUE N.
                'vpsp':{'min': 0, 'max': 360}, # dir. spreading at wave peak
                'vdir':{'min': 0, 'max': 360}, # wave direction rel. true north
                'vmdr':{'min': 0, 'max': 360}, # Mean wave direction from (Mdir)
                'head':{'min': 0, 'max': 360}, # PLAT. HEADING REL. TRUE NORTH
                'relh':{'min': 0, 'max': 360}, # relative humidity
                'hcdt':{'min': 0, 'max': 360}, # current to direction relative true north
                'temp':{'min': 4, 'max': 34}, # Sea temperature
                'atms':{'min': 8, 'max': 1225}, # Atmospheric pressure at sea level
                'dryt':{'min': -2, 'max': 43}, # Air temperature in dry bulb
                'swht':{'min': 0, 'max': 8}, # SWELL HEIGHT
                'wspd':{'min': 0, 'max': 30}, # Horizontal wind speed
                'swpr':{'min': 0, 'max': 12}, # SWELL PERIOD
                'vavt':{'min': 0, 'max': 16}, # AVER. PERIOD HIGHEST 1/3 WAVE
                'vcmx':{'min': 0, 'max': 11}, # MAX CREST TROUGH WAVE HEIGHT
                'vepk':{'min': 0, 'max': 78}, # WAVE SPECTRUM PEAK ENERGY
                'vhm0':{'min': 0, 'max': 7}, # SPECTRAL SIGNIF. WAVE HEIGHT
                'vsmc':{'min': 0, 'max': 10}, # SPECT. MOMENT(0, 2) WAVE PERIOD
                'vtpk':{'min': 0, 'max': 32}, # WAVE SPECTRUM PEAK PERIOD
                'vavh':{'min': 0, 'max': 7}, # AVER. HEIGHT HIGHEST 1/3 WAVE
                'vped':{'min': 0, 'max': 82}, # dir. spreading at wave peak
                'vtdh':{'min': 0, 'max': 16}, # significant wave height
                'vtzm':{'min': 0, 'max': 27}, # period of the highest wave
                'chlt': {'min': 0, 'max': 8},  # total chlorophyll
                'cndc': {'min': 1, 'max': 7},  # electrical conductivity
                'osat': {'min': 83, 'max': 120},  # oxygen saturation
                'phph': {'min': 6, 'max': 9},  # ph
                'psal': {'min': 24, 'max': 40},  # practical salinity
                'ewct': {'min': -7, 'max': 6},  # west-east current component
                'nsct': {'min': -3, 'max': 4},  # south-north current component
                'atmp': {'min': 846, 'max': 1080},  # atmospheric pressure at altitude
                'dewt': {'min': -8, 'max': 28},  # dew point temperature
                'gspd': {'min': 0, 'max': 40},  # gust wind speed
                'vtza': {'min': 0, 'max': 20},  # AVER ZERO CROSSING WAVE PERIOD
                'svel': {'min': 1300, 'max': 165000},  # sound velocity
                'airt': {'min': -2, 'max': 32},  # Temperature of the atmosphere
                'lw': {'min': 4, 'max': 40},  # Downwelling vector irradiance as energy (longwave) in the atmosphere
                'pres': {'min': 0, 'max': 41},  # sea pressure
                'vtm02': {'min': 0, 'max': 13},  # Spectral moments (0, 2) wave period (Tm02)
                'vzmx': {'min': 0, 'max': 16},  # Maximum zero crossing wave height (Hmax)
                'prrt': {'min': 0, 'max': 122},  # hourly precipitation rate
                'slev': {'min': -4, 'max': 27},  # Observed sea level
                'slvr': {'min': -2, 'max': 2},  # Residual (Observed-Predicted sea level)
                'linc': {'min': 10, 'max': 2300},  # long-wave incoming radiation
                'rdin': {'min': 0, 'max': 1100},  # incident radiation
            }

            obsea_values = {
                'longitude':{'min': 1.74, 'max': 1.76},
                'latitude':{'min': 41.18, 'max': 41.19},
                'wdir':{'min': 0, 'max': 360}, # Wind from direction relative true north
                'temp':{'min': 11, 'max': 27}, # Sea temperature
                'atms':{'min': 980, 'max': 1100}, # Atmospheric pressure at sea level
                'dryt':{'min': -1, 'max': 43}, # Air temperature in dry bulb
                'wspd':{'min': 0, 'max': 26}, # Horizontal wind speed
                'cndc': {'min': 3, 'max': 7},  # electrical conductivity
                'psal': {'min': 34, 'max': 40},  # practical salinity
                'pres': {'min': 18, 'max': 22},  # sea pressure
                'svel': {'min': 1300, 'max': 1600},  # Observed sea level
            }

            parameter_qc = self.name_qc(parameter)
            parts = parameter.split("_")

            # Check if there is latitude parameter in self.data
            if 'latitude' not in self.data.keys():
                return

            # Check where is the observation
            if (obsea_values['latitude']['min'] < self.data['latitude']).all():
                if (obsea_values['latitude']['max'] > self.data['latitude']).all():
                    if (obsea_values['longitude']['min'] < self.data['longitude']).all():
                        if (obsea_values['longitude']['max'] > self.data['longitude']).all():
                            impossible_values = obsea_values
            elif (obsea_values['latitude']['min'] < self.data['latitude']).all():
                if (obsea_values['latitude']['max'] > self.data['latitude']).all():
                    if (obsea_values['longitude']['min'] < self.data['longitude']).all():
                        if (obsea_values['longitude']['max'] > self.data['longitude']).all():
                            impossible_values = mediterranean_values
            else:
                return

            self.data.ix[self.data[parameter] < impossible_values[parts[0]]['min'], parameter_qc] = qc_number
            self.data.ix[self.data[parameter] > impossible_values[parts[0]]['max'], parameter_qc] = qc_number

        def spike_test(parameter, influence_in=0.8, lag_in=5, threshold_in=3.5, qc_number = 4):

            # Adaptation of algorithm from https://stackoverflow.com/a/22640362/6029703
            def thresholding_algo(y, lag, threshold_algo, influence):
                signals = np.zeros(len(y))
                filtered_y = np.array(y)
                avg_filter = [0] * len(y)
                std_filter = [0] * len(y)
                avg_filter[lag - 1] = np.mean(y[0:lag])
                std_filter[lag - 1] = np.std(y[0:lag])
                for cont in range(lag, len(y)):
                    if abs(y[cont] - avg_filter[cont - 1]) > threshold_algo * std_filter[cont - 1]:
                        signals[cont] = 1
                        filtered_y[cont] = influence * y[cont] + (1 - influence) * filtered_y[cont - 1]
                        avg_filter[cont] = np.mean(filtered_y[(cont - lag):cont])
                        std_filter[cont] = np.std(filtered_y[(cont - lag):cont])
                    else:
                        signals[cont] = 0
                        filtered_y[cont] = y[cont]
                        avg_filter[cont] = np.mean(filtered_y[(cont - lag):cont])
                        std_filter[cont] = np.std(filtered_y[(cont - lag):cont])
                return signals

            spike_flags = thresholding_algo(y=self.data[parameter].dropna().values, lag=lag_in,
                                         threshold_algo=threshold_in, influence=influence_in)

            parameter_qc = self.name_qc(parameter)

            self.data.ix[spike_flags == 1, parameter_qc] = qc_number

        def range_change_test(parameter, influence_in=0.8, lag_in=5, multiplier_in=3, qc_number=4):

            def slope_algo(y, lag, influence, multiplier_algo):
                signals = np.zeros(len(y))
                filtered_y = np.array(y)
                slope = [0] * len(y)
                slope[lag - 1] = max([abs(x - z) for x, z in zip(filtered_y[:lag - 1], filtered_y[1:lag])])
                for cont in range(lag, len(y)):
                    if abs(y[cont] - y[cont - 1]) > slope[cont - 1] * multiplier_algo:
                        signals[cont] = 1
                        filtered_y[cont] = influence * y[cont] + (1 - influence) * filtered_y[cont - 1]
                    else:
                        signals[cont] = 0
                    slope[cont] = max([abs(x - z) for x, z in zip(
                        filtered_y[cont - lag + 1:cont], filtered_y[cont - lag + 2:cont + 1])])
                return signals

            range_flags = slope_algo(y=self.data[parameter].dropna().values, lag=lag_in, influence=influence_in,
                                  multiplier_algo=multiplier_in)

            parameter_qc = self.name_qc(parameter)

            self.data.ix[range_flags == 1, parameter_qc] = qc_number

        def good_values(parameter, qc_number=1):
            """
            The values that still are with a QC Flag = 0 changes to QC Flag = 1
            :param parameter:
            :return:
            """
            parameter_qc = self.name_qc(parameter)

            self.data.ix[self.data[parameter_qc] == 0, parameter_qc] = qc_number

        def flat_test(parameter, lag_in=5, qc_number=4):
            """
            Flat test.
            :param parameter:
            :param lag_in:
            :return:
            """

            def flat_algo(y, lag):
                """

                :param parameter:
                :param lag:
                :return:
                """
                signals = np.zeros(len(y))
                for cont in range(lag, len(y)):
                    values = y[cont-lag:cont]
                    # Check if all values are equal
                    if (values[1:] == values[:-1]).all():
                        signals[cont] = 1
                    else:
                        signals[cont] = 0
                return signals

            flat_flags = flat_algo(y=self.data[parameter].dropna().values, lag=lag_in)

            parameter_qc = self.name_qc(parameter)

            self.data.ix[flat_flags == 1, parameter_qc] = qc_number

        def qc_procedure(parameter, influencer_proces, threshold_proces, multiplier_proces):
            # Calculation of lag
            lag_qc = 3
            if len(self.data[parameter].dropna().values) == 0:
                # No values
                return
            if len(self.data[parameter].dropna().values) > 10:
                lag_qc = 5
            if len(self.data[parameter].dropna().values) > 100:
                lag_qc = 10
            elif len(self.data[parameter].dropna().values) > 1000:
                lag_qc = 50

            gap_test(parameter)
            location_test(parameter)
            range_test(parameter)
            spike_test(parameter, influencer_proces, lag_qc, threshold_proces)
            range_change_test(parameter, influencer_proces, lag_qc, multiplier_proces)
            flat_test(parameter, lag_qc)
            good_values(parameter)

        if param:
            qc_procedure(param, influencer, threshold, multiplier)
        else:
            for key in self.data.keys():
                if "_qc" in key:
                    continue
                elif "latitude" in key:
                    continue
                elif "longitude" in key:
                    continue
                else:
                    qc_procedure(key, influencer, threshold, multiplier)

    def drop_qc(self, qc_flag):
        """

        :return:
        """
        for key in self.data.keys():
            if "_qc" in key:
                continue
            if "latitude" in key:
                continue
            if "longitude" in key:
                continue
            parameter_qc = self.name_qc(key)
            data = self.data[self.data[parameter_qc] != qc_flag]
            self.data = data

    def name_qc(self, parameter):
        """
        Returns the name of the column with the QC Flag information of the parameter.
        :param parameter: Name of the column od self.data without qc
        :return:
        """
        parts = parameter.split("_")
        if len(parts) == 1:
            parameter_qc = parameter + "_qc"
        elif len(parts) == 2:
            parameter_qc = parts[0] + "_qc_" + parts[1]
        else:
            parameter_qc = "ERROR"

        return parameter_qc

    def info(self, path=None):
        """
        It returns a full summary about what it contains (the metadata.)
        :param path: Path where the file is.
        :return:
        """
        message = ""
        if path:
            message += "Path: {}\n".format(path)
        for key in self.metadata.keys():
            if key == "summary" and type(self.metadata[key]) is dict:
                message += "Summary\n"
                for key_summary in self.metadata['summary']:
                    message += "- {}\n".format(key_summary)
                    for key_parameter in self.metadata['summary'][key_summary]:
                        message += " - {}: {}\n".format(
                            key_parameter.title().replace("_", " "),
                            self.metadata['summary'][key_summary][key_parameter])
            else:
                message += "{}: {}\n".format(key.title().replace("Cdm", "CDM").replace("Qc", "QC").replace("_", " "),
                                             self.metadata[key])
        return message

    def resample(self, rule):
        """
        Convenience method for frequency conversion and resampling of time series of the WaterFrame object.
        :param rule: The offset string or object representing target conversion.
        See http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        """
        try:
            self.data = self.data.resample(rule).mean()
        except TypeError:
            # If you are here is becouse there is not data
            pass
        try:
            self.technical = self.technical.resample(rule).mean()
        except TypeError:
            # If you are here is becouse there is not technical data
            pass

        for key in self.data.keys():
            if "_qc" in key:
                self.data[key] = 8


def plot_corr(param_1, param_2, title="", x_label="", y_label="", legend=[]):
    """
    It creates a graph with all the time series of the list parameters.
    :param title: Title of the graph.
    :param x_label: X label of the graph.
    :param y_label: Y label of the graph.
    :param legend: Labels to show in the legend.
    :param param_1: Parameter to correlate.
    :param param_2: Parameter to correlate.
    :return: The graph.
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress(param_1.values, param_2.values)
    fig_correlation, axes = plt.subplots(nrows=1, ncols=1)
    axes.plot(param_1.values, param_2.values, marker='.', linestyle="")
    axes.plot(param_1.values, param_1.values * slope + intercept)
    axes.set_title(title)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    legend.append("$y = {:.2f}x+{:.2f}$ $r^2={:.2f}$".format(slope, intercept, r_value ** 2))
    axes.legend(legend, loc='best')
    return fig_correlation


class PlotMap:
    def __init__(self, ):
        self.m = Basemap()

    def map_world(self, res='l'):
        """
        It creates a map of the world.
        :return:
        """
        self.m = Basemap(projection='mill', resolution=res)
        # Draw the costal lines
        self.m.drawcoastlines()
        # Fill the continents with black
        self.m.fillcontinents(color='K')

    def map_mediterranean(self, res='l'):
        """
        It creates a map of the Mediterranean.
        :param res: Resolution of the map
        :return:
        """
        self.m = Basemap(projection='mill', resolution=res, llcrnrlat=30, llcrnrlon=-13, urcrnrlat=47, urcrnrlon=38)
        # Draw the costal lines
        self.m.drawcoastlines()
        # Fill the continents with black
        self.m.fillcontinents(color='K')

    def add_pointxxx(self, lon, lat, *arg):
        """Añadimos puntos al mapa
        :param lon: longitud
        :type lon: float
        :param lat: latitud
        :type lat: float
        :param arg: valor R,G,B,C
        :type arg: float
        """
        xpt, ypt = self.m(lon, lat)
        if 1 == len(arg):
            marker_color = arg[0]
            self.m.plot(xpt, ypt, marker='o', color='k', markersize=7)
            # self.m.plot(xpt, ypt, marker='o', color=str(marker_color), markersize=7)
        elif len(arg) == 4:
            color_red = arg[0]
            color_green = arg[1]
            color_blue = arg[2]
            color_clear = arg[3]
            self.m.plot(xpt, ypt, marker='o', color=[color_red, color_green, color_blue, color_clear], markersize=7)

    def add_point(self, lon, lat, color='blue', label=None):
        """Añadimos puntos al mapa
        :param lon: longitud
        :type lon: float
        :param lat: latitud
        :type lat: float
        :param color_in: color of the point.
        :type color_in: str
        """
        x, y = self.m(float(lon), float(lat))
        self.m.plot(x, y, color=color, marker='o', markersize=7)
        if label is not None:
            plt.text(x+10000,y+5000, label)
