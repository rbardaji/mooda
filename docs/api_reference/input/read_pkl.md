# mooda.read_pkl(*path_pkl*)

## Reference

Get a WaterFrame from a pickle file.

### Parameters

path_pkl: Location of the pickle file. (str)

### Returns

wf_pkl: WaterFrame

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it as `example.nc` in the same pyhon script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

# Save wf into a pickle file
wf.to_pkl('example.pkl')

# Get a WaterFrame from a fickle file
wf_from_pickle = md.read_pkl('example.pkl')
print(wf_from_pickle)
```

Output:

```
Memory usage: 14.888 MBytes
Parameters:
  - DEPH: Depth (m)
    - Min value: -3.0
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-19 00:00:00
    - Max value: 21.0
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-19 00:00:00
    - Mean value: 9.0
  - ATMS: Atmospheric pressure at sea level (hPa)
    - Min value: 992.8800471592695
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-19 04:00:00
    - Max value: 1019.9700484459754
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-26 08:00:00
    - Mean value: 1006.2074644589545
  - CNDC: Electrical conductivity (S m-1)
    - Min value: 4.420000209938735
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-19 17:00:00
    - Max value: 4.510000214213505
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-22 11:00:00
    - Mean value: 4.472166879083185
  - DRYT: Air temperature in dry bulb (degrees_C)
    - Min value: 3.9300001866649836
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-30 03:00:00
    - Max value: 15.230000723386183
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-26 10:00:00
    - Mean value: 8.11604205215796
  - PRES: Sea pressure (dbar)
    - Min value: 19.39
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-26 22:00:00
    - Max value: 19.73
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-30 07:00:00
    - Mean value: 19.570583333333335
  - PSAL: Practical salinity (0.001)
    - Min value: 38.07000180822797
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-30 13:00:00
    - Max value: 38.210001814877614
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-19 00:00:00
    - Mean value: 38.148585145293815
  - SVEL: Sound velocity (m s-1)
    - Min value: 1504.1000714409165
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-19 17:00:00
    - Max value: 1506.9400715758093
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-22 14:00:00
    - Mean value: 1505.733613185172
  - TEMP: Sea temperature (degrees_C)
    - Min value: 12.94000061461702
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-19 17:00:00
    - Max value: 13.820000656414777
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-01-22 14:00:00
    - Mean value: 13.452292305616234
  - WDIR: Wind from direction relative true north (degree)
    - Min value: 22.300001059193164
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-22 14:00:00
    - Max value: 335.72001594584435
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-29 23:00:00
    - Mean value: 245.3161783185593
  - WSPD: Horizontal wind speed (m s-1)
    - Min value: 1.0500000498723239
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-19 21:00:00
    - Max value: 17.77000084402971
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-01-27 15:00:00
    - Mean value: 7.082708669743927
```

Return to [API reference](../index_api_reference.md).
