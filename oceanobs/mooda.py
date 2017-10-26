from functools import partial
from PyQt4.QtCore import QThread, SIGNAL
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import matplotlib.style as style
try:
    import inwater as wt
    from mooda_ui import *
except ImportError:
    import oceanobs.inwater as wt
    from oceanobs.mooda_ui import *


class MOODA(QtGui.QMainWindow, Ui_mooda_window):

    def __init__(self, login, password, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Instance variables
        self.downloader = wt.EGIM(login=login, password=password)
        self.download_thread = None
        self.qc_thread = None
        self.plot_thread = None
        self.wf = wt.WaterFrame()
        self.wf_original = wt.WaterFrame()
        self.plot_canvas_1 = None
        self.plot_toolbar_1 = None
        self.plot_canvas_2 = None
        self.plot_toolbar_2 = None
        self.plot_switch = 1
        self.save_path = ""
        self.num = 0  # Number of the place to plot
        self.egim_meanings = {
            "EMSODEV-EGIM-node00001": "EGIM Vilanova",
            "37-14998": "CTD",
            "Workhorse_ADCP_21582": "ADCP",
            "0e5f248e-9e90-465f-91a0-f674b1d4eb3a": "EGIM",
            "SBE54-0049": "Tsunameter",
            "4381-606": "Oximeter",
            "NTURTD-648": "Turbidimeter",
            "icListen-1636": "Hydrophone",
        }



        # Connexions of w_egim
        self.cb_observatories.clicked.connect(self.egim_all_observatories)
        self.lw_observatories.itemClicked.connect(self.egim_write_instruments)
        self.cb_instruments.clicked.connect(self.egim_all_instruments)
        self.lw_instruments.itemClicked.connect(self.egim_write_parameters)
        self.lw_parameters.itemClicked.connect(partial(self.pb_download.setEnabled, True))
        self.cb_parameters.clicked.connect(self.egim_all_parameters)
        self.pb_download.clicked.connect(self.egim_download_data)
        self.pb_save.clicked.connect(self.egim_save_data)
        self.de_start_date.dateChanged.connect(self.egim_start_changed)
        self.de_end_date.dateChanged.connect(self.egim_end_changed)
        self.pb_close_egim.clicked.connect(partial(self.w_egim.setVisible, False))

        # Connexions of w_inspector
        self.pb_plot.clicked.connect(self.inspector_plot)

        # Connexions of menu Actions
        # Menu "File"
        self.a_open.triggered.connect(self.open)
        self.a_download.triggered.connect(self.download)
        self.a_save.triggered.connect(self.save)
        self.a_save_as.triggered.connect(self.save_as)
        self.a_save_log.triggered.connect(self.save_log)
        self.a_close.triggered.connect(self.close_work)
        self.a_quit.triggered.connect(sys.exit)
        # Menu "Data"
        self.a_qc.triggered.connect(self.qc)
        # Sub-menu "Average"
        self.a_none.triggered.connect(self.average_none)
        self.a_minutely.triggered.connect(self.average_minutely)
        self.a_hourly.triggered.connect(self.average_hourly)
        self.a_daily.triggered.connect(self.average_daily)
        self.a_weekely.triggered.connect(self.average_weekly)
        # Menu "View"
        self.a_egim_downloader.triggered.connect(self.w_egim.setVisible)
        self.a_logbook.triggered.connect(self.pte_text.setVisible)
        self.a_data_inspector.triggered.connect(self.w_inspector.setVisible)
        # Menu "Settings"
        # Sub-menu "Plot style"
        self.a_bmh.triggered.connect(self.style_bmh)
        self.a_classic.triggered.connect(self.style_classic)
        self.a_dark.triggered.connect(self.style_dark)
        self.a_fivethirtyeight.triggered.connect(self.style_fivethirtyeight)
        self.a_ggplot.triggered.connect(self.style_ggplot)
        self.a_grayscale.triggered.connect(self.style_grayscale)
        # Sub-menu "Number of plots"
        self.a_1.triggered.connect(self.plot_one)
        self.a_2.triggered.connect(self.plot_two)
        # Menu Help
        self.a_about.triggered.connect(self.about)

        # Visual configuration
        self.w_egim.setVisible(False)
        self.pte_text.setVisible(False)
        self.w_inspector.setVisible(False)
        self.m_data.setEnabled(False)
        self.a_save.setEnabled(False)
        self.a_save_as.setEnabled(False)
        self.a_close.setEnabled(False)
        self.a_save_log.setEnabled(False)
        style.use("ggplot")

        # Add actions recent data
        try:
            actions = []
            with open('recent.txt') as f:
                paths = f.readlines()
                for path in paths:
                    recent_action = QtGui.QAction(path, self)
                    # We save the path into a list with the path and without the last character (\n)
                    path_list = [path[:-1]]
                    recent_action.triggered.connect(partial(self.load_data, path_list))
                    actions.append(recent_action)
            for action in actions:
                self.m_recent_data.addAction(action)
        except FileNotFoundError:
            self.m_recent_data.setEnabled(False)

    def open(self):
        """
        It opens a file and extract a WaterFrame object.
        """

        # Creation of a QFileDialog to know the path
        path = QtGui.QFileDialog.getOpenFileNames(None, 'Open data', "", "pickle (*.pkl);;netCDF (*.nc);;TXT (*.txt)")
        if len(path) > 0:
            # Save the path into the recent.txt file
            with open("recent.txt", "a") as f:
                for path_ in path:
                    f.write(path_ + "\n")
            self.load_data(path)

    def load_data(self, path):
        """
        It load data from a file.
        :param path: List of paths.
        :type path: list
        """
        self.statusbar.showMessage("Opening data. Please wait.")
        print(path[0])
        self.wf = wt.WaterFrame(path[0])
        self.statusbar.showMessage("Done.")
        # Write info in pte_text
        self.pte_text.appendPlainText(self.wf.info(path))

        # Load data to tv_inspector
        self.inspector_load()

    def download(self):
        """
        It opens the widget egim downloader.
        """
        self.w_egim.setVisible(True)
        self.a_egim_downloader.setChecked(True)
        self.egim_write_observatories()

    def save(self):
        """
        It saves the WaterFrame object.
        :return:
        """
        if self.save_path == "":
            self.save_as()
        else:
            self.wf.to_pickle(self.save_path)
            self.statusbar.showMessage("Data saved in {}.".format(self.save_path))

    def save_as(self):
        """
        It saves a WaterFrame Object.
        """
        path = QtGui.QFileDialog.getSaveFileName(self, "Save WaterFrame", "", "*.pkl")
        if len(path) > 0:
            self.save_path = path
            self.wf.to_pickle(path)
            self.statusbar.showMessage("Data saved in {}.".format(self.save_path))

    def save_log(self):
        """
        Save the w_text in a text file.
        """
        path = QtGui.QFileDialog.getSaveFileName(self, "Save Data Logger", "", "*.txt")
        if len(path) > 0:
            f = open(path, 'w')
            f.write(self.pte_text.toPlainText())

    def close_work(self):
        """
        It closes the work widget and delete the actual WaterFrame.
        """

        # Visual configuration
        self.w_inspector.setVisible(False)
        self.a_data_inspector.setChecked(False)
        self.w_tree.clear()
        self.m_data.setEnabled(False)

        self.wf = wt.WaterFrame()

    def qc(self):
        self.statusbar.showMessage("Creating QC Flags. Please, wait.")
        # Download thread configuration
        self.qc_thread = self.QCThread(self.wf)
        self.connect(self.qc_thread, SIGNAL("refresh"), self.qc_refresh)
        self.qc_thread.start()

    def qc_refresh(self, wf_qc):
        """
        It uploads wf.data
        :param wf_qc: New WaterFrame Object
        """
        self.wf.data = wf_qc.data.copy()
        self.statusbar.showMessage("Done.")

    def average_uncheck(self):
        """
        Uncheck all the average possibilities.
        """
        self.a_none.setChecked(False)
        self.a_minutely.setChecked(False)
        self.a_hourly.setChecked(False)
        self.a_daily.setChecked(False)
        self.a_weekely.setChecked(False)

    def average_none(self):
        """
        Set to none the average of data.
        """
        self.average_uncheck()
        self.a_none.setChecked(True)
        # Copy the original data
        self.wf.data = self.wf_original.data.copy()
        self.wf.technical = self.wf_original.technical.copy()

    def average_minutely(self):
        """
        Set to none the average of data.
        """
        self.average_uncheck()
        self.a_minutely.setChecked(True)
        self.statusbar.showMessage("Resampling data. Please wait.")
        # Copy the original data
        self.wf.data = self.wf_original.data.copy()
        self.wf.technical = self.wf_original.technical.copy()
        # Resample
        self.wf.resample('min')
        self.statusbar.showMessage("Done.")

    def average_hourly(self):
        """
        Set to none the average of data.
        """
        self.average_uncheck()
        self.a_hourly.setChecked(True)
        self.statusbar.showMessage("Resampling data. Please wait.")
        # Copy the original data
        self.wf.data = self.wf_original.data.copy()
        self.wf.technical = self.wf_original.technical.copy()
        # Resample
        self.wf.resample('H')
        self.statusbar.showMessage("Done.")

    def average_daily(self):
        """
        Set to none the average of data.
        """
        self.average_uncheck()
        self.a_daily.setChecked(True)
        self.statusbar.showMessage("Resampling data. Please wait.")
        # Copy the original data
        self.wf.data = self.wf_original.data.copy()
        self.wf.technical = self.wf_original.technical.copy()
        # Resample
        self.wf.resample('D')
        self.statusbar.showMessage("Done.")

    def average_weekly(self):
        """
        Set to none the average of data.
        """
        self.average_uncheck()
        self.a_weekely.setChecked(True)
        self.statusbar.showMessage("Resampling data. Please wait.")
        # Copy the original data
        self.wf.data = self.wf_original.data.copy()
        self.wf.technical = self.wf_original.technical.copy()
        # Resample
        self.wf.resample('W')
        self.statusbar.showMessage("Done.")

    def inspector_plot(self):
        """
        It creates the graph and show it into the w_plot.
        :return:
        """
        def remove_plot():
            if self.a_1.isChecked():
                try:
                    self.plot_remove_1()
                except AttributeError:
                    # There is no plot to remove.
                    pass
                try:
                    self.plot_remove_2()
                except AttributeError:
                    # There is no plot to remove.
                    pass
            else:
                if self.plot_switch == 1:
                    try:
                        self.plot_remove_1()
                    except AttributeError:
                        # There is no plot to remove.
                        pass
                else:
                    try:
                        self.plot_remove_2()
                    except AttributeError:
                        # There is no plot to remove.
                        pass

        # Obtain the parameter name of the w_tree
        item = self.w_tree.selectedItems()[0].text(0)

        parts = item.split("(")
        try:
            parameter = parts[1][:-1]
        except IndexError:
            # Nothing to plot
            return
        remove_plot()
        if "slots" in item:
            # It is a predefined plot

            # Plot thread configuration
            # self.plot_thread = self.PlotThread(self.wf, parameter=parameter, predefined=True)
            # self.connect(self.plot_thread, SIGNAL("plot"), self.plot_add_1)
            # self.plot_thread.start()

            fig = self.wf.predefined_plot(parameter)
        elif self.cb_join.isChecked():
            # It is a normal plot, with join argument
            parts = parameter.split("_")
            if self.cb_qc1.isChecked():
                fig = self.wf.plot(parts[0], join=True, qc_flag=1)
            else:
                fig = self.wf.plot(parts[0], join=True)
        elif self.cb_qc1.isChecked():
            fig = self.wf.plot(parameter, qc_flag=1)
        else:
            # It is a normal plot, without join argument
            fig = self.wf.plot(parameter)
        if self.a_1.isChecked():
            self.plot_add_1(fig)
        else:
            if self.plot_switch == 1:
                self.plot_add_1(fig)
                self.plot_switch = 2
            else:
                self.plot_add_2(fig)
                self.plot_switch = 1
        # Resize w_inspector
        self.w_inspector.setMaximumWidth(470)

    def inspector_load(self):

        self.w_tree.clear()

        # Creation of the header
        header = QtGui.QTreeWidgetItem(["Data inspector"])
        self.w_tree.setHeaderItem(header)

        # Metadata in tv_inspector
        metadata_tree = QtGui.QTreeWidgetItem(self.w_tree, ["Metadata"])
        for key in self.wf.metadata.keys():
            if key == "summary":
                summary_tree = QtGui.QTreeWidgetItem(metadata_tree, [key])
                for summary_key in self.wf.metadata['summary'].keys():
                    summary_row = QtGui.QTreeWidgetItem(summary_tree, [summary_key])
                    for parameter_key in self.wf.metadata['summary'][summary_key].keys():
                        QtGui.QTreeWidgetItem(summary_row,
                                              ["{}: {}".format(parameter_key,
                                                               self.wf.metadata['summary'][summary_key]
                                                               [parameter_key])])
            else:
                QtGui.QTreeWidgetItem(metadata_tree, ["{}: {}".format(key, self.wf.metadata[key])])

        # Data in tree
        data_tree = QtGui.QTreeWidgetItem(self.w_tree, ["Data"])
        for key in self.wf.data.keys():
            if "_qc" in key:
                continue
            elif "latitude" in key:
                continue
            elif "longitude" in key:
                continue
            elif "time" in key:
                continue
            QtGui.QTreeWidgetItem(data_tree, ["{} ({})".format(self.wf.acronym[key]['long_name'], key)])

        # Technical in tree
        # Sometimes there are no technical parameters
        if len(self.wf.technical.keys()) > 0:
            technical_tree = QtGui.QTreeWidgetItem(self.w_tree, ["Technical"])
            for key in self.wf.technical.keys():
                QtGui.QTreeWidgetItem(technical_tree, ["{} ({})".format(self.wf.acronym[key]['long_name'], key)])
            predefined_tree = QtGui.QTreeWidgetItem(technical_tree, ["Predefined plots"])
            if all(x in self.wf.technical.keys() for x in
                   ['current_slot1', 'current_slot2', 'current_slot3', 'current_slot4', 'current_slot5', 'voltage']):
                QtGui.QTreeWidgetItem(predefined_tree, ["Current of slots (current_slots)"])
            if all(x in self.wf.technical.keys() for x in
                   ['temperature_slot1', 'temperature_slot2', 'temperature_slot3', 'temperature_slot4',
                    'temperature_slot5']):
                QtGui.QTreeWidgetItem(predefined_tree, ["Temperature of slots (temperature)"])
            if all(x in self.wf.technical.keys() for x in ['sd_slot1', 'sd_slot2', 'sd_slot3', 'sd_slot4', 'sd_slot5']):
                QtGui.QTreeWidgetItem(predefined_tree, ["Remaining memory of slots (sd)"])

        # We copy the dataframes into the wf_original
        self.wf_original.data = self.wf.data.copy()
        self.wf_original.technical = self.wf.technical.copy()
        self.wf_original.metadata = self.wf.metadata.copy()
        self.wf_original.acronym = self.wf.acronym.copy()

        self.w_inspector.setVisible(True)
        self.a_data_inspector.setChecked(True)
        self.m_data.setEnabled(True)
        self.a_save.setEnabled(True)
        self.a_save_as.setEnabled(True)
        self.a_quit.setEnabled(True)
        self.a_close.setEnabled(True)
        self.a_save_log.setEnabled(True)

    def plot_add_1(self, fig):
        """
        It creates a canvas container and place it into the w_plot.
        :param fig: Figure to show
        """
        # We create the canvas and add it into the w_plot.
        self.plot_canvas_1 = FigureCanvas(fig)
        self.vl_plot.addWidget(self.plot_canvas_1)
        self.plot_canvas_1.draw()
        # We create a matplotlib toolbar
        self.plot_toolbar_1 = NavigationToolbar(self.plot_canvas_1, self.w_plot, coordinates=True)
        self.vl_plot.addWidget(self.plot_toolbar_1)
        # Si queremos que el toolbar este fuera, es la siguiente linea
        # self.addToolBar(self.plot_toolbar)

    def plot_add_2(self, fig):
        """
        It creates a canvas container and place it into the w_plot.
        :param fig: Figure to show
        """
        # We create the canvas and add it into the w_plot.
        self.plot_canvas_2 = FigureCanvas(fig)
        self.vl_plot.addWidget(self.plot_canvas_2)
        self.plot_canvas_2.draw()
        # We create a matplotlib toolbar
        self.plot_toolbar_2 = NavigationToolbar(self.plot_canvas_2, self.w_plot, coordinates=True)
        self.vl_plot.addWidget(self.plot_toolbar_2)
        # Si queremos que el toolbar este fuera, es la siguiente linea
        # self.addToolBar(self.plot_toolbar)

    def plot_remove_1(self):
        """
        Remove the actual figure.
        """
        self.plot_canvas_1.close()
        self.vl_plot.removeWidget(self.plot_canvas_1)
        self.plot_canvas_1.close()
        self.vl_plot.removeWidget(self.plot_toolbar_1)
        self.plot_toolbar_1.close()

    def plot_remove_2(self):
        """
        Remove the actual figure.
        """
        self.plot_canvas_2.close()
        self.vl_plot.removeWidget(self.plot_canvas_2)
        self.plot_canvas_2.close()
        self.vl_plot.removeWidget(self.plot_toolbar_2)
        self.plot_toolbar_2.close()

    def plot_one(self):
        """
        It allows to show just one figure.
        """
        if self.a_2.isChecked():
            self.a_2.setChecked(False)
        else:
            self.a_1.setChecked(True)

    def plot_two(self):
        """
        It allows to show two figures.
        """
        if self.a_1.isChecked():
            self.a_1.setChecked(False)
            self.plot_switch = 2
        else:
            self.a_2.setChecked(True)

    def style_uncheck(self):
        """
        Uncheck to all the style actions.
        """
        self.a_bmh.setChecked(False)
        self.a_classic.setChecked(False)
        self.a_dark.setChecked(False)
        self.a_fivethirtyeight.setChecked(False)
        self.a_ggplot.setChecked(False)
        self.a_grayscale.setChecked(False)
        self.a_seaborn.setChecked(False)

    def style_bmh(self):
        """
        It changes the matplotlib style to bmh.
        """
        self.style_uncheck()
        style.use("bmh")
        self.a_bmh.setChecked(True)

    def style_classic(self):
        """
        It changes the matplotlib style to classic.
        """
        self.style_uncheck()
        style.use("classic")
        self.a_classic.setChecked(True)

    def style_dark(self):
        """
        It changes the matplotlib style to dark background.
        """
        self.style_uncheck()
        style.use("dark_background")
        self.a_dark.setChecked(True)

    def style_fivethirtyeight(self):
        """
        It changes the matplotlib style to fivethirtyeight.
        """
        self.style_uncheck()
        style.use("fivethirtyeight")
        self.a_fivethirtyeight.setChecked(True)

    def style_ggplot(self):
        """
        It changes the matplotlib style to ggplot.
        """
        self.style_uncheck()
        style.use("ggplot")
        self.a_ggplot.setChecked(True)

    def style_grayscale(self):
        """
        It changes the matplotlib style to grayscale.
        """
        self.style_uncheck()
        style.use("grayscale")
        self.a_grayscale.setChecked(True)

    def egim_disabled_instruments(self):
        """
        Disable gb_instruments, gb_parameters and gb_dates.
        """
        self.gb_instruments.setEnabled(False)
        self.gb_parameters.setEnabled(False)
        self.gb_dates.setEnabled(False)

    def egim_write_observatories(self):
        """
        It writes in the lw_observatories the list of available observatories.
        """
        self.statusbar.showMessage("Loading observatories. Please wait.")
        self.lw_observatories.clear()
        code = self.downloader.load_observatories()
        self.lw_observatories.clear()
        if len(self.downloader.observatories) > 0:
            for observatory in self.downloader.observatories:
                try:
                    self.lw_observatories.addItem(self.egim_meanings[observatory])
                except KeyError:
                    self.lw_observatories.addItem(observatory)
            self.w_egim.setEnabled(True)
            self.statusbar.showMessage("Please, select an observatory.")
        else:
            if code == 0:
                self.statusbar.showMessage("Error: Please, check the Internet connexion.")
            else:
                self.statusbar.showMessage("Error: Something happen with the connexion.")

    def egim_all_observatories(self, checked):
        """
        It allows to select an observatory.
        :param checked: Check of the self.cb_all_observatories
        """
        if checked:
            self.lw_observatories.setEnabled(False)
            self.gb_instruments.setEnabled(True)
        else:
            self.lw_observatories.setEnabled(True)
            if self.lw_instruments.count() == 0:
                self.gb_instruments.setEnabled(False)

    def egim_write_instruments(self, selection):
        """
        It writes an instrument list into the lw_instruments.
        :param selection: Selected item.
        """
        self.statusbar.showMessage("Loading instruments. Please wait.")
        for key, meaning in self.egim_meanings.items():
            if selection.text() == meaning:
                self.downloader.observatory_name = key
        self.downloader.load_instruments()
        self.lw_instruments.clear()
        if len(self.downloader.instruments) > 0:
            for instrument in self.downloader.instruments:
                try:
                    self.lw_instruments.addItem(self.egim_meanings[instrument])
                except KeyError:
                    self.lw_instruments.addItem(instrument)
            self.gb_instruments.setEnabled(True)
            self.statusbar.showMessage("Please, select an instrument.")
        else:
            self.statusbar.showMessage("Error: Something happen with the connexion.")

    def egim_all_instruments(self, checked):
        """
        It allows to select all instruments.
        :param checked: bool
        """
        if checked:
            self.lw_instruments.setEnabled(False)
            self.gb_parameters.setEnabled(True)
        else:
            self.lw_instruments.setEnabled(True)
            if self.lw_parameters.count() == 0:
                self.gb_parameters.setEnabled(False)

    def egim_write_parameters(self, selection):
        """
        It search and write in the self.lw_parameters the parameters.
        :param selection: list widget item.
        """
        self.statusbar.showMessage("Loading parameters. Please wait.")
        for key, meaning in self.egim_meanings.items():
            if selection.text() == meaning:
                self.downloader.instrument_name = key
        self.downloader.load_parameters()
        self.lw_parameters.clear()
        if len(self.downloader.parameters) > 0:
            for parameter in self.downloader.parameters:
                try:
                    self.lw_parameters.addItem(self.egim_meanings[parameter])
                except KeyError:
                    self.lw_parameters.addItem(parameter)
            self.statusbar.showMessage("Please, select a parameter and click to download.")
            self.gb_parameters.setEnabled(True)
            self.gb_dates.setEnabled(True)
            if self.cb_parameters.isChecked():
                self.lw_parameters.setEnabled(False)
        else:
            self.statusbar.showMessage("There are no parameters, please select an other instrument.")

    def egim_all_parameters(self, checked):
        """
        It allows to select all the parameters.
        :param checked:
        :return:
        """
        if checked:
            self.lw_parameters.setEnabled(False)
            self.gb_dates.setEnabled(True)
            self.pb_download.setEnabled(True)
        else:
            self.lw_parameters.setEnabled(True)
            if self.lw_parameters.count() == 0:
                self.gb_dates.setEnabled(False)
                self.pb_download.setEnabled(False)

    def egim_download_data(self):
        """
        It downloads the selected data.
        """

        # Download thread configuration
        self.download_thread = self.DownloadThread(self.downloader, self.de_start_date.text(), self.de_end_date.text(),
                                                   self.cb_observatories.isChecked(), self.cb_instruments.isChecked(),
                                                   self.cb_parameters.isChecked(), self.lw_parameters.currentItem())
        self.connect(self.download_thread, SIGNAL("message(QString)"), self.statusbar.showMessage)
        self.connect(self.download_thread, SIGNAL("refresh"), self.egim_refresh_downloader)
        self.download_thread.start()

        # Disable buttons
        self.pb_download.setEnabled(False)
        self.pb_save.setEnabled(False)

    def egim_refresh_downloader(self, downloader):
        self.downloader.wf.data = downloader.wf.data.copy()
        self.downloader.wf.technical = downloader.wf.technical.copy()
        self.downloader.wf.acronym = downloader.wf.acronym.copy()
        self.downloader.metadata = downloader.wf.metadata.copy()
        self.pb_save.setEnabled(True)
        self.wf.data = downloader.wf.data.copy()
        self.wf.technical = downloader.wf.technical.copy()
        self.wf.metadata = downloader.wf.metadata.copy()
        self.wf.acronym = downloader.wf.acronym.copy()
        # We select the "time" as index of the pandas DataFrame
        self.wf.data.set_index('time', inplace=True)
        try:
            self.wf.technical.set_index('time', inplace=True)
        except KeyError:
            # There is nothing in self.wf.technical
            pass
        self.inspector_load()

    def egim_start_changed(self):
        self.de_end_date.setDate(self.de_start_date.date().addDays(1))
        self.de_end_date.setMinimumDate(self.de_start_date.date().addDays(1))
        self.pb_download.setEnabled(True)
        # Clear previous data
        self.downloader.clean()

    def egim_end_changed(self):
        self.pb_download.setEnabled(True)
        # Clear previous data
        self.downloader.clean()

    def egim_save_data(self):
        """
        It saves the WaterFrame object.
        """
        path = QtGui.QFileDialog.getSaveFileName(self, "Save WaterFrame", "", "*.pkl")
        if len(path) > 0:
            self.save_path = path
            self.downloader.wf.to_pickle(path)

    def about(self):
        QtGui.QMessageBox.about(self, "About MOODA",
                                "Version: 0.1\n"
                                "Compatible observatories:\n"
                                "\tEGIMs via File->Download data\n"
                                "\tNetCDF from the mooring series of EMODnet\n"
                                "\t\t(www.emodnet-physics.eu/Map/)\n"
                                "\tNetCDF from the mooring series of JERICO\n"
                                "\t\t(www.jerico-ri.eu/data-access/)\n"
                                "\tOBSEA\n"
                                "\t\t(www.obsea.es)\n"
                                "Online documentation: https://github.com/rbardaji/inWater\n"
                                "Source code: https://github.com/rbardaji/inWater")

    class DownloadThread(QThread):
        """
        Thread to create a non blocking downloader
        """
        def __init__(self, downloader, start_date, end_date, all_observatories, all_instruments, all_parameters,
                     parameter_item):
            QThread.__init__(self)

            # Instance variables
            self.downloader = downloader
            self.start_date = start_date
            self.end_date = end_date
            self.all_observatories = all_observatories
            self.all_instruments = all_instruments
            self.all_parameters = all_parameters
            try:
                self.parameter = parameter_item.text()
            except AttributeError:
                self.parameter = ""

        def __del__(self):
            self.wait()

        def run(self):
            if self.all_observatories:
                if self.all_instruments:
                    if self.all_parameters:
                        # Download all parameters from all instruments and all observatories
                        for self.downloader.observatory_name in self.downloader.observatories:
                            for self.downloader.instrument_name in self.downloader.instruments:
                                for self.downloader.parameter_name in self.downloader.parameters:
                                    self.emit(SIGNAL('message(QString)'),
                                              "Downloading {} of {} from {}. Please wait.".format(
                                                  self.downloader.parameter_name, self.downloader.instrument_name,
                                                  self.downloader.observatory_name))
                                    self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")
                    else:
                        # Download one parameter of all instruments and observatories
                        self.downloader.parameter_name = self.parameter
                        for self.downloader.observatory_name in self.downloader.observatories:
                            for self.downloader.instrument_name in self.downloader.instruments:
                                self.emit(SIGNAL('message(QString)'), "Downloading {} from {}. Please wait.".format(
                                    self.downloader.parameter_name, self.downloader.observatory_name))
                            self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")
                else:
                    if self.all_parameters:
                        # Download all the parameters of one instrument of all observatories
                        for self.downloader.observatory_name in self.downloader.observatories:
                            for self.downloader.parameter_name in self.downloader.parameters:
                                self.emit(SIGNAL('message(QString)'), "Downloading {} from {}. Please wait.".format(
                                    self.downloader.parameter_name, self.downloader.observatory_name))
                            self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")

                    else:
                        # Download one parameter of one instrument of all observatories
                        self.downloader.parameter_name = self.parameter
                        for self.downloader.observatory_name in self.downloader.observatories:
                            self.emit(SIGNAL('message(QString)'),
                                      "Downloading {} from {}. Please wait.".format(self.downloader.parameter_name,
                                                                                    self.downloader.observatory_name))
                            self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")
            else:
                if self.all_instruments:
                    if self.all_parameters:
                        # Download all parameters and instruments
                        for self.downloader.instrument_name in self.downloader.instruments:
                            self.downloader.load_parameters()
                            for self.downloader.parameter_name in self.downloader.parameters:
                                self.emit(SIGNAL('message(QString)'), "Downloading {} from {}. Please wait.".format(
                                    self.downloader.parameter_name, self.downloader.instrument_name))
                                self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")
                    else:
                        # Download one parameter of all instruments
                        self.downloader.parameter_name = self.parameter
                        for self.downloader.instrument_name in self.downloader.instruments:
                            self.emit(SIGNAL('message(QString)'), "Downloading {} from {}. Please wait.".format(
                                self.downloader.parameter_name, self.downloader.instrument_name))
                            self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")
                else:
                    if self.all_parameters:
                        # Download all the parameters
                        for self.downloader.parameter_name in self.downloader.parameters:
                            self.emit(SIGNAL('message(QString)'), "Downloading {}. Please wait.".format(
                                self.downloader.parameter_name))
                            self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")

                    else:
                        # Download only one parameter
                        self.downloader.parameter_name = self.parameter
                        self.emit(SIGNAL('message(QString)'), "Downloading {}. Please wait.".format(
                            self.downloader.parameter_name))
                        self.downloader.load_data(self.start_date, self.end_date)
                        self.emit(SIGNAL('message(QString)'), "Done, now you can save it or continue working.")
            self.emit(SIGNAL('refresh'), self.downloader)

    class QCThread(QThread):
        """
        Thread to create a non blocking QC
        """
        def __init__(self, wf):
            QThread.__init__(self)

            # Instance variables
            self.wf_qc = wf

        def __del__(self):
            self.wait()

        def run(self):
            self.wf_qc.qc()
            self.emit(SIGNAL('refresh'), self.wf_qc)

    class PlotThread(QThread):
        """
        Thread to create a non blocking QC
        """
        def __init__(self, wf, parameter, join=False, predefined=False):
            QThread.__init__(self)

            # Instance variables
            self.wf_plot = wf
            self.parameter = parameter
            self.join = join
            self.predefined = predefined

        def __del__(self):
            self.wait()

        def run(self):
            if self.predefined:
                fig = self.wf_plot.predefined_plot(self.parameter)
            else:
                fig = self.wf_plot(self.parameter, join=self.join)
            self.emit(SIGNAL('plot'), fig)


def open_mooda(login, password):
    global app_mooda
    app_mooda = QtGui.QApplication(sys.argv)
    window_mooda = MOODA(login, password)
    window_mooda.show()
    app_mooda.exec_()


def main():
    login_in = ""
    password_in = ""
    if login_in is None:
        print("I'm sorry, EMSODEV API is under development, and now you need a login and a password. "
              "This fact will change before April 2018.")

    open_mooda(login=login_in, password=password_in)

if __name__ == "__main__":
    main()
