import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal
from mpl_toolkits.basemap import Basemap
import datetime


class PlotMap:
    """Map plot management"""
    # Constructor
    def __init__(self, ):
        # Basemap object
        self.m = Basemap()

    def new_map_world(self, res='h'):
        """
        Creation of a world map.
        :param res: Map resolution (c,l,h,f). Defauld h - high
        :type res: char
        """
        self.m = Basemap(projection='mill', resolution=res)
        # Dibuja una linea en los continentes
        self.m.drawcoastlines()
        # Dibuja rios y lagos grandes
        # self.m.drawrivers(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
        # Rellena los continentes
        self.m.fillcontinents(color='K')
        # Dibuja paralelos
        # parallels = np.arange(41., 44, 1.)
        # self.m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
        # Dibuja meridianos
        # meridians = np.arange(0., 5., 1.)
        # self.m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    def new_map_iberic(self, res='h'):
        """Creation of a map of the Iberian Peninsula
        :param res: Map resolution (c,l,h,f). Defauld, h - high
        :type res: char
        """
        self.m = Basemap(projection='mill', llcrnrlat=34, llcrnrlon=-13, urcrnrlat=45, urcrnrlon=4, resolution=res)
        # Dibuja una linea en los continentes
        self.m.drawcoastlines()
        # Dibuja rios y lagos grandes
        # self.m.drawrivers(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
        # Rellena los continentes
        self.m.fillcontinents(color='k')

    def new_map_pyrenees(self, res='h'):
        """Creation of a map of the Pyrenees.
        :param res: Resolucion del mapa (c,l,h,f). Por defecto h - high
        :type res: char
        """
        self.m = Basemap(projection='mill', llcrnrlat=41.5, llcrnrlon=0, urcrnrlat=43, urcrnrlon=4, resolution=res)
        # Dibuja una linea en los continentes
        self.m.drawcoastlines()
        # Dibuja rios y lagos grandes
        self.m.drawrivers(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
        # Rellena los continentes
        self.m.fillcontinents(color='coral')
        # Dibuja paralelos
        parallels = np.arange(41., 44, 1.)
        self.m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
        # Dibuja meridianos
        meridians = np.arange(0., 5., 1.)
        self.m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

        # plt.legend(loc=4)
        # plt.title(title_map)

    def new_map_pyrenees_arcgisapi(self):
        """
        Creation of a map of Pyrenees ussing the arcgis API.
        """
        self.m = Basemap(llcrnrlat=42.45, llcrnrlon=0.65, urcrnrlat=42.8, urcrnrlon=1.5, epsg=5520)
        # http://server.arcgisonline.com/arcgis/rest/services
        self.m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=4000, verbose=True)

        parallels = np.arange(41., 44, 1.)
        self.m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
        # Dibuja meridianos
        meridians = np.arange(0., 5., 1.)
        self.m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    def new_map_mediterranean(self, res='h'):
        """Creation of a map of Spain
        :param res: Map resolution (c,l,h,f). Defauld, h - high
        :type res: char
        """
        self.m = Basemap(projection='mill', llcrnrlat=30, llcrnrlon=-13, urcrnrlat=47, urcrnrlon=38, resolution=res)
        # Dibuja una linea en los continentes
        self.m.drawcoastlines()
        # Dibuja rios y lagos grandes
        # self.m.drawrivers(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
        # Rellena los continentes
        self.m.fillcontinents(color='k')

    def new_map_europe(self, res='h'):
        """Creation of a map of Spain
        :param res: Map resolution (c,l,h,f). Defauld, h - high
        :type res: char
        """
        self.m = Basemap(projection='mill', llcrnrlat=30, llcrnrlon=-13, urcrnrlat=70, urcrnrlon=38, resolution=res)
        # Dibuja una linea en los continentes
        self.m.drawcoastlines()
        # Dibuja rios y lagos grandes
        # self.m.drawrivers(linewidth=0.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)
        # Rellena los continentes
        self.m.fillcontinents(color='k')

    def add_point(self, lon, lat, *arg):
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
            self.m.plot(xpt, ypt, marker='o', color=str(marker_color), markersize=7)
        elif len(arg) == 4:
            color_red = arg[0]
            color_green = arg[1]
            color_blue = arg[2]
            color_clear = arg[3]
            self.m.plot(xpt, ypt, marker='o', color=[color_red, color_green, color_blue, color_clear], markersize=7)


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
            if 'sal_qc' in data_keys:
                self.data.ix[self.data['sal_qc'] != 1, 'sal'] = np.nan
                self.data.ix[self.data['sal_qc'] != 1, 'sal_qc'] = 1

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
            if 'sal_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['sal']), 'sal_qc'] = 9

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
        except KeyError as keyerr:
            self.dialog = "Error: {}".format(keyerr.args)
        except ValueError as valerr:
            self.dialog = "Error: {}".format(valerr.args)

    def clear_bad_data(self):
        """
        Delete all the data with QC flags 2, 3, 4, 6 and 9
        """
        self.data.dropna(axis=0, how='any', inplace=True)
        for key in self.data.keys():
            if "_qc" in key:
                self.data = self.data[self.data[key] != 2]
                self.data = self.data[self.data[key] != 3]
                self.data = self.data[self.data[key] != 4]
                self.data = self.data[self.data[key] != 6]
                self.data = self.data[self.data[key] != 9]

    def delete_param(self, *parameters):
        """
        Delete a parameter or a list of parameters of self.data
        :param parameters: List of parameters to delete.
        """
        for parameter in parameters:
            try:
                self.data.drop(parameter, axis=1, inplace=True)
                self.data.drop(parameter + "_qc", axis=1, inplace=True)
            except KeyError:
                self.dialog = "Error: {}".format(KeyError)

    def use_only(self, *parameters):
        """
        Delete all the parameters not presented in the *parameters list.
        :param parameters: List of parameters to save.
        """
        self.dialog = False
        parameters = list(parameters)
        parameter_list = list()
        parameter_list.append('time_qc')
        for parameter in parameters:
            parameter_list.append(parameter)
            parameter_list.append(parameter+"_qc")
        try:
            self.data = self.data[parameter_list]
        except KeyError:
            self.dialog = "Error: {}".format(KeyError)

    """ Data information"""

    def info_data(self):
        """
        :return: info of the data
        :rtype: str
        """
        # Search for initial and final dates
        try:
            # Look for start and stop time
            start_time = self.data.index.min()
            stop_time = self.data.index.max()
            message = "- Start date: {}\n- End date: {}\n".format(start_time, stop_time)
            # Look for the parameters
            message += "- Parameters and QC flag stadistics: \n"
            for key in self.data.keys():
                if "_qc" in key:
                    continue

                # Look for start and end date
                valid_col = self.data[key+"_qc"].dropna()
                start = valid_col.index[0]
                end = valid_col.index[-1]

                # Write information
                message += "\t- {}, from {} to {}\n".format(key, start, end)
                # QC stadistics
                df_counts = self.data[key+"_qc"].value_counts().reset_index()
                df_counts.columns = ['col_name', 'count']
                for i in range(len(df_counts.index)):
                    message += "\t\t- {}: {:.2f} %\n".format(int(df_counts['col_name'][i]), df_counts['count'][i] /
                                                             self.data[key+"_qc"].count()*100)

        except IndexError:
            message = "Error: No good data."
        return message[:-1]

    def info_metadata(self):
        """
        Return all the metadata information in a string format.
        :return: str, metadata information.
        """
        keys = self.metadata.keys()
        message = ""
        for key in keys:
            if self.metadata[key][0] != " ":
                message += "- {}: {}\n".format(key, str(self.metadata[key][0]))
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

    def plt_qc_cmap(self):
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

    def plt_qc(self):
        """
        Graph of QC.
        :return: Figure
        """
        # Look for qc data
        qc_keys = []
        for key in self.data.keys():
            if '_qc' in key:
                qc_keys.append(key)
        # Plot
        fig_qc, axes = plt.subplots(nrows=len(qc_keys), ncols=1)
        ax_list = self.data[qc_keys].plot(ax=axes, subplots=True, drawstyle='steps-pre', ylim=(0, 10))
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
        if 'volt' in data_keys:
            fig_volt = self.plt_cudi(qc_flag)
            fig_dict['Voltage'] = fig_volt
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

    def plt_multiparam_multiplot(self, qc_flag=None, *parameter):
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


