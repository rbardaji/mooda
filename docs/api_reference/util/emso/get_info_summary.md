# mooda.emso.get_info_summary(*fields*=[], *parameters*=[], platform_codes=[], sites=[])

## Reference

Get the most used fields of the metadatada archivements.

### Parameters

* fields: List of fields to return (List[str])
* parameters: List of 'parameter' (List[str])
* platform_codes: List of 'platform_code' (List[str])
* sites: List of 'site' (List[str])

### Returns

* sumaries: List of metadata archivements (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

sites = emso.get_info_site()
print(*sites, sep='\n')
```

Output:

```
azores
black-sea
canarias
hellenic
ligurian
obsea
pap
smartbay
```

Return to [Index](../../index_api_reference.md).
