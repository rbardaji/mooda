import sys
from matplotlib import style
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import time

try:
    import oceanobs.obsea as obsea
    import oceanobs.emodnet as emodnet
    import oceanobs.emso as emso
    from oceanobs.mainwindow_ui import *
    from oceanobs.emsodev_ui import *
except ImportError:
    import obsea
    import emodnet
    import emso
    from mainwindow_ui import *
    from emsodev_ui import *


class OpenThread(QtCore.QThread):
    """
    Thread to open data.It is used for the gui.
    """
    def __init__(self, path_in):
        QtCore.QThread.__init__(self)

        # Instance variables
        self.path = path_in

    def __del__(self):
        self.wait()

    def run(self):
        # Know if it is an OBSEA file or an EMODnet file
        if self.path[0][-1] == 't' or self.path[0][-1] == 'T':
            ob = obsea.OBSEA(self.path)
        elif self.path[0][-1] == 'l' or self.path[0][-1] == 'L':
            # If you enter here is becouse you have processed data. Yoy can open this type of data with all the
            # libraries of the package.
            ob = emso.EMSO(self.path[0])
        elif self.path[0][-1] == 'c' or self.path[0][-1] == 'C':
            # It is an EMODnet file, so let's open a EMODnet
            ob = emodnet.EMODnet(self.path)
        else:
            return
        self.emit(QtCore.SIGNAL("data_loaded"), ob)
        # self.terminate()


class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)
        self.terminate()
        return


