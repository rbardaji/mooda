# mooda.emso.get_info_fig()

## Reference

Get the available figures.

### Returns

* fig_list: List of available figures (List[str])

### Example

```python
import mooda as md

emso = md.util.EMSO(user='LOGIN', password='PASSWORD')

plot_list = emso.get_info_fig()
print(*plot_list, sep='\n')
```

Output:

```
line
data_interval
map
```

Return to [Index](../../index_api_reference.md).
