# mooda.emso.get_fig_data_interval(*interval*=*'D'*, *depth_max*=*None*, *depth_min*=*None*, *depth_qcs*:=*[]*, *end_time*=*''*, *metadata_ids*=*[]*, *parameters*=*[]*, *platform_codes*=*[]*, *rangeslider*=*False*, *start_time*=*''*, *time_qcs*=*[]*, *title*=*''*, *value_qcs*=*[]*)

## Reference

Get the plotly figure 'Data Interval' from the EMSO ERIC API.

### Parameters

* interval: Period to find a data value (str)
* depth_max: Maximun depth of the measurement (int)
* depth_min: Minimum depth of the measurement (int)
* depth_qcs: List of QC values accepted for the depth_qc field (List[int])
* end_time: Maximum date of the measurement (str)
* metadata_ids: List of accepted 'metadata_id' (List[str])
* parameters: List of accepted 'parameter' (List[str])
* platform_codes: List of accepted 'platform_code' (List[str])
* rangeslider: Enable a range slider on to bottom of the graph (bool)
* start_time: Minimun date of the meassurement (str)
* time_qcs: List of accepted values for the field time_qc (List[int])
* title: Title of the figure (str)
* value_qcs: List of accepted values for the field of value_qc (List[int])

### Returns

* fig: Plotly figure (dict)

### Example

```python
import mooda as md
import plotly.io as pio

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

fig = emso.get_fig_data_interval(parameters=['TEMP'])
pio.show(fig)
```

Output:

![data_interval plot](../img_util/emso_data_interval_TEMP.png)

Return to [Index](../../index_api_reference.md).
