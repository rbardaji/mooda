import mooda as md
from datetime import datetime
from elasticsearch import Elasticsearch

elastic_host = '172.30.133.63'
elastic_port = 9200
elastic_timeout = 80


def elastic_setup():

    def create_api_logs_index(logs_index_name, **kwargs):
        settings = {
            'mappings': {
                'properties': {
                    'user': {'type': 'keyword'},
                    'token': {'type': 'keyword'},
                    'method': {'type': 'keyword'},
                    'base_url': {'type': 'text'},
                    'query_string': {'type': 'text'},
                    'url': {'type': 'text'},
                    'time': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd HH:mm:ss.SSS'
                    },
                }
            }
        }
        es = Elasticsearch(**kwargs)
        es.indices.delete(index=logs_index_name, ignore=404)
        es.indices.create(index=logs_index_name, body=settings)

    md.es_create_indexes('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
                         hosts=[{'host': elastic_host, 'port': elastic_port}])
    create_api_logs_index('emso-api', hosts=[{'host': elastic_host, 'port': elastic_port}])


def ingestion_68422():
    path = r"C:\Users\rbard\Documents\datos\68422\MO_TS_MO_68422.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_68422_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', '')
    if author:
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', '')
    if history:
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['site'] = 'hellenic'

    wf.metadata['parameters'] = []
    for parameter in wf.parameters:
        wf.metadata['parameters'].append(
            f"{parameter} - {wf.vocabulary[parameter]['long_name']} [{wf.vocabulary[parameter]['units']}]")
    wf.metadata['parameters'] = (', ').join(wf.metadata['parameters'])

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def intestion_antares():
    path = r'C:\Users\rbard\Documents\datos\antares\GL_TS_MO_ANTARES.nc'
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_ANTARES_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end [5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', '')
    if author:
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', '')
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)
    wf.metadata['site'] = "ligurian"

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_estoc():
    path = r"C:\Users\rbard\Documents\datos\estoc-c\GL_TS_MO_ESTOC.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")    

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_ESTOC_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact and contact != ' ':
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', '')
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', '')
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)
    wf.metadata['site'] = 'canarias'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_euxro01():
    path = r"C:\Users\rbard\Documents\datos\euxro01\BS_TS_MO_EUXRo01.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_EUXRo01_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)
    wf.metadata['site'] = 'black-sea'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_euxro02():
    path = r"C:\Users\rbard\Documents\datos\euxro02\BS_TS_MO_EUXRo02.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_EUXRo02_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)
    wf.metadata['site'] = 'black-sea'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_euxro03():
    path = r"C:\Users\rbard\Documents\datos\euxro03\BS_TS_MO_EUXRo03.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_EUXRo03_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['site'] = 'black-sea'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_exif0001():
    path = r"C:\Users\rbard\Documents\datos\exif0001\GL_TS_MO_EXIF0001.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_EXIF0001_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['site'] = 'azores'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_exif0002():
    path = r"C:\Users\rbard\Documents\datos\exif0002\GL_TS_MO_EXIF0002.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_EXIF0002_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact and contact != ' ':
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['site'] = 'black-sea'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_galway():
    path = r"C:\Users\rbard\Documents\datos\galway-coast-buoy\Galway-coast-buoy_2015-2019.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_Galway-coastal-buoy_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact and contact != ' ':
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', '')
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', '')
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)
    wf.metadata['geospatial_vertical_min'] = 0
    wf.metadata['geospatial_vertical_max'] = 1
    wf.metadata['site'] = 'smartbay'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_obsea():
    path = r"C:\Users\rbard\Documents\datos\obsea\OBSEA\MO_TS_MO_OBSEA.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_OBSEA_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', '')
    if author and author != '':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', '')
    if history and history != '':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['site'] = 'obsea'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_pap():
    path = r"C:\Users\rbard\Documents\datos\pap-1\GL_TS_MO_PAP-1.nc"
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_PAP-1_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['site'] = 'pap'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


def ingestion_w1m3a():
    path = r'C:\Users\rbard\Documents\datos\w1m3a\MO_TS_MO_W1M3A.nc'
    wf = md.read_nc_emodnet(path)

    # datetime object containing current date and time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Add metadata
    wf.metadata['network'] = 'emso'
    wf.metadata['data_source']: 'emodnet'

    time_coverage_start = wf.metadata.get('time_coverage_start','')
    time_coverage_end = wf.metadata.get('time_coverage_end','')
    if time_coverage_start and time_coverage_end:
        wf.metadata['id'] = f'OS_W1M3A_{time_coverage_start[0:4]}' \
            f'{time_coverage_start[5:7]}{time_coverage_end[0:4]}' \
            f'{time_coverage_end[5:7]}_D'

    contact = wf.metadata.get('contact', '')
    if contact:
        contact += ', help@emso-eu.org'
    else:
        contact = 'help@emso.eu'
    wf.metadata['contact'] = contact

    author = wf.metadata.get('author', False)
    if author and author != ' ':
        author += ', UTM (CSIC)'
    else:
        author = 'UTM (CSIC)'
    wf.metadata['author'] = author

    history = wf.metadata.get('history', False)
    if history and history != ' ':
        history += f', {now_string}: dataset reformated'
    else:
        history = f'{now_string}: dataset reformated'
    wf.metadata['history'] = history

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['parameters'] = (', ').join(wf.parameters)

    wf.metadata['site'] = 'ligurian'

    wf.to_es('emso-data', 'emso-metadata', 'emso-summary', 'emso-vocabulary',
             vocabulary_to_es=False, hosts=[{'host': elastic_host, 'port': elastic_port}],
             timeout=elastic_timeout)


if __name__ == '__main__':
    # print('elastic_setup')
    # elastic_setup()
    # print('ingestion_68422')
    # ingestion_68422()
    # print('intestion_antares')
    # HCSP, TEMP_DOXY
    # intestion_antares()
    # print('ingestion_estoc')
    # ingestion_estoc()
    # print('ingestion_euxro01')
    # ingestion_euxro01()
    # print('ingestion_euxro02')
    # ingestion_euxro02()
    # print('ingestion_euxro03')
    # ingestion_euxro03()
    # print('ingestion_exif0001')
    # ingestion_exif0001()
    print('ingestion_exif0002')
    ingestion_exif0002()
    print('ingestion_galway')
    ingestion_galway()
    print('ingestion_obsea')
    ingestion_obsea()
    print('ingestion_pap')
    ingestion_pap()
    print('ingestion_w1m3a')
    ingestion_w1m3a()
