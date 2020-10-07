from elasticsearch import Elasticsearch


def es_create_indexes(data_index_name='data', metadata_index_name='metadata',
                      summary_index_name='summary', vocabulary_index_name='vocabulary',
                      delete_previous_indexes=True, **kwargs):
    """
    Creation of ElasticSearch Indexes to save a WaterFrame object.
    
    Parameters
    ----------
        data_index_name: str
            Name of the ElasticSearch index that contains the WaterFrame.data documents.
        metadata_index_name: str
            Name of the ElasticSearch index that contains the WaterFrame.metadata documents.
        summary_index_name: str
            Name of the ElasticSearch index that contains the summary documentation.
        vocabulary_index_name: str
            Name of the ElasticSearch index that contains the vocabulary documentation.
        delete_previous_indexes: bool
            Delete previous indexes with the input names and all their documents.
        **kwargs: Elasticsearch object creation arguments.
            See https://elasticsearch-py.readthedocs.io/en/master/index.html#
    
    Returns
    -------
        success: bool
            If sucess is true, indexes where created.
    """
    def create_data_index():
        # Index settings
        # settings = {
        #     'mappings': {
        #         'properties': {
        #             'parameter': {'type': 'keyword'},
        #             'time': {
        #                 'type': 'date',
        #                 'format': 'yyyy-MM-dd HH:mm:ss'
        #             },
        #             'time_qc': {'type': 'integer'},
        #             'depth': {'type': 'float'},
        #             'depth_qc': {'type': 'integer'},
        #             'value': {'type': 'float'},
        #             'value_qc': {'type': 'integer'},
        #             'metadata_id': {'type': 'keyword'},
        #         }
        #     }
        # }

        # New version, 01-09-2020
        settings = {
            'mappings': {
                'properties': {
                    'parameter': {'type': 'keyword'},
                    'time': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd HH:mm:ss'
                    },
                    'time_qc': {'type': 'integer'},
                    'depth': {'type': 'float'},
                    'depth_qc': {'type': 'integer'},
                    'value': {'type': 'float'},
                    'value_qc': {'type': 'integer'},
                    'metadata_id': {'type': 'keyword'},
                    'platform_code': {'type': 'keyword'},
                    'site': {'type': 'keyword'},
                    'institution': {'type': 'text'},
                    'area': {'type': 'text'},
                    'network': {'type': 'text'},
                    'long_name': {'type': 'text'},
                    'units': {'type': 'text'},
                    'location': {'type': 'geo_point'},
                    'location_qc': {'type': 'integer'},
                }
            }
        }

        es.indices.create(index=data_index_name, body=settings)

    def create_metadata_index():

        # Index settings
        settings = {
            'mappings': {
                'properties': {
                    'platform_code': {'type': 'keyword'},
                    'platform_name': {'type': 'keyword'},
                    'ices_platform_code': {'type': 'keyword'},
                    'institution': {'type': 'text', 'analyzer': 'standard'},
                    'date_update': {'type': 'date'},
                    'site_code': {'type': 'keyword'},
                    'wmo_platform_code': {'type': 'keyword'},
                    'source': {'type': 'text', 'analyzer': 'standard'},
                    'history': {'type': 'text', 'analyzer': 'standard'},
                    'data_mode': {'type': 'keyword'},
                    'references': {'type': 'text', 'analyzer': 'standard'},
                    'comment': {'type': 'text', 'analyzer': 'standard'},
                    'summary': {'type': 'text', 'analyzer': 'standard'},
                    'id': {'type': 'keyword'},
                    'area': {'type': 'keyword'},
                    'geospatial_min': {'type': 'geo_point'},
                    'geospatial_max': {'type': 'geo_point'},
                    'geospatial_vertical_min': {'type': 'float'},
                    'time_coverage_start': {'type': 'date'},
                    'time_coverage_end': {'type': 'date'},
                    'institution_references': {'type': 'text', 'analyzer': 'standard'},
                    'contact': {'type': 'text', 'analyzer': 'standard'},
                    'author': {'type': 'text', 'analyzer': 'standard'},
                    'pi_name': {'type': 'text', 'analyzer': 'standard'},
                    'update_interval': {'type': 'keyword'},
                    'wmo_inst_type': {'type': 'keyword'},
                    'qc_manual': {'type': 'text', 'analyzer': 'standard'},
                    'data_type': {'type': 'text', 'analyzer': 'standard'},
                    'naming_authority': {'type': 'keyword'},
                    'quality_control_indicator': {'type': 'integer'},
                    'distribution_statement': {'type': 'text', 'analyzer': 'standard'},
                    'quality_index': {'type': 'keyword'},
                    'citation': {'type': 'text', 'analyzer': 'standard'},
                    'format_version': {'type': 'float'},
                    'Conventions': {'type': 'text', 'analyzer': 'standard'},
                    'title': {'type': 'text', 'analyzer': 'standard'},
                    'data_assembly_center': {'type': 'keyword'},
                    'last_location_observation': {'type': 'geo_point'},
                    'last_date_observation': {'type': 'date'},
                    'parameters': {'type': 'text', 'analyzer': 'standard'},
                    'site': {'type': 'keyword'},
                    'network': {'type': 'keyword'},
                }
            }
        }

        es.indices.create(index=metadata_index_name, body=settings)

    def create_summary_index():
        # Index settings
        settings = {
            'mappings': {
                'properties': {
                    'parameters': {
                        'properties': {
                            'long_name': {'type': 'keyword'},
                            'acronym': {'type': 'keyword'}}},
                    'networks': {'type': 'keyword'},
                    'sites': {'type': 'keyword'}}}}

        # Creation of the index
        es.indices.create(index=summary_index_name, body=settings)

    def create_vocabulary_index():
        # Index settings
        settings = {
            'mappings': {
                'properties': {
                    'long_name': {'type': 'keyword'},
                    'acronym': {'type': 'keyword'},
                    'units': {'type': 'keyword'}}}}

        # Creation of the index
        es.indices.create(index=vocabulary_index_name, body=settings)

    es = Elasticsearch(**kwargs)

    if delete_previous_indexes:
        # Delete indexes, ignore if indexes do not exist
        es.indices.delete(index=data_index_name, ignore=404)
        es.indices.delete(index=metadata_index_name, ignore=404)
        es.indices.delete(index=summary_index_name, ignore=404)
        es.indices.delete(index=vocabulary_index_name, ignore=404)
    
    # Index creation
    create_data_index()
    create_metadata_index()
    create_summary_index()
    create_vocabulary_index()

    success = True
    return success
