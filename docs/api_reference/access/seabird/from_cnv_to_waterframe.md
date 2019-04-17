# SeaBird.from_cnv_to_waterframe(*path*, *qc_tests*=*False*)

From mooda >= 0.4

It is a static method. It reads a cnv datalog file and returns a WaterFrame.

## Parameters

    path: str
        Path where the TOB files is.
    qc_tests: bool (optional, qc_tests=False)
        If true, it executes WaterFrame.qc().

## Returns

    wf: WaterFrame

## Example

For this example we used the [seabird.cnv](../../../data/seabird.cnv) data file.

```python
"""Example code"""
from mooda.access import SeaBird


def example():
    """
    This example shows how to read data from a SBE25 data file.
    """
    wf = SeaBird.from_cnv_to_waterframe("seabird.cnv")
    print(wf)

example()
```

Output:

```bash
Memory usage: 1.42 MBytes

Parameters:
  - PRES: Strain Gauge Pressure (db)
    - Min value: -0.084
    - Date min value: 2019-03-15 08:26:41.250000
    - Max value: 79.507
    - Date max value: 2019-03-15 08:51:29.375000
    - Mean value: 27.583
    - Values with QC = 1: 0.000 %
  - TEMP: Sea Water Temperature (deg C)
    - Min value: 13.277
    - Date min value: 2019-03-15 08:51:28.125000
    - Max value: 15.267
    - Date max value: 2019-03-15 08:26:43.250000
    - Mean value: 13.697
    - Values with QC = 1: 0.000 %
  - PSAL: Turbidity (FTU)
    - Min value: 0.000
    - Date min value: 2019-03-15 08:26:35
    - Max value: 39.628
    - Date max value: 2019-03-15 08:27:02.250000
    - Mean value: 37.308
    - Values with QC = 1: 0.000 %
  - TUR4: Parameter without meaning
    - Min value: 0.000
    - Date min value: 2019-03-15 08:26:35
    - Max value: 24.042
    - Date max value: 2019-03-15 08:54:39.875000
    - Mean value: 0.345
    - Values with QC = 1: 0.000 %
  - FLUO: Fluorescence (mg/m^3)
    - Min value: -0.462
    - Date min value: 2019-03-15 08:26:35
    - Max value: 29.142
    - Date max value: 2019-03-15 08:54:43
    - Mean value: 0.220
    - Values with QC = 1: 0.000 %
  - CNDC: Conductivity (mS/cm)
    - Min value: -0.000
    - Date min value: 2019-03-15 08:26:43.500000
    - Max value: 46.593
    - Date max value: 2019-03-15 08:27:02.250000
    - Mean value: 43.973
    - Values with QC = 1: 0.000 %
```

Return to the [SeaAndSun Index](./index_seabird.md).
