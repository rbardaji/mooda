# Bodc.from_nc_to_waterframe(*path*)

From mooda >= 0.5

It is a static method.

It creates a WaterFrame form data of the nc  file from BODC.

## Parameters

    path: str
        Path where the csv is located.

## Returns

    wf: WaterFrame
        WaterFrame with the data and metadata of the source csv file.

## Example

For this example we use [pap-bodc-ctd_200706212003_201706212129.nc](http://data-test.emso.eu/files/emso/pap/bodc/ctd/48.9990N_16.5020W/2017/06/21/pap-bodc-ctd_200706212003_201706212129.nc)

```python
"""Example code"""
from mooda.bodc import Bodc


def example():
    """
    This example shows how to read data from a NetCDF of BODC.
    """
    wf = Bodc.from_nc_to_waterframe("pap-bodc-ctd_200706212003_201706212129.nc")
    print(wf)

example()

```

Output:

    Memory usage: 6.46 KBytes

    Parameters:
    - PSAL: P_sal_CTD_uncalib (Dmnless)
        - Min value: 35.565
        - PRES min value: 22.0
        - Max value: 35.702
        - PRES max value: 68.0
        - Mean value: 35.629
        - Values with QC = 1: 100.000 %
    - SIGTEQST: Sigma-T (kg/m^3)
        - Min value: 26.345
        - PRES min value: 6.0
        - Max value: 27.113
        - PRES max value: 267.0
        - Mean value: 26.960
        - Values with QC = 1: 100.000 %
    - TEMP: Temp (degC)
        - Min value: 11.740
        - PRES min value: 268.0
        - Max value: 15.282
        - PRES max value: 6.0
        - Mean value: 12.591
        - Values with QC = 1: 100.000 %

Return to the [Bodc Index](index_bodc.md).