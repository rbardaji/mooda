import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import os
import pandas as pd
try:
    import oceanobs.observatory as observatory
except ImportError:
    import observatory


class EMODnet(observatory.Observatory):

    def __init__(self, path=None):
        """
        Constructor of class
        :param path: Path where data is
        :type path: str
        """

        # Temporal data for the csv files
        self.path_metadata_csv = r"metadata_temp.csv"
        self.path_data_csv = r"data_temp.csv"
        # Start word of data in EMODnet csv files
        self.start_word_csv = "DATE"

        if path is not None:
            self.open(path)

    def open(self, path):
        """
        Open the nc or csv file
        :param path: Path where data is
        :type path: str
        :return: True i todo va bien, o str con el error cometido.
        """

        def open_csv(path_csv):
            """
            Open a csv file and extract data and metadata
            :param path_csv: Path fo the csv file
            :type path_csv: str
            """

            def check_qc():
                """
                I detected that sometimes the qc is not correct. With this function we are going to correct thhe qc flags
                :return:
                """
                data_keys = self.data.keys()
                if 'wahe_qc' in data_keys:
                    self.data.ix[pd.isnull(self.data['wahe']), 'wahe_qc'] = 9

            def parse(x):
                """
                Definition of format of data in csv files
                :param x:
                :return:
                """
                return dt.datetime.strptime(x, '%d/%m/%Y  %H:%M:%S')

            def data_format():
                """
                Change the actual names of the data by the standard names defined in oceanobs.
                """
                # Changing the index name
                self.data.index.rename(name='time', inplace=True)
                # Changing the name of the data
                data_keys = self.data.keys()
                for key in data_keys:
                    if 'WDIR.' in key:
                        self.data.rename(columns={key: 'widi'}, inplace=True)
                    if 'ATMS.' in key:
                        self.data.rename(columns={key: 'atm'}, inplace=True)
                    if 'WSPD.' in key:
                        self.data.rename(columns={key: 'wisp'}, inplace=True)
                    if 'VDIR.' in key:
                        self.data.rename(columns={key: 'wadi'}, inplace=True)
                    if 'VTZA.' in key:
                        self.data.rename(columns={key: 'wape'}, inplace=True)
                    if 'DRYT.' in key:
                        self.data.rename(columns={key: 'atemp'}, inplace=True)
                    if 'VTDH.' in key:
                        self.data.rename(columns={key: 'wahe'}, inplace=True)
                    if 'WDIR_QC' in key:
                        self.data.rename(columns={key: 'widi_qc'}, inplace=True)
                    if 'ATMS_QC' in key:
                        self.data.rename(columns={key: 'atm_qc'}, inplace=True)
                    if 'WSPD_QC' in key:
                        self.data.rename(columns={key: 'wisp_qc'}, inplace=True)
                    if 'VDIR_QC' in key:
                        self.data.rename(columns={key: 'wadi_qc'}, inplace=True)
                    if 'VTZA_QC' in key:
                        self.data.rename(columns={key: 'wape_qc'}, inplace=True)
                    if 'DRYT_QC' in key:
                        self.data.rename(columns={key: 'atemp_qc'}, inplace=True)
                    if 'VTDH_QC' in key:
                        self.data.rename(columns={key: 'wahe_qc'}, inplace=True)
                    if 'TIME_QC' in key:
                        self.data.rename(columns={key: 'time_qc'}, inplace=True)
                    if 'POSITION_QC' in key:
                        self.data.rename(columns={key: 'position_qc'}, inplace=True)
                    if '_DM' in key:
                        self.data.drop(key, axis=1, inplace=True)
                        continue
                    if 'DEPH' in key:
                        self.data.drop(key, axis=1, inplace=True)

            def create_metadata():
                """
                Create the metadata dataframe.
                """
                # Extrat metadata information
                bad_metadata = pd.read_csv(self.path_metadata_csv, sep=';', index_col=0, header=None)
                # Creation of the metadata dataframe
                self.metadata = pd.DataFrame({'platform_code': bad_metadata.loc['PLATFORM CODE', [1]],
                                              'wmo_platform_code': bad_metadata.loc['WMO PLATFORM CODE', [1]],
                                              'institution': bad_metadata.loc['INSTITUTION', [1]],
                                              'type': bad_metadata.loc['DATA TYPE', [1]]})
                # We reset the index
                self.metadata.reset_index(drop=True, inplace=True)

            # The EMODNet csv files have 2 tables. One with metadada an another with data.
            # First, we are going to split the csv file to have a file for each table.
            try:
                f_csv = open(path_csv)
            except FileNotFoundError as error:
                self.dialog = error
                return
            f_metadata = open(self.path_metadata_csv, "w")
            f_data = open(self.path_data_csv, "w")
            metadata = True
            for line in f_csv:
                # Change the "," to "." of the files.
                line = line.replace(",", ".")
                # Delete the no usefull part of the metadata file
                line = line.replace("; \n", "\n")
                if line.startswith(self.start_word_csv):
                    # No more metadata, here start the data table
                    metadata = False
                    f_metadata.close()
                if metadata:
                    f_metadata.write(line)
                else:
                    f_data.write(line)
            f_data.close()

            # Metadata creation
            create_metadata()
            # Extract data
            self.data = pd.read_csv(self.path_data_csv, sep=';', parse_dates=[['DATE', ' TIME']], index_col=0,
                                    date_parser=parse)
            # Convert data to numeric
            self.data = self.data.apply(pd.to_numeric, args=('coerce',))
            # Formating data with the oceanobs standard names
            data_format()
            # Check the qc
            check_qc()
            # Delete temporal files
            os.remove(self.path_metadata_csv)
            os.remove(self.path_data_csv)

        def open_nc(path_nc):
            """
            Open a nc file and extract metadata and data
            :param path_nc: Path of the nc file
            :type path_nc: str
            """
            try:
                # Open nc file
                df_nc = nc.Dataset(path_nc)
                # Creation of the metadata dataframe
                parameters = ['platform_code', 'WMO PLATFORM CODE', 'INSTITUTION', 'DATA ASSEMBLY CENTER', 'DATA TYPE']
                values = [df_nc.platform_code, df_nc.wmo_platform_code, df_nc.institution, df_nc.data_assembly_center,
                          df_nc.data_type]
                self.metadata = pd.DataFrame({'platform_code': df_nc.platform_code,
                                              'wmo_platform_code': df_nc.wmo_platform_code,
                                              'institution': df_nc.institution,
                                              'type': [df_nc.data_type]})
                # Creation of the data dataframe
                # The time is the index
                times = df_nc.variables['TIME']
                jd = nc.num2date(times[:], times.units)
                df_dict = {
                    'wahe': df_nc['VTDH'][:][:, 0],
                    'wape': df_nc['VTZA'][:][:, 0],
                    'wadi': df_nc['VDIR'][:][:, 0],
                    'atm': df_nc['ATMS'][:][:, 0],
                    'atemp': df_nc['DRYT'][:][:, 0],
                    'wisp': df_nc['WSPD'][:][:, 0],
                    'widi': df_nc['WDIR'][:][:, 0],
                    'wahe_qc': df_nc['VTDH_QC'][:][:, 0],
                    'wape_qc': df_nc['VTZA_QC'][:][:, 0],
                    'wadi_qc': df_nc['VDIR_QC'][:][:, 0],
                    'atm_qc': df_nc['ATMS_QC'][:][:, 0],
                    'atemp_qc': df_nc['DRYT_QC'][:][:, 0],
                    'wisp_qc': df_nc['WSPD_QC'][:][:, 0],
                    'widi_qc': df_nc['WDIR_QC'][:][:, 0],
                    'time_qc': df_nc['TIME_QC'][:]}
                self.data = pd.DataFrame(df_dict, index=jd)
            except OSError as error:
                self.dialog = error

        def listdir_fullpath(d):
            return [os.path.join(d, f) for f in os.listdir(d)]

        def open_list(path_list):
            big_data = pd.DataFrame()
            for one_path in path_list:
                if os.path.isfile(path):
                    _one_filename, one_file_extension = os.path.splitext(one_path)
                    if one_file_extension == ".csv":
                        self.open_csv(one_path)
                    elif one_file_extension == ".nc":
                        open_nc(one_path)
                    else:
                        self.dialog = "Error: {} is no EMODnet data.".format(path)
                        continue
                    big_data = pd.concat([big_data, self.data])
            self.data = big_data
            # Copy of the data for future resets
            self.data_original = self.data.copy()

        self.dialog = False
        if isinstance(path, str):
            # Know if path is a file or a directory
            if os.path.isfile(path):
                # Path is a file
                # Know if it is a csv or a nc
                _filename, file_extension = os.path.splitext(path)
                if file_extension == ".csv":
                    open_csv(path)
                elif file_extension == ".nc":
                    open_nc(path)
            elif os.path.isdir(path):
                # Path is a directory
                path_lst = listdir_fullpath(path)
                open_list(path_lst)
            else:
                self.dialog = "Error: {} is not exists.".format(path)
        elif isinstance(path, list):
            open_list(path)

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
            tutorial = "Descarrega les dades de "
        return tutorial

