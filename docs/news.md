
# Version control

Our last release is [mooda v0.0.1](https://github.com/rbardaji/mooda/releases). We use [SemVer](http://semver.org/) for versioning.

Given a version number MAJOR.MINOR.PATCH, increment the:

1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible manner, and
3. PATCH version when you make backwards-compatible bug fixes.

These are new features and improvements of note in each release.

## mooda v0.1.0 (Work in progress)

* In mooda/\_\_init\_\_.py:
  * It does not load plotmap.py if you do not have installed the basemap library. We added a warning message.
  * \_\_version\_\_ added.
* In mooda/waterframe.py:
  * barplot(): It creates the graph even without knowing the meaning of the parameters.
  * \_\_repr\_\_: New method. Return a string containing a printable representation of an object.
  * corr(): New function. Compute pairwise correlation of data columns, excluding NA/null values.
  * max_diff(): New function. Calculation the maximum difference between values of two parameters.
* In mooda/access/egim.py:
  * to_csv(): New function. It creates a CSV file following the OceanSites standard.
  * metadata dictionaries: Fixed bug in the long strings of the dictionaries.

## oceanobs is now mooda - mooda v0.0.1 (July, 2018)

Due to the requirements of the EMSODEV project, the package had to be renamed to "mooda." So, the directory where the MOODA app was, is now called as "mooda_gui."  The release count will start again from scratch, calling the first release as "mooda v0.0.1."

## V2.0.0 (June, 2018)

Complete new version. Not compatible with previous version.

## v1.1.1 (January 11, 2018)

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


## V0.5.1 (Not distributed)

**New Features**

* In mainwindow_ui.py:
	* Added offset input in Data -> Compare.
* In gui.py:
	* In class MyApplication:
		* add_param(): Add offset functionality. 
		* compare_add_button(): Add offset functionality.
		* hide_all(): It hides the plot and the comparison option.
		* hide_metadata_plots(): It hides the technical title and the technical list.
		* \_\_init\_\_(): We added the action when users clicks the check box to select all the parameters.
		* selection_all_parameters(): Action when clicking the check box of the parameter widget.
* In emsodev_ui.py: We added a check box to select all the parameters.		
* In emso.py:
	* In class EMSO:
		* plt_egim_slots_current_consumptions(): It creates a plot with the current consumption of all the slots and the input voltage of the EGIM.
		* statistics_slots_current_consumptions(): It calculates the mean, max and min current consumption of each slot. Return a string with the information.
		* plt_egim_energy(): Function deleted. It was not plotting the energy of the EGIM, but the current consumption.
		* plt_egim_current(): It returns a plot of the accumulated-since-last-reset current consumption of the EGIM.
		* how_to_download_data(): Function deleted. It was not useful.
		* statistics_slots_pressure(): It calculates the mean, max and min pressure of each slot. Return a string with the information.		
* In obsea.py:
	* In class OBSEA:
		* estimation_time_to_open(): Function deleted. It was not useful.
		* how_to_download_data(): Function deleted. It was not useful.
* In observatory.py:
	* In class Observatory:
		* plt_depth(): It plots the depth of the sensor over time.
		* statistics_ctd(): It returns a message with the mean, max, min and stand. dev of the measurements of the CTD (temperature, conductivity, pressure, salinity and sound velocity.)
	* New function plt_comparison(): It creates a graph with all the time series of the list parameters.
		* plt_ncus(): It plots the North – South current speed over time.	
* In emodnet.py:
	* In class EMODnet:
		* how_to_download_data(): Function deleted. It was not useful.

**Performance Enhancements**

* In gui.py:
	* Fixed bug importing libraries.
	* In class EMSOdevApp:
		* download_data(): The way to add the start date to download data with the API changed, so we also changed the function. The name of the self.egim column “egim_energy” changes to “egim_current” because it has current consumption values.
		* \_\_init\_\_(): We added the icon of the program.
		* search_observatories(): Auto select the observatory if there is just one.
		* search_instruments(): Auto select the instrument if there is just one.
		* search_parameters(): Auto select the parameter if there is just one.
		* New class: DownloadThread(): It allows multi-threading for the downloading part. Related to this class, we created other functions to communicate variables between threads (def message_for_statusbar() and def refresh_emsodevapi()).
	* In class MyApplication:
		* hide_metadata_plots(): Added the technical plots to the function.
		* make_plots(): Added the technical plots.
		* show_metadata_plots(): Sorted names in the EGIM parameters.
		* hide_all(): Added hide_metadata_plots() and remove_fig().
* In emsodev_ui.py: We changed some visual aspects.
* In emso.py:
	* In class EMSOdevAPI:
		* Fixed bug in the appending data frames.
		* plt_egim_all(): Added the plot of the EGIM current consumption.
		* read_data(): Bug fixed in the API command with an end date. We added the code to download data from the ADCP.
	* In tui():
		* Fixed bug when a user wants to download all the parameters of an instrument.
	* In class EMSO:
		* open(): Changed the way to open pickle files.
		* \_\_init\_\_(): Added the option to open the files.
		* read_data(): Bug fixed in the API command with an end date.
* In mainwindow_ui.py:
	* Adding technical plots.
* In observatory.py:
	* We include the (gsw)[https://pypi.python.org/pypi/gsw/] library.
	* In function qc(): Bug fixed. We changed the name of the variable miutes to minutes.
	* In class Observatory:
		* plt_ts(): We restructured all the function. Now, the plot is nicer.

## V0.4.1 (April 19, 2017)

**New Features**

* In mainwindow_ui.py:
	* Added “Filter-> Butterworth” in “Data” of the menu bar.
	* Added “Clean bad data” in “Data” of the menu bar.
	* Added “Delete parameters” in “Data” of the menu bar.
	* Added Butterworth filter options.
	* Added “Delete parameter” options.
	* Added “EMSO Downloader” option.
* In gui.py:
	* In class MyApplication:
		* \_\_init\_\_(): Added new components and actions.
		* clean_bad_data(): It cleans data from self.data with bad QC flags.
		* butterworth_init(): Initialization of the Butterworth filter option.
		* butterworth_apply(): Apply Butterworth filter to ob.data.
		* delete_parameters(): Action when user click the “Delete parameters” option of the menu bar.
		* delete_apply(): Action when users click the button of the “Delete parameter” options.
		* open(): Now it can open pickle files.
* In observatory.py:
	* In class Observatory:
		* delete_param(): Delete a parameter of self.data.
		* plt_qc_cmap(): Plot of the QC flags, using a color map.
		* use_only(): Delete all parameters of self.data except those selected by the user.
	* New class PlotMat: Helps to make a map with data based on Basemap library.
		* \_\_init\_\_(): Constructor of the class.
		* new_map_world(): Create a world map.
		* new_map_iberian(): Create a map of the Iberian peninsula.
		*  new_map_pyrenees(): Create a map of the Pyrenees.
		* new_map_pyrenees_arcgisapi(): Create a map of the Pyrenees using the ArcGIS API.
		* new_map_mediterranean(): Create a map of the Mediterranean sea.
		* new_map_europe(): Create a map of Europe.
		* add_point(): Adding points to the map.
	* New function qc(): It is the main function to create the QC flags.
* In emso.py:
	* In class EMSO:
		* plt_egim_voltage(): Make a figure with the consumed voltage of the EGIM.
		* info_egim(): Return information about the egim data.
* New qc.py: Contains functions to create the QC flags.
	* qc(): The main function to create the QC flags.

**Performance Enhancements**

* In observatory.py:
	* In class Observatory:
		* resample_data(): Fixed bug with the salinity data.
		* plt_qc(): First useful version.
		* clear_bad_data(): Added np.nan to bad values.
* In emodnet.py:
	* In class EMODnet:
		* open(): It adds latitude and longitude info to the variable self.metadata. Added more parameters to measure.
* In gui.py:
	* In class EMSOdevApp:
		* download_data(): Fixed bug downloading data.
* In emso.py:
	* In class EMSOdevAPI:
		* read_data(): It downloads data from the EGIM.
		* save_as_pickle (): It saves the self.data, self.metadata and self.egim into a pickle file.
	* In class EMSO:
		* \_\_init\_\_: Added variable self.egim.
* In obsea.py:
	* In class OBSEA:
		* open(): Changing the way to create the QC flags.

## V0.3.2 (February 27, 2017)

**Performance Enhancements**

* In obsea.py:
	* class OBSEA:
		* open(): Deleted some print() functions.
* In emso.py: We changed the wrong name of import libraries to the right ones.

## V0.3.1 (February 23, 2017)

**New Features**

* In observatory.py:
	* In class Observatory:
		* info_qc_flags(): It returns information about what means the QC flags.
		* info_metadata(): It returns all the metadata information in a string.
		* info_parameters(): It returns information about the acronyms used in the variable self.data.
		* plt_multiparam_one_plot(): It plot one figure with multiple variables.
		* plt_multiparam_multiplot():  It plots multiple parameters in multiple figures.
		* translator(): It returns the meaning of an acronym.
		* clear_bad_data(): It clears all the data with QC flags equal to 2, 3, 4, 6 and 9.
		* butterworth_filter(): It applies a Butterworth filter to the data. 
* In gui.py:
	* In class MyApplication: 
		* print_text(): It writes text in the text area.
		* view_text(): It shows the text area.
		* view_metadata_plots(): It shows the metadata and plots area.
		* hide_metadata_plots(): It hides the metadata and plots area.
		* show_menus(): It shows some menu options.
		* hide_menus(): It hides some menu options.
		* print_opening_info(): It writes in the text area some basic information about the data that the user is watching.
	* New class – EMSOdevApp: GUI to download data using the EMSOdev DMP API.
		* \_\_init\_\_(): Constructor of the class.
		* hide_connection(): It hides some components of the GUI.
		* search_observatories(): It searches the EMSO observatories and shows them in a list.
		* search_instruments(): It searches the instruments of the EMSO observatories and shows them in a list.
		* search_parameters(): It searches the parameters that are measured with the instruments of the EMSO observatories and show them in a list.
		* input_dates(): It asks the user to input the start date and the end date of the data that he/she want to download.
		* show_date(): It shows a calendar in the GUI.
		* download_data(): It processes to download data with the EMSOdev API.
		* save_data(): It saves the downloaded data into a pickle file (.pkl).
* In obsea.py:
	* class OBSEA:
		* estimation_time_to_open(): It returns a string with information about of how many time takes to open the data.
* New library - emsodev_ui.py: Class generated with pyuic4 with the QT graphical components of the EMSOdev App. The EMSOdev App helps to download EMSO data. 
* New library - emso.py: 
	* class EMSOdevAPI: Class to manage the EMSOdev DMP API.
		* \_\_init\_\_(): Constructor of the class
		* read_observatories(): It looks for observatories and save them into a list in self.observatories.
		* read_instruments(): It looks for instruments of an observatory and saves the names into self.observatories.
		* read_parameters(): It looks for the parameters that the instrument can measure.
		* read_data(): It downloads data from the parameter, instrument, and observatory selected.
		* save_as_pickle(): Save the EGIM data and metadata with the oceanobs standard [REF TO OCEANOBS STANDARD]. The name of the files are metadata_[date].pkl for the metadata and data_[date].pkl for the data.
	* class EMSO: Class to open and manage EMSO data.
		* \_\_init\_\_(): The constructor of the class.
		* open(): It opens pickle files (.pkl) with EMSO data.
		* how_to_download_data(): It returns information about how to download EMSO data.

**Performance Enhancements**

* In observatory.py:
	* In class Observatory:
		* plt_qc(): Changed the graph visualization to understand it easily.
		* plt_all(): Added call to plt_qc() if there are less than 25 values.
		* info_data(): It shows the parameters placed in the self.data.
* In mainwindow_ui.py:
	* Added QC plots.
	* Added View button in the menu bar.
	* Added Text area.
	* Deleted “assembly center” in the metadata information.
	* Deleted “save” in the Report Menu.
* In gui.py:
	* In class MyApplication:
		* \_\_init\_\_(): Added some menu actions. 
		* open(): It writes information in the text area.
		* style_xkcd(): It writes information in the text area and the status bar. 
		* style_bmh(): It writes information in the text area and the status bar.
		* style_classic(): It writes information in the text area and the status bar.
		* style_dark_background(): It writes information in the text area and the status bar.
		* style_fivethirtyeight(): It writes information in the text area and the status bar.
		* style_ggplot(): It writes information in the text area and the status bar.
		* style_grayscale(): It writes information in the text area and the status bar.
		* style_seaborn_bright(): It writes information in the text area and the status bar.
		* style_seaborn_colorblind(): It writes information in the text area and the status bar.
		* style_seaborn_dark(): It writes information in the text area and the status bar.
		* style_seaborn_dark_palette(): It writes information in the text area and the status bar.
		* style_seaborn_darkgrid(): It writes information in the text area and the status bar.
		* style_seaborn_deep(): It writes information in the text area and the status bar.
		* style_seaborn_muted(): It writes information in the text area and the status bar.
		* style_seaborn_notebook(): It writes information in the text area and the status bar.
		* style_seaborn_paper(): It writes information in the text area and the status bar.
		* style_seaborn_pastel(): It writes information in the text area and the status bar.
		* style_seaborn_seaborn_poster(): It writes information in the text area and the status bar.
		* style_seaborn_talk(): It writes information in the text area and the status bar.
		* style_seaborn_ticks(): It writes information in the text area and the status bar.
		* style_seaborn_white(): It writes information in the text area and the status bar.
		* style_seaborn_whitegrid(): It writes information in the text area and the status bar.
		* hide_all(): It hides more things.
		* make_plots(): Added plot of QC.
		* show_metadata(): It shows the metadata information.
		* report_save(): Deleted function.
* In obsea.py
	* In class OBSEA:
		* qc(): Fixed bug.

## V0.2.1 (December 27, 2016)

**New Features**

* In gui.py: Now we can open EMODnet files.
* In observatory.py:
	* plt_atmpres(): It plots pressure at sea level in dBs.
	* plt_atmpres(): It plots sea level in meters.
	* plt_prec(): It plots rain accumulation in millimeters.
	* plt_relhu(): It plots relative humidity in %.
	* plt_gusp(): It plots gust wind speed in meter/second.
	* plt_cudi(): It plots current to a direction relative true north in degrees.
	* plt_cusp(): It plots horizontal current speed in meters/second.

**Performance Enhancements**

* In emodnet.py:
	* open(): Fixed bug opening a list of file paths. We removed the option to open CSV files. It is difficult to understand the columns of the CSV file.
* In gui.py: Fixed bug opening the GUI with an external call.
* In observatory.py: 
	* plt_atm(): Deleted x1000.

##V0.1.1 (November 4, 2016)

**First release**

Set of libraries to analyze EMODnet and OBSEA data easily.

* Libraries:
	* emodnet.py: Library to open data in NetCDF or CSV from the EMODnet portal [http://www.jerico-ri.eu/data-access/]
	* obsea.py: Library to open data in .txt (CSV format) from the OBSEA portal [http://www.upc.edu/cdsarti/OBSEA/]
	* observatory.py: The main library to analyze data.
	* mainwindow_ui.py: It creates the GUI layout. Created by PyQt4 UI code generator 4.11.4.
	* gui.py: Library with all the functions and classes related to the GUI. 
* Functions and classes:
	* In emodnet.py:
		* class EMODnet(): Manage the opening of the EMODnet files.
			* \_\_init\_\_(): Class constructor.
			* open(): It open the netcdf or csv file.
			* how_to_download_data(): It sends a message telling how to download data.
	* In obsea.py:
		* class OBSEA(): Manage the opening of the OBSEA files.
			* \_\_init\_\_(): Class constructor.
			* open(): It opens the csv file.
			* how_to_download_data(): It sends a message telling how to download data.
	* In observatory.py:
		* class Observatory: Data analysis class.
			* \_\_init\_\_(): Class constructor.
			* reset_data(): It reloads the original data.
			* slicing(): It slices data by date conditions.
			* resample data(): It resamples data estimating the average of the values.
			* info_data(): It sends a message with some information of the data that we are using.
			* plt_cond(): It plots the water conductivity over time.
			* plt_temp(): It plots the water temperature over time.
			* plt_atemp(): It plots the air temperature over time.
			*  plt_pres(): It plots the water pressure over time.
			* plt_atm(): It plots the atmospheric pressure over time.
			* plt_sal(): It plots the water salinity over time.
			* plt_ts(): It plots a T-S graph.
			* plt_sovel(): It plots the water sound velocity over time.
			* plt_co2(): It plots the water CO2 over time.
			* plt_wisp(): It plots the water wind speed over time.
			* plt_widi(): It plots the water direction over time.
			* plt_qc(): It plots the QC flags.
			* plt_wadi(): It plots the water direction over time.
			* plt_wape(): It plots the water period over time. 
			* plt_wahe(): It plots the water height over time.
			* plt_all(): It creates all the possible plots.
	* In gui.py:
		* class MyApplication(): Class with all the functions of the GUI. Major functions are used when a button is clicked.
			* \_\_init\_\_(): Class constructor.
			* resample_month(): It resamples data monthly.
			* resample_week(): It resamples data weekly.
			* resample_day(): It resamples data daily.
			* resample_hour(): It resamples data hourly.
			* refresh_fig(): It reloads the actual plot.
			* style_xkcd(): It configures the plot style to “xkcd”. 
			* style_bmh(): It configures the plot style to “bmh”. 
			* style_classic(): It configures the plot style to “classic”.
			* style_dark_background(): It configures the plot style to “dark background”.
			* style_fivethirtyeight(): It configures the plot style to “fivethirtyeight”.
			* style_ggplot(): It configures the plot style to “ggplot”.
			* style_grayscale(): It configures the plot style to “grayscale”.
			* style_seaborn_bright(): It configures the plot style to “seaborn bright”.
			* style_seaborn_colorblind(): It configures the plot style to “seaborn colorblind”.
			* style_seaborn_dark(): It configures the plot style to “seaborn dark”.
			* style_seaborn_dark_palette(): It configures the plot style to “seaborn dark palette”.
			* style_seaborn_darkgrid(): It configures the plot style to “seaborn darkgrid”.
			* style_seaborn_deep(): It configures the plot style to “seaborn deep”.
			* style_seaborn_muted(): It configures the plot style to “seaborn muted”.
			* style_seaborn_notebook(): It configures the plot style to “seaborn notebook”.
			* style_seaborn_paper(): It configures the plot style to “seaborn paper”.
			* style_seaborn_pastel(): It configures the plot style to “seaborn pastel”.
			* style_seaborn_seaborn_poster(): It configures the plot style to “seaborn poster”.
			* style_seaborn_talk(): It configures the plot style to “seaborn talk”.
			* style_seaborn_ticks(): It configures the plot style to “seaborn ticks”.
			* style_seaborn_white(): It configures the plot style to seaborn white”.
			* style_seaborn_whitegrid(): It configures the plot style to seaborn whitegrid”.
			* hide_all(): It hides the metadata information.
			* open(): It opens a data file.
			* show_metadata(): It shows the metadata information.
			* make_plots(): It makes all the possible plots.
			* remove_fig(): It deletes the figure shown on the screen.
			* add_fig(): It adds a figure and a toolbar in the figure container.
			* view_fig():  It shows the selected figure.
			* report_save_as(): It creates a docx file with some data information.
			* report_save(): It saves a docx file with some data information.
			* hide_slicing(): It hides the slicing option.
			* show_slicing(): It shows the slicing options.
			* accept_slicing(): It is the data slicing process.
		* open_gui(): It opens the GUI.
