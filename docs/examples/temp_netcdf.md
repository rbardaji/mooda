# Analyze a water temperature time series from netCDF files

In this example, we will discover if the average temperature of the sea water near Tarragona (Spain) has increased or decreased in recent years. To load and analyze the data we use the WaterFrame object of the oceanobs package and the following functions:

* [WaterFrame.from_netcdf()](../api.md#WaterFrame.from_netcdf(*path*))
* [WaterFrame.parameters()](../api.md#WaterFrame.parameters())
* [WaterFrame.memory_usage()](../api.md#WaterFrame.memory_usage())
* [WaterFrame.only_use()](../api.md#WaterFrame.use_only(*parameters*,_*flags*=*None*,_*dropnan*=*False*))
* [WaterFrame.slice()](../api.md#WaterFrame.slice(*start*,_*end*))
* [WaterFrame.barplot()](../api.md#WaterFrame.barplot(*key*,_*ax*=*None*,_*average_time*=*None*))

Data comes from a netCDF file of [EMODnet](http://www.emodnet.eu/). EMODnet is a network of organizations that make marine data with European format standards (such as SeaDataNet netCDF standards) freely available. For this example, we have to download the "reprocessed data" from 1992 to 2018 of the [Tarragona-coast-buoy](http://www.emodnet-physics.eu/map/platinfo/piroosdownload.aspx?platformid=28150). You need to register (it is free!) to download the file but you don't want to sign in EMODnet, you can download a monthly period.

Customarily, we import as follows:

```python
import oceanobs as oc
import matplotlib.pyplot as plt
```

This is optional, but I like to use the plot style 'ggplot'.

```python
import matplotlib.style as style
style.use('ggplot')
```

Now we create the WaterFrame object and load data from file path location. In our case, we have the file in the same folder of the python script.

```python
wf = oc.WaterFrame()
wf.from_netcdf("IR_TS_MO_Tarragona-coast-buoy.nc")
```

The file contains the parameter "seawater temperature" with the name "TEMP," but it also has other parameters. In fact, the file contains so many parameters that consume a lot of memory.

```python
print("Parameters:", wf.parameters())
print("Memory usage:", wf.memory_usage()/10**6, "MBytes")
```

Output:

```bash
Parameters: ['VAVH', 'TEMP', 'VT110', 'VHM0', 'VHZA', 'VZMX', 'VAVT', 'VH110', 'VMDR', 'VTPK', 'VTZA', 'VTM02']
Memory usage: 83.35604 MBytes
```

Since we only want to use the water temperature, we will eliminate other parameters to reduce the size of the object. Original data has already been processed by its source and data considered as good was marked with QC Flag = 1. We are only going to use the accurate data. We will also remove all NaN (Not a Number) values. Now the memory consumption of our object is much smaller.

```python
wf.use_only('TEMP', flags=1, dropnan=True)
print("Memory usage:", wf.memory_usage()/10**6, "MBytes")
```

Output:

```bash
Memory usage: 1.411648 MBytes
```

We need full year data to calculate the average annual temperature, so let's see what date the data starts and ends. The variable "data" of the WaterFrame object is a Pandas DataFrame so we can use all its functions and properties.

```python
print("Start:", wf.data.index[0])
print("End:", wf.data.index[-1])
```

Output:

```bash
Start: 2013-01-12 10:00:00
End: 2017-03-28 11:00:00
```

Now we know that we only have full years from 2013 to 2016. We are going to work with the complete years eliminating the data after 2016-12-31 23:59:59.

```python
wf.slice('20130101000000', '20161231235959')
```

Finally, we will create a bar graph with the annual average temperature.

```python
wf.barplot(key='TEMP', average_time='A')
plt.show()
```

Output:

<center>
    <figure>
        <img src="../img/examples/netcdf/annual_temp_Tarragona.png" alt="Module types of oceanobs">
        <figcaption> Figure 1: Module types of oceanobs </figcaption>
    </figure>
</center>

The output of the WaterFrame.barplot function is a matplotlib.AxesSubplot so you could stylize the figure with the functions and properties of matplotlib.

From the graph, we can conclude that the average annual water temperature on the coast of Tarragona seems to tend to increase although we have very few data to be able to affirm it. The year with the lowest average temperature was 2013, with 18.6 ºC and the year with the highest average temperature was 2014, with 19.2 ºC.

The complete code:

```python
import oceanobs as oc
import matplotlib.pyplot as plt
import matplotlib.style as style

style.use('ggplot')

wf = oc.WaterFrame()
wf.from_netcdf("IR_TS_MO_Tarragona-coast-buoy.nc")

print("Parameters:", wf.parameters())
print("Memory usage:", wf.memory_usage()/10**6, "MBytes")

wf.use_only('TEMP', flags=1, dropnan=True)
print("Memory usage:", wf.memory_usage()/10**6, "MBytes")

print("Start:", wf.data.index[0])
print("End:", wf.data.index[-1])

wf.slice('20130101000000', '20161231235959')

wf.barplot(key='TEMP', average_time='A')
plt.show()
```
