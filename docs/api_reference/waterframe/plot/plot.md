# WaterFrame.plot(***kwds*)

## Reference

It calls the pandas DataFrame.plot() method.

### Parameters

* **kwds: All other plotting keyword arguments to be passed to [DataFrame.plot()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html#pandas.DataFrame.plot).

### Returns

* ax: Axes of the plot. (matplotlib.AxesSubplot)

## Example

To reproduce the example, download the NetCDF file [here](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201401.nc) and save it as `example.nc` in the same python script folder.

```python
import mooda as md
import matplotlib.pyplot as plt

path = "MO_TS_MO_OBSEA_201401.nc" # Path to the NetCDF file

wf = md.read_nc_emodnet(path)

wf.resample('H')

wf.plot(y=['TEMP', 'ATMS'])
plt.tight_layout()
plt.show()
```

Output:

![Plot example][plot-example]

Return to [mooda.WaterFrame](../waterframe.md).

[plot-example]: ../img_waterframe/plot-example.png
