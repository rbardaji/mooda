# Working with NetCDF data

For this example we need to download a NetCDF file from [EMODNET](http://www.emodnet-physics.eu/Map/). The file that we use is [here](/example_data/netcdf_example.nc). The file contains mooring time series.

First, we import the necessary libraries.

```python
import matplotlib.pyplot as plt
import matplotlib.style as style
from oceanobs import inwater
```

Let's use the "ggplot" style to generate the graphics.

```python
style.use('ggplot')
```

Now, let's open the NetCDF file.

```python
path = r"netcdf_example.nc" # Write here the path of the data file to load.
wf = inwater.WaterFrame(path)
```

Let's see what the WaterFrame object contains.

```python
print(wf.info())
```

    Update Interval: daily
    Data Type: OceanSITES time-series data
    Geospatial Lon Max: 2.7004
    Last Date Observation: 2017-05-28T23:00:00Z
    Geospatial Vertical Max: 30.0
    References: http://www.oceansites.org, http://marine.copernicus.eu
    Distribution Statement: These data follow Copernicus standards; they are public and free of charge. User assumes all risk for use of data. User must display citation in any publication or product using data. User must contact PI prior to any commercial use of data.
    Summary
    - nsct_16.0
     - Long Name: South-north current component
     - Units: m s-1
     - Standard Name: northward_sea_water_velocity
     - Depth: 16.0 m
    - dewt
     - Long Name: Dew point temperature
     - Units: degrees_C
     - Standard Name: dew_point_temperature
     - Depth: 0.0 m
    - temp_1.0
     - Long Name: Sea temperature
     - Units: degrees_C
     - Standard Name: sea_water_temperature
     - Depth: 1.0 m
    ...
	...
	...
	- temp_1.5
		- Long Name: Sea temperature
		- Units: degrees_C
		- Standard Name: sea_water_temperature
		- Depth: 1.5 m
	...
	...
	...


As you can see in the summary, the WaterFrame contains two time series of temperature. A measurement at 1 meter depth (temp_1.0) and another at 1.5 meters (temp_1.5).

Let's create a graph with the temperature data. We assign the parameter of *join* to **True** to join the two time series in the same chart.


```python
wf.plot(param="temp", join=True)
plt.show()
```


![temp_1.0_1.5](/img/examples/netcdf/temp_1.0_1.5.png)


Now we are going to focus on a time series. For example, we will use "temp_1.0".
When we create a graph of that parameter, we see information about QC.


```python
wf.plot(param="temp_1.0")
plt.show()
```


![temp_1.0](/img/examples/netcdf/temp_1.0.png)


As can be seen, the data of "temp_1.0" contain the values of QC = 0, indicating that they have not passed through a QC process. We will recalculate the [QC flags](#note-qc-flags).


```python
wf.qc(param="temp_1.0")
```

And now, we generate the graph again.


```python
wf.plot(param="temp_1.0")
plt.show()
```


![temp_1.0_qc](/img/examples/netcdf/temp_1.0_qc.png)


Here you have the complete example source code.

```python
import matplotlib.pyplot as plt
import matplotlib.style as style
from oceanobs import inwater

style.use('ggplot')

path = r"netcdf_example.nc" # Write here the path of the data file to load.
wf = inwater.WaterFrame(path)

print(wf.info())

wf.plot(param="temp", join=True)
plt.show()

wf.plot(param="temp_1.0")
plt.show()

wf.qc(param="temp_1.0")

wf.plot(param="temp_1.0")
plt.show()
```

# Working with pickle data

For this example we are going to use the pickle file from [here](/example_data/pickle_example.pkl).

First, we import the necessary libraries.

```python
import matplotlib.pyplot as plt
import matplotlib.style as style
from oceanobs import inwater
```

Let's use the "ggplot" style to generate the graphics.

```python
style.use('ggplot')
```

Now, let's open the pickle file.

```python
path = r"pickle_example.pkl" # Write here the path of the data file to load.
wf = inwater.WaterFrame(path)
```

Let's see what the WaterFrame object contains.


```python
print(wf.info())
```

    CDM Data Type: Time-series
    Summary
    - temp_37-14998
     - Units: degree Celsius
     - Standard Name: sea_water_temperature
     - Long Name: Sea water temperature
     - Observatory: EMSODEV-EGIM-node00001
     - Instrument: 37-14998
    Citation: These data were collected and made freely available by the EMSODEV project and the programs that contribute to it.
    Distribution Statement: These data follow Copernicus standards; they are public and free of charge. User assumes all risk for use of data. User must display citation in any publication or product using data. User must contact PI prior to any commercial use of data.
    References: http://www.emsodev.eu/, http://www.emso-eu.org/
    Source: Underwater observatory
    QC Manual: OceanSITES User's Manual v1.2
    Data Type: OceanSITES time-series data

As you can see in the summary, the WaterFrame contains a time series of temperature. We are going to analyze it making a graph.

```python
wf.plot(param="temp_37-14998")
plt.show()
```

![temp_ctd](/img/examples/pickle/temp_ctd.png)

As can be seen, data contain the values of QC = 0, indicating that they have not passed through a QC process. We will recalculate the [QC flags](#note-qc-flags).

```python
wf.qc()
```

And now, we generate the graph again.


```python
wf.plot(param="temp_37-14998")
plt.show()
```


![temp_ctd_qc](/img/examples/pickle/temp_ctd_qc.png)


Here you have the complete example source code.

```python
import matplotlib.pyplot as plt
import matplotlib.style as style
from oceanobs import inwater

style.use('ggplot')

path = r"pickle_example.pkl" # Write here the path of the data file to load.
wf = inwater.WaterFrame(path)

print(wf.info())

wf.plot(param="temp_37-14998")
plt.show()

wf.qc()

wf.plot(param="temp_37-14998")
plt.show()
```

> ### Note: QC Flags
> In a WaterFrame, time series of scientific data are stored inside the variable data (in the case of the example, wf.data). Each data has associated a Quality Control value. 
> Data Quality Control procedures are important for:

> * Detecting missing mandatory information
> * Detecting errors made during the transfer or reformatting
> * Detecting duplicates
> * Detecting remaining outliers (spikes, out of scale data, vertical instabilities etc)
> * Attaching a quality flag to each numerical value in order to modify the observed data points

> The QC Flags that we use are the following:

> QC Flag | Meaning
> ---|---
> 0 | No Quality Control
> 1 | Value seems correct
> 2 | Value appears inconsistent with other values
> 3 | Value seems doubtful
> 4 | Value seems erroneous
> 5 | Value was modified
> 6 | Flagged land test
> 7 | Nominal value
> 8 | Interpolated value
> 9 | Missing value

# Downloading EGIM data

To download data from an EGIM lab, you only need to call the *EGIM* class of the *inwater* module.

```python
from oceanobs import inwater

# input parameters
login_in = "YOUR EMSODEV LOGIN" # Write here your login.
password_in = "YOUR EMSODEV PASSWORD" # Write here your password.
# Name or list of names of observatories where you want to download data.
observatory_in = "all"
# Name or list of names of the instruments that you want to download data. 
instrument_in = "37-14998" 
# Name or list of names of the parameters that you want to download data.
parameter_in = "all" 
start_in = "01/02/2017" # Start date to download data.
end_in = "03/02/2017" # End date to download data.
path_in = "./egim_data.pkl" # Where to save data.

# Call to the class EGIM.
inwater.EGIM(login=login_in, password=password_in, observatory=observatory_in, 
	instrument=instrument_in, parameter=parameter_in, start=start_in, 
	end=end_in, path=path_in)

print("Done!")
```

# Open the GUI

With the graphical interface you can do almost the same thing as programming a script. You can use it with just four line of code.

```python
from oceanobs import mooda

login_in = "YOUR EMSODEV LOGIN"
password_in = "YOUR EMSODEV PASSWORD"

mooda.open(login=login_in, password=password_in) 
```
