import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
import seaborn as sms


class ScatterMatrixPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    def __init__(self, wf, keys):
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param key: key of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.wf.scatter_matrix(keys=keys, ax=self.axes)
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
        closeAct = QAction(QIcon('oceanobs//app//mooda//icon//close.png'),
                           'Close', self)
        closeAct.triggered.connect(self.hide)
        # - Format -
        actionToolbar.addAction(closeAct)

        # Layout
        # - For the Widget
        vPlot = QVBoxLayout()
        vPlot.addWidget(self.plotCanvas)
        vPlot.addWidget(plotToolbar)
        vPlot.addWidget(actionToolbar)
        self.setLayout(vPlot)
