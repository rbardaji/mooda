import os
from numpy import timedelta64
import seaborn as sms
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QComboBox, QLabel, QSpinBox, QToolBar,
                             QVBoxLayout, QWidget)


class HistoPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    # Signals
    msg2Statusbar = pyqtSignal(str)

    def __init__(self, wf, keys):
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param keys: keys of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf
        self.key = keys
        # Name of this object
        self.name = "_".join(keys)
        self.name = "hist_"+self.name

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.axes = self.wf.hist(self.key, mean_line=True, ax=self.axes)
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
        closeAct = QAction(QIcon(path_icon+"close.png"),
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

    def refreshPlot(self):
        """
        It refresh the plot according to the actions of the actionToolbar
        :return:
        """

        self.msg2Statusbar.emit("Making figure")

        # Remove previous axes from the figure
        self.axes.cla()

        # Rol value
        rol = self.rolling.value()
        if rol == 0:
            rol = None

        # Average value
        average = None
        if self.average.currentText() == 'Minutely':
            average = "T"
        elif self.average.currentText() == 'Hourly':
            average = "H"
        elif self.average.currentText() == 'Daily':
            average = "D"
        elif self.average.currentText() == 'Weekly':
            average = "W"

        if len(self.key) > 1:
            for key in self.key:
                second_y = False
                if key == self.right:
                    second_y = True
                self.axes = self.wf.tsplot(keys=key, ax=self.axes,
                                           secondary_y=second_y,
                                           average_time=average,
                                           rolling=rol)
        else:
            key = self.key[0]
            if "_QC" in key:
                self.axes = self.wf.qcplot(key[:-3], ax=self.axes)
            else:
                self.axes = self.wf.tsplot(keys=key, rolling=rol, ax=self.axes,
                                           average_time=average,
                                           secondary_y=False)
        # Plot custom view
        plt.tight_layout()
        if self.right is None:
            sms.despine()

        self.plotCanvas.draw()

        self.msg2Statusbar.emit("Ready")

        print("Done")
