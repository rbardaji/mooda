import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QVBoxLayout, QAction
from PyQt5.QtGui import QIcon
import seaborn as sms


class QCBarPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    def __init__(self, wf):
        """
        :param wf: inWater WaterFrame object
        """
        super().__init__()

        # Instance variables
        self.wf = wf
        self.name = "QC"
        self.key = "all"

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.wf.qcbarplot(key=self.key, ax=self.axes)
        # Plot custom view
        plt.tight_layout()
        sms.despine()

        self.initUI()

    def initUI(self):
        path_icon = str(
            os.path.dirname(os.path.abspath(__file__))) + \
                    "\\..\\icon\\"
        # Canvas
        self.plotCanvas = FigureCanvas(self.fig)
        self.plotCanvas.draw()

        # Matplotlib toolbar
        plotToolbar = NavigationToolbar(self.plotCanvas, self)

        # Custom Toolbar
        actionToolbar = QToolBar(self)
        # - Actions -
        applyAct = QAction(QIcon(path_icon+"refresh.png"),
                           'Refresh', self)
        applyAct.triggered.connect(self.refreshPlot)
        closeAct = QAction(QIcon(path_icon+"close.png"),
                           'Close', self)
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

    def refreshPlot(self):
        """
        It refresh the plot according to the actions of the actionToolbar
        :return:
        """
        # Remove previous axes from the figure
        self.axes.clear()
        self.wf.qcbarplot(key="all", ax=self.axes)
        plt.tight_layout()
        self.plotCanvas.draw()
