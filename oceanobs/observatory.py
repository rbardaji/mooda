import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Observatory:
    """
    Texto explicativo de la clase.
    """

    def __init__(self):
        """
        Constructor of class
        :param path: Path where data is
        :type path: str
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
        :param start_time: start time of the slice with format 'YYYYMMDDHHmmss'
        :type start_time: str
        :param end_time: end time of the slice with format 'YYYYMMDDHHmmss'
        """
        self.data = self.data[start_time:end_time]

    def resample_data(self, how_often):
        """
        Delmamos los datos calculando la media
        :param how_often: Cuanto queremos delmar (Mirar la info de abajo)
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

        def resample_qc():
            data_keys = self.data.keys()
            if 'atm_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['atm']), 'atm_qc'] = 8
            if 'wisp_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['wisp']), 'wisp_qc'] = 8
            if 'widi_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['widi']), 'widi_qc'] = 8
            if 'atemp_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['atemp']), 'atemp_qc'] = 8
            if 'wape_qc' in data_keys:
                self.data.ix[pd.isnull(self.data['wape']), 'wape_qc'] = 8

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

    """ Data information"""

    def info_data(self):
        """
        Obte alguna informacio de les dades que s'estan utilitzant.
        :return: info de data
        :rtype: str
        """
        # Search for initial and final dates
        try:
            start_time = self.data.first_valid_index()
            stop_time = self.data.last_valid_index()
            message = "start time: {}\nstop time: {}".format(start_time, stop_time)
        except IndexError:
            message = "Error: No good data."
        return message

    """ Plot functions """

    def plt_cond(self, qc_flag=None):
        """
        Conductivity vs time plot
        :param qc_flag: It indicates the flag number of the data, you want to plot
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
        Sea temperature vs time plot
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
        Air temperature plot
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
        Pressure vs time plot
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
        Atmospheric pressure vs time plot
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
        Salinity vs time plot
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
        Grafica T-S
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
        Sound velocity vs time plot
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
        Grafica de CO2 i temps
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
        Wind speed vs time plot
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
        Wind direction vs time plot
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
        QC plot
        :return: Figure
        """
        # Creation of the matrix
        index_names = []
        matrix = []
        data_keys = self.data.keys()
        for key in data_keys:
            if 'qc' in key:
                index_names.append(key)
                matrix.append(self.data[key])
        # Creation of the figure
        fig_qc, axes = plt.subplots(nrows=1, ncols=1)
        cax = axes.matshow(matrix)
        # fig_qc.colorbar(cax)
        axes.set_yticklabels(['']+index_names)
        axes.grid('off')

        return fig_qc

    def plt_wadi(self, qc_flag=None):
        """
        Wave direction vs time plot
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
        Wave period vs time plot
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure
        """
        self.dialog = False
        fig_wape, axes = plt.subplots(nrows=1, ncols=1)
        try:
            if qc_flag is None:
                (self.data['wape']).plot(ax=axes)
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
        Wave height plot
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
        Atmospheric pressure at sea level
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
        Observed dea level
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
        Rain acumulation
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
            self.dialog = "Error: No rain acumulation data."
        except TypeError:
            self.dialog = "Error: No rain acumulation data with quality control flag = {}.".format(qc_flag)
        axes.set_title('Precipitation rate')
        axes.set_ylabel('mm')
        axes.set_xlabel('Time UTC')
        return fig_prec

    def plt_relhu(self, qc_flag=None):
        """
        Relative humidity
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
        Gust wind speed
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
        Gust wind speed
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
        Gust wind speed
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
        Create all the possible plots
        :param qc_flag: It indicates the flag number of the data, you want to plot
        :return: Figure dict
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

        return fig_dict
