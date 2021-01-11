# mooda.emso.get_info_fig_plot(*plot*)

## Reference

Get the available arguments for the input plot.

### Parameters

* plot: Figure type (str)

### Returns

* argument_list: List of available arguments (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

plot_list = emso.get_info_fig()
for plot_type in plot_list:
    arguments = emso.get_info_fig_plot(plot_type)
    print(plot_type, *arguments, sep='\n  - ')
```

Output:

```
line
  - platform_code
  - parameter
  - metadata_id
  - value_qc
  - depth_qc
  - time_qc
  - depth_min
  - depth_max
  - start_time
  - end_time
  - size
  - sort
  - x
  - y
  - title
  - color
  - rangeslider
  - line_type_sequence
  - output
data_interval
  - interval
  - platform_code
  - parameter
  - metadata_id
  - value_qc
  - depth_qc
  - time_qc
  - depth_min
  - depth_max
  - start_time
  - end_time
  - title
  - rangeslider
  - output
map
  - platform_code
  - site
  - parameter
  - output
```

Return to [Index](../../index_api_reference.md).
