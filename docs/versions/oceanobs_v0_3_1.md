# Oceanobs v0.3.1

Released: February 23, 2017

New Features

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

Performance Enhancements

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

Return to the [Versions Index](index_versions.md).
