# mooda.es_create_indexes(*delete_previous_indexes*=*True*, ***kwargs*)

## Reference

Creation of ElasticSearch Indexes to save a WaterFrame object.

### Parameters

* data_index_name: Name of the ElasticSearch index that contains the WaterFrame.data documents. (str)
* metadata_index_name:  Name of the ElasticSearch index that contains the WaterFrame.metadata documents. (str)
* summary_index_name: Name of the ElasticSearch index that contains the summary documentation. (str)
* delete_previous_indexes: Delete previous indexes with the input names and all their documents. (bool)
* **kwargs: [Elasticsearch object creation arguments](https://elasticsearch-py.readthedocs.io/en/master/index.html).

### Returns

* success: If sucess is true, indexes where created. (bool)

## Example

To reproduce the example, install run an ElasticSeach server on localhost:9200.

```python
import mooda as md

done = md.es_create_indexes()

if done:
    print("Indexes created.")
```

Output:

```shell
Indexes created.
```

Return to [Index](../index_api_reference.md).