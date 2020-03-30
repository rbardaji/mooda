# Obtain a MD5 code for every NetCDF of a folder and make their MD5 files

In this example, we have used data from the [Dyfamed observatory](https://www.seanoe.org/data/00326/43749/) with key: [70639](https://www.seanoe.org/data/00326/43749/data/70639.zip). We are going to create a MD5 file for each NetCDF file in the folder

```python
import mooda as md
import os

# Make a list of file locations
root = '/path/to/directory/'
nc_files = [os.path.join(root, filename)
         for root, _, filenames in os.walk(root)
         for filename in filenames
         if '.nc' in filename]

for nc_file in nc_files:
    print('Path:', nc_file)
    md5_code = md.md5(nc_file)
    print('MD5:', md5_code)
```

Output:

```shell
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_2014_D_TScurrents.nc
MD5: 36d6fc606a35dda0488b7576f2b2c514
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_2006_TSOF.nc
MD5: b68fe702c9ef5f9a0ff8aeaa2c40077f
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_2005_TSOF.nc
MD5: a58cdb52939023d595df064109d317c2
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_2010_D_SedimentTrap.nc
MD5: 0be1871ae964623347173d43f6031161
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_1996_FCO2TW.nc
MD5: ad861ed36d8d305fe6ba2b03abfa4371
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_1997_FCO2TW.nc
MD5: 61e412e872dcdcb51fe62d4294ddcc2e
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_2012_D_TSCTD.nc
MD5: 66d9df290967290cd947cd811b8b422b
Path: ./dyfamed/dyfamed-mooring/OS_DYFAMED_1998_TSOF.nc
MD5: d1d237845f866175973ba55ab8e6af6b
Path: ./dyfamed/dyfamed-mooring/DYF57_2017.nc
MD5: 30dd80a4c4c3369e6a7c98d8ff7bc6de
...
```

Return to the [Index of examples](index_examples.md).
