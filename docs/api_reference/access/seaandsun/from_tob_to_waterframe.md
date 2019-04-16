# SeaAndSun.from_txt_to_waterframe(*sensor_model*, *path*, *qc_tests*=*False*)

From mooda >= 0.4

It is a static method. It reads a TOB datalog file and returns a WaterFrame.

## Parameters

    path: str
        Path where the TOB files is.
    qc_tests: bool (optional, qc_tests=False)
        If true, it executes WaterFrame.qc().

## Returns

    wf: WaterFrame

## Example

For this example we used the [seaandsun.TOB](../../../data/seaandsun.TOB) data file.

```python
"""Example code"""
from mooda.access import Licor


def example():
    """
    This example shows how to read data from a Licor data file.
    """
    wf = SeaAndSun.from_tob_to_waterframe("seaandsun.TOB")
    print(wf)

example()
```

Output:

```bash
Memory usage: 63.80 KBytes

Parameters:
  - BATT: Remaining battery (Volt)
    - Min value: 1.420
    - Date min value: 2019-03-15 12:31:47.856000
    - Max value: 1.420
    - Date max value: 2019-03-15 12:31:47.856000
    - Mean value: 1.420
    - Values with QC = 1: 0.000 %
  - PRES: Sea water pressure (dBar)
    - Min value: 0.950
    - Date min value: 2019-03-15 12:31:56.492000
    - Max value: 9.440
    - Date max value: 2019-03-15 12:34:31.648000
    - Mean value: 3.097
    - Values with QC = 1: 0.000 %
  - TEMP: Sea water temperature (degree Celsius)
    - Min value: 13.640
    - Date min value: 2019-03-15 12:34:30.600000
    - Max value: 14.080
    - Date max value: 2019-03-15 12:32:25.536000
    - Mean value: 13.897
    - Values with QC = 1: 0.000 %
  - CNDC: Parameter without meaning
    - Min value: 44.910
    - Date min value: 2019-03-15 12:34:43.156000
    - Max value: 45.380
    - Date max value: 2019-03-15 12:32:36.520000
    - Mean value: 45.183
    - Values with QC = 1: 0.000 %
  - PSAL: Parameter without meaning
    - Min value: 38.090
    - Date min value: 2019-03-15 12:32:29.200000
    - Max value: 38.190
    - Date max value: 2019-03-15 12:32:47.516000
    - Mean value: 38.149
    - Values with QC = 1: 0.000 %
```

Return to the [SeaAndSun Index](./index_seaandsun.md).
