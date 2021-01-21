import requests
import json
from typing import Dict, List, Tuple
import urllib.parse

url = 'http://api.emso.eu'

class EMSO():
    """
    Manage the EMSO ERIC API (http://api.emso.eu)

    Parameters
    ----------
        user: str
            User or email of the EMSO ERIC API.
        password: str
    """

    def __init__(self, user: str='', password: str=''):

        # Creation of a requests session
        self.api = requests.Session()
        self.token = ''

        if user and password:
            # Get API token
            query = f'{url}/user/authorization?user={user}&password={password}'
            r = requests.get(query)
            if r.status_code == 201:
                self.token = r.json()['result']
                # Update requests session with the authorization header
                self.api.headers.update({'Authorization': self.token})
            else:
                raise Exception('Incorrect user or password')

    def post_user_email(self, message: Dict[str, str]) -> str:
        """
        Send an email to help@emso-eu.org

        Parameters
        ----------
            message: dict
                {'subject': 'Subject of the email',
                 'content': 'Content of the email'}
        
        Returns
        -------
            response_message: str
                Response from the API
        """
        query = f'{url}/user/email'
        message_json = json.dumps(message)

        response = self.api.post(query, payload=message_json)
        response_message = response.json()['message']
        return response_message

    def get_user_query(self, size: int=10, sort: str='desc') -> List[str]:
        """
        Get the queries of the user

        Parameters
        ----------
            size: int
                Number of results (def: 10, max:10000)
            sort: str
                Order of the values (def: 'desc', options: 'asc', 'desc')
        Returns
        -------
            query_list: List[str]
                List of the queries of the user
        """
        query = f'{url}/user/query?size={size}&sort={sort}'

        query_list = []
        r = self.api.get(query)
        if r.status_code == 201:
            query_list = r.json()['result']
        
        return query_list

    def get_info_fig(self) -> List[str]:
        """
        Get the available figures

        Returns
        -------
            fig_list: List[str]
                List of available figures
        """
        fig_list = []

        query = f'{url}/info/fig'
        r = self.api.get(query)
        if r.status_code == 200:
            fig_list = r.json()['result']

        return fig_list

    def get_info_fig_plot(self, plot: str) -> List[str]:
        """
        Get the available arguments for the input plot

        Parameters
        ----------
            plot: str
                Figure type
        
        Returns
        -------
            argument_list: List[str]
                List of available arguments
        """
        argument_list = []

        query = f'{url}/info/fig/{plot}'
        r = self.api.get(query)
        if r.status_code == 200:
            argument_list = r.json()['result']

        return argument_list

    def get_info_fig_plot_argument(
        self, plot:str, argument:str) -> Tuple[str, List[str]]:
        """
        Get argument information and available options

        Parameters
        ----------
            plot: str
                Figure type
            argument: str
                Figure argument

        Returns
        -------
            argument_info: Tuple[str, List[str]]
                (meaning of the argument, list of available options)
        """
        message = ''
        option_list = []

        query = f'{url}/info/fig/{plot}/{argument}'
        r = self.api.get(query)
        if r.status_code == 200 or r.status_code == 201:
            r_json = r.json()
            message = r_json['message']
            option_list = r_json['result']

        return (message, option_list)

    def get_info_metadata_id(self, platform_codes:List[str]=[], sites:List[str]=[]) -> List[str]:
        """
        Get the ID of the metadata archivements of the EMSO ERIC API

        Parameters
        ----------
            platform_codes: List[str]
                List of platform_code
            sites: List[str]
                List of site
        
        Returns
        -------
            metadata_ids: List[str]
                List of 'metadata_id'
        """
        metadata_ids = []

        # Make query
        query = f'{url}/info/metadata_id'
        if platform_codes or sites:
            query += '?'
            if platform_codes:
                query += f'platform_code={(",").join(platform_codes)}'
            if sites:
                if query[-1] != '?':
                    query += '&'
                query += f'site={(",").join(sites)}'

        r = self.api.get(query)
        if r.status_code == 201:
            metadata_ids = r.json()['result']
        return metadata_ids

    def get_info_parameter(self, platform_codes:List[str]=[], sites:List[str]=[]) -> List[str]:
        """
        Get available parameters of the EMSO ERIC API

        Parameters
        ----------
            platform_codes: List[str]
                List of platform_code
            sites: List[str]
                List of site
        
        Returns
        -------
            parameters: List[str]
                List of 'parameter'
        """
        parameters = []

        # Make query
        query = f'{url}/info/parameter'
        if platform_codes or sites:
            query += '?'
            if platform_codes:
                query += f'platform_code={(",").join(platform_codes)}'
            if sites:
                if query[-1] != '?':
                    query += '&'
                query += f'site={(",").join(sites)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            parameters = r.json()['result']
        return parameters

    def get_info_platform_code(self, parameters:List[str]=[], sites:List[str]=[]) -> List[str]:
        """
        Get available platfom codes ('platform_code') of the EMSO ERIC API

        Parameters
        ----------
            parameters: List[str]
                List of 'parameter'
            sites: List[str]
                List of site
        
        Returns
        -------
            platform_codes: List[str]
                List of 'platform_code'
        """
        platform_codes = []

        # Make query
        query = f'{url}/info/platform_code'
        if parameters or sites:
            query += '?'
            if parameters:
                query += f'parameter={(",").join(parameters)}'
            if sites:
                if query[-1] != '?':
                    query += '&'
                query += f'site={(",").join(sites)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            platform_codes = r.json()['result']

        return platform_codes

    def get_info_site(self) -> List[str]:
        """
        Get available sites ('site') of the EMSO ERIC API
        
        Returns
        -------
            sites: List[str]
                List of 'site'
        """
        sites = []

        # Make query
        query = f'{url}/info/site'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            sites = r.json()['result']

        return sites

    def get_info_summary(self, fields:List[str]=[], parameters:List[str]=[],
                         platform_codes:List[str]=[], sites:List[str]=[]) -> List[dict]:
        """
        Get the most used fields of the metadatada archivements

        Parameters
        ----------
            fields: List[str]
                    List of fields to return
            parameters: List[str]
                List of 'prameter'
            platform_codes: List[str]
                List of 'platform_code'
            sites: List[str]
                List of 'site'

        Returns
        -------
            sumaries: List[dict]
                List of metadata archivements
        """
        sumaries = []

        # Make the query
        query = f'{url}/info/summary'

        if fields or parameters or platform_codes or sites:
            query += '?'
            if fields:
                query += f'field={(",").join(fields)}'
            if parameters:
                if query[-1] != '?':
                    query += '&'
                query += f'parameter={(",").join(parameters)}'
            if platform_codes:
                if query[-1] != '?':
                    query += '&'
                query += f'platform_code={(",").join(platform_codes)}'
            if sites:
                if query[-1] != '?':
                    query += '&'
                query += f'site={(",").join(sites)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            sumaries = r.json()['result']
        return sumaries

    def get_metadata(self, fields:List[str]=[], metadata_ids:List[str]=[],
                     platform_codes:List[str]=[], sites:List[str]=[]) -> List[dict]:
        """
        Get all fields of the metadatada archivements

        Parameters
        ----------
            fields: List[str]
                    List of fields to return
            metadata_ids: List[str]
                List of 'metadata_id'
            parameters: List[str]
                List of 'prameter'
            platform_codes: List[str]
                List of 'platform_code'
            sites: List[str]
                List of 'site'

        Returns
        -------
            metadatas: List[dict]
                List of metadata archivements
        """
        metadatas = []

        # Make the query
        query = f'{url}/metadata'

        if fields or metadata_ids or platform_codes or sites:
            query += '?'
            if fields:
                query += f'field={(",").join(fields)}'
            if metadata_ids:
                if query[-1] != '?':
                    query += '&'
                query += f'metadata_id={(",").join(metadata_ids)}'
            if platform_codes:
                if query[-1] != '?':
                    query += '&'
                query += f'platform_code={(",").join(platform_codes)}'
            if sites:
                if query[-1] != '?':
                    query += '&'
                query += f'site={(",").join(sites)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            metadatas = r.json()['result']

        return metadatas

    def get_data(self, depth_max:float=None, depth_min:float=None, depth_qcs:List[int]=[],
                 end_time:str='', metadata_ids:List[str]=[], size:int=10, sort:str='desc',
                 parameters:List[str]=[], platform_codes:List[str]=[], start_time:str='',
                 time_qcs:List[int]=[], value_qcs:List[int]=[]) -> List[dict]:
        """
        Get data from the EMSO ERIC API

        Parameters
        ----------
            depth_max: int
                Maximun depth of the measurement
            depth_min: int
                Minimum depth of the measurement
            depth_qcs: List[int]
                List of QC values accepted for the depth_qc field
            end_time: str
                Maximum date of the measurement
            metadata_ids: List[str]
                List of accepted 'metadata_id'
            size: int
                Number of values to be returned
            sort: str
                Options: 'asc' or 'desc'. Get the first or last (in time) measurements
            parameters: List[str]
                List of accepted 'parameter'
            platform_codes: List[str]
                List of accepted 'platform_code'
            start_time: str
                Minimun date of the meassurement
            time_qcs: List[int]
                List of accepted values for the field time_qc
            value_qcs: List[int]
                List of accepted values for the field of value_qc
        
        Returns
        -------
            data_list: List[dict]
                The data
        """
        data_list = []

        if size is None:
            size = 10
        if sort is None:
            sort = 'desc'

        # Make the query
        query = f'{url}/data?size={size}&sort={sort}'

        if depth_max or depth_min or depth_qcs or end_time or metadata_ids or \
            parameters or platform_codes or start_time or time_qcs or value_qcs:

            if depth_max:
                query += f'&depth_max={depth_max}'
            if depth_min:
                query += f'&depth_min={depth_min}'
            if depth_qcs:
                depth_qcs_str = map(str, depth_qcs)
                query += f'&depth_qc={(",").join(depth_qcs_str)}'
            if end_time:
                query += f'&end_time={end_time}'
            if metadata_ids:
                query += f'&metadata_id={(",").join(metadata_ids)}'
            if parameters:
                query += f'&parameter={(",").join(parameters)}'
            if platform_codes:
                query += f'&platform_code={(",").join(platform_codes)}'
            if start_time:
                query += f'&start_time={start_time}'
            if time_qcs:
                time_qcs_str = map(str, time_qcs)
                query += f'&time_qc={(",").join(time_qcs_str)}'
            if value_qcs:
                value_qcs_str = map(str, value_qcs)
                query += f'&value_qc={(",").join(value_qcs_str)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            data_list = r.json()['result']

        return data_list

    def get_fig_data_interval(self, interval:str='D', depth_max:int=None, depth_min:int=None,
                              depth_qcs:List[int]=[], end_time:str='', metadata_ids:List[str]=[],
                              parameters:List[str]=[], platform_codes:List[str]=[],
                              rangeslider:bool=False, start_time:str='', time_qcs:List[int]=[],
                              title:str='', value_qcs:List[int]=[]) -> dict:
        """
        Get the plotly figure 'Data Interval' from the EMSO ERIC API

        Parameters
        ----------
            interval: str
                Period to find a data value
            depth_max: int
                Maximun depth of the measurement
            depth_min: int
                Minimum depth of the measurement
            depth_qcs: List[int]
                List of QC values accepted for the depth_qc field
            end_time: str
                Maximum date of the measurement
            metadata_ids: List[str]
                List of accepted 'metadata_id'
            parameters: List[str]
                List of accepted 'parameter'
            platform_codes: List[str]
                List of accepted 'platform_code'
            rangeslider: bool
                Enable a range slider on to bottom of the graph
            start_time: str
                Minimun date of the meassurement
            time_qcs: List[int]
                List of accepted values for the field time_qc
            title: str
                Title of the figure
            value_qcs: List[int]
                List of accepted values for the field of value_qc
        
        Returns
        -------
            fig: dict
                Plotly figure
        """
        # Add the number
        if len(interval) < 2:
            interval = '1' + interval

        interval_str = interval.replace(
            'S', 's').replace('T', 'm').replace('H', 'h').replace('D', 'd')

        fig = {}

        if rangeslider:
            rangeslider_str = 'true'
        else:
            rangeslider_str = 'false'

        # Make the query
        query = f'{url}/fig/data_interval/{interval_str}?rangeslider={rangeslider_str}'

        print(query)

        if depth_max or depth_min or depth_qcs or end_time or metadata_ids or \
            parameters or platform_codes or start_time or time_qcs or \
            value_qcs or title or rangeslider:

            if depth_max:
                query += f'&depth_max={depth_max}'
            if depth_min:
                query += f'&depth_min={depth_min}'
            if depth_qcs:
                depth_qcs_str = map(str, depth_qcs)
                query += f'&depth_qc={(",").join(depth_qcs_str)}'
            if end_time:
                query += f'&end_time={end_time}'
            if metadata_ids:
                query += f'&metadata_id={(",").join(metadata_ids)}'
            if parameters:
                query += f'&parameter={(",").join(parameters)}'
            if platform_codes:
                query += f'&platform_code={(",").join(platform_codes)}'
            if start_time:
                query += f'&start_time={start_time}'
            if time_qcs:
                time_qcs_str = map(str, time_qcs)
                query += f'&time_qc={(",").join(time_qcs_str)}'
            if title:
                query += f'&title={title}'
            if value_qcs:
                value_qcs_str = map(str, value_qcs)
                query += f'&value_qc={(",").join(value_qcs_str)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            fig = r.json()['result']

        return fig

    def get_fig_line(self, depth_max:int=None, depth_min:int=None, depth_qcs:List[int]=[],
                     end_time:str='', metadata_ids:List[str]=[], parameters:List[str]=[],
                     platform_codes:List[str]=[], size:int=10, start_time:str='', sort:str='desc',
                     time_qcs:List[int]=[], title:str='', value_qcs:List[int]=[], x='time',
                     y='value') -> dict:
        """
        Get the plotly figure 'line' from the EMSO ERIC API

        Parameters
        ----------
            depth_max: int
                Maximun depth of the measurement
            depth_min: int
                Minimum depth of the measurement
            depth_qcs: List[int]
                List of QC values accepted for the depth_qc field
            end_time: str
                Maximum date of the measurement
            metadata_ids: List[str]
                List of accepted 'metadata_id'
            parameters: List[str]
                List of accepted 'parameter'
            platform_codes: List[str]
                List of accepted 'platform_code'
            size: int
                Number of values to make the graph
            start_time: str
                Minimun date of the meassurement
            sort: str
                Options: 'asc' or 'desc'. Get the first or last (in time) measurements
            time_qcs: List[int]
                List of accepted values for the field time_qc
            title: str
                Title of the figure
            value_qcs: List[int]
                List of accepted values for the field of value_qc
            x: str
                Field for the x-axis
            y: str
                Field for the y-axis
        Returns
        -------
            fig: dict
                Plotly figure
        """
        fig = {}

        if size is None:
            size = 10
        if sort is None:
            sort = 'desc'
        if x is None:
            x = 'time'
        if y is None:
            y = 'value'

        # Make the query
        query = f'{url}/fig/line?size={size}&sort={sort}&x={x}&y={y}'

        if depth_max or depth_min or depth_qcs or end_time or metadata_ids or \
            parameters or platform_codes or start_time or time_qcs or value_qcs:

            if depth_max:
                query += f'&depth_max={depth_max}'
            if depth_min:
                query += f'&depth_min={depth_min}'
            if depth_qcs:
                depth_qcs_str = map(str, depth_qcs)
                query += f'&depth_qc={(",").join(depth_qcs_str)}'
            if end_time:
                query += f'&end_time={end_time}'
            if metadata_ids:
                query += f'&metadata_id={(",").join(metadata_ids)}'
            if parameters:
                query += f'&parameter={(",").join(parameters)}'
            if platform_codes:
                query += f'&platform_code={(",").join(platform_codes)}'
            if start_time:
                query += f'&start_time={start_time}'
            if time_qcs:
                time_qcs_str = map(str, time_qcs)
                query += f'&time_qc={(",").join(time_qcs_str)}'
            if title:
                query += f'&title={title}'
            if value_qcs:
                value_qcs_str = map(str, value_qcs)
                query += f'&value_qc={(",").join(value_qcs_str)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            fig = r.json()['result']

        return fig

    def get_fig_map(self, parameters:List[str]=[], platform_codes:List[str]=[],
                    sites:List[str]=[]) -> dict:
        """
        Get the plotly figure 'Map' from the EMSO ERIC API

        Parameters
        ----------
            parameters: List[str]
                List of accepted 'parameter'
            platform_codes: List[str]
                List of accepted 'platform_code'
            site: List[str]
                List of accepted 'site'
        Returns
        -------
            fig: dict
                Plotly figure
        """
        fig = {}

        # Make the query
        query = f'{url}/fig/map'

        if parameters or platform_codes or sites:
            query += '?'
            if parameters:
                query += f'parameter={(",").join(parameters)}'
            if platform_codes:
                if query[-1] != '?':
                    query += '&'
                query += f'platform_code={(",").join(platform_codes)}'
            if sites:
                if query[-1] != '?':
                    query += '&'
                query += f'site={(",").join(sites)}'

        # Send the query
        r = self.api.get(query)
        if r.status_code == 201:
            fig = r.json()['result']

        return fig
