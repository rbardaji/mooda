# mooda.emso.get_metadata(*fields*=[], *metadata_ids*=[], *platform_codes*=[], *sites*=[])

## Reference

Get all fields of the metadatada archivements.

### Parameters

* fields: List of fields to return (List[str])
* metadata_ids: List of 'metadata_id' (List[str])
* parameters: List of 'prameter' (List[str])
* platform_codes: List of 'platform_code' (List[str])
* sites: List of 'site' (List[str])

### Returns

* metadatas: List of metadata archivements (List[dict])                

### Example

```python
import mooda as md
import pprint  # For nice printing

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

metadatas = emso.get_metadata()
for metadata in metadatas:      
    pprint.pprint(metadata)
```

Output:

```
{'Conventions': 'CF-1.6 OceanSITES-Manual-1.2 Copernicus-InSituTAC-SRD-1.4 '
                'Copernicus-InSituTAC-ParametersList-3.1.0',
 'area': 'Global Ocean',
 'author': 'Coriolis and Copernicus data provider, UTM (CSIC)',
 'cdm_data_type': 'Time-series',
...
...
...
            'de mesures provenant de capteurs sur une ligne instrumentee',
 'testOutOfDate': 'now-1day',
 'time_coverage_end': '2020-11-09T23:31:12Z',
 'time_coverage_start': '2019-07-20T12:29:58Z',
 'title': 'EMSO Ligure Ouest : ALBATROSS capteur MICROCAT (NetCDF files)'}
```

Return to [Index](../../index_api_reference.md).
