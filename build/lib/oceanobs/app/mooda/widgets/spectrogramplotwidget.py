import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
import seaborn as sms


class SpectrogramPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    def __init__(self, wf):
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param key: key of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf
        self.name = "Spectrogram"

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.wf.spectroplot()
        plt.colorbar()
        # Plot custom view
        plt.tight_layout()
        sms.despine()

        self.initUI()

    def initUI(self):

        # Canvas
        self.plotCanvas = FigureCanvas(self.fig)
        self.plotCanvas.draw()

        # Matplotlib toolbar
        plotToolbar = NavigationToolbar(self.plotCanvas, self)

        # Custom Toolbar
        actionToolbar = QToolBar(self)
        # - Actions -
        applyAct = QAction(QIcon('./icon/refresh.png'), 'Refresh', self)
        applyAct.triggered.connect(self.refreshPlot)
        closeAct = QAction(QIcon('./icon/close.png'), 'Close', self)
        closeAct.triggered.connect(self.hide)
        # - Format -
        actionToolbar.addAction(applyAct)
        actionToolbar.addAction(closeAct)

        # Layout
        # - For the Widget
        vPlot = QVBoxLayout()
        vPlot.addWidget(self.plotCanvas)
        vPlot.addWidget(plotToolbar)
        vPlot.addWidget(actionToolbar)
        self.setLayout(vPlot)

    def refreshPlot(self, wf_refresh=None):
        """
        It refresh the plot according to the actions of the actionToolbar

        Parameters
        ----------
            wf_refresh: None, Optional
                This argument is not used in the function but we need it
                to be compatible with the other plot widgets.
        :return:
        """
        # Remove previous axes from the figure
        self.axes.clear()
        self.wf.spectroplot()
        plt.tight_layout()
        self.plotCanvas.draw()
