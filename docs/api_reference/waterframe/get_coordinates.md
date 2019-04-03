# WaterFrame.get_coordinates()

(mooda >= v0.3.0)

It returns the minimum and maximum coordinates placed in the metadata.

## Returns

    coordinates: tuple of tuples
        ((minimum latitude, minimum longitude, minimum depth), (maximum latitude, maximum longitude, maximum depth))

## Example

```python
from mooda import WaterFrame

# I downloaded the NetCDF file from
# http://193.144.35.225/emso_sites/data/obsea/OS_OBSEA_2016120120170426_R_37-14998.nc
NC_FILE = r"path to the netcdf"

wf = WaterFrame(NC_FILE)

coords = wf.get_coordinates()

print("Minimum latitude:", coords[0][0])
print("Minimum longitude:", coords[0][1])
print("Minimum depth:", coords[0][2])
print("Maximum latitude:", coords[0][2])
print("Maximum longitude:", coords[0][2])
print("Maximum depth:", coords[0][2])
```

Output:

    Minimum latitude: 41.182
    Minimum longitude: 1.752
    Minimum depth: 17.841
    Maximum latitude: 17.841
    Maximum longitude: 17.841
    Maximum depth: 17.841

Return to the [WaterFrame Index](index_waterframe.md).
