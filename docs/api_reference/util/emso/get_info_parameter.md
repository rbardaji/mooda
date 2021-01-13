# mooda.emso.post_user_email(*message*)

## Reference

Get available parameters of the EMSO ERIC API.

### Parameters

* platform_codes: List of platform_code (List[str])
* sites: List of site (List[str])

### Returns

* parameters: RList of 'parameter' (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

parameters = emso.get_info_parameter()
print(*parameters, sep='\n')
```

Output:

```
ALTS - Altitude [meter]
ATMS - Atmospheric pressure at sea level [hPa]
CNDC - Electrical conductivity [S m-1]
DENS - Sea water density [kg m-3]
DEWT - Dew point temperature [degrees_C]
...
...
...
VTPK - Wave period at spectral peak / peak period (Tp) [s]
VTZM - Period of the highest wave (Thmax) [s]
VZMX - Maximum zero crossing wave height (Hmax) [m]
WDIR - Wind from direction relative true north [degree]
WSPD - Horizontal wind speed [m s-1]
```
Return to [Index](../../index_api_reference.md).
