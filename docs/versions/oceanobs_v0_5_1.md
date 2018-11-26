# Oceanobs v0.5.1

New Features

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

Performance Enhancements

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
  * We include the [gsw](https://pypi.python.org/pypi/gsw/) library.
  * In function qc(): Bug fixed. We changed the name of the variable minutes to minutes.
  * In class Observatory:
    * plt_ts(): We restructured all the function. Now, the plot is nicer.

Return to the [Versions Index](index_versions.md).
