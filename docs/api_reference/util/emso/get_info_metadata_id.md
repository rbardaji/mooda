# mooda.emso.get_info_metadata_id(*platform_codes*=[], *sites*=[])

## Reference

Get the ID of the metadata archivements of the EMSO ERIC API.

### Parameters

* platform_codes: List of platform_code (List[str])
* sites: List of site (List[str])     

### Returns

* metadata_ids: List of 'metadata_id' (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

metadata_ids = emso.get_info_metadata_id()
print(*metadata_ids, sep='\n')
```

Output:

```
OS_PAP-1_200905201807_D
OS_Galway-coastal-buoy_201510201902_D
OS_EXIF0001_201009202004_D
OS_EXIF0002_201009202002_D
OS_W1M3A_200406201806_D
...
...
...
OS_68422_200711202004_D
OS_Marmara-BPR3_201905_TS
OS_Marmara-BPR2_201811201905_D
OS_Marmara-BPR1_201801201808_D
OS_ALBATROSS_201907202011_D
```

Return to [Index](../../index_api_reference.md).
