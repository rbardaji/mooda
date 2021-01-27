# mooda.widget_qc(*wf*, *parameter*, *range_test*=*[-1000, 1000]*, *spike_window*=*100*, *spike_threshold*=*3.5*, *spike_influence*=*0.5*)

## Reference

It makes a Data QC Widget for Jupyter Notebook.

### Parameters

* wf: WaterFrame
* parameter: Parameter (str)
* range_test: Limits for the range test [min value, max value] (List[float])
* spike_window: Window for the spike test (int)
* spike_threshold: Float for the spike test (float)
* spike_influence: Influence of the bad data on the spike test (float)

### Returns

* main_box: Jupyter notebook widget (ipwidgets.VBox)

## Example

To reproduce the example, download the pikle files [test_qc.pkl](https://github.com/rbardaji/mooda/blob/master/docs/examples/data/test_qc.pkl).

```python
import mooda as md

# Location of the dataset
path = r'docs\examples\data\test_qc.pkl'
# Read the dataset
wf = md.read_pkl(path)

gui = md.widget_qc(wf, 'TEMP', range_test=[0, 50])
gui
```

Output:

![Output qc widget](../img_util/qc_widget-widget.png)

Return to [Index](../../index_api_reference.md).
