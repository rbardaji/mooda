# WaterFrame.to_es(*data_index_name*=*'data'*, *metadata_index_name*=*'metadata'*, *summary_index_name*=*'summary'*, *qc_to_ingest*=*[0, 1]*, ***kwargs*)

## Reference

Injestion of the WaterFrame into a ElasticSeach DB.

## Parameters

* data_index_name: Name of the ElasticSearch index that contains the WaterFrame.data documents. (str)
* metadata_index_name: Name of the ElasticSearch index that contains the WaterFrame.metadata documents. (str)
* summary_index_name: Name of the ElasticSearch index that contains the summary documents. (str)
* summary_index_name: Name of the ElasticSearch index that contains the summary documents. (str)
* qc_to_intest: QC Flags of data to be ingested to the ElasticSearch DB. (list of int)
* **kwargs: [Elasticsearch object creation arguments](https://elasticsearch-py.readthedocs.io/en/master/index.html).

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201402.nc) and start an ElasticSearch service on localhost:9200.

```python
import mooda as md

path_netcdf = 'MO_TS_MO_OBSEA_201402.nc'  # Path of the NetCDF file

# Create a WaterFrame from the EMODnet NetCDF file.
wf = md.read_nc_emodnet(path_netcdf)

# Add some mandatory metadata information
wf.metadata['network'] = 'emodnet'

# Execute the following line to create the ElaticSearch indexes (just the first time)
# md.es_create_indexes()

wf.to_es()
```

Output:

```shell
ATMS from MO_TS_MO_OBSEA_201402 ingested: 0 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 1 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 2 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 3 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 4 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 5 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 6 of 628
ATMS from MO_TS_MO_OBSEA_201402 ingested: 7 of 628
...
```

Return to [mooda.WaterFrame](../waterframe.md).
