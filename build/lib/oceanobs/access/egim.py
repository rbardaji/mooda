import ast
from io import StringIO
import requests
from oceanobs import WaterFrame
import pandas as pd


class EGIM:
    """Class to download EGIM data from the EMSODEV DMP."""

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
            r = requests.get('http://api.emsodev.eu/observatories',
                             auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:
            answer = r.json()
            observatoryList = [observatory['name'] for observatory in answer]
            return r.status_code, observatoryList
        else:
            return r.status_code, None

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
            r = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments'.format(
                    observatory), auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:
            answer = r.json()
            instrumentList = answer['instruments']
            return r.status_code, instrumentList
        else:
            return r.status_code, None

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
            r = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments/{}'.format(
                    observatory, instrument), auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:
            answer = r.json()
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
            return r.status_code, metadata_dict
        else:
            return r.status_code, None

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
            r = requests.get(
                'http://api.emsodev.eu/observatories/{}/instruments/{}/'
                'parameters'.format(observatory, instrument),
                auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:
            answer = r.json()
            parameterList = answer['parameters']
            return r.status_code, parameterList
        else:
            return r.status_code, None

    def observation(self, observatory, instrument, parameter, startDate=None,
                    endDate=None, limit=None):
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
            startDate: str, optional (startDate = None)
                Beginning date for the time series range. The date format is
                dd/MM/yyyy.
                If the start time is not supplied, we are going to use 'limit'.
            endDate: str
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
            if startDate and endDate:
                query = 'http://api.emsodev.eu/observatories' + \
                        '/{}/instruments'.format(observatory) + \
                        '/{}/parameters/{}?startDate={}&endDate={}'.\
                    format(instrument, parameter, startDate,
                           endDate)
            elif startDate:
                query = 'http://api.emsodev.eu/observatories' + \
                        '/{}/instruments/{}/parameters/{}?startDate={}'.\
                        format(observatory, instrument, parameter, startDate)
        try:
            r = requests.get(query, auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:
            answer = r.json()
            observations = []
            for observation in answer['observations']:
                observations.append((observation['phenomenonTime'],
                                     observation['value']))
            # Format data
            df = pd.DataFrame({parameter: [x[1] for x in observations],
                               'time': [x[0] for x in observations]})
            # Changing the time values to a datatime
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.rename(columns={"time": "TIME"}, inplace=True)
            df.set_index('TIME', inplace=True)

            return r.status_code, df
        else:
            return r.status_code, None

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
            r = requests.get('http://api.emsodev.eu/observatories' +
                             '/{}/instruments/{}/acousticfiledate'.format(
                                 observatory, instrument),
                             auth=(self.login, self.password))
        except requests.RequestException:
            return None, None
        if r.status_code == 200:
            answer = r.json()
            dateList = answer['acousticOobservationDate']
            return r.status_code, dateList
        else:
            return r.status_code, None

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
                wf.data.rename(columns={"depth": "DEPTH"}, inplace=True)
                wf.data["DEPTH_QC"] = 0
                wf.meaning['DEPTH'] = {"long_name": "depth", "units": "meters"}
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
