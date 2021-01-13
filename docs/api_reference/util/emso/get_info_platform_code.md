# mooda.emso.get_info_platform_code(*parameters*=[], *sites*=[])

## Reference

Get available platfom codes ('platform_code') of the EMSO ERIC API.

### Parameters

* parameters: List of 'parameter' (List[str])
* sites: List of site (List[str])

### Returns

* platform_codes: List of 'platform_code' (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

platform_codes = emso.get_info_platform_code()
print(*platform_codes, sep='\n')
```

Output:

```
68422
ALBATROSS
ANTARES
ESTOC-C
EUXRo01
...
...
...
Marmara-BPR2
Marmara-BPR3
OBSEA
PAP-1
W1M3A
```

Return to [Index](../../index_api_reference.md).
