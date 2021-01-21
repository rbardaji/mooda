""" Main implementation of the class WaterFrame """
import sys
from pandas import DataFrame


class WaterFrame:

    from .analysis import (
        min, max, copy, use_only, rename, corr, max_diff, time_intervals, resample, slice_time,
        info_metadata, info_vocabulary, drop, reduce_memory)
    from .output import to_nc, to_pkl, to_json, to_es, metadata_to_html, to_csv
    from .plot import plot_timeseries, plot_timebar, plot_hist, plot
    from .qc import qc_flat_test, qc_range_test, qc_spike_test, qc_replace, qc_syntax_test
    from .iplot import (
        iplot_location, iplot_timeseries, iplot, iplot_scatter, iplot_line,
        iplot_data_intervals)

    def __init__(self, df=None, metadata=None, vocabulary=None):
        """ Constructor """
        if df:
            self.data = df
        else:
            self.data = DataFrame()

        if metadata:
            self.metadata = metadata
        else:
            self.metadata = dict()

        if vocabulary:
            self.vocabulary = vocabulary
        else:
            self.vocabulary = dict()

    def __repr__(self):
        """ Implementation of repr """

        # Memory use message
        memory_bytes = self.memory_usage
        units = "Bytes"
        if memory_bytes > 1000000000:
            memory_bytes /= 1000000000
            units = "GBytes"
        elif memory_bytes > 1000000:
            memory_bytes /= 1000000
            units = "MBytes"
        elif memory_bytes > 1000:
            memory_bytes /= 1000
            units = "KBytes"
        size_message = f"Memory usage: {memory_bytes:.3f} {units}"

        # Parameters message
        parameters_message = "Parameters:"
        for parameter in self.parameters:
            try:
                parameters_message += f"\n  - {parameter}: " + \
                    f"{self.vocabulary[parameter]['long_name']}" + \
                    f" ({self.vocabulary[parameter]['units']})"
            except KeyError:
                parameters_message += \
                    "\n  - {}: Parameter without meaning".format(parameter)

            # Min, max and mean info
            min_dict = self.min(parameter)
            max_dict = self.max(parameter)
            value_mean = self.data[parameter].mean()
            if min_dict is not None and max_dict is not None:
                # min value string
                parameters_message += f"\n    - Min value: {min_dict[parameter]}"
                for key, value in min_dict.items():
                    if key == parameter:
                        continue
                    else:
                        parameters_message += f"\n      - {key}: {value}"
                # max value string
                parameters_message += f"\n    - Max value: {max_dict[parameter]}"
                for key, value in max_dict.items():
                    if key == parameter:
                        continue
                    else:
                        parameters_message += f"\n      - {key}: {value}"
                # mean value string
                parameters_message += f"\n    - Mean value: {value_mean}"
            else:
                parameters_message += "\n    - Parameter without values."

        message = size_message + "\n" + parameters_message

        return message

    def _repr_html_(self, *args, **kwargs):
        data_html = self.data._repr_html_()

        metadata_list = ''
        for key, value in self.metadata.items():
            metadata_list += f'<li><b>{key}</b>: {value}</li>'

        dictionary_html = f'<div><p>Metadata:</p><ul>{metadata_list}</ul><p>Data:</p></div>'
        return dictionary_html + data_html

    @property
    def parameters(self):
        """
        Get the keys of data with "QC" columns.
        """
        return_keys = []
        keys = self.data.keys()
        for key in keys:
            try:
                if "_QC" in key:
                    continue
                for key_qc in keys:
                    if "_QC" not in key_qc:
                        continue
                    if key_qc == f"{key}_QC":
                        return_keys.append(key)
            except TypeError:
                # TypeError: argument of type 'Timestamp' is not iterable
                continue
        return return_keys

    @property
    def memory_usage(self):
        """
        It returns the memory usage of the WaterFrame in bytes.
        """
        size = sys.getsizeof(self.data) + sys.getsizeof(self.metadata)
        return size

    @property
    def empty(self):
        """
        It return True if the data is empty.

        Returns
        -------
            empty: bool
        """
        empty = self.data.empty
        return empty
