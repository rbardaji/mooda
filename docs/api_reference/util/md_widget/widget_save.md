# mooda.widget_save(*wf*)

## Reference

It make a Jupyter notebook widget that allows to save the WaterFrame to a file.

### Parameters

* wf: WaterFrame

### Returns

* main_box: Jupyter notebook widget (ipwidgets.VBox)

## Example

```python
import mooda as md

wf = md.WaterFrame()

gui = md.widget_save(wf)
gui
```

Output:

![Output save widget](../img_util/output-save-widget.png)

Return to [Index](../../index_api_reference.md).