class EMSOdevApp(QtGui.QMainWindow, Ui_mw_emsodev):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Logo
        self.setWindowIcon(QtGui.QIcon('img/logo.png'))

        # Instance variables
        self.ensodev_api = None
        self.download_thread = None

        # Call for the EMSOdev API
        self.ensodev_api = emso.EMSOdevAPI()

        # Hide all the components of the connection
        self.hide_connection()
        # Resize window
        self.adjustSize()
        # Write instructions on the statusbar
        self.statusbar.showMessage("Enter login and password.")

        # Button actions
        self.pb_connect.clicked.connect(self.search_observatories)
        self.pb_download.clicked.connect(self.download_data)
        self.pb_save.clicked.connect(self.save_data)

        # List actions
        self.lw_observatories.itemClicked.connect(self.search_instruments)
        self.lw_instruments.itemClicked.connect(self.search_parameters)
        self.lw_parameters.itemClicked.connect(self.input_dates)

        # Calendar action
        self.calendar.clicked.connect(self.show_date)

    def hide_connection(self):
        """
        Hide all the components of the window
        """
        self.gb_observatories.hide()
        self.gb_instruments.hide()
        self.gb_parameters.hide()
        self.gb_dates.hide()
        self.pb_download.hide()
        self.pb_save.hide()

    def search_observatories(self):
        """
        Search for the observatories of EMSO via the EMSOdev API
        :return:
        """
        # Hide instruments, parameters and the download button
        self.gb_instruments.hide()
        self.gb_parameters.hide()
        self.pb_download.hide()
        # Call for the EMSOdev API
        self.ensodev_api = emso.EMSOdevAPI(self.le_login.text(), self.le_password.text())
        # Cleaning the list of instruments and parameters to select. If you are here, the instruments and the parameters
        # should be re-serched.
        self.ensodev_api.instruments = []
        self.ensodev_api.parameters = []
        # Search observatories
        self.statusbar.showMessage("Searching for observatories...")
        code = self.ensodev_api.read_observatories()
        # Error response code
        if code != 200:
            self.statusbar.showMessage("Error: Impossible to connect. Status code: {}".format(code))
        else:
            self.gb_observatories.show()
            self.gb_connection.hide()
            # Insert in lw_observatories the results
            self.lw_observatories.clear()
            for observatory in self.ensodev_api.observatories:
                self.lw_observatories.addItem(observatory)
            # Resize window
            self.adjustSize()
            # Write how to procedire
            self.statusbar.showMessage("Select an observatory.")

    def search_instruments(self, item):
        """
        Search for the instruments of a observatory
        :param item: Name of the selected observatory
        """
        # Save the observatory name
        self.ensodev_api.observatory_name = item.text()
        # Hide components
        self.gb_parameters.hide()
        self.gb_dates.hide()
        self.pb_download.hide()
        # We clean the parameters list
        self.ensodev_api.parameters = []
        # Search instruments
        self.statusbar.showMessage("Searching for instruments in {}...".format(self.ensodev_api.observatory_name))
        code = self.ensodev_api.read_instruments()
        # Error code
        if code != 200:
            self.statusbar.showMessage("Error: Impossible to connect. Status code: {}".format(code))
        else:
            # Insert in lw_instruments the results
            self.lw_instruments.clear()
            for instrument in self.ensodev_api.instruments:
                self.lw_instruments.addItem(instrument)
                # Show the instrument grupBox
            self.gb_instruments.show()
            # Resize window
            self.adjustSize()
            # Write how to procedire
            self.statusbar.showMessage("Select an instrument.")

    def search_parameters(self, item):
        """
        Search for the parameter that the user want to download.
        :param item: Name of the instrument
        """
        # Hide components
        self.pb_download.hide()
        self.gb_dates.hide()
        # Save the instrument name
        self.ensodev_api.instrument_name = item.text()
        # Search for the parameters
        self.statusbar.showMessage("Searching for parameters in {}...".format(self.ensodev_api.instrument_name))
        code = self.ensodev_api.read_parameters()
        if code != 200:
            self.statusbar.showMessage(("Error: Impossible to connect. Status code: {}".format(code)))
        else:
            # Insert in lw_parameters the results
            self.lw_parameters.clear()
            for parameter in self.ensodev_api.parameters:
                self.lw_parameters.addItem(parameter)
            # Show the instrument grupBox
            self.gb_parameters.show()
            # Resize window
            self.adjustSize()
            # Write how to procedire
            self.statusbar.showMessage("Select a parameter.")

    def input_dates(self, item):
        """
        Select the start and stop dates.
        :param item:
        :return:
        """
        # Save the parameter to download data
        self.ensodev_api.parameter_name = item.text()
        # Show the dates grup box
        self.gb_dates.show()
        # Write how to procedire
        self.statusbar.showMessage("Select the dates.")

    def show_date(self, date):
        # Show the date
        if self.rb_start.isChecked():
            self.l_start.setText(date.toString(format("dd/MM/yyyy")))
            # Show the buttons
            self.pb_download.show()
            self.pb_save.show()
        else:
            self.l_stop.setText(date.toString(format("dd/MM/yyyy")))

    def download_data(self):
        """
        Download data
        """

        def thread_download_data():
            start_date = self.l_start.text()
            if self.l_stop.text() == "Now":
                stop_date = ""
            else:
                stop_date = self.l_stop.text()

            self.statusbar.showMessage("Downloading data...")
            code = self.ensodev_api.read_data(start_date, stop_date)
            if code != 200:
                self.statusbar.showMessage("Error: Impossible to connect. Status code: {}".format(code))
            else:
                print("Result (5 first values):")
                print(self.ensodev_api.data.head())
                self.statusbar.showMessage("Done. ")

        # Downloading data
        self.download_thread = GenericThread(thread_download_data)
        self.download_thread.start()

    def save_data(self):
        """
        Save the data that was downloaded.
        """
        # Open a directory dialog
        path = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        # Save as pickle
        self.ensodev_api.save_as_pickle(path)
        self.statusbar.showMessage("Files saved on: {}.".format(path))

    # def thread_download_data(self):
    #     start_date = self.l_start.text()
    #     if self.l_stop.text() == "Now":
    #         stop_date = ""
    #     else:
    #         stop_date = self.l_stop.text()
    #
    #     self.statusbar.showMessage("Downloading data...")
    #     code = self.ensodev_api.read_data(start_date, stop_date)
    #     if code != 200:
    #         self.statusbar.showMessage("Error: Impossible to connect. Status code: {}".format(code))
    #     else:
    #         print("Result (5 first values):")
    #         print(self.ensodev_api.data.head())
    #         self.statusbar.showMessage("Done. ")


