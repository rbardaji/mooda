# WaterFrame.info_metadata(*keys*=*None*)

## Reference

It returns a formatted string with the vocabulary information.

### Parameters

* keys: Keys of WaterFrame.vocabulary (str or list of str)

### Returns

* message: Message with the vocabulary information. (str)

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

print(wf.info_vocabulary())
```

Output:

```shell
  - TIME
    - valid_min: 0.0
    - valid_max: 90000.0
    - QC_indicator: 1
    - QC_procedure: 1
    - axis: T
    - long_name: Time
    - standard_name: time
  - TIME_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - POSITION_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - DEPH
    - axis: Z
    - positive: down
    - long_name: Depth
    - standard_name: depth
    - units: m
  - DEPH_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - ATMS
    - standard_name: air_pressure_at_sea_level
    - units: hPa
    - long_name: Atmospheric pressure at sea level
  - ATMS_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - CNDC
    - standard_name: sea_water_electrical_conductivity
    - units: S m-1
    - long_name: Electrical conductivity
  - CNDC_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - DRYT
    - standard_name: air_temperature
    - units: degrees_C
    - long_name: Air temperature in dry bulb
  - DRYT_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - PRES
    - long_name: Sea pressure
    - standard_name: sea_water_pressure
    - units: dbar
  - PRES_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - PSAL
    - standard_name: sea_water_practical_salinity
    - units: 0.001
    - long_name: Practical salinity
  - PSAL_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - SVEL
    - standard_name: speed_of_sound_in_sea_water
    - units: m s-1
    - long_name: Sound velocity
  - SVEL_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - TEMP
    - standard_name: sea_water_temperature
    - units: degrees_C
    - long_name: Sea temperature
  - TEMP_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - WDIR
    - standard_name: wind_from_direction
    - units: degree
    - long_name: Wind from direction relative true north
  - WDIR_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
  - WSPD
    - standard_name: wind_speed
    - units: m s-1
    - long_name: Horizontal wind speed
  - WSPD_QC
    - long_name: quality flag
    - conventions: OceanSITES reference table 2
    - valid_min: 0
    - valid_max: 9
    - flag_values: [0 1 2 3 4 5 6 7 8 9]
    - flag_meanings: no_qc_performed good_data probably_good_data bad_data_that_are_potentially_correctable bad_data value_changed not_used nominal_value interpolated_value missing_value
```

Return to [mooda.WaterFrame](../waterframe.md).
