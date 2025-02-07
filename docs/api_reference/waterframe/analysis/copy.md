# WaterFrame.copy()

## Reference

It returns a copy of the WaterFrame.

### Returns

* new_wf: A copy of the WaterFrame (WaterFrame).

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md

path_netcdf = "example.nc"  # Path of the NetCDF file

wf = md.read_nc(path_netcdf)

wf2 = wf.copy()
print(wf2)
```

Output:

```shell
Memory usage: 142.443 MBytes
Parameters:
  - DEPH: Depth (m)
    - Min value: -3.0
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-01 00:00:00
    - Max value: 21.0
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-01 00:00:00
    - Mean value: 9.0
  - ATMS: Atmospheric pressure at sea level (hPa)
    - Min value: 1006.8800478242338
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-14 05:00:00
    - Max value: 1025.4900487081613
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-01 09:00:00
    - Mean value: 1017.5967096494596
  - CNDC: Electrical conductivity (S m-1)
    - Min value: 5.170000245561823
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-30 08:00:00
    - Max value: 5.3300002531614155
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-01 00:00:00
    - Mean value: 5.273734224847897
  - DRYT: Air temperature in dry bulb (degrees_C)
    - Min value: 15.91000075568445
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-23 05:00:00
    - Max value: 28.32000134512782
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-25 15:00:00
    - Mean value: 20.34341990687051
  - PRES: Sea pressure (dbar)
    - Min value: 19.72
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-03 07:00:00
    - Max value: 20.01
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-27 08:00:00
    - Mean value: 19.84277243589743
  - PSAL: Practical salinity (0.001)
    - Min value: 37.700001790653914
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-01 22:00:00
    - Max value: 38.13000181107782
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-21 03:00:00
    - Mean value: 37.96530629043469
  - SVEL: Sound velocity (m s-1)
    - Min value: 1525.3400724497624
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-30 13:00:00
    - Max value: 1529.8600726644509
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-01 00:00:00
    - Mean value: 1528.1274283513858
  - TEMP: Sea temperature (degrees_C)
    - Min value: 20.0500009523239
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-30 12:00:00
    - Max value: 21.860001038294286
      - DEPTH: 1
      - POSITION: 0
      - TIME: 2014-10-01 00:00:00
    - Mean value: 21.11221254123777
  - WDIR: Wind from direction relative true north (degree)
    - Min value: 0.5700000270735472
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-28 23:00:00
    - Max value: 359.9000170943327
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-02 21:00:00
    - Mean value: 214.56036012377496
  - WSPD: Horizontal wind speed (m s-1)
    - Min value: 0.28000001329928637
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-09 09:00:00
    - Max value: 141420.00671708956
      - DEPTH: 0
      - POSITION: 0
      - TIME: 2014-10-03 19:00:00
    - Mean value: 22843.48113884289
```

Return to [mooda.WaterFrame](../waterframe.md).
