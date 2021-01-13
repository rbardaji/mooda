# mooda.emso.get_info_fig_plot_argument(*plot*, *argument*)

## Reference

Get argument information and available options.

### Parameters

* plot: Figure type (str)
* argument: Figure argument (str)

### Returns

* argument_info: (meaning of the argumnt, list of available options) (Tuple[str, List[str]])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

plot_list = emso.get_info_fig()
for plot_type in plot_list:
    print(plot_type)
    arguments = emso.get_info_fig_plot(plot_type)
    for argument in arguments:
        argument_info = emso.get_info_fig_plot_argument(plot_type, argument)
        print('  -', argument, '->', argument_info[0])
        for option in argument_info[1]:
            print('    -', option)
```

Output:

```
line
  - platform_code -> Available platform codes (platform_code)
    - 68422    
    - ALBATROSS
    - ANTARES  
    - ESTOC-C  
...
...
...
    - WDIR
    - WSPD
  - output -> Response output
    - html
    - json
```
Return to [Index](../../index_api_reference.md).