def qc(data):
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
    :param data: Data variable with the oceanobs standard.
    :return data: Data varable with the oceanobs standard.
    """

    def qc_init(data):
        """
        Start with the QC flags. Writing "0" to all flags.
        Indicate that, for the moment, no data has qc.
        :param data: Data variable with the oceanobs standard.
        :return data: Data varable with the oceanobs standard.
        """
        data['time_qc'] = 0
        data_keys = data.keys()
        if 'temp' in data_keys:
            data['temp_qc'] = 0
        if 'atemp' in data_keys:
            data['atemp_qc'] = 0
        if 'cond' in data_keys:
            data['cond_qc'] = 0
        if 'sal' in data_keys:
            data['sal_qc'] = 0
        if 'sovel' in data_keys:
            data['sovel_qc'] = 0
        if 'pres' in data_keys:
            data['pres_qc'] = 0
        if 'atm' in data_keys:
            data['atm_qc'] = 0
        if 'wis' in data_keys:
            data['wis_qc'] = 0
        if 'wid' in data_keys:
            data['wid_qc'] = 0
        if 'ph' in data_keys:
            data['ph_qc'] = 0
        if 'tur' in data_keys:
            data['tur_qc'] = 0
        if 'oxy' in data_keys:
            data['oxy_qc'] = 0
        if 'depth' in data_keys:
            data['depth_qc'] = 0
        return data

    def qc_missing_values(data):
        """
        First level of qc. Look for missing values. Writing "9" to the flag.
        :param data: Data variable with the oceanobs standard.
        :return data: Data varable with the oceanobs standard.
        """
        data_keys = data.keys()
        if 'temp_qc' in data_keys:
            data.ix[pd.isnull(data['temp']), 'temp_qc'] = 9
        if 'sal_qc' in data_keys:
            data.ix[pd.isnull(data['sal']), 'sal_qc'] = 9
        if 'cond_qc' in data_keys:
            data.ix[pd.isnull(data['cond']), 'cond_qc'] = 9
        if 'sovel_qc' in data_keys:
            data.ix[pd.isnull(data['sovel']), 'sovel_qc'] = 9
        if 'pres_qc' in data_keys:
            data.ix[pd.isnull(data['pres']), 'pres_qc'] = 9
        if 'atm_qc' in data_keys:
            data.ix[pd.isnull(data['atm']), 'atm_qc'] = 9
        if 'wis_qc' in data_keys:
            data.ix[pd.isnull(data['wisp']), 'wisp_qc'] = 9
        if 'wid_qc' in data_keys:
            data.ix[pd.isnull(data['widi']), 'widi_qc'] = 9
        if 'atemp_qc' in data_keys:
            data.ix[pd.isnull(data['atemp']), 'atemp_qc'] = 9
        if 'ph_qc' in data_keys:
            data.ix[pd.isnull(data['ph']), 'ph_qc'] = 9

        return data

    def qc_impossible_values(data):
        """
        Second level of qc. Find the data that seems erroneous. Writing "4" to the flag.
        This test applies only where conditions can be further qualified. In this case, specific ranges for
        observations from the Mediterranean (OBSEA) further restrict what are considered sensible values.
        :param data: Data variable with the oceanobs standard.
        :return data: Data varable with the oceanobs standard.
        """
        data_keys = data.keys()
        if 'time_qc' in data_keys:
            # Year greater than 2008
            data.ix[data.index < datetime.datetime(2008, 1, 1), 'time_qc'] = 4
        if 'temp_qc' in data_keys:
            # Sea Water Temperature in range 10°C to 28°C
            data.ix[data['temp'] < 10.0, 'temp_qc'] = 4
            data.ix[data['temp'] > 28.0, 'temp_qc'] = 4
        if 'sal_qc' in data_keys:
            # Salinity in range 35 to 39
            data.ix[data['sal'] < 35.0, 'sal_qc'] = 4
            data.ix[data['sal'] > 39.0, 'sal_qc'] = 4
        if 'cond_qc' in data_keys:
            # Conductivity in range 3.5S/m to 6.5S/m
            data.ix[data['cond'] < 3.5, 'cond_qc'] = 4
            data.ix[data['cond'] > 6.5, 'cond_qc'] = 4
        if 'sovel_qc' in data_keys:
            # Sound velocity in range 1480m/s to 1550m/s
            data.ix[data['sovel'] < 1480.0, 'sovel_qc'] = 4
            data.ix[data['sovel'] > 1550.0, 'sovel_qc'] = 4
        if 'pres_qc' in data_keys:
            # Pressure in range 18 dbar to 21 dbar
            data.ix[data['pres'] < 18.0, 'pres_qc'] = 4
            data.ix[data['pres'] > 21.0, 'pres_qc'] = 4
        if 'atm_qc' in data_keys:
            # Sea level air pressure in range 850hPa to 1060hPa (mbar)
            data.ix[data['atm'] < 0.850, 'atm_qc'] = 4
            data.ix[data['atm'] > 1.060, 'atm_qc'] = 4
        if 'wis_qc' in data_keys:
            # Wind speed in range 0m/s to 60m/s
            data.ix[data['wisp'] < 0.0, 'wisp_qc'] = 4
            data.ix[data['wisp'] > 60.0, 'wisp_qc'] = 4
        if 'wid_qc' in data_keys:
            # Wind Direction in range 0° to 360°
            data.ix[data['widi'] < 0.0, 'widi_qc'] = 4
            data.ix[data['widi'] > 360.0, 'widi_qc'] = 4
        if 'atemp_qc' in data_keys:
            # Air Temperature in range -10°C + 40°C
            data.ix[data['atemp'] < -10.0, 'atemp_qc'] = 4
            data.ix[data['atemp'] > 40.0, 'atemp_qc'] = 4

        return data

    def qc_spyke_test(data):
        """
        Third level of qc. Find the data that appears inconsistent with other values. Writing "2" to the flag.
        A large difference between sequential measurements, where one measurement is quite different from
        adjacent ones, is a spike in both size and gradient. The test does not consider the differences in
        depth, but assumes a sampling that adequately reproduces the temperature and salinity changes with
        depth. The algorithm is used on both the temperature and salinity instruments:
            Test value = |V2 - (V3 + V1)/2| - |(V3 ? V1) / 2|
        where V2 is the measurement being tested as a spike, and V1 and V3 are the values above and below.
        :param data: Data variable with the oceanobs standard.
        :return data: Data varable with the oceanobs standard.
        """
        def spyke_formula(v1, v2, v3):
            """
            This is the formula we have to use for the spyke test
            :param v2: Measurement being tested
            :param v1: Before measurement
            :param v3: Next measurement
            :return: Test value
            """
            test_val = np.abs(v2 - (v3 + v1) / 2) - np.abs((v3 - v1) / 2)
            return test_val

        data_keys = data.keys()
        time1 = datetime.datetime.now()
        if 'temp_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['temp_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.1°C for sampling interval of less
                # than 1 minute
                test_value = spyke_formula(data['temp'][i - 1], data['temp'][i],data['temp'][i + 1])
                # The value of the spike formula cannot be > 0.1*minute. Let's calculate the minutes between
                # the measurements
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.1*minutes:
                    data.set_value(data.index[i], 'temp_qc', 2)

        if 'cond_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['cond_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.1 for sampling interval of less
                # than 1 minute
                test_value = spyke_formula(data['cond'][i - 1], data['cond'][i], data['cond'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.1*minutes:
                    data.set_value(data.index[i], 'cond_qc', 2)
        if 'sal_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['sal_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.5 for sampling interval of less
                # than 1 minute
                test_value = spyke_formula(data['sal'][i - 1], data['sal'][i], data['sal'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.5*minutes:
                    data.set_value(data.index[i], 'sal_qc', 2)
        if 'pres_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['pres_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 1.0 for sampling interval of less
                # than 1 minute
                test_value = spyke_formula(data['pres'][i - 1], data['pres'][i], data['pres'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 1.0*minutes:
                    data.set_value(data.index[i], 'pres_qc', 2)
        if 'atm_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['atm_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 5.0 for sampling interval of less
                # than 1 minute
                test_value = spyke_formula(data['atm'][i - 1], data['atm'][i], data['atm'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 5.0*minutes:
                    data.set_value(data.index[i], 'atm_qc', 2)
        if 'atemp_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['atemp_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.2 for sampling interval of less
                # than 1 minute
                test_value = spyke_formula(data['atemp'][i - 1], data['atemp'][i], data['atemp'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.2*minutes:
                    data.set_value(data.index[i], 'atemp_qc', 2)
        return data

    def qc_gradient_test(data):
        """
        Fourth level of qc. Find the data that appears inconsistent with other values. Writing "2" to the flag.
        This test is failed when the difference between vertically adjacent measurements is too steep.
        The test does not consider the differences in depth, but assumes a sampling that adequately reproduces
        the temperature and salinity changes with depth:
            Test value = | V2 - (V3 + V1)/2 |
        where V2 is the measurement being tested as a spike, and V1 and V3 are the values above and below.
        :param data: Data variable with the oceanobs standard.
        :return data: Data varable with the oceanobs standard.
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

        data_keys = data.keys()
        if 'temp_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['temp_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.2°C for sampling interval of less
                # than 1 minute
                test_value = gradient_formula(data['temp'][i - 1], data['temp'][i], data['temp'][i + 1])
                # Calculation of the minutes
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.2*minutes:
                    # Check the next value
                    if (i + 2) <= len(data.index):
                        minutes = (data.index[i+1] - data.index[i]).total_seconds()/60
                        test_value = gradient_formula(data['temp'][i], data['temp'][i + 1], data['temp'][i + 2])
                        if test_value > 0.2*minutes:
                            # If it has an other time an error it means that it is a spyke detected with the
                            # gradient
                            data.set_value(data.index[i], 'temp_qc', 2)
                        else:
                            # If now it is ok, it means that the spyke was the previous value
                            data.set_value(data.index[i-1], 'temp_qc', 2)
                    else:
                        data.set_value(data.index[i], 'temp_qc', 2)
        if 'cond_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['cond_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.2 for sampling interval of less
                # than 1 minute
                test_value = gradient_formula(data['cond'][i - 1], data['cond'][i], data['cond'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.2*minutes:
                    # Check the next value
                    if (i + 2) <= len(data.index):
                        minutes = (data.index[i+1] - data.index[i]).total_seconds()/60
                        test_value = gradient_formula(data['cond'][i], data['cond'][i + 1], data['cond'][i + 2])
                        if test_value > 0.2*minutes:
                            # If it has an other time an error it means that it is a spyke detected with the
                            # gradient
                            data.set_value(data.index[i], 'cond_qc', 2)
                        else:
                            # If now it is ok, it means that the spyke was the previous value
                            data.set_value(data.index[i-1], 'cond_qc', 2)
                    else:
                        data.set_value(data.index[i], 'cond_qc', 2)
        if 'sal_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['sal_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 1 for sampling interval of less
                # than 1 minute
                test_value = gradient_formula(data['sal'][i - 1], data['sal'][i], data['sal'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 1.0*minutes:
                    # Check the next value
                    if (i + 2) <= len(data.index):
                        minutes = (data.index[i+1] - data.index[i]).total_seconds()/60
                        test_value = gradient_formula(data['sal'][i], data['sal'][i + 1], data['sal'][i + 2])
                        if test_value > 1.0*minutes:
                            # If it has an other time an error it means that it is a spyke detected with the
                            # gradient
                            data.set_value(data.index[i], 'sal_qc', 2)
                        else:
                            # If now it is ok, it means that the spyke was the previous value
                            data.set_value(data.index[i-1], 'sal_qc', 2)
                    else:
                        data.set_value(data.index[i], 'sal_qc', 2)
        if 'pres_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['pres_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 2.0 for sampling interval of less
                # than 1 minute
                test_value = gradient_formula(data['pres'][i - 1], data['pres'][i], data['pres'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 2.0*minutes:
                    # Check the next value
                    if (i + 2) <= len(data.index):
                        minutes = (data.index[i+1] - data.index[i]).total_seconds()/60
                        test_value = gradient_formula(data['pres'][i], data['pres'][i + 1], data['pres'][i + 2])
                        if test_value > 2.0*minutes:
                            # If it has an other time an error it means that it is a spyke detected with the
                            # gradient
                            data.set_value(data.index[i], 'pres_qc', 2)
                        else:
                            # If now it is ok, it means that the spyke was the previous value
                            data.set_value(data.index[i-1], 'pres_qc', 2)
                    else:
                        data.set_value(data.index[i], 'pres_qc', 2)
        if 'atm_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['atm_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 10.0 for sampling interval of less
                # than 1 minute
                test_value = gradient_formula(data['atm'][i - 1], data['atm'][i], data['atm'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 10.0*minutes:
                    # Check the next value
                    if (i + 2) <= len(data.index):
                        minutes = (data.index[i+1] - data.index[i]).total_seconds()/60
                        test_value = gradient_formula(data['atm'][i], data['atm'][i + 1], data['atm'][i + 2])
                        if test_value > 10.0*minutes:
                            # If it has an other time an error it means that it is a spyke detected with the
                            # gradient
                            data.set_value(data.index[i], 'atm_qc', 2)
                        else:
                            # If now it is ok, it means that the spyke was the previous value
                            data.set_value(data.index[i-1], 'atm_qc', 2)
                    else:
                        data.set_value(data.index[i], 'atm_qc', 2)
        if 'atemp_qc' in data_keys:
            for i in range(len(data.index)):
                if i == 0 or i == len(data.index) - 1 or data['atemp_qc'][i] == 4:
                    continue
                # Value appears inconsistent when the test value exceeds 0.4 for sampling interval of less
                # than 1 minute
                test_value = gradient_formula(data['atemp'][i - 1], data['atemp'][i], data['atemp'][i + 1])
                minutes = (data.index[i] - data.index[i - 1]).total_seconds()/60
                if test_value > 0.4*minutes:
                    # Check the next value
                    if (i + 2) <= len(data.index):
                        minutes = (data.index[i+1] - data.index[i]).total_seconds()/60
                        test_value = gradient_formula(data['atemp'][i], data['atemp'][i + 1], data['atemp'][i + 2])
                        if test_value > 0.4*minutes:
                            # If it has an other time an error it means that it is a spyke detected with the
                            # gradient
                            data.set_value(data.index[i], 'atemp_qc', 2)
                        else:
                            # If now it is ok, it means that the spyke was the previous value
                            data.set_value(data.index[i-1], 'atemp_qc', 2)
                    else:
                        data.set_value(data.index[i], 'atemp_qc', 2)
        return data

    def qc_good_data(data):
        """
        Final level of qc. Find data that seems correct. Writing "2" to the flag.
        Data was not flagged previously in "qc_impossible_values()", "qc_spyke_test()" and "qc_gradient_test()".
        :param data: Data variable with the oceanobs standard.
        :return data: Data varable with the oceanobs standard.
        """
        data_keys = data.keys()
        if 'time_qc' in data_keys:
            data.ix[data['time_qc'] == 0, 'time_qc'] = 1
        if 'temp_qc' in data_keys:
            data.ix[data['temp_qc'] == 0, 'temp_qc'] = 1
        if 'air_temp_qc' in data_keys:
            data.ix[data['air_temp_qc'] == 0, 'air_temp_qc'] = 1
        if 'cond_qc' in data_keys:
            data.ix[data['cond_qc'] == 0, 'cond_qc'] = 1
        if 'sal_qc' in data_keys:
            data.ix[data['sal_qc'] == 0, 'sal_qc'] = 1
        if 'sovel_qc' in data_keys:
            data.ix[data['sovel_qc'] == 0, 'sovel_qc'] = 1
        if 'pres_qc' in data_keys:
            data.ix[data['pres_qc'] == 0, 'pres_qc'] = 1
        if 'atm_qc' in data_keys:
            data.ix[data['atm_qc'] == 0, 'atm_qc'] = 1
        if 'wisp_qc' in data_keys:
            data.ix[data['wisp_qc'] == 0, 'wisp_qc'] = 1
        if 'widi_qc' in data_keys:
            data.ix[data['widi_qc'] == 0, 'widi_qc'] = 1
        if 'atemp_qc' in data_keys:
            data.ix[data['atemp_qc'] == 0, 'atemp_qc'] = 1
        if 'ph_qc' in data_keys:
            data.ix[data['ph_qc'] == 0, 'ph_qc'] = 1
        if 'tur_qc' in data_keys:
            data.ix[data['tur_qc'] == 0, 'tur_qc'] = 1
        if 'oxy_qc' in data_keys:
            data.ix[data['oxy_qc'] == 0, 'oxy_qc'] = 1
        if 'depth_qc' in data_keys:
            data.ix[data['depth_qc'] == 0, 'depth_qc'] = 1
        return data

    data = qc_init(data)
    data = qc_missing_values(data)
    data = qc_impossible_values(data)
    data = qc_spyke_test(data)
    data = qc_gradient_test(data)
    data = qc_good_data(data)

    return data