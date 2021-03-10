# How to calculate Absolute Salinity and Water Density

In this example we will use a NetCDF file from EMSO-Ligurian's DYFAMED platform. The original file can be found in [SeaNoe](https://www.seanoe.org/data/00326/43749/) and a compact version of the data in the EMSO ERIC File Explorer.

The DYFAMED platform is a moored surface buoy located at 43.826N, 9.111W. The complete metadata of the file is [here](https://data.emso.eu). The original file contains data from the following parameters:

* Dissolved Oxygen
* Bottom-top current component
* South-north current component
* Wesr-east current component
* Practical salinity
* Horizontal current speed
* Current to direction relative true north
* Practical salinity
* Sea temperature
* Sea pressure

As you know, metadata and parameters can also be printed from the code with ```print(wf.parameters)``` and ```print(wf.info_metadata()``` In this example we will not paint this information because without the output it is too long.

Water density is calculated from:

* Absolute salinity (ASAL)
* Sea temperature (TEMP)
* Sea pressure (PRES)

We have data on water temperature and pressure, but we lack absolute salinity values, in g/Kg. For this reason we will also have to calculate the Absolute salinity.

To calculate absolute salinity we need:

* Practical Salinity (PSAL)
* Water pressure (PRES)
* The sampling location (latitude, longitude)

The formulas for calculating absolute salinity and density are complex. Luckily, in mooda we import the [swg library](https://github.com/TEOS-10/GSW-Python) (thank you guys!), with which these calculations are done and then we package the results in our WaterFrame by adding the data quality control column.

In short, the following figure summarizes what we do in this example:

Here's the code:

```python
import mooda as md
import plotly

path = 'DYFAMED.nc'  # Location of the DYFAMED NetCDF file

wf = md.read_nc_emodnet(path=path)

# This function defaults to the columns PSAL, PRES,
# and the latitude and longitude that is in the
# metadata.last_latitude_observation and metadata.last_longitude_observation
wf.psal2asal()
# This function defaults to PSAL, TEMP, and PRES values
wf.asal_temp2dens()

print(wf)
```

Output:
```
Memory usage: 288.669 MBytes
Parameters:
  - PRES: Sea pressure (dbar)
    - Min value: 0.0
      - DEPTH: 200.0
      - TIME: 2012-07-28 19:00:00
    - Max value: 2306.048095703125
      - DEPTH: 2300.0
      - TIME: 2018-05-19 22:30:00
    - Mean value: 898.0645751953125
  - TEMP: Sea temperature (degrees_C)
    - Min value: 12.814001083374023
      - DEPTH: 200.0
      - TIME: 2010-01-22 06:00:01
    - Max value: 26.990001678466797
      - DEPTH: 200.0
      - TIME: 2012-07-28 20:00:00
    - Mean value: 13.354386329650879
  - HCDT: Current to direction relative true north (degree)
    - Min value: -177.38900756835938
      - DEPTH: 1010.0
      - TIME: 2018-03-19 04:00:00
    - Max value: 361.030029296875
      - DEPTH: 210.0
      - TIME: 2015-10-17 13:30:00
    - Mean value: 110.81519317626953
  - HCSP: Horizontal current speed (m s-1)
    - Min value: 0.0
      - DEPTH: 210.0
      - TIME: 2010-10-13 11:00:00
    - Max value: 2.3410000801086426
      - DEPTH: 200.0
      - TIME: 2012-07-28 22:00:00
    - Mean value: 0.040210939943790436
  - PSAL: Practical salinity (0.001)
    - Min value: 0.1940000057220459
      - DEPTH: 607.0
      - TIME: 2014-03-06 22:00:00
    - Max value: 39.19900131225586
      - DEPTH: 679.0
      - TIME: 2012-12-26 09:00:00
    - Mean value: 37.56760025024414
  - EWCT: West-east current component (m s-1)
    - Min value: -0.3020000159740448
      - DEPTH: 200.0
      - TIME: 2018-03-24 09:00:00
    - Max value: 0.26900002360343933
      - DEPTH: 200.0
      - TIME: 2018-03-16 02:30:00
    - Mean value: -0.016304045915603638
  - NSCT: South-north current component (m s-1)
    - Min value: -0.29200002551078796
      - DEPTH: 200.0
      - TIME: 2018-02-28 19:00:00
    - Max value: 0.4140000343322754
      - DEPTH: 200.0
      - TIME: 2018-03-03 08:30:00
    - Mean value: -0.007212391123175621
  - VCSP: Bottom-top current component (m s-1)
    - Min value: -0.12200000882148743
      - DEPTH: 210.0
      - TIME: 2010-11-01 02:00:00
    - Max value: 0.11300000548362732
      - DEPTH: 210.0
      - TIME: 2011-01-06 09:00:00
    - Mean value: -2.210260163337807e-06
  - DOX2: Dissolved oxygen (µmol kg-1)
    - Min value: 153.72300720214844
      - DEPTH: 382.0
      - TIME: 2015-04-02 18:00:00
    - Max value: 211.53001403808594
      - DEPTH: 350.0
      - TIME: 2018-02-14 19:00:00
    - Mean value: 184.86233520507812
  - ASAL: Absolute Salinity (g/kg)
    - Min value: 0.19492444218321797
      - DEPTH: 607.0
      - TIME: 2014-03-06 22:00:00
    - Max value: 39.38582464194125
      - DEPTH: 679.0
      - TIME: 2012-12-26 10:30:00
    - Mean value: 37.646703858025084
  - DENS: In-situ density (kg/m)
    - Min value: 1002.421021899315
      - DEPTH: 607.0
      - TIME: 2014-03-10 07:30:00
    - Max value: 1038.942522565931
      - DEPTH: 2300.0
      - TIME: 2018-05-19 22:30:00
    - Mean value: 1032.6838044116012
```

Return to the [Index of examples](index_examples.md).

