# Oceanobs v0.1.1

Released: November 4, 2016

First release. Set of libraries to analyze EMODnet and OBSEA data easily.

* Libraries:
  * emodnet.py: Library to open data in NetCDF or CSV from the EMODnet portal
  * obsea.py: Library to open data in .txt (CSV format) from the OBSEA portal
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
      * plt_pres(): It plots the water pressure over time.
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

Return to the [Versions Index](index_versions.md).
