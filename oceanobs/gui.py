import sys
from matplotlib import style

from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

from mainwindow_ui import *
try:
    import oceanobs.obsea as obsea
    import oceanobs.emodnet as emodnet
except ImportError:
    import obsea
    import emodnet


class MyApplication(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Define the style of plots
        style.use('ggplot')

        # Class variables
        self.canvas = None
        self.toolbar_plot = None
        self.data = None
        self.fig_dict = {}
        self.ob = None
        self.actual_fig = ""
        self.report_path = ""

        # Menu "File"
        self.actionOpenData.triggered.connect(self.open)
        self.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        # Menu "Report"
        # Hide menu
        self.menuReport.menuAction().setVisible(False)
        self.actionSave_as.triggered.connect(self.report_save_as)
        self.actionSave.triggered.connect(self.report_save)

        # Menu "Data"
        self.menuData.menuAction().setVisible(False)
        self.actionSlicing.triggered.connect(self.show_slicing)
        # Sub-menu "Resample"
        self.actionMonth_frequency.triggered.connect(self.resample_month)
        self.actionWeekly_frequency.triggered.connect(self.resample_week)
        self.actionDay_frequency.triggered.connect(self.resample_day)
        self.actionHourly_frequency.triggered.connect(self.resample_hour)
        # Slicing option
        self.slicing_accept_button.clicked.connect(self.accept_slicing)
        self.slicing_cancel_button.clicked.connect(self.hide_slicing)

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

        # Hide all inforamtion
        self.hide_all()
        self.hide_slicing()

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
        self.make_plots()
        self.remove_fig()
        self.add_fig(self.fig_dict[self.actual_fig])

    def style_xkcd(self):
        plt.xkcd()
        self.refresh_fig()

    def style_bmh(self):
        style.use('bmh')
        self.refresh_fig()

    def style_classic(self):
        style.use('classic')
        self.refresh_fig()

    def style_dark_background(self):
        style.use('dark_background')
        self.refresh_fig()

    def style_fivethirtyeight(self):
        style.use('fivethirtyeight')
        self.refresh_fig()

    def style_ggplot(self):
        style.use('ggplot')
        self.refresh_fig()

    def style_grayscale(self):
        style.use('grayscale')
        self.refresh_fig()

    def style_seaborn_bright(self):
        style.use('seaborn-bright')
        self.refresh_fig()

    def style_seaborn_colorblind(self):
        style.use('seaborn-colorblind')
        self.refresh_fig()

    def style_seaborn_dark(self):
        style.use('seaborn-dark')
        self.refresh_fig()

    def style_seaborn_dark_palette(self):
        style.use('seaborn-dark-palette')
        self.refresh_fig()

    def style_seaborn_darkgrid(self):
        style.use('seaborn-darkgrid')
        self.refresh_fig()

    def style_seaborn_deep(self):
        style.use('seaborn-deep')
        self.refresh_fig()

    def style_seaborn_muted(self):
        style.use('seaborn-muted')
        self.refresh_fig()

    def style_seaborn_notebook(self):
        style.use('seaborn-notebook')
        self.refresh_fig()

    def style_seaborn_paper(self):
        style.use('seaborn-paper')
        self.refresh_fig()

    def style_seaborn_pastel(self):
        style.use('seaborn-pastel')
        self.refresh_fig()

    def style_seaborn_seaborn_poster(self):
        style.use('seaborn-poster')
        self.refresh_fig()

    def style_seaborn_talk(self):
        style.use('seaborn-talk')
        self.refresh_fig()

    def style_seaborn_ticks(self):
        style.use('seaborn-ticks')
        self.refresh_fig()

    def style_seaborn_white(self):
        style.use('seaborn_white')
        self.refresh_fig()

    def style_seaborn_whitegrid(self):
        style.use('seaborn-whitegrid')
        self.refresh_fig()

    def hide_all(self):
        """
        Escondemos la informacion de metadatos
        :return:
        """
        self.title_platform_code.hide()
        self.platform_code.hide()
        self.wmo_code.hide()
        self.title_wmo_code.hide()
        self.institution.hide()
        self.title_institution.hide()
        self.assembly_center.hide()
        self.title_assembly_center.hide()
        self.type.hide()
        self.title_type.hide()
        self.title_plots.hide()
        self.title_above.hide()
        self.above_list.hide()
        self.title_under.hide()
        self.under_list.hide()

    def open(self):
        """
        Open data file
        """
        path = QtGui.QFileDialog.getOpenFileNames(None, 'Open TXT or netCDF', "", "TXT (*.txt);;netCDF (*.nc)")
        if len(path) > 0:
            # Open observatory object
            self.statusbar.showMessage("Opening data. Please wait.")
            # Know if it is an OBSEA file or an EMODnet file
            if path[0][-1] == 't' or path[0][-1] == 'T':
                # It is a txt file so let's open OBSEA
                self.ob = obsea.OBSEA(path)
            else:
                # It is an EMODnet file, so let's open a EMODnet
                self.ob = emodnet.EMODnet(path)
            if self.ob.dialog:
                # Error message
                self.statusbar.showMessage(self.ob.dialog)
                return
            # Extract metadata information
            self.show_metadata(self.ob.metadata)
            # Añadimos las figuras
            self.make_plots()
            # Remove the figure that is shown in the screen
            self.remove_fig()
            self.statusbar.showMessage("Done.")
            # Show menu "Data"
            self.menuData.menuAction().setVisible(True)

    def show_metadata(self, metadata):
        """
        Mostramos los metadatos
        :param metadata: los metadatos
        :type metadata: Pandas dataframe
        """
        self.platform_code.setText(metadata['platform_code'][0])
        self.platform_code.show()
        self.title_platform_code.show()
        self.wmo_code.setText(metadata['wmo_platform_code'][0])
        self.wmo_code.show()
        self.title_wmo_code.show()
        self.institution.setText(metadata['institution'][0])
        self.institution.show()
        self.title_institution.show()
        # self.assembly_center.setText(metadata.loc['DATA ASSEMBLY CENTER'].item())
        # self.assembly_center.show()
        # self.title_assembly_center.show()
        self.type.setText(metadata['type'][0])
        self.type.show()
        self.title_type.show()

    def make_plots(self):
        """
        Make all plots.
        """
        def under_show(text):
            self.under_list.addItem(text)
            self.title_under.show()
            self.under_list.show()
            self.title_plots.show()

        def above_show(text):
            self.above_list.addItem(text)
            self.title_above.show()
            self.above_list.show()
            self.title_plots.show()

        plt.close("all")
        # Clean figure lists
        self.above_list.clear()
        self.under_list.clear()
        # Create all plots
        self.fig_dict = self.ob.plt_all()
        # Show the plot list
        plot_keys = self.fig_dict.keys()
        if 'Salinity' in plot_keys:
            under_show('Salinity')
        if 'Temperature' in plot_keys:
            under_show('Temperature')
        if 'Sound velocity' in plot_keys:
            under_show('Sound velocity')
        if 'Pressure' in plot_keys:
            under_show('Pressure')
        if 'Conductivity' in plot_keys:
            under_show('Conductivity')
        if 'Atmospheric pressure' in plot_keys:
            above_show('Atmospheric pressure')
        if 'Wind speed' in plot_keys:
            above_show('Wind speed')
        if 'Wind direction' in plot_keys:
            above_show('Wind direction')
        if 'Air temperature' in plot_keys:
            above_show('Air temperature')
        if 'Wave height' in plot_keys:
            under_show('Wave height')
        if 'Wave direction' in plot_keys:
            under_show('Wave direction')
        if 'Wave period' in plot_keys:
            under_show('Wave period')
        if 'Pressure sea level' in plot_keys:
            above_show('Pressure sea level')
        if 'Sea level' in plot_keys:
            under_show('Sea level')
        if 'Rain acumulation' in plot_keys:
            above_show('Rain acumulation')
        if 'Relative humidity' in plot_keys:
            above_show('Relative humidity')
        if 'Gust wind speed' in plot_keys:
            above_show('Gust wind speed')
        if 'Current speed' in plot_keys:
            under_show('Current speed')
        if 'Current direction' in plot_keys:
            under_show('Current direction')

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

    def report_save_as(self):
        filename = QtGui.QFileDialog.getSaveFileName(None, "Save file", "", ".docx")
        if len(filename) > 0:
            self.report_path = filename
            try:
                self.em.summary_report(self.report_path)
            except:
                print("Error")

    def report_save(self):
        if self.report_path == "":
            filename = QtGui.QFileDialog.getSaveFileName(None, "Save file", "", ".docx")
            if len(filename) > 0:
                self.report_path = filename
        if self.report_path != "":
            try:
                self.em.summary_report(self.report_path)
            except:
                print("Error")

        try:
            self.em.summary_report(self.report_path)
        except:
            print("Error")

    def hide_slicing(self):
        """
        Hide the slicing option
        """
        self.slicing_start_label.hide()
        self.slicing_stop_label.hide()
        self.slicing_start_time.hide()
        self.slicing_end_time.hide()
        self.slicing_accept_button.hide()
        self.slicing_cancel_button.hide()

    def show_slicing(self):
        """
        Show slicing options.
        """
        self.slicing_start_label.show()
        self.slicing_stop_label.show()
        self.slicing_start_time.show()
        self.slicing_end_time.show()
        self.slicing_accept_button.show()
        self.slicing_cancel_button.show()

    def accept_slicing(self):
        """
        Data slicing process
        """
        def formating_time(time):
            """
            Formating data
            Our time has a format like this: 01/01/2000 0:00:00
            We need something like this: 20000101000000
            :param time: time that you want to be formatted
            :type time:str
            :return: formated time
            """
            if time[12] == ':':
                time = time[6:10]+time[3:5]+time[0:2]+'0'+time[11]+time[13:15]+time[16:]
            else:
                time = time[6:10]+time[3:5]+time[0:2]+time[10:12]+time[13:15]+time[16:]
            return time

        start_time = self.slicing_start_time.text()
        start_time = formating_time(start_time)
        stop_time = self.slicing_end_time.text()
        stop_time = formating_time(stop_time)
        self.ob.slicing(start_time, stop_time)
        self.make_plots()
        self.remove_fig()
        self.hide_slicing()


def open_gui():
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    open_gui()
