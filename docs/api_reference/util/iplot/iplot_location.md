# mooda.iplot_location(*list_wf*)

## Reference

It creates a Plotly Figure with a map and a spot of the measurement location of the input WaterFrames.

### Parameters

* list_wf: List of WaterFrames to be concatenated. (List of WaterFrames)

### Returns

* figure: Dictionary of Plotly figure. (dict)

## Example

To reproduce the example, download the NetCDF files [MO_TS_MO_OBSEA_201401.nc](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA_201401.nc) and [MO_TS_MO_OBSEA_201402.nc](http://data.emso.eu/files/emso/obsea/mo/ts/MO_TS_MO_OBSEA_201402.nc).

```python
import mooda as md
import plotly.graph_objects as go

path = "MO_TS_MO_OBSEA_201401.nc"

wf = md.read_nc_emodnet(path)
list_wf = [wf]

fig = md.iplot_location(list_wf)
go.Figure(fig).show()
```

Output:

![iPlot location example][iplot-location]

*Note: This image is NOT the real output. This image is the output, saved in PNG.*

Return to [mooda.WaterFrame](../../index_api_reference.md).

[iplot-location]: ../img_util/iplot_location_example.png
