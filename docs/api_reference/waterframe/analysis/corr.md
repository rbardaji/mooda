# WaterFrame.corr(*parameter1*, *parameter2*, *method*=*'pearson'*, *min_periods*=*1*)

## Reference

Compute pairwise correlation of data columns of parameter1 and parameter2, excluding NA/null values.

### Parameters

* parameter1: Column name of *WaterFrame*.*data* to correlate. (str)
* parameter2: Column name of *WaterFrame*.*data* to correlate. (str)
* method: 'pearson', 'kendall' or 'spearman'. (str)
  * pearson: standard correlation coefficient
  * kendall: Kendall Tau correlation coefficient
  * spearman: Spearman rank correlation
* min_periods: Minimum number of observations required per pair of columns to have a valid result. Currently only available for Pearson and Spearman correlation. (int)

### Returns

* correlation_number: float

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it in the same python script folder.

```python
import mooda as md

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

print(f'Available parameters: {list(wf.parameters)}')

parameter1 = 'TEMP'  # Temperature
parameter2 = 'CNDC'  # Conductivity

print('Correlation factor between ',
      f"{wf.vocabulary.get(parameter1).get('long_name')} and ",
      f"{wf.vocabulary.get(parameter2).get('long_name')}: ",
      f"{wf.corr(parameter1, parameter2)}")
```

Output:

```shell
Available parameters: ['DEPH', 'ATMS', 'CNDC', 'DRYT', 'PRES', 'PSAL', 'SVEL', 'TEMP', 'WDIR', 'WSPD']
Correlation factor between  Sea temperature and  Electrical conductivity:  0.9745679306570474
```

Return to [mooda.WaterFrame](../waterframe.md).
