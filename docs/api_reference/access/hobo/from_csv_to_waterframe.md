# Hobo.from_csv_to_waterframe(*path*, *qc_tests*=*False*)

From mooda >= 0.3

It is a static method.

It creates a WaterFrame form data of the csv file of a HOBO logger.

## Parameters

    path: str
        Path where the csv is located.
    qc_tests: bool (optional)
        Make the QC test of the WaterFrame before return it.

## Returns

    wf: WaterFrame
        WaterFrame with the data and metadata of the source csv file.

## Example

For this example we use [hobo.csv](../../../data/hobo.csv)

```python
"""Example code"""
from mooda.access import Hobo


def example():
    """
    This example shows how to read data from a HOBO data file.
    """
    wf = Hobo.from_csv_to_waterframe("hobo.csv")
    print(wf)

example()

```
