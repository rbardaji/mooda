import json
from elasticsearch import Elasticsearch, exceptions
from time import sleep


def to_es(self, data_index_name='data', metadata_index_name='metadata',
          summary_index_name='summary', qc_to_ingest=[0, 1], **kwargs):
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
        qc_to_intest: list of int
            QC Flags of data to be ingested to the ElasticSearch DB.
        **kwargs: Elasticsearch object creation arguments.
            See https://elasticsearch-py.readthedocs.io/en/master/index.html#
    """
    def data_ingestion(es, data_index_name, data_dict):

        data_id = f"{data_dict['metadata_id']}_{data_dict['parameter']}_{data_dict['time'].replace(' ', 'T')}_{data_dict['depth']}"
        data_json = json.dumps(data_dict)
        es.index(index=data_index_name, id=data_id, body=data_json)

        return True

    def summary_ingestion(es, summary_index_name, summary_dict):

        try:
            # Read emso-stats
            response = es.get(index='emso-stats', id='datalab')
            es_summary = response['_source']

            es_summary['sites'] = list(set(es_summary['sites'] + summary_dict['sites']))
            es_summary['networks'] = list(set(es_summary['networks'] + summary_dict['networks']))
            param_list = []

            for stats_parameter in summary_dict['parameters']:

                tengui = False
                for summary_parameter in es_summary['parameters']:
                    if summary_parameter['acronym'] == stats_parameter['acronym'] or \
                        'QC' in summary_parameter['acronym']:
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
        es.index(index=metadata_index_name, id=metadata_dict['id'], body=metadata_json)
        return True
    
    es = Elasticsearch(**kwargs)

    # Add parameters in metadata information
    self.metadata['parameters'] = self.parameters

    ok = metadata_ingestion(es, metadata_index_name, self.metadata)
    if ok:
        print(f"Metadata {self.metadata['id']} ingested")
    else:
        print(f"Error: Metadata {self.metadata['id']} not ingested")
    
    summary_dict = {
        'sites': [self.metadata['site_code']],
        'networks': [self.metadata['network']],
        'parameters': []}
    for key, value in self.vocabulary.items():
        if '_QC' not in key or 'TIME' not in key or 'DEPH' not in key:
            try:
                summary_dict['parameters'].append({'long_name': value['long_name'], 'acronym': key})
            except KeyError:
                print(f"Caution: {key} doesn't contain 'long_name'")

    ok = summary_ingestion(es, summary_index_name, summary_dict)
    if ok:
        print('Stats updated')
    else:
        print('Error: Stats not updated')

    for parameter in self.parameters:
        mini_wf = self.copy()
        try:
            mini_wf.data = self.data[[parameter, parameter+'_QC', 'DEPH', 'DEPH_QC', 'TIME_QC']]
        except KeyError:
            mini_wf.data = self.data[[parameter, parameter+'_QC', 'TIME_QC']]
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

            for num, (index, row) in enumerate(df.iterrows()):
                data_dict = {
                    'parameter': parameter,
                    'time': str(index)[:19],
                    'time_qc': int(row['TIME_QC']),
                    'depth': str(row['DEPH']),
                    'depth_qc': int(row['DEPH_QC']),
                    'value': str(row[parameter]),
                    'value_qc': int(row[parameter+'_QC']),
                    'metadata_id': self.metadata['id']
                }

                ok = data_ingestion(es, data_index_name, data_dict)
                if ok:
                    print(f"{data_dict['parameter']} from {data_dict['metadata_id']} ingested: {num} of {len(df.index)}")
                else:
                    print(f"ERROR: {data_dict['parameter']} from {data_dict['metadata_id']} NOT ingested: {num} of {len(df.index)}")

                # Wait for ES operations
                sleep(0.01)
