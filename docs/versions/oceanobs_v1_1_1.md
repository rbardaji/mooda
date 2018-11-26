# Oceanobs v1.1.1

Released: January 11, 2018

A new version of oceanobs with incompatible API changes. We deleted observatory.py to simplifier the code. The philosophy of the package is the previous one, but we mixed the access modules and the analysis modules into a new module called inWater.py.

* In inWater.py:
  * In class EGIM: Class to download EGIM data using the EMSODEV DMP API.
    * _\_init\_\_(): Constructor.
    * load_observatories(): It searches the available EGIMs and saves their names into the variable observatories.
    * load_instruments(): It searches the available instruments of the selected EGIM (saved into observatory_name) and saves their names into the variable instruments.
    * load_parameters(): It searches the available parameters of a selected instrument (saved into instrument_name) of a selected EGIM (saved into observatory_name) and saves their names into the variable parameters.
    * load_data(): It downloads the observations of a selected parameter (saved into parameter_name) of a selected instrument (saved into instrument_name) of a selected EGIM (saved into observatory_name). It saves their values into the variable observations and finally, appends the observations into the variable wf in the correct format.
    * auto_download(): It downloads the observations of a all the parameters of parameters of all the instruments of instruments of all the EGIMs of observatories.
    * clean(): It erase all data placed into the instance variables data and technical.
  * In class WaterFrame: Class to manage data series from marine observatories.
    * _\_init\_\_(): Constructor.
    * from_netcdf(): It loads data from a NetCDF file.
    * from_csv(): It loads data from a text file with a CSV format.
    * from_pickle(): It loads data from a pickle file.
    * add_netcdf(): It adds the data of a NetCDF file to the instance variable data.
    * to_pickle(): It saves a WaterFrame object to a pickle (serialize) object in the input path.
    * plot(): It creates the figure of the input parameter.
    * plot_ts(): It creates a TS diagram.
    * predefined_plot(): It creates some basic technical plots.
    * qc(): It analyzes the values of the variable data and changes the QC flags from 0 to the corresponding number.
    * drop_qc(): It deletes all values with the QC flag number different to qc_flag.
    * name_qc(): It returns the name of the column with the QC Flag information of the parameter.
    * info(): It returns a full summary of what contains the WaterFrame object.
    * resample(): It samples and averages the variables data and technical according to the input rule.
    * Function plot_corr(): It creates a graph with the linear regression between the two input parameters.
  * PlotMap: It contains functions related to the management of maps.
    * _\_init\_\_(): Constructor.
    * map_world(): It creates a map of the world.
    * map_mediterranean(): It creates a map of the Mediterranean.
    * add_point(): It adds points to the map.
    * add_pointxxx(): It adds points to the map.

Return to the [Versions Index](index_versions.md).
