# mooda.widget_emso(*wf*, *depth_range*=*[-10, 10000]*, *user*=*''*, *password*=*''*, *token*=*''*)

## Reference

It makes a Jupyter notebook widget to download data from the EMSO API.

### Parameters

* wf: WaterFrame
* depth_range: Range of depth (List[float])
* user:  User for the EMSO ERIC API (str)
* password:  Password for the EMSO ERIC API (str)
* token: Token for the EMSO ERIC API (str)

### Returns

* main_box: Jupyter notebook widget (ipwidgets.VBox)

## Example

```python
import mooda as md

wf = md.WaterFrame()

gui = md.widget_emso(wf)
gui
```

Output:

![EMSO map](../img_util/emso-map.png)
![Output emso widget](../img_util/widget-emso.png)

Return to [Index](../../index_api_reference.md).
