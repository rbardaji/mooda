import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal


class Observatory:
    """
    Texto explicativo de la clase.
    """

    def __init__(self):
        """
        Constructor of class
        """
        # Object instance variables
        self.data = None
        self.metadata = None
        self.data_original = None
        self.dialog = False

    """ Data management functions """

    def reset_data(self):
        """
        Reload the original data
        """
        self.data = self.data.copy()

    def slicing(self, start_time, end_time):
        """
        Slicing by date conditions.
        :param start_time: start time of the slice with format 'YYYYMMDDHHmmss'.
        :type start_time: str
        :param end_time: end time of the slice with format 'YYYYMMDDHHmmss'.
        """
        self.data = self.data[start_time:end_time]

    def resample_data(self, how_often):
        """
        Resample data. This function calculate an average of the values if it is necessary.
        :param how_often: Frequency to that we want the data.
        :type how_often: str
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
        def change_bad_values():
            data_keys = self.data.keys()
            if 'atm' in data_keys:
                self.data.ix[self.data['atm_qc'] != 1, 'atm'] = np.nan
                self.data.ix[self.data['atm_qc'] != 1, 'atm_qc'] = 1
            if 'wisp_qc' in data_keys:
                self.data.ix[self.data['wisp_qc'] != 1, 'wisp'] = np.nan
                self.data.ix[self.data['wisp_qc'] != 1, 'wisp_qc'] = 1
            if 'widi_qc' in data_keys:
                self.data.ix[self.data['widi_qc'] != 1, 'widi'] = np.nan
                self.data.ix[self.data['widi_qc'] != 1, 'widi_qc'] = 1
            if 'atemp_qc' in data_keys:
                self.data.ix[self.data['atemp_qc'] != 1, 'atemp'] = np.nan
                self.data.ix[self.data['atemp_qc'] != 1, 'atemp_qc'] = 1
            if 'wape_qc' in data_keys:
                self.data.ix[self.data['wape_qc'] != 1, 'wape'] = np.nan
                self.data.ix[self.data['wape_qc'] != 1, 'wape_qc'] = 1
            if 'wahe_qc' in data_keys:
                self.data.ix[self.data['wahe_qc'] != 1, 'wahe'] = np.nan
                self.data.ix[self.data['wahe_qc'] != 1, 'wahe_qc'] = 1
            if 'wadi_qc' in data_keys:
                self.data.ix[self.data['wadi_qc'] != 1, 'wadi'] = np.nan
                self.data.ix[self.data['wadi_qc'] != 1, 'wadi_qc'] = 1
            if 'temp_qc' in data_keys:
                self.data.ix[self.data['temp_qc'] != 1, 'temp'] = np.nan
                self.data.ix[self.data['temp_qc'] != 1, 'temp_qc'] = 1

        def resample_qc():
            data_keys = self.data.keys()
            if 'atm_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['atm']), 'atm_qc'] = 9
            if 'wisp_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['wisp']), 'wisp_qc'] = 9
            if 'widi_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['widi']), 'widi_qc'] = 9
            if 'atemp_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['atemp']), 'atemp_qc'] = 9
            if 'wape_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['wape']), 'wape_qc'] = 9
            if 'temp_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['temp']), 'temp_qc'] = 9

        # Change the bad values
        change_bad_values()
        # Resample
        try:
            self.data = self.data.resample(how_often).mean()
        except AttributeError:
            self.dialog = "Error: Cannot resample becouse there is no data."
        # Change qc flag to interpolated value
        resample_qc()
        # Interpolarization
        self.data.interpolate(inplace=True)

    def butterworth_filter(self, component, order=2, cutoff_frequency=0.01):
        """
        Apply the Butterworth Filter to the data.
        :param component: Name of the parameter that you want to filter.
        :type component: str
        :param order: Filter order
        :type order: int
        :param cutoff_frequency: Cutoff frequency
        :type  cutoff_frequency: float
        :return:
        """
        self.dialog = None
        try:
            # First, design the Buterworth filter
            b, a = signal.butter(order, cutoff_frequency, output='ba')
            # Second, apply the filter
            filtered_data = signal.filtfilt(b, a, self.data[component])
            # Changing the QC flac to say that the value was modified.
            self.data.ix[self.data[component] != filtered_data, component+'_qc'] = 5
            # Adding the values
            self.data[component] = filtered_data
        except KeyError:
            self.dialog = "Error: {}".format(KeyError)

    def clear_bad_data(self):
        """
        Delete all the data with QC flags 2, 3, 4, 6 and 9
        """
        for key in self.data.keys():
            if "_qc" in key:
                self.data = self.data[self.data[key] != 2]
                self.data = self.data[self.data[key] != 3]
                self.data = self.data[self.data[key] != 4]
                self.data = self.data[self.data[key] != 6]
                self.data = self.data[self.data[key] != 9]

    """ Data information"""

    def info_data(self):
        """
        Return when your data start and stop in terms of time.
        :return: info de data
        :rtype: str
        """
        # Search for initial and final dates
        try:
            # Look for start and stop time
            start_time = self.data.first_valid_index()
            stop_time = self.data.last_valid_index()
            message = "start time: {}\nstop time: {}\n".format(start_time, stop_time)
            # Look for the parameters
            message += "Parameters: "
            for key in self.data.keys():
                if "_qc" in key:
                    continue
                message += "{}, ".format(key)
        except IndexError:
            message = "Error: No good data."
        return message[:-2]

    def info_metadata(self):
        """
        Return all the metadata information in a string format.
        :return: str, metadata information.
        """
        keys = self.metadata.keys()
        message = ""
        for key in keys:
            if self.metadata[key][0] != " ":
                message += "{}: {}\n".format(key, str(self.metadata[key][0]))
        return message[:-1]  # Delete the last "\n"

    @staticmethod
    def info_qc_flags():
        """
        Plot information
        :return: string with the information
        """
        info = "We are using the GLOBAL QCFF flags.\n" \
               "Flag - Meaning\n" \
               "0 - no quality control\n" \
               "1 - value seems correct\n" \
               "2 - value appears inconsistent with other values\n" \
               "3 - value seems doubtful\n" \
               "4 - value seems erroneous\n" \
               "5 - value was modified\n" \
               "6 - flagged land test\n" \
               "7 - nominal_value\n" \
               "8 - interpolated value\n" \
               "9 - value missing"
        return info

    def info_parameters(self):
        """
        Gives information about what parameters are you using in the variable self.data
        :return: string with the information
        """
        message = ""
        for key in self.data.keys():
            if "time_qc" == key:
                message += "time_qc: Quality control flag related to the time of the measurement (the time is" + \
                          " the index of the data frame).\n"
            if "temp" == key:
                message += "temp: Temperature of the water in Celsius degrees.\n"
            if "temp_qc" == key:
                message += "temp_qc: Quality control flag related to the temperature of the water.\n"
            if "atemp" == key:
                message += "atemp: Air temperatre in Celsius degree.\n"
            if "atemp_qc" == key:
                message += "atemp_qc: Quality control flag related to the air temperature.\n"
            if "cond" == key:
                message += "cond: Conductivity of the water in S/m.\n"
            if "cond_qc" == key:
                message += "Quality control flag related to the conductivity.\n"
            if "sal" == key:
                message += "sal: Salinity of the water in PSU.\n"
            if "sal_qc" == key:
                message += "sal_qc: Quality control flag related to the salinity of the water.\n"
            if "pres" == key:
                message += "pres: Pressure of the sensor in water in dBars.\n"
            if "atm" == key:
                message += "atm: Atmospheric pressure in dBars.\n"
            if "atm_qc" == key:
                message += "atm_qc: Quality control flag related to the atmospheric pressure.\n"
            if "wis" == key:
                message += "wis: Wind speed in m/s.\n"
            if "wis_qc" == key:
                message += "wis_qc: Quality control flag related to the wind speed.\n"
            if "ph" == key:
                message += "ph: Power of hydrogen (pH, no units of measurement).\n"
            if "ph_qc" == key:
                message += "ph_qc: Quality control flag related to the pH.\n"
            if "wad" == key:
                message += "wad: Wave direction relative to true north in degrees.\n"
            if "wad_qc" == key:
                message += "wap_qc: Quality control flag related to the zero-crossing wave period.\n"
            if "sovel" == key:
                message += "sovel: Sound velocity in m/s.\n"
            if "sovel_qc" == key:
                message += "sovel_qc: Quality control flag related to the sound velocity.\n"
            if "depth" == key:
                message += "depth: Depth of the sensor in m.\n"
            if "depth_qc" == key:
                message += "depth_qc: Quality control flag related to the depth.\n"
            if "tur" in key:
                message += "tur: Turbidity in NTU.\n"
            if "tur_qc" == key:
                message += "tur_qc:  Quality control flag related to the turbidity.\n"
            if "oxy" in key:
                message += "oxy: Oxygen concentration in ?????.\n"
            if "oxy_qc" == key:
                message += "oxy_qc: Quality control flag related to the oxygen concentration.\n"
            if "asa" == key:
                message += "asa: Air saturation in %.\n"
            if "asa_qc" == key:
                message += "asa_qc: Quality control flag related to the air saturation.\n"
            if "sele" == key:
                message += "sele: Observed sea level in meters.\n"
            if "sele_qc" == key:
                message += "Quality control flag related to the observed sea level.\n"

        return message[:-1]

    @staticmethod
    def translator(parameter):
        """
        It helps to understand the data names.
        :param parameter: Name of the variable that you want to understand
        :return: tuple (2x1) with the real name and the values of the variable
        """

        translation = (None, None)
        if "temp" == parameter:
            translation = ("Sea temperature", "degrees Celsius")
        if "atemp" == parameter:
            translation = ("Air temperatre", "degrees Celsius")
        if "cond" == parameter:
            translation = ("Conductivity", "S/m")
        if "sal" == parameter:
            translation = ("Salinity", "PSU")
        if "pres" == parameter:
            translation = ("Pressure", "dBars")
        if "atm" == parameter:
            translation = ("Atmospheric pressure", "dBars")
        if "wis" == parameter:
            translation = ("Wind speed", "m/s")
        if "ph" == parameter:
            translation = ("pH", "(no units)")
        if "wad" == parameter:
            translation = ("Wave direction relative to true north", "degrees")
        if "sovel" == parameter:
            translation = ("Sound velocity", "m/s")
        if "depth" == parameter:
            translation = ("Depth", "m")
        if "tur" == parameter:
            translation = ("Turbidity", "NTU")
        if "oxy" == parameter:
            translation = ("Oxygen", "???")
        if "asa" == parameter:
            translation = ("Air saturation", "%")
        if "sele" == parameter:
            translation = ("Sea level", "m")

        return translation

    """ Plot functions """

    """def plt_hist_wind_speed(self):
        # Wave height
        fig_air, axes = plt.subplots(nrows=1, ncols=1)
        self.data['WSPD'].plot.hist(ax=axes,)
        axes.set_title('Wind speed histogram')
        axes.set_ylabel('hours')
        axes.set_xlabel('meter/second')

        return fig_air

    def plt_maximun_windspeed(self):
        # Wave height

        fig_maw_wind, axes = plt.subplots(nrows=1, ncols=1)
        self.data.groupby(pd.TimeGrouper('D')).WSPD.max().plot(ax=axes,)
        axes.set_title('Maximun windspeed')
        axes.set_ylabel('meter/second')
        axes.set_xlabel('Days')
        return fig_maw_wind"""

    def plt_cond(self, qc_flag=None):
        """
        Graph of conductivity vs time.
        :param qc_flag: It indicates the QC flag number of the data you want to plot
        :return: Figure
        """
        self.dialog = False

        fig_cond, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['cond'].plot(ax=axes)
            else:
                self.data['cond'][self.data['cond_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No conductivity data."
        except TypeError:
            self.dialog = "Error: No conductivity data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Conductivity')
        axes.set_ylabel('s/m')
        axes.set_xlabel('Time UTC')
        return fig_cond

    def plt_temp(self, qc_flag=None):
        """
        Graph of Sea temperature vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_temp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['temp'].plot(ax=axes)
            else:
                self.data['temp'][self.data['temp_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No sea tempreture data."
        except TypeError:
            self.dialog = "Error: No sea temperature data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Sea temperature')
        axes.set_ylabel('ºC')
        axes.set_xlabel('Time UTC')
        return fig_temp

    def plt_atemp(self, qc_flag=None):
        """
        Graph of Air temperature vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_atemp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['atemp'].plot(ax=axes)
            else:
                self.data['atemp'][self.data['atemp_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No air tempreture data."
        except TypeError:
            self.dialog = "Error: No air temperature data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Air temperature')
        axes.set_ylabel('ºC')
        axes.set_xlabel('Time UTC')
        return fig_atemp

    def plt_pres(self, qc_flag=None):
        """
        Graph of pressure vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['pres'].plot(ax=axes)
            else:
                self.data['pres'][self.data['pres_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No pressure data."
        except TypeError:
            self.dialog = "Error: No pressure data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Pressure')
        axes.set_xlabel('Time UTC')
        axes.set_ylabel('DBar')
        return fig_pres

    def plt_atm(self, qc_flag=None):
        """
        Graph of atmospheric pressure vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_pres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                (self.data['atm']).plot(ax=axes)
            else:
                (self.data['atm'][self.data['atm_qc'] == qc_flag]).plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No atmospheric pressure data."
        except TypeError:
            self.dialog = "Error: No atmospheric pressure data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Atmospheric pressure')
        axes.set_xlabel('Time UTC')
        axes.set_ylabel('hPa')
        return fig_pres

    def plt_sal(self, qc_flag=None):
        """
        Graph of salinity vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_sal, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['sal'].plot(ax=axes)
            else:
                self.data['sal'][self.data['sal_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No salinity data."
        except TypeError:
            self.dialog = "Error: No salinity data with quality control flag = {}.".format(qc_flag)
        axes.set_title("Salinity")
        axes.set_xlabel("Time UTC")
        axes.set_ylabel("PSU")
        return fig_sal

    def plt_ts(self):
        """
        Graph of T-S.
        :return: figura
        """
        fig_ts, axes = plt.subplots(nrows=1, ncols=1)
        axes.plot(self.data['temperatura'], self.data['salinitat'], linestyle="None", marker=".")
        axes.set_title("Temperature - Salinity")
        axes.set_xlabel("Tempreature (Celsius degree)")
        axes.set_ylabel("Salinity (PSU)")
        return fig_ts

    def plt_sovel(self, qc_flag=None):
        """
        Graph of sound velocity vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_sovel, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['sovel'].plot(ax=axes)
            else:
                self.data['sovel'][self.data['sovel_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No sound velocity data."
        except TypeError:
            self.dialog = "Error: No sound velocity data with quality control flag = {}.".format(qc_flag)
        axes.set_title("Sound velocity")
        axes.set_xlabel("Time UTC")
        axes.set_ylabel("m/s")
        return fig_sovel

    def plt_co2(self):
        """
        Graph of CO2 vs time.
        :return: figura
        """
        fig_co2, axes = plt.subplots(nrows=1, ncols=1)
        self.data['co2'].plot(ax=axes)
        axes.set_title("CO2")
        axes.set_xlabel("Time UTC")
        axes.set_ylabel("CO2 (ppm)")
        return fig_co2

    def plt_wisp(self, qc_flag=None):
        """
        Graph of wind speed vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_ws, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['wisp'].plot(ax=axes)
            else:
                self.data['wisp'][self.data['wisp_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No sound velocity data."
        except TypeError:
            self.dialog = "Error: No sound velocity data with quality control flag = {}.".format(qc_flag)
        axes.set_title("Wind Speed")
        axes.set_ylabel("m/s")
        axes.set_xlabel("Time UTC")
        return fig_ws

    def plt_widi(self, qc_flag=None):
        """
        Graph of wind direction vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_wd, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['widi'].plot(ax=axes)
            else:
                self.data['widi'][self.data['widi_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No sound velocity data."
        except TypeError:
            self.dialog = "Error: No wind direction data with quality control flag = {}.".format(qc_flag)
        axes.set_title("Wind direction relative to North")
        axes.set_xlabel("Time UTC")
        axes.set_ylabel("Degrees")
        return fig_wd

    def plt_qc(self):
        """
        Graph of QC.
        :return: Figure
        """
        def select_qc_data():
            """
            Selection of qc data.
            :return: pandas Dataframe with the QC data.
            """
            # init pandas DataFrame
            data_qc_ = pd.DataFrame()
            # Look for QC data
            data_keys = self.data.keys()
            for key in data_keys:
                if '_qc' in key:
                    data_qc_ = data_qc_.append(self.data[key])
            return data_qc_

        def cmap_discretize(cmap_input, ncolors):
            """
            Return a discrete colormap from the continuous colormap cmap.
            :param cmap_input: colormap instance, eg. cm.jet.
            :param ncolors: number of colors.
            :return ncolors.LinearSegmentedColormap
            """

            if type(cmap_input) == str:
                plt.get_cmap(cmap_input)
            colors_i = np.concatenate((np.linspace(0, 1., ncolors), (0., 0., 0., 0.)))
            colors_rgba = cmap_input(colors_i)
            indices = np.linspace(0, 1., ncolors+1)
            cdict = {}
            for ki, key in enumerate(('red', 'green', 'blue')):
                cdict[key] = [(indices[i], colors_rgba[i-1, ki], colors_rgba[i, ki]) for i in range(ncolors+1)]
            # Return colormap object.
            return mcolors.LinearSegmentedColormap(cmap_input.name + "_%d" % ncolors, cdict, 1024)

        def colorbar_index(ncolors, cmap_input):
            """
            Return a discrete colormap from the continuous colormap cmap.
            :param ncolors: number of colors.
            :param cmap_input: colormap instance, eg. cm.jet.
            """
            yticklabels = ['0, no QC', '1, correct', '2, inconsistent', '3, doubtful', '4, erroneous', '5, modified',
                           '6, land test', '7, nominal value', '8, interpolated', '9, value missing']

            mappable = cm.ScalarMappable(cmap=cmap_input)
            mappable.set_array([])
            mappable.set_clim(-0.5, ncolors+0.5)
            colorbar = plt.colorbar(mappable)
            colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
            colorbar.set_ticklabels(yticklabels)
            # colorbar.set_ticklabels(range(ncolors))

        data_qc = select_qc_data()

        fig_qc, ax = plt.subplots()

        # Creation of a discret cmap
        cmap = plt.get_cmap('jet')
        cmap_disc = cmap_discretize(cmap_input=cmap, ncolors=10)
        # Creation of the colorbar
        colorbar_index(ncolors=10, cmap_input=cmap_disc)
        # Creation of the graph
        ax.pcolor(data_qc, cmap=cmap_disc, edgecolor='w', vmin=0, vmax=9)
        ax.set_xlim(0, len(data_qc.keys()))
        # Adding text to the headmap
        for y in range(data_qc.shape[0]):
            for x in range(data_qc.shape[1]):
                plt.text(x + 0.5, y + 0.5, "{}".format(int(data_qc.iloc[y, x])), horizontalalignment='center',
                         verticalalignment='center', color='w')
        plt.yticks(np.arange(0.5, len(data_qc.index), 1), data_qc.index)
        plt.xticks(np.arange(0.5, len(data_qc.columns), 1), data_qc.columns)
        fig_qc.autofmt_xdate()

        return fig_qc

    def plt_wadi(self, qc_flag=None):
        """
        Graph of wave direction vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_wadi, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['wadi'].plot(ax=axes)
            else:
                self.data['wadi'][self.data['wadi_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No wave direction data."
        except TypeError:
            self.dialog = "Error: No wave direction data with quality control flag = {}.".format(qc_flag)
        axes.set_title("Wave direction relative true north")
        axes.set_ylabel("degree")
        axes.set_xlabel("Time UTC")
        return fig_wadi

    def plt_wape(self, qc_flag=None):
        """
        Graph of wave period vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_wape, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['wape'].plot(ax=axes)
            else:
                (self.data['wape'][self.data['wape_qc'] == qc_flag]).plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No wave period data."
        except TypeError:
            self.dialog = "Error: No wave period data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Wave period')
        axes.set_xlabel('Time UTC')
        axes.set_ylabel('seconds')

        return fig_wape

    def plt_wahe(self, qc_flag=None):
        """
        Graph of wave height vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_atemp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['wahe'].plot(ax=axes)
            else:
                self.data['wahe'][self.data['wahe_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No wave height data."
        except TypeError:
            self.dialog = "Error: No wave height data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Significant wave height')
        axes.set_ylabel('meters')
        axes.set_xlabel('Time UTC')
        return fig_atemp

    def plt_atmpres(self, qc_flag=None):
        """
        Graph of atmospheric pressure at sea level vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_atmpres, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['atmpres'].plot(ax=axes)
            else:
                self.data['atmpres'][self.data['atmpres_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No atmospheric pressure data."
        except TypeError:
            self.dialog = "Error: No atmospheric pressure data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Pressure at sea level')
        axes.set_ylabel('dB')
        axes.set_xlabel('Time UTC')
        return fig_atmpres

    def plt_sele(self, qc_flag=None):
        """
        Graph of sea level vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_sele, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['sele'].plot(ax=axes)
            else:
                self.data['sele'][self.data['sele_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No sea level data."
        except TypeError:
            self.dialog = "Error: No sea level data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Observed sea level')
        axes.set_ylabel('m')
        axes.set_xlabel('Time UTC')
        return fig_sele

    def plt_prec(self, qc_flag=None):
        """
        Graph of rain accumulation vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_prec, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['prec'].plot(ax=axes)
            else:
                self.data['prec'][self.data['prec_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No rain accumulation data."
        except TypeError:
            self.dialog = "Error: No rain accumulation data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Precipitation rate')
        axes.set_ylabel('mm')
        axes.set_xlabel('Time UTC')
        return fig_prec

    def plt_relhu(self, qc_flag=None):
        """
        Graph of relative humidity vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_relhu, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['relhu'].plot(ax=axes)
            else:
                self.data['relhu'][self.data['relhu_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No relative humidity data."
        except TypeError:
            self.dialog = "Error: No relative humidity data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Relative humidity')
        axes.set_ylabel('%')
        axes.set_xlabel('Time UTC')
        return fig_relhu

    def plt_gusp(self, qc_flag=None):
        """
        Graph of gust wind speed vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_gusp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['gusp'].plot(ax=axes)
            else:
                self.data['gusp'][self.data['gusp_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No gust wind speed data."
        except TypeError:
            self.dialog = "Error: No gust wind speed data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Gust wind speed')
        axes.set_ylabel('m/s')
        axes.set_xlabel('Time UTC')
        return fig_gusp

    def plt_cusp(self, qc_flag=None):
        """
        Graph of current speed vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_cusp, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['cusp'].plot(ax=axes)
            else:
                self.data['cusp'][self.data['cusp_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No currrent speed data."
        except TypeError:
            self.dialog = "Error: No currrent speed data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Horitzontal current speed')
        axes.set_ylabel('m/s')
        axes.set_xlabel('Time UTC')
        return fig_cusp

    def plt_cudi(self, qc_flag=None):
        """
        Graph of current direction vs time.
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_cudi, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                self.data['cudi'].plot(ax=axes)
            else:
                self.data['cudi'][self.data['cudi_qc'] == qc_flag].plot(ax=axes)
        except KeyError:
            self.dialog = "Error: No currrent direction data."
        except TypeError:
            self.dialog = "Error: No currrent direction data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Current to direction relative true north')
        axes.set_ylabel('degrees')
        axes.set_xlabel('Time UTC')
        return fig_cudi

    def plt_all(self, qc_flag=None):
        """
        Create all the possible grapths
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Dictionary where the ‘keys’ are the name of the figures and the ‘values’ are matplotlib-figure objects.
        """
        fig_dict = {}
        data_keys = self.data.keys()
        if 'cond' in data_keys:
            fig_cond = self.plt_cond(qc_flag)
            fig_dict['Conductivity'] = fig_cond
        if 'temp' in data_keys:
            fig_temp = self.plt_temp(qc_flag)
            fig_dict['Temperature'] = fig_temp
        if 'pres' in data_keys:
            fig_pres = self.plt_pres(qc_flag)
            fig_dict['Pressure'] = fig_pres
        if 'sal' in data_keys:
            fig_sal = self.plt_sal(qc_flag)
            fig_dict['Salinity'] = fig_sal
        if 'sovel' in data_keys:
            fig_sovel = self.plt_sovel(qc_flag)
            fig_dict['Sound velocity'] = fig_sovel
        if 'atm' in data_keys:
            fig_atm = self.plt_atm(qc_flag)
            fig_dict['Atmospheric pressure'] = fig_atm
        if 'wisp' in data_keys:
            fig_wisp = self.plt_wisp(qc_flag)
            fig_dict['Wind speed'] = fig_wisp
        if 'widi' in data_keys:
            fig_widi = self.plt_widi(qc_flag)
            fig_dict['Wind direction'] = fig_widi
        if 'atemp' in data_keys:
            fig_atemp = self.plt_atemp(qc_flag)
            fig_dict['Air temperature'] = fig_atemp
        if 'wahe' in data_keys:
            fig_wahe = self.plt_wahe(qc_flag)
            fig_dict['Wave height'] = fig_wahe
        if 'wadi' in data_keys:
            fig_wadi = self.plt_wadi(qc_flag)
            fig_dict['Wave direction'] = fig_wadi
        if 'wape' in data_keys:
            fig_wape = self.plt_wape(qc_flag)
            fig_dict['Wave period'] = fig_wape
        if 'atmpres' in data_keys:
            fig_atmpres = self.plt_atmpres(qc_flag)
            fig_dict['Pressure sea level'] = fig_atmpres
        if 'sele' in data_keys:
            fig_sele = self.plt_sele(qc_flag)
            fig_dict['Sea level'] = fig_sele
        if 'prec' in data_keys:
            fig_prec = self.plt_prec(qc_flag)
            fig_dict['Rain acumulation'] = fig_prec
        if 'relhu' in data_keys:
            fig_relhu = self.plt_relhu(qc_flag)
            fig_dict['Relative humidity'] = fig_relhu
        if 'gusp' in data_keys:
            fig_gusp = self.plt_gusp(qc_flag)
            fig_dict['Gust wind speed'] = fig_gusp
        if 'cusp' in data_keys:
            fig_cusp = self.plt_cusp(qc_flag)
            fig_dict['Current speed'] = fig_cusp
        if 'cudi' in data_keys:
            fig_cudi = self.plt_cudi(qc_flag)
            fig_dict['Current direction'] = fig_cudi
        if len(self.data.index) < 25:
            fig_qc = self.plt_qc()
            fig_dict['QC flags'] = fig_qc

        return fig_dict

    def plt_multiparam_one_plot(self, *parameter, qc_flag=None):
        """
        Plot multiple parametes.
        :param parameter: List of parameters to plot
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_multiple, axes = plt.subplots(nrows=1, ncols=1)
        try:
            title = ""
            if qc_flag is None:
                for param in parameter:
                    meaning, units = self.translator(param)
                    title += "{} and ".format(meaning)
                    self.data[param].plot(ax=axes, label="{} in {}".format(meaning, units))
            else:
                for param in parameter:
                    param_qc = param + '_qc'
                    meaning, units = self.translator(param)
                    title += "{} and ".format(meaning)
                    self.data[param][self.data[param_qc] == qc_flag].plot(ax=axes, label="{} in {}".format(meaning,
                                                                                                           units))
            title = title[:-5]
            axes.set_title(title)
            axes.set_xlabel('Time UTC')
            axes.legend()
        except KeyError:
            self.dialog = "Error"
        except TypeError:
            self.dialog = "Error".format(qc_flag)
        return fig_multiple

    def plt_multiparam_multiplot(self, *parameter, qc_flag=None):
        """
        Plot multiple parametes.
        :param parameter: List of parameters to plot
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """

        self.dialog = False
        fig_multiplot, axes = plt.subplots(nrows=len(parameter), ncols=1, sharex=True)
        try:
            if qc_flag is None:
                i = 0
                for param in parameter:
                    self.data[param].plot(ax=axes[i])
                    title, units = self.translator(param)
                    axes[i].set_title(title)
                    axes[i].set_ylabel(units)
                    i += 1
            else:
                for param in parameter:
                    param_qc = param + '_qc'
                    self.data[param][self.data[param_qc] == qc_flag].plot(ax=axes)
                    title, units = self.translator(param)
                    axes[i].set_title(title)
                    axes[i].set_ylabel(units)
        except KeyError:
            self.dialog = "Error"
        except TypeError:
            self.dialog = "Error".format(qc_flag)
        axes[i-1].set_xlabel('Time UTC')

        return fig_multiplot
