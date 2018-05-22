import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
import seaborn as sms


class QCPlotWidget(QWidget):
    """Pyqt5 widget to show plots. It is used in PlotSplitter."""

    def __init__(self, wf, key):
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param key: key of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf
        self.key = key
        # Name of this object
        self.name = "new"

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        # The name will be the key
        self.name = key
        if "_QC" in key:
            self.wf.qcplot(key[:-3], ax=self.axes)
        else:
            return
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
        refreshAct = QAction(QIcon('oceanobs//app//mooda//icon//refresh.png'),
                             'Refresh', self)
        refreshAct.triggered.connect(self.refreshPlot)
        closeAct = QAction(QIcon('oceanobs//app//mooda//icon//close.png'),
                           'Close', self)
        closeAct.triggered.connect(self.hide)
        # - Format -
        actionToolbar.addAction(refreshAct)
        actionToolbar.addSeparator()
        actionToolbar.addAction(closeAct)

        # Layout
        # - For the Widget
        vPlot = QVBoxLayout()
        vPlot.addWidget(self.plotCanvas)
        vPlot.addWidget(plotToolbar)
        vPlot.addWidget(actionToolbar)
        self.setLayout(vPlot)

    def refreshPlot(self):
        """
        It refresh the plot according to the actions of the actionToolbar
        :return:
        """
        # Remove previous axes from the figure
        self.axes.clear()
        # Remake the plot
        self.wf.qcplot(self.key[:-3], ax=self.axes)

        plt.tight_layout()
        self.plotCanvas.draw()
