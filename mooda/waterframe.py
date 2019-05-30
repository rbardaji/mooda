"""It just contains the WaterFrame class"""
# pylint: disable=C0103, too-many-lines
import copy
import io
import pickle
import sys
import datetime
import warnings
import json
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd


class WaterFrame:
    """Object to manage data series from marine observatories.
    Its most important instance variables are the following:

    data: A pandas DataFrame that contains the measurement values of the
    timeserie.

    metadata: A dictionary that contains the metadata information of the
    timeserie."""

    def __init__(self, path=None, df=None, metadata=None, meaning=None):
        """It creates the instance following variables:
        data -- A pandas DataFrame that contains the measurement values of the
        time series.
        metadata -- A dictionary that contains the metadata information of the
        time series.
        meaning -- A dictionary that contains the meaning of the keys of data
        (i.e. "TEMP": "Sea water temperature")

        Parameters
        ----------
            path: str, optional
                Create a WaterFrame with the data of the file of the path.
                The file must be a NetCDF, a CSV or a JSON string
            df: pandas Dataframe
                pandas DataFrame
            metadata: dict
                Metadata dictionary
            meaning: dict
                Meaning dictionary
        """
        # Instance variables
        self.data = pd.DataFrame()
        self.metadata = dict()
        self.meaning = dict()

        if metadata is not None:
            self.metadata = metadata
        if meaning is not None:
            self.meaning = meaning
        if df is not None:
            self.from_dataframe(df)
        if path:
            done = self.from_json(path)
            if not done:
                parts = path.split(".")
                if parts[-1] == "nc":
                    # It is a NetCDF file
                    self.from_netcdf(path)
                if parts[-1] == "csv":
                    # It is a CSV file
                    self.from_csv(path)

        # Check if data is multiindex and change to single index
        if isinstance(self.data.index, pd.core.index.MultiIndex):
            try:
                self.data.reset_index(inplace=True)
                self.data.set_index('TIME', inplace=True)
                # self.data.index = pd.to_datetime(self.data.index)
                self.data.sort_index(inplace=True)
            except Exception as e:
                pass

    def __repr__(self):
        """
        Return a string containing a printable representation of an object.
        """
        parameters = "Parameters: {}".format((", ").join(self.parameters()))

        # Memory use message
        memory_usage = self.memory_usage()
        units = "Bytes"
        if memory_usage > 1000000000:
            memory_usage /= 1000000000
            units = "GBytes"
        elif memory_usage > 1000000:
            memory_usage /= 1000000
            units = "MBytes"
        elif memory_usage > 1000:
            memory_usage /= 1000
            units = "KBytes"
        size_message = "Memory usage: {:.2f} {}".format(memory_usage, units)

        qc_values = self.info_qc()

        # Parameters message
        parameters = self.parameters()
        if not parameters:
            parameters_message = "There is no data."
        else:
            parameters_message = "Parameters:"
            for parameter in parameters:
                try:
                    parameters_message += "\n  - {}: {} ({})".format(
                        parameter, self.meaning[parameter]["long_name"],
                        self.meaning[parameter]["units"])
                except KeyError:
                    parameters_message += \
                        "\n  - {}: Parameter without meaning".format(parameter)

                # Min, max and mean info
                date_min, value_min = self.min(parameter)
                date_max, value_max = self.max(parameter)
                value_mean = self.mean(parameter)
                parameters_message += "\n    - Min value: {:.3f}".format(
                    value_min)
                parameters_message += "\n    - {} min value: {}".format(
                    self.data.index.name, date_min)
                parameters_message += "\n    - Max value: {:.3f}".format(
                    value_max)
                parameters_message += "\n    - {} max value: {}".format(
                    self.data.index.name, date_max)
                parameters_message += "\n    - Mean value: {:.3f}".format(
                    value_mean)

                # Percentage of data with QC Flag = 1
                # Calculation of the total of the vales
                total_values = 0
                for _qc_flags, counts in qc_values[parameter].items():
                    total_values += counts
                # Calculation of the percentage
                percentage = 0
                if 1.0 in qc_values[parameter]:
                    percentage = qc_values[parameter][1.0]/total_values*100
                parameters_message += \
                    "\n    - Values with QC = 1: {:.3f} %".format(percentage)

        message = size_message + "\n\n" + parameters_message

        return message

    def from_netcdf(self, path):
        """Load and decode a dataset from a NetCDF file. The compatible
        netCDF files are from the mooring-buoys of
        [EMODNET](http://www.emodnet-physics.eu/Map/),
        [JERICO](http://www.jerico-ri.eu/data-access/),
        [EMSO](http://emso.eu)
        and time series with [NetCDF](http://www.oceansites.org/data/)
        format.

        Parameters
        ----------
            path: str, obj
                Path to a netCDF file or an OpenDAP URL.
                File-like objects are opened with scipy.io.netcdf
                 (onlynetCDF3 supported).
        Returns
        -------
            True/False: Bool
                It indicates if the procedure was successful."""
        def drop(ds_in):
            """Drop some parameters of the dataset.

            Parameters
            ----------
                ds_in: xarray.Dataset
                    Input dataset.
            Returns
            -------
                ds_out: xarray.Dataset
                    Output dataset"""
            # Creation of a list with the variables to drop. We are going to
            # drop all variables with a "_DM" in the key name.
            vars2drop = []
            for k in ds_in.variables.keys():
                if '_DM' in k:
                    vars2drop.append(k)

            # Dropping the previous list and some other variables
            ds_out = ds_in.drop(vars2drop)
            if 'POSITIONING_SYSTEM' in ds_in.variables.keys():
                ds_out = ds_out.drop('POSITIONING_SYSTEM')
            if 'DC_REFERENCE' in ds_in.variables.keys():
                ds_out = ds_out.drop('DC_REFERENCE')
            if 'LATITUDE' in ds_in.variables.keys():
                ds_out = ds_out.drop('LATITUDE')
            if 'LONGITUDE' in ds_in.variables.keys():
                ds_out = ds_out.drop('LONGITUDE')
            if 'POSITION_QC' in ds_in.variables.keys():
                ds_out = ds_out.drop('POSITION_QC')
            if 'DEPH' in ds_in.variables.keys():
                ds_out = ds_out.drop('DEPH')
            if 'DEPH_QC' in ds_in.variables.keys():
                ds_out = ds_out.drop('DEPH_QC')

            return ds_out

        # Check if path contanins a ".nc" file and then, complete the process
        if (isinstance(path, str) and '.nc' in path) or isinstance(path, io.BytesIO):
            # Convert the nc to a xarray dataset
            ds = xr.open_dataset(path)
            # Save metadata
            self.metadata = dict(ds.attrs)
            # Delete not used vars
            ds = drop(ds)
            # Save the meanings
            for variable in ds.variables:
                if '_QC' in variable:
                    continue
                else:
                    self.meaning[variable] = dict(ds[variable].attrs)
                    # Conversion to all strings
                    for key, value in self.meaning[variable].items():
                        self.meaning[variable][key] = str(value)

            # We add the meaning of DEPTH
            self.meaning['DEPTH'] = {
                "long_name": "depth_of_measure",
                "units": "meters"}

            # Conversion to the dataframe
            self.data = ds.to_dataframe()

            # Set index
            # self.data = self.data.reset_index().set_index('TIME')
            # self.data.sort_index()

            return True
        else:
            return False

    def to_netcdf(self, path):
        """
        It creates a netCDF3 file.

        Parameters
        ----------
            path: str,
                Path to a netCDF file to save.

        Returns
        -------
            True: bool
                It indicates that the process was successfully completed.
        """
        # Sometimes the metadata contains a list of str
        # It can crash the creation of the NetCDF3_64Bits.
        # We are going to change the list of str to str
        metadata_netcdf = self.metadata.copy()
        for key, value in metadata_netcdf.items():
            if isinstance(value, list):
                metadata_netcdf[key] = ', '.join(value)

        # Creation of an xarray dataset
        ds = xr.Dataset(data_vars=self.data, attrs=metadata_netcdf)
        for key in self.parameters():
            ds[key].attrs = self.meaning[key]

        # Creation of the nc file
        ds.to_netcdf(path, format="NETCDF3_64BIT")

        return True

    def from_csv(self, path, metadata=None, meaning=None, **kwds):
        """
        It reads data from a CSV file.

        It uses the pandas.read_csv(). All parameters of read_csv() can be input here.

        Parameters
        ----------
            path: str
                Path of the CSV file.
            metadata: dict
                Metadata dictionary.
            meaning: dict
                Meaning dictionary.
            **kwds: arguments
                All arguments of pandas.read_csv()

        Return
        ------
            True: bool
                Operation successful.
        """
        if metadata is not None:
            self.metadata = metadata
        if meaning is not None:
            self.meaning = meaning

        df = pd.read_csv(path, **kwds)

        self.from_dataframe(df)

        return True

    def from_pickle(self, path):
        """
        Load and decode a WaterFrame object from a pickle file.

        Parameters
        ----------
            path: str
                Path to a pickle file.
        Returns
        -------
            True/False; Bool
                It indicates if the procedure was successful."""
        # Check if path contanins a ".pkl" file and then, complete the process
        if '.pkl' in path:
            temp_dict = pickle.load(open(path, "rb"))
            self.__dict__.clear()
            self.__dict__.update(temp_dict)
            return True
        else:
            return False

    def to_pickle(self, path):
        """It creates a pickle (serialize) file of the WaterFrame.

        Parameters
        ----------
            path: str
                Path to save the pickle file.

        Returns
            True: bool
                If the file is created, it returns True.
        """
        pickle.dump(self.__dict__, open(path, "wb"))

        return True

    def from_dataframe(self, df, metadata=None, meaning=None):
        """
        It creates save the input pandas DataFrame into the WaterFrame.

        Parameters
        ----------
            df: pandas DataFrame
                pandas DataFrame
            metadata : dict
                Metadata information.
            meaning: dict
                Parameter meanings.

        Return
        ------
            True: bool
                Operation successful.
        """
        # Save metadata
        if metadata is not None:
            self.metadata = metadata

        # Save meaning
        if meaning is not None:
            self.meaning = meaning

        # Save df
        self.data = df.copy()
        # Adding QC keys
        df_keys = list(df.keys())
        wf_keys = list(self.data.keys())
        for key in df_keys:
            if "{}_QC".format(key) not in wf_keys:
                self.data["{}_QC".format(key)] = 0

        return True

    def to_csv(self, path):
        """
        It saves the Waterframe data and metadata into a CSV file.

        Parameters
        ----------
            path: str
                Path to save the csv file.

        Returns
        -------
            True/False: bool
                It indicates if the process was successful
        """
        # Create the file
        csv_file = open(path, 'w')

        # Save the metadata
        csv_file.write("#Global attributes;Value\n")
        for key, val in self.metadata.items():
            if isinstance(val, list):
                try:
                    value = ', '.join(val)
                except TypeError:
                    # It happens with data from Pangea
                    # with the "event" key, that it is a list of dict
                    value = ""
            else:
                value = val
            csv_file.write("# ")
            csv_file.write(key)
            csv_file.write(';="')
            csv_file.write(value)
            csv_file.write('"\n')

        # Add three empty lines
        csv_file.write("\n\n\n")

        # Save the data
        self.data.to_csv(csv_file, sep=";", header=True)

        # Close the file
        csv_file.close()

        return True

    def tsplot(self, keys=None, rolling=None, ax=None, average_time=None,
               secondary_y=False, color=None):
        """Plot timeseries.

        Parameters
        ----------
            keys: list of str, str, optional (keys = None)
                keys of self.data to plot. If keys is None, all parameters
                will be ploted.
            rolling: int, optional (rolling = None)
                Size of the moving window. It is the number of observations
                used for calculating the statistic.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
            average_time: str, optional (average_time = None)
                It calculates an average value of a time interval. You can find
                all of the resample options here:
                http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
            secondary_y: bool, optional (secondary_y = False)
                Plot on the secondary y-axis.
            color: str or list of str, optional (color = None)
                Any matplotlib color. It will be applied to the traces.
        Returns
        -------
            ax: matplotlib.AxesSubplot
                New axes of the plot.
        """
        def make_plot(df_in, ax_in, key_in, color_in):
            # Calculation of the std and the mean
            roll = df_in[key_in].rolling(rolling, center=True)
            m = roll.agg(['mean', 'std'])
            # rename 'mean' column
            m.rename(columns={'mean': key_in}, inplace=True)
            ax_out = m[key_in].plot(ax=ax_in, secondary_y=secondary_y,
                                    legend=True, color=color_in)
            ax_out.fill_between(m.index,
                                m[key_in] - m['std'], m[key_in] + m['std'],
                                alpha=.25, color=color_in)
            # Write axes
            try:
                ax_out.set_ylabel(self.meaning[key_in]['units'])
            except KeyError:
                warnings.warn("No units on y_label")

            return ax_out

        # Check keys
        if keys is None:
            keys = self.parameters()

        # Extract data
        df = self.data[keys].dropna().reset_index().set_index('TIME')
        df.index.rename("Date", inplace=True)

        # Resample data
        if average_time is None:
            pass
        else:
            df = df.resample(average_time).mean()

        # Calculation of the rolling value
        if rolling is None:
            if df.size <= 100:
                rolling = 1
            elif df.size <= 1000:
                rolling = df.size//10
            elif df.size <= 10000:
                rolling = df.size // 100
            else:
                rolling = df.size // 1000

        if isinstance(keys, str):
            key = keys
            ax = make_plot(df, ax, key, color)
        elif isinstance(keys, list):
            if color is None:
                for key in keys:
                    ax = make_plot(df, ax, key, color)
            else:
                for key, color_line in zip(keys, color):
                    ax = make_plot(df, ax, key, color_line)
        return ax

    def barplot(self, key, ax=None, average_time=None):
        """Bar Plot.

        Parameters
        ----------
            key: list of str
                keys of self.data to plot.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
            average_time: str, optional (average_time = None)
                It calculates an average value of a time interval. You can find
                all of the resample options here:
                http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        Returns
        -------
            ax: matplotlib.AxesSubplot
                New axes of the plot.
        """
        def format_year(x):
            return datetime.datetime.\
                strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y')

        # Extract data
        df = self.data[key].dropna().reset_index().set_index('TIME')
        df.index.rename("Date", inplace=True)

        # Resample data
        if average_time is None:
            pass
        else:
            df = df.resample(average_time).mean()

        if isinstance(key, list):
            ax = df[key].plot.bar(ax=ax, legend=True)
        else:
            ax = df[key].plot.bar(ax=ax)
            # Write axes
            try:
                ax.set_ylabel(self.meaning[key]['units'])
            except KeyError:
                print("Warning: We don't know the units of", key,
                      "Please, add info into self.meaning[", key, "['units']")

            if average_time == 'A':
                ax.set_xticklabels([format_year(x.get_text())
                                    for x in ax.get_xticklabels()])

        return ax

    def hist(self, parameter=None, mean_line=False, **kwds):
        """Make a histogram of the WaterFrame's.

        A histogram is a representation of the distribution of data.
        This function calls DataFrame.hist(), on each parameter of the
        WaterFrame, resulting in one histogram per parameter.

        Parameters
        ----------
            parameter: str, list of str, optional (parameter=None)
                keys of self.data to plot. If parameter=None, it will plot all
                parameters.
            mean_line: bool, optional (mean_line=False)
                 It draws a line representing the average of the dataset.
            **kwds:
                All other plotting keyword arguments to be passed to
                DataFrame.hist().
                https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.hist.html
        Returns
        -------
            axes: matplotlib.AxesSubplot or numpy.ndarray of them
                New axes of the plot.
        """
        if parameter is None:
            parameter = self.parameters()

        if isinstance(parameter, str):
            parameter = [parameter]

        axes = self.data.hist(column=parameter, **kwds)
        parameter_counter = 0
        try:
            for ax in axes:
                ax.set_xlabel("Values")
                ax.set_ylabel("Frequency")
                if mean_line is True:
                    if parameter_counter < len(parameter):
                        x_mean = self.mean(parameter[parameter_counter])
                        ax.axvline(x_mean, color='k',
                                   linestyle='dashed',
                                   linewidth=1)

                        parameter_counter += 1
        except AttributeError:

            # Creation of the mean line
            parameter_counter = 0
            for irow in range(len(axes)):
                for icol in range(len(axes[irow])):
                    if parameter_counter < len(parameter):
                        axes[irow, icol].set_xlabel("Values")
                        axes[irow, icol].set_ylabel("Frequency")
                        if mean_line is True:
                            x_mean = self.mean(axes[irow, icol].get_title())
                            axes[irow, icol].axvline(x_mean, color='k',
                                                     linestyle='dashed',
                                                     linewidth=1)
                        parameter_counter += 1

        return axes

    def scatter_matrix(self, keys, ax=None):
        """
        Draw a matrix of scatter plots.

        Parameters
        ----------
            key: list of str
                keys of self.data to plot.
                Keys must contain different words.
                ex:
                    keys = ['VAVH', 'VCMX'] is ok.
                    keys = ['VAVH', 'VAVH'] is not ok.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.

        Returns
        -------
            ax: matplotlib.AxesSubplot or False
                New axes of the plot.
                It returns False if operation is not successful.
        """
        if isinstance(keys, list):
            # Remove duplicate keys
            keys = list(set(keys))
            if len(keys) > 1:
                # Extract data
                df = self.data[keys]
                ax = pd.plotting.scatter_matrix(df, diagonal='kde', ax=ax)
                return ax
            else:
                return False
        else:
            return False

    def qcplot(self, parameters=None, ax=None):
        """
        Plot the timeserie with dots of different colours according to the QC
        Flag.

        Parameters
        ----------
            parameters: string or list of strings, optional
            (parameters = None)
                key of self.data to apply the test.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
        Returns
        -------
            ax: matplotlib.AxesSubplot or False
                New axes of the plot. It returns False if the operation was
                not successful.
        """
        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        for parameter in parameters:
            if "_QC" in parameter:
                return False
            else:
                # Extract data
                df = self.data[
                    [parameter, parameter+'_QC']].dropna().reset_index().set_index('TIME')
                df.index.rename("Date", inplace=True)
                # Sometimes Depth is on the df
                if "DEPTH" in df.keys():
                    del df['DEPTH']
                # Create a dataframe divided with flags
                for flag in range(0, 10):
                    df_ = pd.DataFrame()
                    df_['{}'.format(flag)] = df.ix[df[parameter+'_QC'] == flag, parameter]
                    if df_.index.size > 0:
                        # Change line style -> Maybe not necessary
                        line = ""
                        ax = df_.plot(ax=ax, marker='.', linestyle=line)
                ax.set_ylabel(self.meaning[parameter]['units'])
                ax.legend(title="QC Flags")

        return ax

    def qcbarplot(self, parameters=None, ax=None):
        """
        Bar plot with the count of values with a  '_QC' in the keys of
        self.data.

        Parameters
        ----------
            parameters: string or list of strings, optional
            (parameters = None)
                key of self.data to apply the test.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
        Returns
        -------
            ax: matplotlib.AxesSubplot or False
                New axes of the plot. It returns False if the operation was
                not successful.
        """
        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        key_list = []  # List of parameter names
        values_list = []  # List of counters of each flag
        for parameter in parameters:
            if "_QC" in parameter:
                return False
            else:
                key_list.append(parameter)
                values_list.append(pd.value_counts(self.data[parameter+"_QC"]))

            # Obtain the different values of QC
            qc_values = []
            for value in values_list:
                for key in value.keys():
                    if key not in qc_values:
                        qc_values.append(key)

            # Creation of a dataframe with the count info
            df = pd.DataFrame(values_list, key_list)
            # Creation of the plot
            ax = df.sort_index().plot.bar(ax=ax, legend=False)
            # Set labels
        ax.set_ylabel("Number of measurements")
        #  TODO: Bug on labels
        ax.legend(title="QC Flags", labels=qc_values)

        return ax

    def spectroplot(self):
        """
        It plots the spectrometer of the acoustic data.

        Returns
        -------
            matplotlib.Figure
                New axes of the plot.
        """

        # Prepare data
        time = self.data.index
        wavelength = []
        values = []
        for key in self.data.keys():
            try:
                wavelength.append(float(key))
                values.append(self.data[key].values)
            except ValueError:
                pass

        # Creation of figure
        return plt.pcolormesh(time, wavelength, values)

    def profileplot(self, parameter_y, parameter_x=None, ax=None,):
        """
        It creates a graph a profile plot.
        Y-axes suppose to be a depth related parameter.

        Parameters
        ----------
            parameter_y: str
                y-axes parameter.
            parameters_x: list of str, str (optional,
            parameters_x = None)
                x-axes parameter.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
        Returns
        -------
            ax_out: matplotlib.AxesSubplot
                New axes of the plot.
        """

        # Check the type of parameter_x
        if isinstance(parameter_x, str):
            parameter_x = [parameter_x]

        # Extract data
        parameter_y = [parameter_y]
        keys = parameter_y + parameter_x
        df = self.data[keys].dropna().reset_index().set_index('TIME')
        df.index.rename("Date", inplace=True)

        ax_out = df.plot.scatter(x=parameter_x[0], y=parameter_y[0], ax=ax)

        if len(parameter_x) == 1:
            ax_out.set_xlabel("{} ({})".format(self.meaning[parameter_x[0]]['long_name'],
                                               self.meaning[parameter_x[0]]['units']))
        ax_out.set_ylabel("{} ({})".format(self.meaning[parameter_y[0]]['long_name'],
                                           self.meaning[parameter_y[0]]['units']))

        ax_out.invert_yaxis()
        ax_out.ticklabel_format(useOffset=False)
        # ax_out.legend().set_visible(False)
        ax_out.set_title('Profile Plot')

        return ax_out

    def spike_test(self, parameters=None, window=0, threshold=3, flag=4):
        """
        It checks if there is any spike in the time series.

        Parameters
        ----------
            parameters: string or list of strings, optional
            (parameters = None)
                key of self.data to apply the test.
            window: int, optional (window = 0)
                Size of the moving window of values to calculate the mean.
                If it is 0, the function calculates the optimal window.
            threshold: int, optional (threshold = 3)
                The z-score at which the algorithm signals.
            flag: int, optional (flag = 4)
                Flag value to write in on the fail values.

        Returns
        -------
            True/False: bool
                It indicates if the process is (not) successful.
        """

        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        for parameter in parameters:
            # Auto calculation of window
            if window == 0:
                window = int(len(self.data[parameter])/100)
                if window < 3:
                    window = 3
                elif window > 100:
                    window = 100

            signals = self.data[
                parameter].rolling(window=window, center=True).mean().fillna(method='bfill')
            difference = np.abs(self.data[parameter] - signals)
            outlier_idx = difference > threshold
            self.data.ix[outlier_idx, parameter + '_QC'] = flag

        return True

    def peak_test(self):
        """
        https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/43512887#43512887
        """
        pass

    def range_test(self, parameters=None, flag=4, limits=None):
        """
        Check if the values of a parameter are out of range.

        Parameters
        ----------
            parameters: string or list of strings, optional
            (parameters = None)
                key of self.data to apply the test.
            flag: int, optional (flag = 4)
                Flag value to write in on the fail values.
            limits: tuple, optional (range = None)
                (Min value, max value) of the range of correct values.

        Returns
        -------
            True/False: bool
                It indicates if the process is (not) successful.
        """
        ranges = {
            'ATMP': [600, 1500],  # atmospheric pressure at altitude
            'ATMS': [0, 2000],  # Atmospheric pressure at sea level
            'CHLT': [0, 30],  # total chlorophyll
            'CNDC': [0, 30],  # electrical conductivity
            'DRYT': [-20, 60],  # air temperature at sea level
            'GSPD': [0, 40],  # gust wind speed
            'HCDT': [0, 360],  # current to direction relative true north
            'HEAD': [0, 360],  # PLAT. HEADING REL. TRUE NORTH
            'LINC': [0, 3000],  # long-wave incoming radiation
            'LW': [0, 50],  # Downwelling vector radiance as energy
            'OSAT': [0, 200],  # oxygen saturation
            'PHPH': [0, 14],  # ph
            'PRES': [0, 500],  # sea pressure
            'PRRT': [0, 200],  # hourly precipitation rate
            'PSAL': [0, 40],  # practical salinity
            'RDIN': [0, 1100],  # incident radiation
            'SVEL': [130, 180000],  # sound velocity
            'SWDR': [0, 360],  # SWELL DIRECTION REL TRUE N.
            'SWHT': [0, 50],  # SWELL HEIGHT
            'SWPR': [0, 20],  # SWELL PERIOD
            'TEMP': [0, 50],  # Sea temperature
            'VAVH': [0, 20],  # AVER. HEIGHT HIGHEST 1/3 WAVE
            'VAVT': [0, 20],  # AVER. PERIOD HIGHEST 1/3 WAVE
            'VCMX': [0, 20],  # MAX CREST TROUGH WAVE HEIGHT
            'VDIR': [0, 360],  # wave direction rel. true north
            'VEPK': [0, 100],  # WAVE SPECTRUM PEAK ENERGY
            'VHM0': [0, 20],  # SPECTRAL SIGNIFICANT WAVE HEIGHT
            'VMDR': [0, 360],  # Mean wave direction
            'VPED': [0, 360],  # dir. spreading at wave peak
            'VPSP': [0, 360],  # dir. spreading at wave peak
            'VSMC': [0, 20],  # SPECTUM MOMENT(0, 2) WAVE PERIOD
            'VTDH': [0, 40],  # significant wave height
            'VTM02': [0, 13],  # Spectral moments (0, 2) wave period (Tm02)
            'VTPK': [0, 40],  # WAVE SPECTRUM PEAK PERIOD
            'VTZA': [0, 40],  # AVER ZERO CROSSING WAVE PERIOD
            'VTZM': [0, 40],  # period of the highest wave
            'VZMX': [0, 20],  # Maximum zero crossing wave height
            'WDIR': [0, 360],  # Wind from direction relative true north
            'WSPD': [0, 50],  # Horizontal wind speed
        }

        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        for parameter in parameters:
            if limits:
                self.data.ix[self.data[parameter] < limits[0], parameter + '_QC'] = flag
                self.data.ix[self.data[parameter] > limits[1], parameter + '_QC'] = flag
            elif parameter in ranges.keys():
                self.data.ix[self.data[parameter] < ranges[parameter][0], parameter + '_QC'] = flag
                self.data.ix[self.data[parameter] > ranges[parameter][1], parameter + '_QC'] = flag
        return True

    def flat_test(self, parameters=None, window=2, flag=4):
        """
        It detects if there are equal consecutive values in the time series.

        Parameters
        ----------
            parameters: string or list of strings, optional
            (parameters = None)
                key of self.data to apply the test.
            window: int, optional (window = 1)
                Size of the moving window of values to calculate the mean.
                If it is 0, the function calculates the optimal window.
            flag: int, optional (flag = 4)
                Flag value to write in on the fail values.

        Returns
        -------
            True/False: bool
                It indicates if the process is (not) successful.
        """
        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        if window == 0:
            window = 2
        if window > 0:
            df = self.data.rolling(window).std()

        for parameter in parameters:
            if '_QC' in parameter:
                return False
            else:
                self.data.ix[df[parameter] == 0, parameter + '_QC'] = flag
        return True

    def flag2flag(self, parameters=None, original_flag=0, translated_flag=1):
        """
        It changes the flags of the key, from original_flag to translated_flag.

        Parameters
        ----------
            parameters: string, list of strings optional
            (parameters = None)
                Key of self.data to apply the test.
            original_flag: int, optional (original_flag = 0)
                Flag number to translate.
            translated_flag: int, optional (translated_flag = 1)
                Translation of the original flag number.

        Returns
        -------
            True/False: bool
                The operation is (not) successful.
        """
        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        for parameter in parameters:
            if '_QC' in parameter:
                return False
            self.data[parameter+'_QC'].replace(original_flag, translated_flag,
                                               inplace=True)

    def reset_flag(self, parameters=None, flag=0):
        """
        It sets the flag values of the parameter to "flag".

        Parameters
        ----------
            parameters: string, list of strings optional
            (parameters = None)
                Key of self.data to apply the test.
            flag: int, optional (flag = 0)
                Flag value to write.

        Returns
        -------
            True/False: bool
                The operation is (not) successful.
        """
        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        for parameter in parameters:
            if parameter in self.parameters():
                self.data[parameter + '_QC'] = flag
            else:
                return False
        return True

    def qc(self, parameters=None, window=0, threshold=3, bad_flag=4, good_flag=1):
        """
        Auto QC process.

        Parameters
        ----------
            parameters: string, list of strings optional
            (parameters = None)
                Key of self.data to apply the test.
            window: int, optional (window = 0)
                Size of the moving window of values to calculate the mean.
                If it is 0, the function calculates the optimal window.
            threshold: int, optional (threshold = 3)
                The z-score at which the algorithm signals.
            bad_flag: int, optional (flag = 4)
                Flag value to write in on the fail values.
            good_flag: int, optional (flag = 1)
                Flag value to write in on the good values.

        Returns
        -------
            True/False: bool
                The operation is (not) successful.
        """

        if parameters is None:
            parameters = self.parameters()
        elif isinstance(parameters, str):
            parameters = [parameters]
        elif isinstance(parameters, list):
            pass
        else:
            return False

        self.reset_flag(parameters)
        self.range_test(parameters, flag=bad_flag)
        self.spike_test(parameters, window=window, threshold=threshold, flag=bad_flag)
        self.flat_test(parameters, window=window, flag=bad_flag)
        answer = self.flag2flag(parameters, translated_flag=good_flag)

        return answer

    def value2nan(self, parameters=None, flags=4):
        """
        It changes the values of the parameters to NaN depending on the input flag.

        Parameters
        ----------
        parameters: string, list of strings optional
            (parameters = None)
            Key of self.data to apply the test.
        flags: int, list of int, optional (flag = 4)
            Flags of the value to change.
        """
        if parameters is None:
            parameters = self.parameters()
        if isinstance(flags, int):
            flags = [flags]
        
        for parameter in parameters:
            for flag in flags:
                self.data.ix[self.data[parameter + "_QC"] == flag, parameter] = np.NaN
                self.data.ix[self.data[parameter + "_QC"] == flag, parameter + '_QC'] = np.NaN
    
    def info_qc(self):
        """
        It returns a dictionary with the count and percentage of the QC flag.

        Return
        ------
            qc_dict: dict
                {NAME OF THE PARAMETER: {QC FLAG: int}}
        """
        qc_dict = {}
        for parameter in self.parameters():
            info = self.data[parameter+"_QC"].value_counts().to_dict()
            qc_dict[parameter] = info

        return qc_dict

    def drop(self, keys=None, flags=None):
        """
        Remove required keys (and associated QC keys) from self.data requested
        axis removed.

        Parameters
        ----------
            keys: str, list of str
                keys of self.data to drop.
            flags: list of int, int, None, optional (flags = None)
                Number of flag to drop. It can be None, int or a list of int.
                If it is None, column will be deleted.
        Returns
        -------
            True/False: bool
                It indicates that the process was successful."""
        # Look for QC keys and append to "keys"
        keys_qc = []
        if keys is None:
            keys = self.parameters()
        if isinstance(keys, str):
            key_qc = keys + "_QC"
            keys_qc.append(key_qc)
            # Cast keys (str) to list
            keys = [keys]
            keys += keys_qc
        elif isinstance(keys, list):
            for key in keys:
                # Check if key+"_QC" exists in self.data
                if key + "_QC" in self.data.keys():
                    keys_qc.append(key+"_QC")
            keys += keys_qc
        # Drop
        if flags is None:
            self.data.drop(keys, axis=1, inplace=True)
        else:
            # If it is an Int, cast to list
            if isinstance(flags, int):
                flags = [flags]
            for key_qc in keys_qc:
                for flag in flags:
                    try:
                        self.data.drop(
                            self.data[self.data[key_qc] == flag].index,
                            inplace=True)
                    except KeyError:
                        # No data with this QC
                        pass
                    except TypeError:
                        # Possible: TypeError, 'NoneType' object is not iterable
                        # No values with this QC
                        pass
        return True

    def rename(self, old_name, new_name):
        """
        It renames keys of self.data.

        Parameters
        ----------
            old_name: str
                key name to change.
            new_name: str
                New name of the key.

        Returns
        -------
            True: bool
                The operation is successful.

        """
        self.data.rename(columns={old_name: new_name}, inplace=True)
        self.data.rename(columns={old_name+'_QC': new_name+'_QC'},
                         inplace=True)
        try:
            self.meaning[new_name] = self.meaning.pop(old_name)
            return True
        except KeyError:
            warnings.warn("Parameter without meaning")

    def concat(self, waterframe):
        """
        The concat function does all of the heavy lifting of performing
        concatenation operations along an axis while performing optional set
        logic (union or intersection) of the indexes on the other axes.

        Parameters
        ----------
            waterframe: WaterFrame
                WaterFrame object to concat to self

        Returns
        -------
            True: bool
                The operation is successful.
        """
        if self.data.index.size > 0:
            # Check if keys of waterframes contain the same name
            keys_self = self.data.keys()
            keys_new = waterframe.data.keys()
            for key in keys_new:
                if '_QC' in key:
                    continue
                if key in keys_self:
                    # It is a repeated key

                    # Look for number of copy
                    copy_number = 1
                    saved_number = 0
                    for key_self in keys_self:
                        if '_QC' in key_self:
                            continue
                        if '{}(NEW'.format(key) in key_self:
                            saved_number = int(
                                key_self.split("(NEW")[1].split(")")[0])
                            saved_number += 1
                    if saved_number > copy_number:
                        copy_number = saved_number

                    # Rename the new waterframe
                    waterframe.rename(key,
                                      "{}(NEW{})".format(key, copy_number))
                    keys_new += ['{}(SN{})'.format(key, copy_number)]

            # Delete duplicated indexes
            self.data = self.data.loc[
                ~self.data.index.duplicated(keep='first')]
            waterframe.data = waterframe.data.loc[
                ~waterframe.data.index.duplicated(keep='first')]

            # Concat dataframes
            frames = [self.data, waterframe.data]
            self.data = pd.concat(frames, axis=1)

            # Merge dictionaries
            self.meaning = {**self.meaning, **waterframe.meaning}
            # Merge of metadata
            for key in waterframe.metadata.keys():
                if key in self.metadata.keys():
                    if waterframe.metadata[key] == self.metadata[key]:
                        # Skip if we already have the metadata.
                        continue
                    else:
                        # Merge the two values of metadata.
                        self.metadata[key] += ", {}".format(
                            waterframe.metadata[key])

        else:
            self.data = waterframe.data.copy()
            self.meaning = waterframe.meaning.copy()
            self.metadata = waterframe.metadata.copy()

        return True

    def resample(self, rule, method='mean'):
        """
        Convenience method for frequency conversion and sampling of
        time series of the WaterFrame object.

        Parameters
        ----------
            rule: str
                The offset string or object representing target conversion.
                You can find all of the resample options here:
                http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
            method: "mean", "max", "min", optional, (method = "mean")
                Save the new value with the mean(), max() or min() function.

        Returns
        -------
            True/False: bool
                It indicates that the process was successful.
        """
        # It only can be possible if the dataframe only contain 1 index.
        if len(self.data.index.names) == 1:
            if method == "mean":
                self.data = self.data.resample(rule).mean()
            elif method == "max":
                self.data = self.data.resample(rule).max()
            elif method == "min":
                self.data = self.data.resample(rule).min()
            # Change "_QC" values to 0
            for key in self.data.keys():
                if "_QC" in key:
                    self.data[key] = 0
            return True
        else:
            return False

    def slice_time(self, start=None, end=None):
        """
        Delete data outside the time interval.

        Parameters
        ----------
            start: str, timestamp, optional (start=None)
                Start time interval with format 'YYYYMMDDhhmmss' or timestamp.
            end: str, timestamp, optional (end=None)
                End time interval with format 'YYYYMMDDhhmmss' or timestamp.

        Returns
        -------
            True: bool
                The operation is successful.

        """
        if isinstance(self.data.index, pd.core.index.MultiIndex):
            # Sometimes, you have multiindex TIME and DEPTH
            self.data.reset_index(inplace=True)
            self.data.set_index('TIME', inplace=True)

        self.data.sort_index(inplace=True)

        if start is None:
            datetime_end = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')
            end_slice = self.data.index.searchsorted(datetime_end)
            self.data = self.data.ix[:end_slice]

        if end is None:
            datetime_start = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
            start_slice = self.data.index.searchsorted(datetime_start)
            self.data = self.data.ix[start_slice:]

        if start is not None and end is not None:
            datetime_start = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
            start_slice = self.data.index.searchsorted(datetime_start)
            datetime_end = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')
            end_slice = self.data.index.searchsorted(datetime_end)
            self.data = self.data.ix[start_slice:end_slice]

        return True

    def clear(self):
        """
        It delete all data and metadata of the waterframe.
        """
        self.data = pd.DataFrame()
        self.metadata = dict()
        self.meaning = dict()

    def memory_usage(self):
        """
        Memory usage of the WaterFrame.

        Returns
        -------
            size: int
                Number of bytes in use.
        """
        size = sys.getsizeof(self.data) + sys.getsizeof(self.metadata)
        return size

    def parameters(self):
        """
        It return the parameter list used in this WaterFrame.
        The parameters are the keys of self.data without "_QC".

        Returns
        -------
            parameter_list: list of str
                Parameters used in the WaterFrame.
        """

        parameter_list = [key for key in self.data.keys()
                          if "_QC" not in key
                          if key+"_QC" in self.data.keys()]

        return parameter_list

    def use_only(self, parameters=None, flags=None, dropnan=False):
        """
        Drop all parameters not presented in the input list with QC flags
        different than given in the input flags.

        Parameters
        ----------
            parameters: list of str, str, optional (parameters = None)
                Parameter to save in the WaterFrame.
            flags: list of int, int, None, optional (flags = None)
                QC Flag of the parameter to save.
            dropnan: Bool, optional (dropnan = False)
                Drop all lines of self.data that contain a nan in any of their
                columns.

        Returns
        -------
            True/False: bool
                The operations is successful.

        """

        if parameters is None:
            parameters = self.parameters()

        if isinstance(parameters, str):
            parameters = [parameters]

        # Check if parameters exist
        for parameter in parameters:
            if parameter not in self.parameters():
                warnings.warn("Parameter not found.")
                return False

        # Calculation of parameters to drop
        drop_parameters = [drop_param for drop_param in self.parameters()
                           if drop_param not in parameters]

        if drop_parameters:
            self.drop(keys=drop_parameters)
        if flags:
            if isinstance(flags, int):
                flags = [flags]
            # Calculation of flags to drop
            drop_flags = [i for i in range(10) if i not in flags]
            self.drop(keys=parameters, flags=drop_flags)
        if dropnan:
            self.data.dropna(inplace=True)

        return True

    def corr(self, parameter1, parameter2, method='pearson', min_periods=1):
        """
        Compute pairwise correlation of data columns of parameter1 and
        parameter2, excluding NA/null values.

        Parameters
        ----------
            parameter1: str
                Key name of the column 1 to correlate.
            parameter2: str
                Key name of the column 2 to correlate.
            method: {‘pearson’, ‘kendall’, ‘spearman’}
                pearson : standard correlation coefficient
                kendall : Kendall Tau correlation coefficient
                spearman : Spearman rank correlation
            min_periods : int, optional
                Minimum number of observations required per pair of columns to
                have a valid result. Currently only available for pearson and
                spearman correlation
        Returns
        -------
            correlation_number: float
        """
        correlation_number = self.data[
            parameter1].corr(self.data[parameter2], method=method,
                             min_periods=min_periods)
        return correlation_number

    def max_diff(self, parameter1, parameter2):
        """
        Calculation the maximum difference between values of two parameters.

        Parameters
        ----------
            parameter1: str
                Key name of the column 1 to calculate the difference.
            parameter2: str
                Key name of the column 2 to calculate the difference.
        Returns
        -------
            (where, value): Pandas DataFrame Index, float
                It returns the position (index) and value of the maximum
                difference.
        """

        where = (self.data[parameter1] - self.data[parameter2]).abs().idxmax()
        value = (self.data[parameter1] - self.data[parameter2]).abs().max()

        return (where, value)

    def datetime_intervals(self, parameter):
        """
        It returns the index (TIME) of intervals between NaNs.

        Parameters
        ----------
            parameter: str
                Parameter to check.

        Returns
        -------
            intervals: [(str, str)]
                List of tuples with the start and end time of each interval of
                data.
        """
        # Creation of a timeseries with the positions of null values
        ts = self.data[parameter].isnull()

        # Check where are the intervals
        intervals = []
        in_interval = False
        for index, value in ts.items():
            if in_interval is False and value is False:
                in_interval = True
                start = index.strftime('%Y-%m-%d %H:%M:%S')
            if in_interval is True and value is True:
                in_interval = False
                end = index.strftime('%Y-%m-%d %H:%M:%S')
                intervals.append((start, end))

        return intervals

    def mean(self, parameter):
        """
        It returns the mean value of a parameter.

        Parameters
        ----------
            parameter: str
                Parameter to calculate the mean.

        Returns
        -------
            mean_value:
                Mean of values of the parameter.
        """

        mean_value = self.data[parameter].mean()

        return mean_value

    def max(self, parameter):
        """
        It returns the max value of a parameter.

        Parameters
        ----------
            parameter: str
                Parameter to calculate the mean.

        Returns
        -------
            (where, max_value): (str, float)
                (Index of the max value of the parameter, Max values of the
                parameter)
        """

        where = self.data[parameter].idxmax()
        max_value = self.data[parameter].max()

        return (where, max_value)

    def min(self, parameter):
        """
        It returns the min value of a parameter.

        Parameters
        ----------
            parameter: str
                Parameter to calculate the mean.

        Returns
        -------
            (where, min_value): (str, float)
                (Index of the minimum value, Min values of the parameter).
        """
        where = self.data[parameter].idxmin()
        min_value = self.data[parameter].min()

        return (where, min_value)

    def copy(self):
        """
        It creates a copy of self

        Returns
        -------
            c: WaterFrame
                Copy of self.
        """
        c = copy.deepcopy(self)
        return c

    def info_metadata(self, keys=None):
        """
        It returns a string with the metadata information.

        Parameters
        ----------
            keys: string or list of strings (optional)
                The return message will contain the information of the input keys.
                If keys is None, all keys will be added to the return message.

        Returns
        -------
            message: string
                Message with the metadata information.
        """

        if keys is None:
            keys = self.metadata.keys()

        message = ""
        for key, value in self.metadata.items():
            if key in keys and str(value).strip() != "":
                message += "  - {}: {}\n".format(key, value)

        return message[:-1]

    def info_meaning(self, keys=None):
        """
        It returns a string with the meanings information.

        Parameters
        ----------
            keys: string or list of strings (optional)
                The return message will contain the information of the input keys.
                If keys is None, all keys will be added to the return message.

        Returns
        -------
            message: string
                Message with the meanings information.
        """

        if keys is None:
            keys = self.meaning.keys()

        message = ""
        for key, meaning_dict in self.meaning.items():
            if key in keys:
                message += "  - {}\n".format(key)
                for meaning_key, meaning_value in meaning_dict.items():
                    if meaning_value.strip() != "":
                        message += "    - {}: {}\n".format(meaning_key, meaning_value)

        return message[:-1]

    def __setitem__(self, key, data):
        """
        Set the value of *data* at *key* of *WaterFrame.data*.

        Parameters
        ----------
        key: string or list of string
            Key of DataFrame *WaterFrame.data*.
        data: any
            Values to be placed into WaterFrame.data[key].
        """
        self.data[key] = data

    def __getitem__(self, key):
        """
        Get the values of *WaterFrame.data[key]*.

        Parameters
        ----------
        key: string or list of string
            Key of DataFrame *WaterFrame.data*.
        """
        return self.data[key]

    def plot(self, **kwds):
        """
        It calls the pandas DataFrame.plot() method.

        Parameters
        ----------
            **kwds: arguments
                pandas plot() arguments.

        Returns
        -------
            axes : matplotlib.axes.Axes or numpy.ndarray of them
        """
        axes = self.data.plot(**kwds)

        return axes

    def get_coordinates(self):
        """
        It returns the minimum and maximum coordinates placed in the metadata.

        Returns
        -------
            coordinates: tuple of tuples
                ((minimum latitude, minimum longitude, minimum depth),
                 (maximum latitude, maximum longitude, maximum depth))
        """
        min_lat = None
        min_lon = None
        max_lat = None
        max_lon = None
        min_depth = None
        max_depth = None

        metadata_keys = self.metadata.keys()
        if "geospatial_lat_min" in metadata_keys:
            min_lat = self.metadata["geospatial_lat_min"]
        if "geospatial_lat_max" in metadata_keys:
            max_lat = self.metadata["geospatial_lat_max"]
        if "geospatial_vertical_min" in metadata_keys:
            min_depth = self.metadata["geospatial_vertical_min"]
        if "geospatial_vertical_max" in metadata_keys:
            max_depth = self.metadata["geospatial_vertical_max"]
        if "geospatial_lon_max" in metadata_keys:
            min_lon = self.metadata["geospatial_lon_max"]
        if "geospatial_lon_max" in metadata_keys:
            max_lon = self.metadata["geospatial_lon_max"]

        coordinates = ((min_lat, min_lon, min_depth), (max_lat, max_lon, max_depth))

        return coordinates

    def to_json(self):
        """
        It creates a JSON string with the WaterFrame information.

        Returns
        -------
            json_string: str
                JSON string.
        """

        big_dict = {
            "metadata": self.metadata,
            "meaning": self.meaning,
            "data": self.data.to_json()
        }

        json_string = json.dumps(big_dict)

        return json_string

    def from_json(self, json_string):
        """
        It loads a WaterFrame object from a JSON string.

        Parameters
        ----------
            json_string: str
                String that contains a JSON.

        Returns
        -------
            done: bool
                True if the operation is successful.
        """

        done = False
        try:
            big_dict = json.loads(json_string)

            keys = big_dict.keys()
            if "metadata" in keys:
                self.metadata = big_dict["metadata"].copy()
            if "meaning" in keys:
                self.meaning = big_dict["meaning"].copy()
            if "data" in keys:
                self.data = pd.read_json(big_dict["data"])
            else:
                self.data = pd.read_json(big_dict)

            done = True
        except ValueError:
            pass
        return done

    def __getattr__(self, key):
        """
        Get values from *self.metadata[key]*.

        Parameters
        ----------
            key: str
                key of self.metadata

        Returns
        -------
            value:
                Value of self.metadata
        """
        if key.startswith('__'):
            raise AttributeError(key)

        value = self.metadata[key]

        return value

    def empty(self):
        """
        It return True if the dataframe is empty.

        Returns
        -------
            empty: bool
        """
        empty = self.data.empty
        return empty
