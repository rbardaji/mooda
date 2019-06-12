# WaterFrame.from_json(*self*, *json_string*)

(mooda >= v0.3.0)

It loads a WaterFrame object from a JSON string.

## Parameters

    json_string: str
        String that contains a JSON.

## Returns

    done: bool
        True if the operation is successful.

## Example

```python
from mooda import WaterFrame

# I downloaded the NetCDF file from
# http://193.144.35.225/emso_sites/data/obsea/OS_OBSEA_2016120120170426_R_37-14998.nc
NC_FILE = r"path to the netcdf"

wf = WaterFrame(NC_FILE)

json_string = wf.to_json()

wf2 = WaterFrame()
wf2.from_json(json_string)
# or simply add the json_string on the arguments of the WaterFrame creation
# wf2 = WaterFrame(json_string)
print(wf2)
```

Output:

    Memory usage: 44.02 MBytes

    Parameters:
    - PSAL: Salinity of the water column (PSU)
        - Min value: 35.685
        - Date min value: 2017-03-09 15:44:59
        - Max value: 38.114
        - Date max value: 2017-03-10 16:43:33
        - Mean value: 37.816
        - Values with QC = 1: 89.292 %
    - MPMN: Moored instrument depth (meters)
        - Min value: 17.841
        - Date min value: 2017-03-04 06:18:59
        - Max value: 19.879
        - Date max value: 2017-02-13 12:37:24
        - Mean value: 18.721
        - Values with QC = 1: 88.408 %
    - CNDC: Electrical conductivity of the water column (S/m)
        - Min value: 4.200
        - Date min value: 2017-03-09 15:44:59
        - Max value: 4.783
        - Date max value: 2017-04-20 02:08:44
        - Mean value: 4.471
        - Values with QC = 1: 79.588 %
    - TEMP:  Temperature of the water column (degree_Celsius)
        - Min value: 12.031
        - Date min value: 2017-02-06 15:57:34
        - Max value: 16.555
        - Date max value: 2017-04-20 02:08:34
        - Mean value: 13.767
        - Values with QC = 1: 90.076 %
    - SVEL: Sound velocity of the water column (meters/second)
        - Min value: 1499.917
        - Date min value: 2017-02-06 16:00:34
        - Max value: 1515.239
        - Date max value: 2017-04-20 02:08:44
        - Mean value: 1506.325
        - Values with QC = 1: 77.020 %

Return to the [WaterFrame Index](index_waterframe.md).
