import json
from elasticsearch import Elasticsearch, exceptions
from time import sleep


def to_es(self, data_index_name='data', metadata_index_name='metadata',
          summary_index_name='summary', vocabulary_index_name='vocabulary',
          qc_to_ingest=[0, 1], parameters=None, metadata_to_es=True,
          data_to_es=True, summary_to_es=True, vocabulary_to_es=True, start=None,
          **kwargs):
    """
    Injestion of the WaterFrame into a ElasticSeach DB.

    Parameters
    ----------
        data_index_name: str
            Name of the ElasticSearch index that contains the WaterFrame.data documents.
        metadata_index_name: str
            Name of the ElasticSearch index that contains the WaterFrame.metadata documents.
        summary_index_name: str
            Name of the ElasticSearch index that contains the summary documents.
        vocabulary_index_name: str
            Name of the ElasticSearch index that contains the summary documentation.
        qc_to_intest: list of int
            QC Flags of data to be ingested to the ElasticSearch DB.
        parameters: list of str
            List of parameters to ingest. If parameters is None, all parameters will be ingested.
        metadata_to_es: bool
            If True, metadata will be ingested.
        data_to_es: bool
            If True, data will be ingested.
        vocabulary_to_es: bool
            If True, vocabulary will be ingested.
        **kwargs: Elasticsearch object creation arguments.
            See https://elasticsearch-py.readthedocs.io/en/master/index.html#
    """
    def data_ingestion(es, data_index_name, list_data_dict, start_in):

        bulk_size = len(list_data_dict)
        try:
            print(list_data_dict[1]['parameter'], "to ingest:", bulk_size, "records")
        except IndexError:
            pass
        while bulk_size >= 100:
            if start_in:
                if bulk_size <= start_in:
                    try:
                        es.bulk(index=data_index_name, body=list_data_dict[:100], refresh=True)
                    except ValueError:
                        # Empty body
                        pass
                    list_data_dict = list_data_dict[100:]
                    bulk_size -= 100
                else:
                    list_data_dict = list_data_dict[start_in:]
                    bulk_size = start_in
            else:
                try:
                    es.bulk(index=data_index_name, body=list_data_dict[:100], refresh=True)
                except ValueError:
                    # Empty body
                    pass
                list_data_dict = list_data_dict[100:]
                bulk_size -= 100
            try:
                print(list_data_dict[1]['parameter'], "to ingest:", bulk_size, "records")
            except IndexError:
                pass
        if bulk_size > 0:
            es.bulk(index=data_index_name, body=list_data_dict, refresh=True)

        return True

    def summary_ingestion(es, summary_index_name, summary_dict):

        try:
            # Read emso-stats
            response = es.get(index=summary_index_name, id='datalab')
            es_summary = response['_source']

            es_summary['sites'] = list(set(es_summary['sites'] + summary_dict['sites']))

            es_summary['networks'] = list(set(es_summary['networks'] + summary_dict['networks']))
            param_list = []

            for stats_parameter in summary_dict['parameters']:
                tengui = False
                for summary_parameter in es_summary['parameters']:
                    if summary_parameter['acronym'] == stats_parameter['acronym'] and \
                        'units' in stats_parameter:
                        # print('tengui')
                        tengui = True
                        break
                if not tengui:
                    param_list.append(stats_parameter)
            es_summary['parameters'] += param_list

            # Ingest updated stats
            es.index(index=summary_index_name, id='datalab', body=es_summary)
            return True

        except exceptions.NotFoundError:
            summary_json = json.dumps(summary_dict)
            es.index(index=summary_index_name, id='datalab', body=summary_json)
            return True

    def get_metadata(es, metadata_index_name, search):
        """
        Get a list with the metadata information.
        """

        search_body = {
            'query': {
                'bool': {
                    'must': []
                }
            }  
        }
        if search.get('platform_code'):
            search_body['query']['bool']['must'].append(
                {'term': {'platform_code': search.get('platform_code')}})
        if search.get('geospatial_lat_min'):
            search_body['query']['bool']['must'].append(
                {'term': {'geospatial_lat_min': search.get('geospatial_lat_min')}})
        if search.get('geospatial_lon_min'):
            search_body['query']['bool']['must'].append(
                {'term': {'geospatial_lon_min': search.get('geospatial_lon_min')}})

        # Search query in metadata index
        response = es.search(index=metadata_index_name, body=search_body)
        
        if response['hits']['hits']:
            # Create a metadata dict with the metadata info and the id of the index
            for hit in response['hits']['hits']:
                return hit['_id'], hit['_source']['time_coverage_start'], hit['_source']['time_coverage_end']
        else:
            return False

    def metadata_ingestion(es, metadata_index_name, metadata_dict):

        metadata_search = {
            'platform_code': metadata_dict['platform_code'],
            'time_coverage_start': metadata_dict['time_coverage_start'],
            'time_coverage_end': metadata_dict['time_coverage_end']
        }

        result = get_metadata(es, metadata_index_name, metadata_search)

        if result:
            metadata_id = result[0]
            start = result[1]
            end = result[2]

            metadata_dict['id'] = metadata_id
            if metadata_dict.get('time_coverage_start') > start:
                metadata_dict['time_coverage_start'] = start
            if metadata_dict.get('time_coverage_end') < end:
                metadata_dict['time_coverage_end'] = end

        metadata_json = json.dumps(metadata_dict)
        # Create or update document
        try:
            es.delete(index=metadata_index_name, id=metadata_dict['id'])
        except exceptions.NotFoundError:
            pass
        es.index(index=metadata_index_name, id=metadata_dict['id'], body=metadata_json)
        return True
    
    es = Elasticsearch(**kwargs)

    if metadata_to_es:
        # Add parameters in metadata information
        parameters_string = []
        for parameter in self.parameters:
            parameters_string.append(
                f"{parameter} - {self.vocabulary[parameter]['long_name']} [{self.vocabulary[parameter]['units']}]")

        self.metadata['parameters'] = parameters_string

        ok = metadata_ingestion(es, metadata_index_name, self.metadata)
        if ok:
            print(f"Metadata {self.metadata['id']} ingested")
        else:
            print(f"Error: Metadata {self.metadata['id']} not ingested")
    
    if summary_to_es:
        summary_dict = {
            'sites': [self.metadata['site']],
            'networks': [self.metadata['network']],
            'parameters': []}
        for key, value in self.vocabulary.items():
            if '_QC' not in key or 'TIME' not in key or 'DEPH' not in key:
                try:
                    summary_dict['parameters'].append(
                        {
                            'long_name': value['long_name'],
                            'acronym': key,
                            'units': value['units']})
                except KeyError:
                    print(f"Caution: {key} doesn't contain 'long_name'")

        ok = summary_ingestion(es, summary_index_name, summary_dict)
        if ok:
            print('Stats updated')
        else:
            print('Error: Stats not updated')

    if data_to_es:
        if parameters is None:
            parameters = self.parameters

        for parameter in self.parameters:

            print(f'Parameter to ingest: {parameter}')
            print(f'Total parameters [{self.parameters}]')
            # Only upload the input parameters
            if parameter not in parameters:
                continue

            mini_wf = self.copy()
            try:
                mini_wf.data = self.data[[parameter, parameter+'_QC', 'DEPH', 'DEPH_QC', 'TIME_QC']]
            except KeyError:
                mini_wf.data = self.data[[parameter, parameter+'_QC', 'TIME_QC']].copy()
                mini_wf.data['DEPH'] = mini_wf.data.index.get_level_values('DEPTH')
                if 'DEPTH_QC' in self.data.keys():
                    mini_wf.data['DEPH_QC'] = self.data['DEPTH_QC']
                else:
                    mini_wf.data['DEPH_QC'] = 0

            mini_wf.data = mini_wf.data.dropna()

            mini_wf.data.reset_index(inplace=True)
            mini_wf.data.set_index('TIME', inplace=True)

            df_init = mini_wf.data

            for qc_value in qc_to_ingest:
                df = df_init[df_init[parameter+'_QC'] == qc_value]

                list_data_dict = []
                for index, row in df.iterrows():

                    index_dict = {
                        'index': {
                            # '_id': f"{self.metadata['id']}_{parameter}_{str(index)[:19].replace(' ', 'T')}_{str(row['DEPH'])}"
                            '_id': f"{self.metadata['id']}_{parameter}_{str(index).replace(' ', 'T')}_{str(row['DEPH'])}"
                        }
                    }
                    list_data_dict.append(index_dict)

                    data_dict = {
                        'parameter': parameter,
                        'time': str(index)[:19],
                        'time_qc': int(row['TIME_QC']),
                        'depth': str(row['DEPH']),
                        'depth_qc': int(row['DEPH_QC']),
                        'value': str(row[parameter]),
                        'value_qc': int(row[parameter+'_QC']),
                        'metadata_id': self.metadata['id'],
                        'platform_code': self.metadata['platform_code'],
                        'institution': self.metadata['institution'],
                        'area': self.metadata['area'],
                        'long_name': self.vocabulary[parameter]['long_name'],
                        'units': self.vocabulary[parameter]['units'],
                        'location': {
                            'lat': self.metadata['last_latitude_observation'],
                            'lon': self.metadata['last_longitude_observation'],
                        },
                        'location_qc': 0,
                    }
                    list_data_dict.append(data_dict)

                if list_data_dict:
                    ok = data_ingestion(es, data_index_name, list_data_dict, start)
                    if ok:
                        print(f"Data from {parameter} with QC {qc_value} ingested")
                    else:
                        print(f"ERROR in ingestion of data from {parameter}")

                    # Wait for ES operations
                    sleep(0.01)

            print(f'Parameter ingested: {parameter}')
            print(f'Total parameters [{self.parameters}]')

    if vocabulary_to_es:
        for key, value in self.vocabulary.items():
            if '_QC' in key or key in [
                'DEPTH', 'LATITUDE', 'LONGITUDE', 'TIME', 'station_name'] :
                continue

            vocabulary_dict = {
                'acronim': key,
                'long_name': value['long_name'],
                'units':  value['units']
            }

            vocabulary_json = json.dumps(vocabulary_dict)
            # Create or update document
            es.index(index=vocabulary_index_name, id=key, body=vocabulary_json)
