import pickle
import sys
import datetime
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr


class WaterFrame:
    """Object to manage data series from marine observatories.
    Its most important instance variables are the following:

    data: A pandas DataFrame that contains the measurement values of the
    timeserie.

    metadata: A dictionary that contains the metadata information of the
    timeserie."""

    def __init__(self):
        """It creates the instance following variables:
        data -- A pandas DataFrame that contains the measurement values of the
        time series.
        metadata -- A dictionary that contains the metadata information of the
        time series.
        meaning -- A dictionary that contains the meaning of the keys of data
        (i.e. "TEMP": "Sea water temperature")"""
        # Instance variables
        self.data = pd.DataFrame()
        self.metadata = dict()
        self.meaning = dict()

    def __repr__(self):
        """
        Return a string containing a printable representation of an object.
        """
        message = "Parameters: " + str(self.parameters())
        return message

    def from_netcdf(self, path):
        """Load and decode a dataset from a NetCDF file. The compatible
        netCDF files are from the mooring-buoys of
        [EMODNET](http://www.emodnet-physics.eu/Map/),
        [JERICO](http://www.jerico-ri.eu/data-access/),
        and time series with [NetCDF](http://www.oceansites.org/data/)
        format.

        Parameters
        ----------
            path: str
                Path to a netCDF file.
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
        if '.nc' in path:
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
            # We add the meaning of DEPTH
            self.meaning['DEPTH'] = {
                "long_name": "depth_of_measure",
                "units": "meters"}

            # Conversion to the dataframe
            self.data = ds.to_dataframe()

            # Set index
            self.data = self.data.reset_index().set_index('TIME')
            # self.data.sort_index()

            return True
        else:
            return False

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
        """
        pickle.dump(self.__dict__, open(path, "wb"))

    def tsplot(self, keys, rolling=None, ax=None, average_time=None,
               secondary_y=False):
        """Plot timeseries.

        Parameters
        ----------
            keys: list of str, str
                keys of self.data to plot.
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
        Returns
        -------
            ax: matplotlib.AxesSubplot
                New axes of the plot.
        """
        def make_plot(df_in, ax_in, key_in):
            # Calculation of the std and the mean
            roll = df_in[key_in].rolling(rolling, center=True)
            m = roll.agg(['mean', 'std'])
            # rename 'mean' column
            m.rename(columns={'mean': key_in}, inplace=True)
            ax_out = m[key_in].plot(ax=ax_in, secondary_y=secondary_y,
                                    legend=True)
            ax_out.fill_between(m.index,
                                m[key_in] - m['std'], m[key_in] + m['std'],
                                alpha=.25)
            # Write axes
            try:
                ax_out.set_ylabel(self.meaning[key_in]['units'])
            except KeyError:
                warnings.warn("No units on y_label")

            return ax_out

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
            ax = make_plot(df, ax, key)
        elif isinstance(keys, list):
            for key in keys:
                ax = make_plot(df, ax, key)
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
            ax: matplotlib.AxesSubplot
                New axes of the plot.
        """
        # Remove duplicate keys
        keys = list(set(keys))
        if len(keys) > 1:
            # Extract data
            df = self.data[keys]
            ax = pd.plotting.scatter_matrix(df, diagonal='kde', ax=ax)
            return ax

    def qcplot(self, key, ax=None):
        """
        Plot the timeserie with dots of different colours according to the QC
        Flag.

        Parameters
        ----------
            key: str
                key of self.data to plot.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
        Returns
        -------
            ax: matplotlib.AxesSubplot
                New axes of the plot.
        """
        # Extract data
        df = self.data[
            [key, key+'_QC']].dropna().reset_index().set_index('TIME')
        df.index.rename("Date", inplace=True)
        # Sometimes Depth is on the df
        if "DEPTH" in df.keys():
            del df['DEPTH']
        # Create a dataframe divided with flags
        for flag in range(0, 10):
            df_ = pd.DataFrame()
            df_['{}'.format(flag)] = df.ix[df[key+'_QC'] == flag, key]
            if df_.index.size > 0:
                # Change line style -> Maybe not necessary
                '''
                if flag == 1:
                    line = '-'
                else:
                    line = ""
                '''
                line = ""
                ax = df_.plot(ax=ax, marker='.', linestyle=line)
        ax.set_ylabel(self.meaning[key]['units'])
        ax.legend(title="QC Flags")

        return ax

    def qcbarplot(self, key="all", ax=None):
        """
        Bar plot with the count of values with a  '_QC' in the keys of
        self.data.

        Parameters
        ----------
            key: str or list of str, optional (key = "all")
                keys of self.data to plot.
            ax: matplotlib.axes object, optional (ax = None)
                It is used to add the plot to an input axes object.
        Returns
        -------
            ax: matplotlib.AxesSubplot
                New axes of the plot.
        """
        if key == "all":
            # Creation of dataframe with the count information
            key_list = []
            values_list = []
            for key_qc in self.data.keys():
                if 'TIME' in key_qc:
                    continue
                if '_QC' in key_qc:
                    key_list.append(key_qc[:-3])
                    values_list.append(pd.value_counts(self.data[key_qc]))

            df = pd.DataFrame(values_list, key_list)
            # Creation of the plot
            ax = df.sort_index().plot.bar(ax=ax)
            # Set labels
            ax.set_ylabel("Number of measurements")
            ax.legend(title="QC Flags")
        else:
            # Obtain the key with QC
            key_qc = key + "_QC"
            # Create the graph
            ax = pd.value_counts(
                self.data[key_qc]).sort_index().plot.bar(ax=ax)
            # Set labels
            ax.set_ylabel("Number of measurements")
            ax.set_xlabel("QC flag")

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

    def spike_test(self, key, window=0, threshold=3, flag=4):
        """
        It detects spikes in a timeserie.

        Parameters
        ----------
            key: str
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
            outlier_idx: numpy array
                Array with the flags result of the test."""

        # Auto calculation of window
        if window == 0:
            window = int(len(self.data[key])/100)
            if window < 3:
                window = 3
            elif window > 100:
                window = 100

        signals = self.data[
            key].rolling(window=window,
                         center=True).mean().fillna(method='bfill')
        difference = np.abs(self.data[key] - signals)
        outlier_idx = difference > threshold
        self.data.ix[outlier_idx, key+'_QC'] = flag

        return outlier_idx

    def range_test(self, key, flag=4):
        """
        Check impossible values of a parameter.
        Parameters
        ----------
            key: str
                key of self.data to apply the test.
            flag: int, optional (flag = 4)
                Flag value to write in on the fail values.
        Returns
        -------
            True/False: bool
                It indicates if the process was successfully."""
        ranges = {
            'ATMP': [600, 1500],  # atmospheric pressure at altitude
            'ATMS': [0, 2000],  # Atmospheric pressure at sea level
            'CHLT': [0, 30],  # total chlorophyll
            'CNDC': [0, 30],  # electrical conductivity
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

        if key in ranges.keys():
            self.data.ix[self.data[key] < ranges[key][0], key+'_QC'] = flag
            self.data.ix[self.data[key] > ranges[key][1], key + '_QC'] = flag
            return True
        else:
            return False

    def flat_test(self, key, window=1, flag=4):
        """
        It detects no changes in values of time-series.

        Parameters
        ----------
            key: str
                key of self.data to apply the test.
            window: int, optional (window = 1)
                Size of the moving window of values to calculate the mean.
                If it is 0, the function calculates the optimal window.
            flag: int, optional (flag = 4)
                Flag value to write in on the fail values.
        Returns
        -------
            signals: numpy array
                Array with the flags result of the test."""
        if window == 0:
            window = 1
        if window > 0:
            signals = []
            for i in range(len(self.data[key])):
                try:
                    if self.data[key][i] - self.data[key][i-window] == 0:
                        signals.append(True)
                    else:
                        signals.append(False)
                except IndexError:
                    signals.append(False)

            self.data.ix[signals, key + '_QC'] = flag

            return signals
        else:
            return False

    def flag2flag(self, key, original_flag=0, translated_flag=1):
        """
        It changes the flags of the key, from original_flag to translated_flag.

        Parameters
        ----------
            key: str
                key of self.data to apply the test.
            original_flag: int, optional (original_flag = 0)
                Flag number to translate.
            translated_flag: int, optional (translated_flag = 1)
                Translation of the original flag number."""
        self.data[key+'_QC'].replace(original_flag, translated_flag,
                                     inplace=True)

    def reset_flag(self, key, flag=0):
        """
        It changes all the flags of the key to the input flag value.

        Parameters
        ----------
            key: str
                key of self.data to apply the test.
            flag: int, optional (flag = 0)
                Flag value to write.
        """
        for i in range(10):
            self.data[key + '_QC'].replace(i, flag, inplace=True)

    def qc(self, key, window=3, threshold=3, bad_flag=4, good_flag=1):
        """
        Auto QC process.

        Parameters
        ----------
            key: str
                key of self.data to apply the test.
            window: int, optional (window = 0)
                Size of the moving window of values to calculate the mean.
                If it is 0, the function calculates the optimal window.
            threshold: int, optional (threshold = 3)
                The z-score at which the algorithm signals.
            bad_flag: int, optional (flag = 4)
                Flag value to write in on the fail values.
            good_flag: int, optional (flag = 1)
                Flag value to write in on the good values."""
        self.range_test(key=key, flag=bad_flag)
        self.spike_test(key=key, window=window, threshold=threshold,
                        flag=bad_flag)
        self.flat_test(key=key, window=window, flag=bad_flag)
        self.flag2flag(key=key, original_flag=0, translated_flag=good_flag)

        self.flag2flag(key=key)

    def drop(self, keys, flags=None):
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
        return True

    def rename(self, old_name, new_name):
        """
        It renames keys of self.data.

        Parameters
        ----------
            old_name: str
                key name to change.
            new_name: str
                New name of the key."""
        self.data.rename(columns={old_name: new_name}, inplace=True)
        self.data.rename(columns={old_name+'_QC': new_name+'_QC'},
                         inplace=True)
        self.meaning[new_name] = self.meaning.pop(old_name)

    def concat(self, waterframe):
        """
        The concat function does all of the heavy lifting of performing
        concatenation operations along an axis while performing optional set
        logic (union or intersection) of the indexes on the other axes.

        Parameters
        ----------
            waterframe: WaterFrame
                WaterFrame object to concat to self
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

    def slice_time(self, start, end):
        """
        Delete data outside the time interval.

        Parameters
        ----------
            start: str, timestamp
                Start time interval with format 'YYYYMMDDhhmmss' or timestamp.
            end: str, timestamp
                End time interval with format 'YYYYMMDDhhmmss' or timestamp.
        """
        if isinstance(self.data.index, pd.core.index.MultiIndex):
            # Sometimes, you have multiindex TIME and DEPTH
            self.data.reset_index(inplace=True)
            self.data.set_index('TIME', inplace=True)

        self.data.sort_index(inplace=True)
        datetime_start = datetime.datetime.strptime(start, '%Y%m%d%H%M%S')
        datetime_end = datetime.datetime.strptime(end, '%Y%m%d%H%M%S')
            
        start_slice = self.data.index.searchsorted(datetime_start)
        end_slice = self.data.index.searchsorted(datetime_end)
        self.data = self.data.ix[start_slice:end_slice]

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

    def use_only(self, parameters, flags=None, dropnan=False):
        """
        Drop all parameters not presented in the input list with QC flags
        different than given in the input flags.

        Parameters
        ----------
            parameters: list of str, str
                Parameter to save in the WaterFrame.
            flags: list of int, int, None, optional (flags = None)
                QC Flag of the parameter to save.
            dropnan: Bool, optional (dropnan = False)
                Drop all lines of self.data that contain a nan in any of their
                columns.
        """

        if isinstance(parameters, str):
            parameters = [parameters]

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