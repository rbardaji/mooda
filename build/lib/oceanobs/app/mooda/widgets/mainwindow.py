import os
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QSplitter,
                             QFileDialog, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt
from oceanobs.app.mooda.widgets import (TextFrame, PlotSplitter,
                                        EgimDownloaderFrame)
from oceanobs import WaterFrame


class MOODA(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        path_icon = str(
            os.path.dirname(os.path.abspath(__file__))) + \
                    "\\..\\icon\\"
        # Status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        # Create text zone
        self.datalog = TextFrame()
        self.datalog.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # Plot Area
        self.plotArea = PlotSplitter()
        self.plotArea.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.plotArea.msg2TextArea[str].connect(self.datalog.write)

        # EGIM Downloader
        self.egimDownloader = EgimDownloaderFrame()
        self.egimDownloader.msg2Statusbar[str].connect(
            self.statusbar.showMessage)
        self.egimDownloader.wf2plotSplitter[WaterFrame].connect(
            self.openFile)

        # Menu bar
        menubar = self.menuBar()
        # - Menu File -
        fileMenu = menubar.addMenu('&File')
        # -- New project --
        newAct = QAction(QIcon(
            path_icon+'\\new.png'),
                         '&New project', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('Clear the actual data frame to start a new one')
        newAct.triggered.connect(self.plotArea.newWaterFrame)
        fileMenu.addAction(newAct)
        # -- Open --
        openAct = QAction(QIcon(
            path_icon+'\\open.svg'),
                          '&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open data files for analyzing')
        openAct.triggered.connect(self.openFile)
        fileMenu.addAction(openAct)
        # -- Add --
        addAct = QAction(QIcon(
            path_icon+'\\add.svg'),
                         '&Add', self)
        addAct.setStatusTip('Add data to the current dataset')
        addAct.triggered.connect(lambda: self.openFile(concat=True))
        fileMenu.addAction(addAct)
        # --- EGIM downloader ---
        downloaderAct = QAction(QIcon(
            path_icon+'\\cloud.png'),
                                '&EGIM downloader', self)
        downloaderAct.setStatusTip(
            'Open and analyze data from EMSODEV servers')
        downloaderAct.triggered.connect(self.openEgimDownloader)
        fileMenu.addAction(downloaderAct)
        # --- Separator ---
        fileMenu.addSeparator()
        # --- Save as ---
        self.saveAct = QAction(QIcon(
            path_icon+'\\save.png'),
                               '&Save as...', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save current data into a pickle')
        self.saveAct.triggered.connect(self.saveFile)
        fileMenu.addAction(self.saveAct)
        # --- Separator ---
        fileMenu.addSeparator()
        # -- Exit --
        exitAct = QAction(QIcon(
            path_icon+'\\exit.svg'),
                          'E&xit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAct)

        # - Menu Data -
        dataMenu = menubar.addMenu('&Data')
        # -- Submenu Quality control --
        qcMenu = QMenu('&QC', self)
        # --- Auto QC ---
        self.qcAutoAct = QAction(QIcon(
            path_icon+'\\qc.png'),
                                 '&Auto', self)
        self.qcAutoAct.triggered.connect(self.plotArea.qcWidget.apply)
        qcMenu.addAction(self.qcAutoAct)
        # --- Preferences QC ---
        self.qcPreferencesAct = QAction('&Preferences...', self)
        self.qcPreferencesAct.triggered.connect(self.plotArea.qcWidget.show)
        qcMenu.addAction(self.qcPreferencesAct)
        dataMenu.addMenu(qcMenu)
        # -- Delete parameters --
        self.deleteAct = QAction(QIcon(
            path_icon+'\\delete.png'),
                                 '&Remove parameters',
                                 self)
        self.deleteAct.triggered.connect(self.plotArea.dropWidget.show)
        dataMenu.addAction(self.deleteAct)
        # -- Rename parameters --
        self.renameAct = QAction(QIcon(
            path_icon+'\\rename.png'),
                                 'Re&name parameters',
                                 self)
        self.renameAct.triggered.connect(self.plotArea.renameWidget.show)
        dataMenu.addAction(self.renameAct)
        # -- Resample data --
        self.resampleAct = QAction(QIcon(
            path_icon+'\\resample.png'),
                                   'Resam&ple data',
                                   self)
        self.resampleAct.triggered.connect(self.plotArea.resampleWidget.show)
        dataMenu.addAction(self.resampleAct)
        # -- Slice data --
        self.sliceAct = QAction(QIcon(
            path_icon+'\\slice.png'),
                                '&Slice data', self)
        self.sliceAct.triggered.connect(self.plotArea.sliceWidget.show)
        dataMenu.addAction(self.sliceAct)

        # - Menu View -
        viewMenu = menubar.addMenu('&View')
        # -- Datalog --
        datalogAct = QAction(QIcon(
            path_icon+'\\log.png'),
                             '&Datalog', self)
        datalogAct.setShortcut('F1')
        datalogAct.setStatusTip('Show the text area')
        datalogAct.triggered.connect(
            lambda: self.datalog.setVisible(not self.datalog.isVisible()))
        viewMenu.addAction(datalogAct)
        # -- Metadata --
        self.metadataAct = QAction(QIcon(
            path_icon+'\\metadata.png'),
                                   '&Metadata', self)
        self.metadataAct.setShortcut('F2')
        self.metadataAct.setStatusTip("Show metadata area")
        self.metadataAct.triggered.connect(
            lambda: self.plotArea.vMetadataWidget.setVisible(
                not self.plotArea.vMetadataWidget.isVisible()))
        viewMenu.addAction(self.metadataAct)
        # -- Data --
        self.dataViewAct = QAction(QIcon(
            path_icon+'\\graph.png'),
                                   '&Parameters', self)
        self.dataViewAct.setShortcut('F3')
        self.dataViewAct.setStatusTip("Show data area")
        self.dataViewAct.triggered.connect(
            lambda: self.plotArea.vDataSplitter.setVisible(
                not self.plotArea.vDataSplitter.isVisible()))
        viewMenu.addAction(self.dataViewAct)

        # Splitter
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.egimDownloader)
        splitter.addWidget(self.plotArea)
        splitter.addWidget(self.datalog)

        # Main Window
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('MOODA')
        self.setWindowIcon(QIcon(
            path_icon+'\\mooda.png'))
        self.setCentralWidget(splitter)
        self.show()

        # Initial configuration
        # - Hide components
        self.egimDownloader.hide()
        self.datalog.hide()
        self.plotArea.hide()
        # - Write date and time into 'text'
        datetime_ = QDateTime.currentDateTime()
        self.datalog.write(datetime_.toString(Qt.DefaultLocaleLongDate))
        # - Disable actions from menus
        self.deleteAct.setEnabled(False)
        self.saveAct.setEnabled(False)
        self.qcAutoAct.setEnabled(False)
        self.qcPreferencesAct.setEnabled(False)
        self.metadataAct.setEnabled(False)
        self.dataViewAct.setEnabled(False)
        self.renameAct.setEnabled(False)
        self.resampleAct.setEnabled(False)
        self.sliceAct.setEnabled(False)

    def openEgimDownloader(self):
        """It shows the EgimDownloaderFrame."""
        self.egimDownloader.show()
        if self.egimDownloader.egimList.count() == 0:
            # New frame
            self.egimDownloader.reload()

    def openFile(self, wf=None, concat=False):
        """
        It opens a QFileDialog and load the input file
        :param wf: WaterFrame object
        :param concat: It adds the new WaterFrame into the actual Dataframe
        """
        if wf:
            fileName = wf
        else:
            # Open the save file dialog
            fileName, _ = QFileDialog.getOpenFileName(
                caption="Open data file", directory="",
                filter="NETcdf (*.nc);;Pickle (*.pkl)")

        # Send the path to the PlotFrame to be opened
        if fileName:
            ok = self.plotArea.openData(fileName, concat)
            if ok:
                # Show plot area
                self.plotArea.show()
                # Enable actions
                self.deleteAct.setEnabled(True)
                self.saveAct.setEnabled(True)
                self.metadataAct.setEnabled(True)
                self.dataViewAct.setEnabled(True)
                self.qcPreferencesAct.setEnabled(True)
                self.qcAutoAct.setEnabled(True)
                self.renameAct.setEnabled(True)
                self.resampleAct.setEnabled(True)
                self.sliceAct.setEnabled(True)

    def saveFile(self):
        """
        It opens a QFileDialog and save current data
        """
        # Open the save file dialog
        fileName, _ = QFileDialog.getSaveFileName(
            caption="Open data file", directory="",
            filter="Pickle (*.pkl)")
        if fileName:
            self.plotArea.saveData(fileName)
