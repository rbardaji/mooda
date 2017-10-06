# inwater

Data access and analysis module.

## - *class* **WaterFrame**

Class to manage data series from marine observatories. The compatible input data are from the following observatories:

* [EMSO](http://www.emso-eu.org/) Generic Instrument Module ([EGIM](http://www.emsodev.eu)) in pickle file format.

* [OBSEA](http://www.upc.edu/cdsarti/OBSEA/) in text files with CSV format.

* [EMODNET](http://www.emodnet-physics.eu/Map/) and [JERICO](http://www.jerico-ri.eu/data-access/) in [NetCDF](http://www.oceansites.org/data/) format.

The scientific data is saved into the instance variable *data* and the technical data (e.g. voltage of sensors) is saved into the instance variable *technical*.

The variable *data* is a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) that contains keys with QC flags (e.g. temp_qc is the key that contains the QC flags of the key temp). 

### - \_\_init\_\_(*path*=**None**)

Constructor. It creates the following instance variables:

* data: [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) with scientific values.
* metadata: Dictionary with metadata information.
* technical: [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) with instrumental values (e.g. voltage and current consumption of sensors). 
* acronym: Dictionary with the meaning of the keys of the *data* variables.

### - from_netcdf(*path*)

It loads data from a [NetCDF](http://www.oceansites.org/data/) file. It adds data values into the variable *data* and the metadata information into *metadata*.

Input | Description | Type
--- | --- | ---
path | It is the path of the [NetCDF](http://www.oceansites.org/data/) file. | string

### - from_csv(*path*)

It loads data from a text file with a CSV format. It adds data values into the variable *data* and creates the metadata information. The CSV file comes from [OBSEA](http://www.upc.edu/cdsarti/OBSEA/) and the metadata information contains predefined information added by code.

Input | Description | Type
--- | --- | ---
path | It is the path of the CSV file. | string

### - from_pickle(*path*)

It loads data from a pickle file. It copies the *data*, *metadata*, *technical* and *acronym* from the *WaterFrame* object of the pickle file to the instance variables.

Input | Description | Type
--- | --- | ---
path | It is the path of the pickle file. | string

### - plot(*param*, *join*=**False**)

It creates the figure of the input parameter.

Input | Description | Type
--- | --- | ---
param | Key of the *data* or *technical* variable to plot. | string
join | Some keys are similar, but with suffixes (i.e. temp_1, temp_2). If *join* = **True**, the figure will contain all the similar keys. | bool

Return | Description | Type
--- | --- | ---
fig | Figure with the graph. | [matplotlib.figure](https://matplotlib.org/api/figure_api.html)

### - plot_ts(*name_temp*)

It creates a [TS diagram](https://en.wikipedia.org/wiki/Temperature_vs._specific_entropy_diagram).

Input | Description | Type
--- | --- | ---
name_temp | Key of the *data* variable that contains the temperature values. | string

Return | Description | Type
--- | --- | ---
fig_ts | Figure with the graph. | [matplotlib.figure](https://matplotlib.org/api/figure_api.html)

### - predefined_plot(*name*, *average_time*=**'W'**)

It creates some basic technical plots. This function is useful if you are using  technical data from an [EGIM](http://www.emsodev.eu).

Input | Description | Type
--- | --- | ---
name | Name of the plot. Options: *current_slots*, *temperature* and *sd*. | string
average_time | It resamples and averages the *technical* data according to the input [rule](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases). | string

Return | Description | Type
--- | --- | ---
fig | Figure with the graph. | [matplotlib.figure](https://matplotlib.org/api/figure_api.html)

### - qc(*param*=**None**, *influencer*=**0.7**)

It analyzes the values of the variable *data* and changes the QC flags from 0 to the corresponding number.

Input | Description | Type
--- | --- | ---
param | Key of *data* to analyze. If *data* = **None**, all keys will be analyzed. | string
influencer | Influence of erroneous values for in the QC algorithm. **0** means that the algorithm will ignore the erroneous values and **1** means that the algorithm will use the values. The between values means that the algorithm will use some percent of the value. | float
threshold | A threshold of X will signal if a datapoint is X standard deviations away from the moving mean. It is used for the spike procedure. | float
multiplier | The multiplier value to calculate the maximum value of the slope procedure. | float

### - info(*path*=**None**)

It returns a full summary of what contains the *WaterFrame* object.

Input | Description | Type
--- | --- | ---
path | The path of the data file. It is not necessary to introduce the parameter. | string

Return | Description | Type
--- | --- | ---
message | Summary of what contains the *WaterFrame* object. | string

### - resample(*rule*)

It resamples and averages the variables *data* and *technical* according the input [rule](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases). 

Input | Description | Type
--- | --- | ---
rule | [Rule](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases) to resample the variables *data* and *technical*. | string

### - add_netcdf(*path*)

It adds the data of a NetCDF file to the instance variable *data*.

Input | Description | Type
--- | --- | ---
path | It is the path of the [NetCDF](http://www.oceansites.org/data/) file. | string


## - *class* **EGIM**

Class to download [EGIM](http://www.emsodev.eu) data using the EMSODEV DMP API.

The class uses instance variables to save data. So, the functions change the values of the instance variables.

### - \_\_init\_\_(*login*=**None**, *password*=**None**, *observatory*=**None**, *instrument*=**None**, *parameter*=**None**, *path*=**None**, *start*=**None**, *end*=**None**)

Constructor. It creates the following instance variables:

* *login*: Login to use the EMSODEV DMP API.
* *password*: Password to use the EMSODEV DMP API.
* *observatories*: List of available [EGIMs](http://www.emsodev.eu).
* *instruments*: List of available instruments of an [EGIM](http://www.emsodev.eu).
* *parameters*: List of available parameters of an instrument.
* *observations*: Values of a parameter.
* *observatory_name*: Name of the selected observatory to download data.
* *instrument_name*: Name of the selected instrument to download data.
* *parameter_name*: Name of the selected parameter to download data.
* *wf*: *WaterFrame* object to save the downloaded data.

Input | Description | Type
--- | --- | ---
login | Login to use the EMSODEV DMP API. | string
password | Password to use the EMSODEV DMP API. | string
observatory | Observatories to download data. | list[string] or string
instrument | Instruments to download data. | list[string] or string
parameter | Parameters to download data. | list[string] or string
path | Path to save the *WaterFrame* object into a Pickle file. | string
start | Start date to download data with format *"dd/mm/yyyy"*. | string
end | End date to download data with format *"dd/mm/yyyy"*. | string

### - load_observatories()

It searches the available [EGIMs](http://www.emsodev.eu) and saves their names into the variable *observatories*.

Return | Description | Type
--- | --- | ---
status | [Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | int

### - load_instruments()

It searches the available instruments of the selected [EGIM](http://www.emsodev.eu) (saved into *observatory_name*) and saves their names into the variable *instruments*.

Return | Description | Type
--- | --- | ---
status | [Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | int

### - load_parameters()

It searches the available parameters of a selected instrument (saved into *instrument_name*) of a selected [EGIM](http://www.emsodev.eu) (saved into *observatory_name*) and saves their names into the variable *parameters*.

Return | Description | Type
--- | --- | ---
status | [Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | int

### - load_data(*start_date*, *end_date*=**""**)

It downloads the observations of a selected parameter (saved into *parameter_name*) of a selected instrument (saved into *instrument_name*) of a selected [EGIM](http://www.emsodev.eu) (saved into *observatory_name*). It saves their values into the variable *observations* and finally, appends the *observations* into the variable *wf* in the correct format.

Input | Description | Type
--- | --- | ---
start_date | Start date to download data, with format “dd/mm/yyyy”. | string
end_date | End date to download data, with format “dd/mm/yyyy”. If *end_date*=**" "**, end_date is today. | string

Return | Description | Type
--- | --- | ---
status | [Status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) | int

### - auto_download(*path_in*, *start_in*, *end_in*=**None**)

It downloads the observations of a all the parameters of *parameters* of all the instruments of *instruments* of all the [EGIMs](http://www.emsodev.eu) of *observatories*. It saves their values into the variable *observations* and finally, appends the *observations* into the variable *wf* in the correct format.

Input | Description | Type
--- | --- | ---
path_in | Path to save the *WaterFrame* object into a Pickle file. | string
start_in | Start date to download data, with format “dd/mm/yyyy”. | string
end_in | End date to download data, with format “dd/mm/yyyy”. If *end_in*=**None**, end_in is today. | string

Return | Description | Type
--- | --- | ---
answer | **True** if the process was ok or **False** if the process was ok. | bool

### - clean()

It erase all data placed into the instance variables *data* and *technical*.

## - plot_corr(*param_1*, *param_2*, *title*=**""**, *x_label*=**""**, *y_label*=**""**, *legend*=**[]**)

It creates a graph with the linear regression between the two input parameters.

Input | Description | Type
--- | --- | ---
param_1 | Name of the parameter 1 to plot. | string
param_2 | Name of the parameter 2 to plot. | string
title | Text of the title of the graph. | string
x_label | Text of the x label of the graph. | string
y_label | Text of the y label of the graph. | string
legend | List of names to write on the legend. | string

Return | Description | Type
--- | --- | ---
fig_correlation | Figure with the graph. | [matplotlib.figure](https://matplotlib.org/api/figure_api.html)