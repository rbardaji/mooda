import datetime
from PyQt5.QtWidgets import (QFrame, QPushButton, QListWidget,
                             QAbstractItemView, QLabel, QDateEdit, QSpinBox,
                             QWidget, QVBoxLayout, QHBoxLayout, QInputDialog,
                             QLineEdit)
from PyQt5.QtCore import pyqtSignal, QThread, QTime, QDateTime, QDate
from mooda import WaterFrame
from mooda.access import EGIM


class EgimDownloaderFrame(QFrame):
    """Frame to download data from EMSODEV servers"""

    # Signals
    msg2Statusbar = pyqtSignal(str)
    wf2plotSplitter = pyqtSignal(WaterFrame)

    class DownloadParameterThread(QThread):
        """
        The process to download data from the API is very slow.
        We are going to use this thread to download data without block the app.
        """
        def __init__(self, downloader):
            QThread.__init__(self)

            self.downloader = downloader

        def __del__(self):
            self.wait()

        def run(self):
            if self.downloader.instrumentList.currentItem().text() \
               == "icListen-1636":
                date = datetime.datetime.strptime(
                    self.downloader.dateList.currentItem().text(),
                    "%Y-%m-%d").strftime("%d/%m/%Y")
                self.downloader.downloadAcoustic(
                    date, self.downloader.hourMinuteList.currentItem().text())
            else:
                parameters = [item.text() for item in
                              self.downloader.parameterList.selectedItems()]
                for parameter in parameters:
                    self.downloader.downloadParameter(parameter)

    def __init__(self):
        super().__init__()

        # Instance variables
        self.downloader = EGIM()
        self.wf = WaterFrame()
        self.metadata = dict()
        self.dates = []
        self.myThread = None
        # Save the login of the EMSODEV API
        self.downloader.login = "emsodev"
        self.downloader.password = ""

        self.initUI()

    def initUI(self):

        # Buttons
        downloadButton = QPushButton("Download", self)
        downloadButton.clicked.connect(self.downloadClick)
        downloadButton.setEnabled(False)
        closeButton = QPushButton("Close", self)
        closeButton.clicked.connect(self.hide)

        # Lists
        self.egimList = QListWidget(self)
        self.egimList.itemClicked.connect(self.loadInstruments)
        self.egimList.setMaximumWidth(200)

        self.instrumentList = QListWidget(self)
        self.instrumentList.itemClicked.connect(self.loadParameters)
        self.instrumentList.setMaximumWidth(290)

        self.metadataList = QListWidget(self)

        self.parameterList = QListWidget(self)
        self.parameterList.setSelectionMode(
            QAbstractItemView.ExtendedSelection)
        self.parameterList.itemClicked.connect(
            lambda: downloadButton.setEnabled(True))

        self.dateList = QListWidget(self)
        self.dateList.itemClicked.connect(self.loadTimes)
        self.dateList.setMaximumWidth(150)
        self.hourMinuteList = QListWidget(self)
        self.hourMinuteList.itemClicked.connect(
            lambda: downloadButton.setEnabled(True))
        self.hourMinuteList.setMaximumWidth(150)

        # Labels
        egimLabel = QLabel("EGIM", self)
        instrumentLabel = QLabel("Instrument", self)
        metadataLabel = QLabel("Metadata", self)
        parameterLabel = QLabel("Parameter", self)
        startDateLabel = QLabel("Start date", self)
        endDateLabel = QLabel("End date", self)
        limitLabel = QLabel("Get last X values", self)
        hourLabel = QLabel("Hour and minute (HHMM)", self)
        dateLabel = QLabel("Available dates", self)

        # Date edit
        self.startDateEdit = QDateEdit(self)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setDateTime(QDateTime(QDate(2017, 1, 27),
                                                 QTime(0, 0, 0)))
        self.startDateEdit.setMinimumDateTime(QDateTime(QDate(2017, 1, 27),
                                                        QTime(0, 0, 0)))
        self.endDateEdit = QDateEdit(self)
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.setDateTime(QDateTime(QDate(2017, 1, 27),
                                               QTime(0, 0, 0)))
        self.endDateEdit.setMinimumDateTime(QDateTime(QDate(2017, 1, 27),
                                                      QTime(0, 0, 0)))

        # Spin box
        self.limitSpinBox = QSpinBox(self)
        self.limitSpinBox.setMinimum(0)
        self.limitSpinBox.setMaximum(9999999999)
        self.limitSpinBox.setSingleStep(100)
        self.limitSpinBox.valueChanged.connect(self.enableDate)

        # Custom Widgets

        # Widget for dates of the acoustic data
        self.acousticDateWidget = QWidget(self)
        # - Layout
        vAcousticDate = QVBoxLayout()
        vAcousticDate.addWidget(dateLabel)
        vAcousticDate.addWidget(self.dateList)
        vAcousticDate.addWidget(hourLabel)
        vAcousticDate.addWidget(self.hourMinuteList)
        self.acousticDateWidget.setLayout(vAcousticDate)
        self.acousticDateWidget.setMaximumWidth(175)
        self.acousticDateWidget.setEnabled(False)

        # Widget for dates of parameters
        self.parameterDateWidget = QWidget(self)
        # - Layout
        vparameterDate = QVBoxLayout()
        vparameterDate.addWidget(startDateLabel)
        vparameterDate.addWidget(self.startDateEdit)
        vparameterDate.addWidget(endDateLabel)
        vparameterDate.addWidget(self.endDateEdit)
        vparameterDate.addWidget(limitLabel)
        vparameterDate.addWidget(self.limitSpinBox)
        vparameterDate.addStretch()
        self.parameterDateWidget.setLayout(vparameterDate)
        self.parameterDateWidget.setEnabled(False)

        # Layout
        # - Vertical layout for EGIM --
        vEgim = QVBoxLayout()
        vEgim.addWidget(egimLabel)
        vEgim.addWidget(self.egimList)
        # -- Vertical layout for instruments -
        vInstrument = QVBoxLayout()
        vInstrument.addWidget(instrumentLabel)
        vInstrument.addWidget(self.instrumentList)
        # - Vertical layout for parameters -
        vParameter = QVBoxLayout()
        vParameter.addWidget(metadataLabel)
        vParameter.addWidget(self.metadataList)
        vParameter.addWidget(parameterLabel)
        vParameter.addWidget(self.parameterList)
        # - Vertical layout for dates and buttons
        vButton = QVBoxLayout()
        vButton.addWidget(downloadButton)
        vButton.addWidget(closeButton)
        vButton.addStretch()
        # - Layout of the frame -
        hFrame = QHBoxLayout()
        hFrame.addLayout(vEgim)
        hFrame.addLayout(vInstrument)
        hFrame.addLayout(vParameter)
        hFrame.addWidget(self.parameterDateWidget)
        hFrame.addWidget(self.acousticDateWidget)
        hFrame.addLayout(vButton)

        self.setLayout(hFrame)

    def loadObservatories(self):
        """
        It asks for the available EGIM observatories and write its names into
        self.egimList
        """

        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading observatories")
        # Clear self.egimList
        self.egimList.clear()
        # Ask for the observatories
        code, observatoryList = self.downloader.observatories()
        if code:
            if code == 200:
                # It means that you are going good
                self.egimList.addItems(observatoryList)
                # Send a message for the statusbar
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def loadInstruments(self, observatory):
        """
        It asks for the available instruments and write its names into
        self.instrumentList

        Parameters
        ----------
            observatory: item
                item from self.observatoryList
        """
        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading instruments")
        # Clear self.instrumentList
        self.instrumentList.clear()
        # Ask for instruments
        code, instrumentList_ = self.downloader.instruments(observatory.text())
        if code:
            if code == 200:
                # It means that you are going good
                # Obtain all sensor names of instrumentList_
                sensorType = [
                    instrument['name'] for instrument in instrumentList_]
                self.instrumentList.addItems(sensorType)
                # Add tooltip
                for i in range(self.instrumentList.count()):
                    self.instrumentList.item(i).setToolTip(
                        '<p><b>Sensor Type</b><br>' +
                        '{}</p><p>'.format(instrumentList_[i]['sensorType']) +
                        '<b>Long Name</b><br>' +
                        '{}</p>'.format(instrumentList_[i]['sensorLongName']) +
                        '<p></p><p><b>S/N</b><br>' +
                        '{}</p>'.format(instrumentList_[i]['sn']))
                # Send a message for the statusbar
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def loadParameters(self, instrument):
        """
        It asks for the available parameters and metadata and write them into
        self.parameterList and self.metadataList
        """
        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading parameters")
        # Clear self.parameterList and self.metadataList
        self.parameterList.clear()
        self.metadataList.clear()
        self.parameterDateWidget.setEnabled(False)
        self.acousticDateWidget.setEnabled(False)

        # If instrument is an icListener, check times
        if instrument.text() == "icListen-1636":
            self.acousticDateWidget.setEnabled(True)
            # Ask for dates
            code, self.dates = self.downloader.acoustic_date(
                self.egimList.currentItem().text(), instrument.text())
            if code == 200:
                dateList = [
                    date['acousticObservationDate'] for date in self.dates]
                self.dateList.addItems(dateList)

            else:
                self.msg2Statusbar.emit(
                    "Impossible to connect to the EMSODEV DMP API")
                return
            return

        self.parameterDateWidget.setEnabled(True)

        # Ask for metadata
        code, self.metadata = self.downloader.metadata(
            self.egimList.currentItem().text(), instrument.text())
        if code == 200:
            items = []
            for key, value in self.metadata.items():
                items.append("{}: {}".format(key, value))
            self.metadataList.addItems(items)
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")
            return

        # Ask for parameters
        code, parameterList_ = self.downloader.parameters(
            self.egimList.currentItem().text(), instrument.text())
        if code:
            if code == 200:
                # It means that you are going good
                # Obtain all parameter names of parameterList_
                names = [parameter['name'] for parameter in parameterList_]
                self.parameterList.addItems(names)
                self.parameterList.sortItems()
                # Add tooltip
                for i in range(self.parameterList.count()):
                    self.parameterList.item(i).setToolTip(
                        '<b>Units:</b> {}'.format(parameterList_[i]['uom']))
                # Send a message for the statusbar
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def loadTimes(self, date_item):
        """
        Write items into self.hourMinuteList QListWidget
        """
        for date in self.dates:
            if date['acousticObservationDate'] == date_item.text():
                timeList = []
                for time in date['observationsHourMinuteList']:
                    timeList.append(time['acousticObservationHourMinute'])
                self.hourMinuteList.addItems(timeList)

    def reload(self):
        """It clear all lists and load again the observatories."""
        # Check the password of the API
        if self.downloader.password is None:
            self.msg2Statusbar.emit(
                "Password is required to download data from EMSODEV")
            text, ok = QInputDialog.getText(self, "Attention", "Password",
                                            QLineEdit.Password)
            if ok:
                self.downloader.password = text
            else:
                return
        self.loadObservatories()

    def downloadClick(self):
        """Function when user click download"""

        self.myThread = self.DownloadParameterThread(self)
        self.myThread.start()

    def downloadParameter(self, parameter):
        """It download data with the observation function of EGIM"""

        # Send a message for the statusbar
        self.msg2Statusbar.emit("Downloading {}".format(parameter))

        code, df = self.downloader.observation(
            observatory=self.egimList.currentItem().text(),
            instrument=self.instrumentList.currentItem().text(),
            parameter=parameter,
            startDate=self.startDateEdit.text(),
            endDate=self.endDateEdit.text(),
            limit=self.limitSpinBox.text())
        if code:
            if code == 200:
                self.msg2Statusbar.emit("Waterframe creation")
                # It means that you are going good
                wf = self.downloader.to_waterframe(data=df,
                                                   metadata=self.metadata)
                # print(wf.data.head())
                # Send a signal with the new WaterFrame
                self.wf2plotSplitter.emit(wf)
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def downloadAcoustic(self, date, time):
        # Send a message for the statusbar
        self.msg2Statusbar.emit(
            "Downloading acoustic file from {}, {}".format(date, time))

        code, df, metadata = self.downloader.acoustic_observation(
            observatory=self.egimList.currentItem().text(),
            instrument=self.instrumentList.currentItem().text(),
            date=date,
            hour_minute=time)
        if code:
            if code == 200:
                self.msg2Statusbar.emit("Waterframe creation")
                # It means that you are going good
                wf = self.downloader.to_waterframe(data=df, metadata=metadata)
                # Send a signal with the new WaterFrame
                self.wf2plotSplitter.emit(wf)
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def enableDate(self):
        """Enable or disable date elements"""
        if int(self.limitSpinBox.text()) > 0:
            self.startDateEdit.setEnabled(False)
            self.endDateEdit.setEnabled(False)
        else:
            self.startDateEdit.setEnabled(True)
            self.endDateEdit.setEnabled(True)