class MyApplication(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('img/logo.png'))

        # Define the style of plots
        style.use('ggplot')

        # Instance variables
        self.canvas = None
        self.toolbar_plot = None
        self.data = None
        self.fig_dict = {}
        self.egim_dict = {}
        self.ob = None
        self.actual_fig = ""
        self.report_path = ""
        self.emsodevapp = EMSOdevApp()
        self.mix = pd.DataFrame()
        self.op_thread = None
        self.plots_thread = None

        # Menu "File"
        self.actionOpenData.triggered.connect(self.open)
        self.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.action_open_emsodev.triggered.connect(self.emsodevapp.show)

        # Menu "Report"
        # Hide menu
        self.actionSave_as.triggered.connect(self.report_save_as)

        # Menu "Data"
        self.actionSlicing.triggered.connect(self.w_slicing.show)
        self.action_clean_bad_data.triggered.connect(self.clean_bad_data)
        self.action_delete_parameters.triggered.connect(self.delete_parameters)
        # Delete options
        self.pb_clear_apply.clicked.connect(self.delete_apply)
        self.pb_clear_cancel.clicked.connect(self.w_delete.hide)
        # Sub-menu "Resample"
        self.actionMonth_frequency.triggered.connect(self.resample_month)
        self.actionWeekly_frequency.triggered.connect(self.resample_week)
        self.actionDay_frequency.triggered.connect(self.resample_day)
        self.actionHourly_frequency.triggered.connect(self.resample_hour)
        # Slicing option
        self.slicing_accept_button.clicked.connect(self.accept_slicing)
        self.slicing_cancel_button.clicked.connect(self.w_slicing.hide)
        # Sub-menu Filter
        self.action_butterworth.triggered.connect(self.butterworth_init)
        # Butterworth option
        self.pb_butterworth_cancel.clicked.connect(self.w_butterworth.hide)
        self.pb_butterworth_apply.clicked.connect(self.butterworth_apply)
        # Plot data
        self.action_plot_menu.triggered.connect(self.menu_plot)
        # Buttons
        self.pb_plot_close.clicked.connect(self.w_plot.hide)
        self.pb_plot_plot.clicked.connect(self.direct_plot)
        # Compare data
        self.action_compare.triggered.connect(self.add_param)
        # Buttons
        self.pb_compare_close.clicked.connect(self.w_compare.hide)
        self.pb_compare_add.clicked.connect(self.compare_add_button)
        self.pb_compare_del.clicked.connect(self.compare_del_button)
        self.pb_compare_plot.clicked.connect(self.compare_plot_button)
        # Add action in the selection of lists
        self.existent_param_list.itemClicked.connect(self.write_le_text)
        # Menu "view"
        self.actionMetadata_Plots.triggered.connect(self.view_metadata_plots)
        self.actionText_info.triggered.connect(self.view_text)

        # Menu "Settings"
        # Sub-menu "Plot style"
        self.actionBmh.triggered.connect(self.style_bmh)
        self.actionClassic.triggered.connect(self.style_classic)
        self.actionDark_background.triggered.connect(self.style_dark_background)
        self.actionFivethirtyeight.triggered.connect(self.style_fivethirtyeight)
        self.actionGgplot.triggered.connect(self.style_ggplot)
        self.actionGrayscale.triggered.connect(self.style_grayscale)
        self.actionSeaborn_bright.triggered.connect(self.style_seaborn_bright)
        self.actionSeaborn_colorblind.triggered.connect(self.style_seaborn_colorblind)
        self.actionSeaborn_dark.triggered.connect(self.style_seaborn_dark)
        self.actionSeaborn_dark_palette.triggered.connect(self.style_seaborn_dark_palette)
        self.actionSeaborn_darkgrid.triggered.connect(self.style_seaborn_darkgrid)
        self.actionSeaborn_deep.triggered.connect(self.style_seaborn_deep)
        self.actionSeaborn_muted.triggered.connect(self.style_seaborn_muted)
        self.actionSeaborn_notebook.triggered.connect(self.style_seaborn_notebook)
        self.actionSeaborn_paper.triggered.connect(self.style_seaborn_paper)
        self.actionSeaborn_pastel.triggered.connect(self.style_seaborn_pastel)
        self.actionSeaborn_poster.triggered.connect(self.style_seaborn_seaborn_poster)
        self.actionSeaborn_talk.triggered.connect(self.style_seaborn_talk)
        self.actionSeaborn_triks.triggered.connect(self.style_seaborn_ticks)
        self.actionSeaborn_white.triggered.connect(self.style_seaborn_white)
        self.actionSeaborn_whitegrid.triggered.connect(self.style_seaborn_whitegrid)
        self.actionXkcd.triggered.connect(self.style_xkcd)

        # Acction when you select a figure
        self.under_list.itemClicked.connect(self.view_fig)
        self.above_list.itemClicked.connect(self.view_fig)
        self.qc_list.itemClicked.connect(self.view_fig)
        self.technical_list.itemClicked.connect(self.view_fig)

        # Hide all inforamtion
        self.hide_all()

        # Notify that everithing is correct and print it
        self.print_text("oceanobs GUI started at " + datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    """ PRINT AND REPORT OPTIONS """

    def report_save_as(self):
        filename = QtGui.QFileDialog.getSaveFileName(None, "Save file", "", ".txt")
        if len(filename) > 0:
            self.report_path = filename
            with open(self.report_path, 'a') as report:
                report.write(self.text_area.toPlainText())
            self.statusbar.showMessage("Report saved.")

    def print_text(self, text):
        """
        Print the text in the text area.
        :param text: Text to add to the text area
        """
        self.text_area.appendPlainText(text)

    def print_opening_info(self, path):
        """
        Write basic information about the data
        :param path: path where data is.
        """
        self.print_text("Opening data from:")
        for text in path:
            self.print_text("\t" + text)
        try:
            self.print_text("METADATA INFORMATION")
            self.print_text(self.ob.info_metadata())
        except AttributeError:
            self.statusbar.showMessage("Metadata is needed.")
        self.print_text("DATA INFORMATION")
        self.print_text(self.ob.info_data())

    """ FIGURE VIEW MANAGING """

    def remove_fig(self):
        """
        Delete the figure that is shown
        """
        try:
            self.plot_vertical_layout.removeWidget(self.canvas)
            self.canvas.close()
            self.plot_vertical_layout.removeWidget(self.toolbar_plot)
            self.toolbar_plot.close()
        except AttributeError:
            # We can enter here the first time becouse there is no figure. We don't have to do anything, it's ok.
            pass

    def add_fig(self, fig):
        """
        Añade una figura al contenedor de figuras y el tipico toolbar
        :param fig: Figura que queremos que se visualice
        :type fig: figure object
        """
        # Añadimos la figura
        self.canvas = FigureCanvas(fig)
        self.plot_vertical_layout.addWidget(self.canvas)
        self.canvas.draw()
        # Añadimos el toolbar
        self.toolbar_plot = NavigationToolbar(self.canvas, self.plot_window, coordinates=True)
        self.plot_vertical_layout.addWidget(self.toolbar_plot)
        # Si queremos que el toolbar este fuera, es la siguiente linea
        # self.addToolBar(self.toolbar_plot)

    def view_fig(self, item):
        """
        Muestra en el contenedor de figuras la figura seleccionada del self.plot_list
        :param item: titulo de la figura que se quiere visaulizar
        """
        self.remove_fig()
        fig_title = item.text()
        self.actual_fig = fig_title
        self.add_fig(self.fig_dict[fig_title])

    """ OPEN DATA, MENU FILE, OPEN """

    def finish_open(self, ob_in):
        """
        The open process is done via the OpenThread
        :param ob_in: observatory object.
        :return:
        """
        self.ob = ob_in
        # Error message
        if self.ob.dialog:
            self.statusbar.showMessage(self.ob.dialog)
            return
        self.statusbar.showMessage("Done.")
        # Hide all
        self.hide_all()
        # Remove the figure that is shown in the screen
        self.remove_fig()
        self.show_menus()
        if self.cb_load_all_plots.isChecked():
            # Create all plots
            try:
                self.fig_dict = self.ob.plt_all()
            except AttributeError:
                pass
            try:
                # This is just for EMSO
                self.egim_dict = self.ob.plt_egim_all()
            except AttributeError:
                pass
            self.show_plots()

    def open(self):
        """
        Open data file.
        """

        path = QtGui.QFileDialog.getOpenFileNames(None, 'Open TXT, netCDF or pickle', "",
                                                  "pickle (*.pkl);;netCDF (*.nc);;TXT (*.txt)")
        if len(path) > 0:
            self.statusbar.showMessage("Opening data. Please wait.")
            self.op_thread = OpenThread(path)
            self.connect(self.op_thread, QtCore.SIGNAL("data_loaded"), self.finish_open)
            self.op_thread.start()

    """ SHOW AND HIDE COMPONENTS OF THE GUI, MENU VIEW """

    def view_metadata_plots(self):
        """
        Show or hide the metadata info and plots
        """
        # Know if it is shown or hiden
        if self.title_plots.isHidden():
            self.show_metadata_plots()
        else:
            self.hide_metadata_plots()

    def hide_all(self):
        """
        Hide all the components of the GUI
        :return:
        """
        self.hide_metadata_plots()
        self.text_area.hide()
        self.w_slicing.hide()
        self.w_butterworth.hide()
        self.hide_menus()
        self.w_delete.hide()
        self.w_compare.hide()
        self.hide_metadata_plots()
        self.remove_fig()
        self.w_preferences.hide()
        self.w_plot.hide()

    def hide_menus(self):
        """
        Hide menu options
        """
        self.menuData.menuAction().setVisible(False)
        self.menuReport.menuAction().setVisible(False)
        self.actionMetadata_Plots.setVisible(False)
        self.menuPlot_stype.menuAction().setVisible(False)

    def show_menus(self):
        """
        Show some menu opcions
        """
        self.menuData.menuAction().setVisible(True)
        self.menuReport.menuAction().setVisible(True)
        self.actionMetadata_Plots.setVisible(True)
        self.menuPlot_stype.menuAction().setVisible(True)

    def hide_metadata_plots(self):
        """
        Hide the column of metadata and plots
        """
        self.title_platform_code.hide()
        self.platform_code.hide()
        self.wmo_code.hide()
        self.title_wmo_code.hide()
        self.institution.hide()
        self.title_institution.hide()
        self.type.hide()
        self.title_type.hide()
        self.title_plots.hide()
        self.title_above.hide()
        self.above_list.hide()
        self.title_under.hide()
        self.under_list.hide()
        self.title_qc.hide()
        self.qc_list.hide()
        self.title_technical.hide()
        self.technical_list.hide()

    def show_metadata_plots(self):
        """
        Show the column of metadata and plots
        """
        if self.platform_code.text() != " ":
            self.platform_code.show()
            self.title_platform_code.show()
        if self.wmo_code.text() != " ":
            self.wmo_code.show()
            self.title_wmo_code.show()
        if self.platform_code.text() != " ":
            self.institution.show()
            self.title_institution.show()
        if self.platform_code.text() != " ":
            self.type.show()
            self.title_type.show()
        if self.above_list.count() > 0:
            self.title_plots.show()
            self.title_above.show()
            self.above_list.sortItems()
            self.above_list.show()
        if self.under_list.count() > 0:
            self.title_plots.show()
            self.title_under.show()
            self.under_list.show()
        if self.qc_list.count() > 0:
            self.title_plots.show()
            self.title_qc.show()
            self.qc_list.show()
        if self.technical_list.count() > 0:
            self.title_plots.show()
            self.title_technical.show()
            self.technical_list.sortItems()
            self.technical_list.show()

    def show_metadata(self, metadata):
        """
        Show metadata
        :param metadata: the metadata
        :type metadata: Pandas dataframe
        """
        try:
            self.platform_code.setText(metadata['platform_code'][0])
            self.wmo_code.setText(metadata['wmo_platform_code'][0])
            self.institution.setText(metadata['institution'][0])
            self.type.setText(metadata['type'][0])
            self.show_metadata_plots()
        except TypeError:
            self.statusbar.showMessage("Error: No metadata found.")

    def show_plots(self):
        """
        Make all plots.
        """

        # plt.close("all")
        # Clean figure lists
        self.above_list.clear()
        self.under_list.clear()
        self.qc_list.clear()
        self.technical_list.clear()
        # Create all plots
        try:
            # Show the plot list
            plot_keys = self.fig_dict.keys()
            # Adding items to under_list
            if 'Salinity' in plot_keys:
                self.under_list.addItem('Salinity')
            if 'Temperature' in plot_keys:
                self.under_list.addItem('Temperature')
            if 'Sound velocity' in plot_keys:
                self.under_list.addItem('Sound velocity')
            if 'Pressure' in plot_keys:
                self.under_list.addItem('Pressure')
            if 'Conductivity' in plot_keys:
                self.under_list.addItem('Conductivity')
            if 'Wave height' in plot_keys:
                self.under_list.addItem('Wave height')
            if 'Wave direction' in plot_keys:
                self.under_list.addItem('Wave direction')
            if 'Wave period' in plot_keys:
                self.under_list.addItem('Wave period')
            if 'Sea level' in plot_keys:
                self.under_list.addItem('Sea level')
            if 'Current speed' in plot_keys:
                self.under_list.addItem('Current speed')
            if 'Current direction' in plot_keys:
                self.under_list.addItem('Current direction')
            # Adding items to above_list
            if 'Atmospheric pressure' in plot_keys:
                self.above_list.addItem('Atmospheric pressure')
            if 'Wind speed' in plot_keys:
                self.above_list.addItem('Wind speed')
            if 'Wind direction' in plot_keys:
                self.above_list.addItem('Wind direction')
            if 'Air temperature' in plot_keys:
                self.above_list.addItem('Air temperature')
            if 'Pressure sea level' in plot_keys:
                self.above_list.addItem('Pressure sea level')
            if 'Rain acumulation' in plot_keys:
                self.above_list.addItem('Rain acumulation')
            if 'Relative humidity' in plot_keys:
                self.above_list.addItem('Relative humidity')
            if 'Gust wind speed' in plot_keys:
                self.above_list.addItem('Gust wind speed')
            # Adding items to qc_list
            if 'QC flags' in plot_keys:
                self.qc_list.addItem('QC flags')
        except AttributeError:
            # If you are here, there is not any plot of data
            self.statusbar.showMessage("There is no data.")
        try:
            # This is just for EMSO
            # Show the plot list
            plot_keys = list(self.egim_dict.keys())
            # Adding items to technical list
            self.technical_list.addItems(plot_keys)
            # Joining the dicts
            self.fig_dict = {**self.fig_dict, **self.egim_dict}
        except AttributeError:
            pass
        # Refresh lists
        self.hide_metadata_plots()
        self.show_metadata_plots()
        self.statusbar.showMessage("Done.")

    def view_text(self):
        """
        Show or hide the scrollable text part.
        """
        if self.text_area.isHidden():
            self.text_area.show()
        else:
            self.text_area.hide()

    """ RESAMPLE DATA, MENU DATA, RESAMPLE """

    def resample_month(self):
        """
        Resample data monthly
        """
        self.ob.resample_data('M')
        self.make_plots()
        # Remove the figure that is shown in the screen
        self.remove_fig()

    def resample_week(self):
        """
        Resample data weekely
        """
        self.ob.resample_data('W')
        self.make_plots()
        # Remove the figure that is shown in the screen
        self.remove_fig()

    def resample_day(self):
        """
        Resample data dayly
        """
        self.ob.resample_data('D')
        self.make_plots()
        # Remove the figure that is shown in the screen
        self.remove_fig()

    def resample_hour(self):
        """
        Resample data hourly
        """
        self.ob.resample_data('H')
        self.make_plots()
        # Remove the figure that is shown in the screen
        self.remove_fig()

    def refresh_fig(self):
        if self.cb_load_all_plots.isChecked():
            self.statusbar.showMessage("Updating figures. Please wait.")
            self.finish_open(self.ob)
            self.remove_fig()
            try:
                self.add_fig(self.fig_dict[self.actual_fig])
            except KeyError:
                # If you are here is becouse you don't have selected any figure.
                pass
            self.statusbar.showMessage("Done.")

    """ MENU COMPARE DATA """

    def add_param(self):
        """
        Adding the selected parameter to the mix pandas data frame.
        """
        # Clear the list of existing_param_list
        self.existent_param_list.clear()
        # Clear the text of the line edit.
        self.le_param_name.clear()
        self.le_offset.clear()
        # Adding all the parameters to the existent_param_list
        # First, let's create a list of items
        items_data = self.ob.data.keys()
        # Adding the item list to the existing_param_list
        self.existent_param_list.addItems(items_data)
        try:
            # This is just for EGIM data
            items_egim = self.ob.egim.keys()
            self.existent_param_list.addItems(items_egim)
        except AttributeError:
            pass
        # Write instructions
        self.statusbar.showMessage("Select a parameter, write a name and click to Add.")
        # Show widget
        self.w_compare.show()

    def compare_add_button(self):
        """
        Action when the user press the add button of the compare data option.
        """
        item_selected_list = [item.text() for item in self.existent_param_list.selectedItems()]
        # Check if there is any selected item
        if len(item_selected_list) == 0:
            self.statusbar.showMessage("Select a parameter, write a name and click to Add.")
            return
        # Read the name of the parameter in the line edit
        if self.le_param_name.text() == "":
            self.statusbar.showMessage("Select a parameter, write a name and click to Add.")
            return
        # Chack the input of offset
        offset = 0.0
        if len(self.le_offset.text()) > 0:
            try:
                offset = float(self.le_offset.text())
            except ValueError:
                self.statusbar.showMessage("The offset is not a number.")
                return
        self.statusbar.showMessage("Working. Please wait.")
        # Add the parameter to the mix pandas data frame
        try:
            self.mix[self.le_param_name.text()] = self.ob.data[item_selected_list[0]] + offset
        except KeyError:
            # If you are here is becouse it is an egim parameter
            self.mix[self.le_param_name.text()] = self.ob.egim[item_selected_list[0]] + offset
        # Add to the comparation list
        self.comparation_list.addItem(self.le_param_name.text())
        # Clear the text of the line edit.
        self.le_param_name.clear()
        self.le_offset.clear()
        self.statusbar.showMessage("Select a parameter, write a name and click to Add.")

    def write_le_text(self, item):
        """
        Write the text to the line edit.
        :param item: Item selected.
        """
        self.le_param_name.setText(item.text())

    def compare_del_button(self):
        """
        Delete some parameters of the compare_list
        """
        list_items = self.comparation_list.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.comparation_list.takeItem(self.comparation_list.row(item))
            del self.mix[item]

    def compare_plot_button(self):
        """
        Plot with the selected parameters.
        """
        self.statusbar.showMessage("Working. Please wait.")
        fig_compare, axes = plt.subplots(nrows=1, ncols=1)
        self.mix.interpolate().plot(ax=axes)
        axes.set_title('Comparation')
        # Show the figure
        self.remove_fig()
        self.add_fig(fig_compare)
        self.statusbar.showMessage("Done.")

    """ SLICING DATA, MENU DATA, SLICING """

    def accept_slicing(self):
        """
        Data slicing process
        """

        def formating_time(time_in):
            """
            Formating data
            Our time has a format like this: 01/01/2000 0:00:00
            We need something like this: 20000101000000
            :param time_in: time that you want to be formatted
            :type time_in:str
            :return: formated time
            """
            if time_in[12] == ':':
                time_in = time_in[6:10] + time_in[3:5] + time_in[0:2] + '0' + time_in[11] + time_in[13:15] + \
                          time_in[16:]
            else:
                time_in = time_in[6:10] + time_in[3:5] + time_in[0:2] + time_in[10:12] + time_in[13:15] + time_in[16:]
            return time_in

        start_time = self.slicing_start_time.text()
        start_time = formating_time(start_time)
        stop_time = self.slicing_end_time.text()
        stop_time = formating_time(stop_time)
        self.ob.slicing(start_time, stop_time)
        self.make_plots()
        self.remove_fig()
        self.w_slicing.hide()

    """ CLEAN BAD DATA, MENU DATA, CLEAN BAD DATA"""

    def clean_bad_data(self):
        """
        Clean bad data
        """
        self.statusbar.showMessage("Cleaning, please wait.")
        self.ob.clear_bad_data()
        self.make_plots()
        # Remove the figure that is shown in the screen
        self.remove_fig()
        self.print_text("Cleaned bad data.")
        self.statusbar.showMessage("Done, cleaned bad data.")

    """ DELETE PARAMETERS """

    def delete_parameters(self):
        """
        Delete parameters of ob.data
        """
        # Adding the parameters to the comboBox
        for key in self.ob.data.keys():
            if "_qc" in key:
                continue
            self.cb_clear_parameters.addItem(key)
        self.w_delete.show()

    def delete_apply(self):
        """
        Action to click apply button
        """
        self.print_text("Deleting {} data.".format(self.cb_clear_parameters.currentText()))
        self.statusbar.showMessage("Deleting {} data.".format(self.cb_clear_parameters.currentText()))
        self.ob.delete_param(self.cb_clear_parameters.currentText())
        self.make_plots()
        self.remove_fig()
        # Close the option
        self.w_delete.hide()
        self.statusbar.showMessage("Done.")

    """ FILTERING """

    def butterworth_init(self):
        """
        Add the parameters in the comboBox and show the options
        """
        # Adding the parameters
        for key in self.ob.data.keys():
            if "_qc" in key:
                continue
            self.cb_butterworth_parameters.addItem(key)
        # Show the option
        self.w_butterworth.show()

    def butterworth_apply(self):
        """
        Apply the butterworth filter to the data.
        """
        self.print_text("Applying Butterworth filter to {}.".format(self.cb_butterworth_parameters.currentText()))
        self.statusbar.showMessage("Applying Butterworth filter to {}.".format(
            self.cb_butterworth_parameters.currentText()))
        self.ob.butterworth_filter(component=self.cb_butterworth_parameters.currentText())
        self.make_plots()
        self.remove_fig()
        # Close the option
        self.w_butterworth.hide()
        self.statusbar.showMessage("Done.")

    """ MENU DATA, PLOT"""

    def menu_plot(self):
        # Clear the list of parameters
        self.parameter_plot_list.clear()
        # Adding all the parameters to the parameter_plot_list
        # First, let's create a list of items
        items_data = self.ob.data.keys()
        # Adding the item list to the existing_param_list
        self.parameter_plot_list.addItems(items_data)
        try:
            # This is just for EGIM data
            items_egim = self.ob.egim.keys()
            self.parameter_plot_list.addItems(items_egim)
        except AttributeError:
            pass
        # Write instructions
        self.statusbar.showMessage("Select a parameter and click Plot.")
        self.w_plot.show()

    def direct_plot(self):
        item_text = [item.text() for item in self.parameter_plot_list.selectedItems()]
        if len(item_text) > 0:
            self.statusbar.showMessage("Working. Please wait.")
            fig_compare, axes = plt.subplots(nrows=1, ncols=1)
            self.ob.data[item_text].interpolate().plot(ax=axes)
            axes.set_title(item_text[0])
            # Show the figure
            self.remove_fig()
            self.add_fig(fig_compare)
            self.statusbar.showMessage("Done.")

    """ PLOT STYLE OPTIONS, MENU SETTINGS, PLOT STYLE """

    def style_xkcd(self):
        plt.xkcd()
        self.refresh_fig()
        self.print_text("Plot style changed to xkcd.")
        self.statusbar.showMessage("Plot style changed to xkcd.")

    def style_bmh(self):
        style.use('bmh')
        self.refresh_fig()
        self.print_text("Plot style changed to bmh.")
        self.statusbar.showMessage("Plot style changed to bmh.")

    def style_classic(self):
        style.use('classic')
        self.refresh_fig()
        self.print_text("Plot style changed to classic.")
        self.statusbar.showMessage("Plot style changed to classic.")

    def style_dark_background(self):
        style.use('dark_background')
        self.refresh_fig()
        self.print_text("Plot style changed to dark_background.")
        self.statusbar.showMessage("Plot style changed to dark_background.")

    def style_fivethirtyeight(self):
        style.use('fivethirtyeight')
        self.refresh_fig()
        self.print_text("Plot style changed to fivethirtyeight.")
        self.statusbar.showMessage("Plot style changed to fivethirtyeight.")

    def style_ggplot(self):
        style.use('ggplot')
        self.refresh_fig()
        self.print_text("Plot style changed to ggplot.")
        self.statusbar.showMessage("Plot style changed to ggplot.")

    def style_grayscale(self):
        style.use('grayscale')
        self.refresh_fig()
        self.print_text("Plot style changed to grayscale.")
        self.statusbar.showMessage("Plot style changed to grayscale.")

    def style_seaborn_bright(self):
        style.use('seaborn-bright')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-bright.")
        self.statusbar.showMessage("Plot style changed to seaborn-bright.")

    def style_seaborn_colorblind(self):
        style.use('seaborn-colorblind')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-colorblind.")
        self.statusbar.showMessage("Plot style changed to seaborn-colorblind.")

    def style_seaborn_dark(self):
        style.use('seaborn-dark')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-dark.")
        self.statusbar.showMessage("Plot style changed to seaborn-dark.")

    def style_seaborn_dark_palette(self):
        style.use('seaborn-dark-palette')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-dark-palette.")
        self.statusbar.showMessage("Plot style changed to seaborn-dark-palette.")

    def style_seaborn_darkgrid(self):
        style.use('seaborn-darkgrid')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-darkgrid.")
        self.statusbar.showMessage("Plot style changed to seaborn-darkgrid.")

    def style_seaborn_deep(self):
        style.use('seaborn-deep')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-deep.")
        self.statusbar.showMessage("Plot style changed to seaborn-deep.")

    def style_seaborn_muted(self):
        style.use('seaborn-muted')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-muted.")
        self.statusbar.showMessage("Plot style changed to seaborn-muted.")

    def style_seaborn_notebook(self):
        style.use('seaborn-notebook')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-notebook.")
        self.statusbar.showMessage("Plot style changed to seaborn-notebook.")

    def style_seaborn_paper(self):
        style.use('seaborn-paper')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-paper.")
        self.statusbar.showMessage("Plot style changed to seaborn-paper.")

    def style_seaborn_pastel(self):
        style.use('seaborn-pastel')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-pastel.")
        self.statusbar.showMessage("Plot style changed to seaborn-pastel.")

    def style_seaborn_seaborn_poster(self):
        style.use('seaborn-poster')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-poster.")
        self.statusbar.showMessage("Plot style changed to seaborn-poster.")

    def style_seaborn_talk(self):
        style.use('seaborn-talk')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-talk.")
        self.statusbar.showMessage("Plot style changed to seaborn-talk.")

    def style_seaborn_ticks(self):
        style.use('seaborn-ticks')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-ticks.")
        self.statusbar.showMessage("Plot style changed to seaborn-ticks.")

    def style_seaborn_white(self):
        style.use('seaborn_white')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn_white.")
        self.statusbar.showMessage("Plot style changed to seaborn_white.")

    def style_seaborn_whitegrid(self):
        style.use('seaborn-whitegrid')
        self.refresh_fig()
        self.print_text("Plot style changed to seaborn-whitegrid.")
        self.statusbar.showMessage("Plot style changed to seaborn-whitegrid.")


def open_gui():
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())


def open_emsodev_app():
    app_emso = QtGui.QApplication(sys.argv)
    window_emso = EMSOdevApp()
    window_emso.show()
    app_emso.exec_()


if __name__ == "__main__":
    open_gui()
    # open_emsodev_app()
