# Licor.from_txt_to_waterframe(*sensor_model*, *path*, *qc_tests*=*False*)

From mooda >= 0.3

It is a static method. It reads a txt datalog file and returns a WaterFrame.
Be careful, the txt file uses to contain the datalog model but for this method, you need to provide the sensor model.

## Parameters

    model: str
        Model of the sensor.
    path: str
        Path of the txt file.
    qc_tests: bool (optional)
        It indicates if QC test should be passed.

## Returns

    wf: WaterFrame

## Example

For this example we used the [licor.txt](../../../data/licor.txt) data file.

```python
"""Example code"""
from mooda.access import Licor


def example():
    """
    This example shows how to read data from a Licor data file.
    """
    wf = Licor.from_txt_to_waterframe(model="LI-192", path="licor.TXT")
    print(wf)

example()
```

Return to the [Licor Index](./index_licor.md).
