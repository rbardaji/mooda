# Oceanobs v0.4.1

Released: April 19, 2017

New Features

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
    * new_map_pyrenees(): Create a map of the Pyrenees.
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

Performance Enhancements

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

Return to the [Versions Index](index_versions.md).