if __name__ == '__main__':
    import sys
    from matplotlib import style
    style.use('ggplot')

    print("Ejemplo clase EMODnet")

    # Path de datos
    # CSV
    # path_data = \
    #     r"C:\Users\rbard\OneDrive\Code\Python\Pruebas Mooda\CSV_61196\IR_LATEST_TS_MO_61196_20160729-formatted.csv"
    # Netcdf
    path_data = r"C:\Users\raul\SkyDrive\Code\Python\Pruebas Mooda\NetCDF_61196\IR_LATEST_TS_MO_61196_20160729.nc"
    print("Path de datos: {}".format(path_data))

    print("Loading data, please wait.")
    ob = EMODnet(path_data)
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

    # print("Resampling weekly frequency.")
    # ob.resample_data('W')
    # if ob.dialog:
    #     print(ob.dialog)
    #     sys.exit()
    # else:
    #     print("Done.")

    # Plots
    # print("Making plots.")
    # ob.plt_all()
    # ob.plt_qc()
    # print("Done.")

    # Slicing
    # print("Slicing.")
    # start = '20160729010000'
    # stop = '20160729090000'
    # print("Start: {}/{}/{} {}:{}:{}, Stop: {}/{}/{} {}:{}:{}".format(start[:4], start[4:6], start[6:8], start[8:10],
    #                                                                  start[10:12],  start[12:], stop[:4], stop[4:6],
    #                                                                  stop[6:8], stop[8:10], stop[10:12],  stop[12:]))
    # ob.slicing(start, stop)
    # print("Done.")

    print(ob.data)
    # print(ob.info_data())
    # print(ob.how_to_download_data())

    plt.show()
