# WaterFrame.info_metadata(*keys*=*None*)

## Reference

It returns a formatted string with the metadata information.

### Parameters

* keys: Keys of WaterFrame.metadata (str or list of str)

### Returns

* message: Message with the metadata information. (str)

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

print(wf.info_metadata())
```

Output:

```shell
- platform_code: OBSEA
- institution: SARTI Research Group. Electronics Dept. Universitat Politecnica de Catalunya (UPC)
- institution_edmo_code: 2150
- date_update: 2019-07-08T10:11:04Z
- site_code: OBSEA
- source: moored surface buoy
- history: 2018-01-18T13:39:07Z : Creation
- data_mode: R
- references: http://www.oceansites.org, http://marine.copernicus.eu
- id: MO_TS_MO_OBSEA_201401
- area: Mediterranean
- geospatial_lat_min: 41.182
- geospatial_lat_max: 41.182
- geospatial_lon_min: 1.75235
- geospatial_lon_max: 1.75235
- geospatial_vertical_min: -3.0
- geospatial_vertical_max: 21.0
- time_coverage_start: 2014-01-19T00:00:00Z
- time_coverage_end: 2014-01-31T23:00:00Z
- institution_references: http://www.obsea.es/, http://cdsarti.org/
- contact: Daniel Mihai Toma, daniel.mihai.toma@upc.edu, cmems-service@hcmr.gr
- author: Universitat Politecnica de Catalunya (UPC), Med ROOS data center (HCMR)
- pi_name: Joaquin del Rio, joaquin.del.rio@upc.edu
- update_interval: daily
- qc_manual: OceanSITES User's Manual v1.2
- data_type: OceanSITES time-series data
- netcdf_version: netCDF-4 classic model
- naming_authority: OceanSITES
- cdm_data_type: Time-series
- quality_control_indicator: 6
- distribution_statement: These data follow Copernicus standards; they are public and free of charge. User assumes all risk for use of data. User must display citation in any publication or product using data. User must contact PI prior to any commercial use of data.
- quality_index: A
- citation: These data were collected and made freely available by the Copernicus project and the programs that contribute to it
- format_version: 1.2
- Conventions: CF-1.6 OceanSITES-Manual-1.2 Copernicus-InSituTAC-SRD-1.4 Copernicus-InSituTAC-ParametersList-3.1.0
- title: Med Sea - NRT in situ Observations
- data_assembly_center: HCMR
- last_latitude_observation: 41.182
- last_longitude_observation: 1.75235
- last_date_observation: 2014-01-31T23:00:00Z
```

Return to [mooda.WaterFrame](../waterframe.md).
