# mooda.get_user_query(*size*=10, *sort*='desc')

## Reference

Get the queries of the user.

### Parameters

* size: Number of results [def: 10, max:10000] (int)
* sort: Order of the values [def: 'desc', options: 'asc', 'desc'] (str) 

### Returns

* query_list: List of the queries of the user (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

query_list = emso.get_user_query()
print(*query_list, sep='\n')
```

Output:
```
http://api.emso.eu/user/query?size=10&sort=desc
http://api.emso.eu/user/query?size=10&sort=desc
http://api.emso.eu/fig/data_interval/10d?rangeslider=false&parameter=TEMP
http://api.emso.eu/data?parameter=TEMP&platform_code=ANTARES,OBSEA&depth_min=10&depth_max=100&start_time=2016-05-08%2000%3A00%3A00&end_time=2020-06-09%2000%3A00%3A00&size=10&output=json
http://api.emso.eu/info/parameter?platform_code=ANTARES,OBSEA
http://api.emso.eu/info/parameter?platform_code=ANTARES
http://api.emso.eu/info/platform_code
http://api.emso.eu/fig/map
http://api.emso.eu/data?parameter=&platform_code=&depth_min=10&depth_max=100&start_time=1970-01-01%2000%3A00%3A00&end_time=1970-01-01%2000%3A00%3A00&size=10&output=json
http://api.emso.eu/data?parameter=&platform_code=&depth_min=10&depth_max=100&start_time=1970-01-01%2000%3A00%3A00&end_time=1970-01-01%2000%3A00%3A00&size=10&output=json
```

Return to [Index](../../index_api_reference.md).
