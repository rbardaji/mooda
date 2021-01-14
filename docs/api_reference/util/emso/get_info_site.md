# mooda.emso.get_info_site()

## Reference

Get available sites ('site') of the EMSO ERIC API.

### Returns

* sites: List of 'site' (List[str])

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
