""" Module to access to Pangea (https://www.pangaea.de/)
Adaptation of code from https://github.com/huberrob/panpython by Robert Huber and Markus Stocker
"""
import warnings
from xml.etree import ElementTree
import io
import re
import requests
import pandas as pd
from mooda import WaterFrame


class Pangaea:
    """ Main class of the module"""

    def __init__(self, id_data=None):
        """
        Constructor

        Parameters
        ----------
            id_data: int
                Id of the datasource.
        """
        self.id = 0  # pylint: disable=C0103
        self.data = None

        if id_data is None:
            self.metadata = dict()
            self.data = pd.DataFrame()
        else:
            if isinstance(id_data, int):
                self.id = id_data
            else:
                raise TypeError('id_data must be an integer.')

            # Add metadata to self.metadata
            self.metadata = self.get_metadata(self.id)

            # Add data to self.data
            self.data = self.get_data(id_data)

            print(self.data.head())

    @staticmethod
    def get_metadata(id_data):
        """
        It calls to the Pangea API to obtain metadata information.

        Parameters
        ----------
            id_data: int
                Id of the data that you want to obtain the metadata.

        Returns
        -------
            metadata: dict
                Dictionary with metadata information

        """
        metadata_url = f"https://doi.pangaea.de/10.1594/PANGAEA.{id_data}?format=metainfo_xml"
        metadata = dict()

        response = requests.get(metadata_url)
        if response.status_code != 404:
            xml = ElementTree.fromstring(response.text)
            namespace = {'md': 'http://www.pangaea.de/MetaData'}

            # Read metadata
            metadata['login_status'] = xml.find('./md:technicalInfo/md:entry[@key="loginOption"]',
                                                namespace).get('value')
            if metadata['login_status'] != 'unrestricted':
                warnings.warn(f"Dataset with id {id_data} is protected")
            try:
                metadata['hierarchy_level'] = xml.find(
                    './md:technicalInfo/md:entry[@key="hierarchyLevel"]', namespace).get('value')
                if metadata['hierarchy_level'] == "parent":
                    warnings.warn(f"Dataset with id {id_data} is of type parent")
            except AttributeError:
                metadata['hierarchy_level'] = "child"
            metadata['title'] = xml.find("./md:citation/md:title", namespace).text
            metadata['year'] = xml.find("./md:citation/md:year", namespace).text
            metadata['doi'] = xml.find("./md:citation/md:URI", namespace).text
            metadata['topotype'] = xml.find("./md:extent/md:topoType", namespace).text
            metadata['authors'] = [", ".join((author.find("md:lastName", namespace).text,
                                              author.find("md:firstName", namespace).text))
                                   for author in xml.findall("./md:citation/md:author", namespace)]
            # Parameters
            metadata['parameters'] = dict()
            short_names = dict()
            xml_matrix_column = xml.findall("./md:matrixColumn", namespace)
            for matrix in xml_matrix_column:
                xml_type = matrix.get('type')
                source = matrix.get('source')
                xml_parameter = matrix.find("md:parameter", namespace)
                # Name
                name = xml_parameter.find('md:name', namespace).text
                # Short name
                short_name = xml_parameter.find('md:shortName', namespace).text
                # Rename duplicate short_name
                if short_name in short_names:
                    short_name += f"_{short_names[short_name]}"
                    short_names[short_name] += 1
                else:
                    short_names[short_name] = 1
                # Unit
                try:
                    unit = xml_parameter.find('md:unit', namespace).text
                except AttributeError:
                    if name == "DATE/TIME":
                        pass
                    else:
                        warnings.warn(f"Parameter {name} without units")
                    unit = None
                # Parameter id
                try:
                    id_parameter = xml_parameter.get('id').split(".")[2]
                except AttributeError:
                    warnings.warn(f'Parameter "{name}" without id')
                    id_parameter = None

                parameter_dict = {'type': xml_type,
                                  'source': source,
                                  'name': name,
                                  'short_name': short_name,
                                  'units': unit,
                                  'id': id_parameter}
                metadata['parameters'][short_name] = parameter_dict

            # Events
            xml_events = xml.findall("./md:event", namespace)
            metadata['events'] = [{'label': event.find('./md:label', namespace).text,
                                   'latitude': event.find('./md:latitude', namespace).text,
                                   'longitude': event.find('./md:longitude', namespace).text,
                                   'elevation': event.find('./md:elevation', namespace).text,
                                   'date_time': event.find('./md:dateTime', namespace).text
                                   } for event in xml_events]

        else:
            warnings.warn(f"Dataset with id {id_data} does not exist")

        return metadata

    @staticmethod
    def get_data(id_data):
        """
        Obtain the data from Pangea data with the input id.

        Parameters
        ----------
            id_data: int
                Id of the data source.

        Returns
        -------
            df: pandas.DataFrame
        """
        data_url = f"https://doi.pangaea.de/10.1594/PANGAEA.{id_data}?format=textfile"
        xml = requests.get(data_url).text
        data = re.sub(r"/\*(.*)\*/", "", xml, 1, re.DOTALL).strip()
        df_pangea = pd.read_csv(io.StringIO(data), index_col=False, error_bad_lines=False,
                                sep=u'\t')

        # Replace Quality Flags
        df_pangea.replace(regex=r'^[\?/\*#\<\>]', value='', inplace=True)
        # Adjust Column Data Types
        df_pangea = df_pangea.apply(pd.to_numeric, errors='ignore')
        if 'Date/Time' in df_pangea.columns:
            df_pangea['Date/Time'] = pd.to_datetime(df_pangea['Date/Time'],
                                                    format='%Y/%m/%dT%H:%M:%S')

        return df_pangea

    def to_waterframe(self, id_data=None, data=None, metadata=None):
        """
        It creates a mooda.WaterFrame object.

        Parameters
        ----------
            id_data: int (optional, id_data=None)
                Id if the dataset of pangea to use.
            data: pandas.DataFrame (optional, data=None)
                DataFrame to include into the WaterFrame.
            metadata: dict (optional, metadata=None)
                Metadata to include into the WaterFrame.

        Returns
        -------
            wf_pangea: mooda.WaterFrame
                WaterFrame object.
        """
        # Check where to find data and metadata
        if id_data:
            metadata_pangea = self.get_metadata(id_data)
            data_pangea = self.get_data(id_data)
        else:
            if data:
                data_pangea = data
            else:
                data_pangea = self.data
            if metadata:
                metadata_pangea = metadata
            else:
                metadata_pangea = self.metadata

        # Change names of columns
        # Delete the units from the column names (ex: Elevation [m] -> Elevation)
        # and Date/Time to TIME
        # Delete "Event" column
        for key in data_pangea.keys():
            if "[" in key:
                data_pangea.rename(columns={key: key.split(" [")[0]}, inplace=True)
            elif key == "Date/Time":
                data_pangea.rename(columns={key: "TIME"}, inplace=True)
            elif key == "Event":  # TODO: Check what is "Event"
                del data_pangea["Event"]

        # Set index to TIME
        try:
            data_pangea.set_index("TIME", inplace=True)
        except KeyError:
            warnings.warn('There is no "TIME" in the columns of the dataframe. The WaterFrame' +
                          ' will not contain a time index.')

        # Set meaning
        meaning_pangea = metadata_pangea['parameters']
        # Add "long_name" to the dictionary if it does not exist
        for meaning in meaning_pangea:
            keys = meaning_pangea[meaning].keys()
            if "long_name" not in keys and "name" in keys:
                meaning_pangea[meaning]["long_name"] = meaning_pangea[meaning]["name"]

        wf_pangea = WaterFrame(df=data_pangea, metadata=metadata_pangea, meaning=meaning_pangea)

        return wf_pangea

    @staticmethod
    def from_source_to_waterframe(id_data=None, data=None, metadata=None):
        """
        It creates a mooda.WaterFrame object.

        Parameters
        ----------
            id_data: int (optional, id_data=None)
                Id if the dataset of pangea to use.
            data: pandas.DataFrame (optional, data=None)
                DataFrame to include into the WaterFrame.
            metadata: dict (optional, metadata=None)
                Metadata to include into the WaterFrame.

        Returns
        -------
            wf_pangea: mooda.WaterFrame
                WaterFrame object.
        """
        # Check where to find data and metadata
        if id_data:
            metadata_pangea = Pangea.get_metadata(id_data)
            data_pangea = Pangea.get_data(id_data)
        else:
            if data and metadata:
                data_pangea = data
                metadata_pangea = metadata
            else:
                warnings.warn("You must insert id_data or data and metadata.")
                return False

        # Change names of columns
        # Delete the units from the column names (ex: Elevation [m] -> Elevation)
        # and Date/Time to TIME
        # Delete "Event" column
        for key in data_pangea.keys():
            if "[" in key:
                data_pangea.rename(columns={key: key.split(" [")[0]}, inplace=True)
            elif key == "Date/Time":
                data_pangea.rename(columns={key: "TIME"}, inplace=True)
            elif key == "Event":  # TODO: Check what is "Event"
                del data_pangea["Event"]

        # Set index to TIME
        try:
            data_pangea.set_index("TIME", inplace=True)
        except KeyError:
            warnings.warn('There is no "TIME" in the columns of the dataframe. The WaterFrame' +
                          ' will not contain a time index.')

        # Set meaning
        meaning_pangea = metadata_pangea['parameters'].copy()
        # Add "long_name" to the dictionary if it does not exist
        for meaning in meaning_pangea:
            keys = meaning_pangea[meaning].keys()
            if "long_name" not in keys and "name" in keys:
                meaning_pangea[meaning]["long_name"] = meaning_pangea[meaning]["name"]
        # Delete 'parameters' and 'events' from the metadata
        del metadata_pangea['parameters']
        del metadata_pangea['events']

        wf_pangea = WaterFrame(df=data_pangea, metadata=metadata_pangea, meaning=meaning_pangea)

        return wf_pangea
