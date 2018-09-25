from PyQt5.QtWidgets import (QWidget, QLabel, QListWidget, QPushButton,
                             QVBoxLayout, QSplitter, QGroupBox, QRadioButton,
                             QAbstractItemView, QPlainTextEdit)
from PyQt5.QtCore import pyqtSignal, Qt
from mooda import WaterFrame
from mooda.app.mooda_gui.widgets import (DropWidget, QCWidget, RenameWidget,
                                         ResampleWidget, SliceWidget,
                                         ScatterMatrixPlotWidget, QCPlotWidget,
                                         TSPlotWidget, QCBarPlotWidget,
                                         SpectrogramPlotWidget)


class PlotSplitter(QSplitter):
    """Pyqt5 widget to show data in plots and lists."""

    # Signals
    msg2Statusbar = pyqtSignal(str)
    msg2TextArea = pyqtSignal(str)

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        # Instance variables
        self.wf = WaterFrame()
        # List of PlotWidget, to control them in any case
        self.plotWidgetList = []

        self.initUI()

    def initUI(self):
        """UI creator"""

        # Lists
        self.metadataList = QListWidget(self)
        self.dataList = QListWidget(self)
        self.dataList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.dataList.itemClicked.connect(self.dataListClick)
        self.graphList = QListWidget(self)
        self.graphList.itemClicked.connect(self.graphClick)

        # PlainTextEdit
        self.otherInfoPlainText = QPlainTextEdit(self)

        # Labels
        metadataLabel = QLabel("Metadata")
        dataLabel = QLabel("Data")
        graphLabel = QLabel("Graph")
        infoLabel = QLabel("Other information")

        # DropWidget
        self.dropWidget = DropWidget()
        self.dropWidget.list2drop[list, list, bool].connect(self.dropData)
        self.dropWidget.hide()

        # Group Box
        plotGroupBox = QGroupBox("Plot properties", self)
        vPlotGroupBox = QVBoxLayout()
        # - RadioButton
        self.autoPlotRadioButton = QRadioButton("Auto plot", self)
        self.autoPlotRadioButton.setChecked(True)
        self.multipleParameterRadioButton = QRadioButton("Click to plot", self)
        self.correlationRadioButton = QRadioButton("Correlation", self)
        self.parameterQCRadioButton = QRadioButton("QC of the parameter", self)
        vPlotGroupBox.addWidget(self.autoPlotRadioButton)
        vPlotGroupBox.addWidget(self.multipleParameterRadioButton)
        vPlotGroupBox.addWidget(self.correlationRadioButton)
        vPlotGroupBox.addWidget(self.parameterQCRadioButton)
        plotGroupBox.setLayout(vPlotGroupBox)

        # QCWidget
        self.qcWidget = QCWidget()
        self.qcWidget.list2qc[list].connect(self.applyQC)
        self.qcWidget.hide()

        # RenameWidget
        self.renameWidget = RenameWidget()
        self.renameWidget.key2change[str, str].connect(self.applyRename)
        self.renameWidget.hide()

        # ResampleWidget
        self.resampleWidget = ResampleWidget()
        self.resampleWidget.resampleRule[str].connect(self.applyResample)
        self.resampleWidget.hide()

        # SliceWidget
        self.sliceWidget = SliceWidget()
        self.sliceWidget.sliceTimes[str, str].connect(self.applySlice)
        self.sliceWidget.hide()

        # Splitters
        self.vDataSplitter = QSplitter(Qt.Vertical)
        # Custom Widget Metadata
        self.vMetadataWidget = QWidget()

        # Buttons
        # - For metadata area
        hideMetadataButton = QPushButton("Hide")
        hideMetadataButton.clicked.connect(self.vMetadataWidget.hide)
        # - For data Area
        plotButton = QPushButton("Plot")
        plotButton.clicked.connect(self.addPlot)
        hideDataButton = QPushButton("Hide")
        hideDataButton.clicked.connect(self.vDataSplitter.hide)

        # Custom Widget Data
        # - Data Widget
        parameterWidget = QWidget()
        # -- Layout
        vData = QVBoxLayout()
        vData.addWidget(dataLabel)
        vData.addWidget(self.dataList)
        vData.addWidget(plotGroupBox)
        vData.addWidget(plotButton)
        parameterWidget.setLayout(vData)
        # - Graph Widget
        graphWidget = QWidget()
        # -- Layout
        vGraph = QVBoxLayout()
        vGraph.addWidget(graphLabel)
        vGraph.addWidget(self.graphList)
        vGraph.addWidget(hideDataButton)
        graphWidget.setLayout(vGraph)
        # - Data splitter
        self.vDataSplitter.addWidget(parameterWidget)
        self.vDataSplitter.addWidget(graphWidget)

        # Layouts
        # - Metadata -
        vMetadata = QVBoxLayout()
        vMetadata.addWidget(metadataLabel)
        vMetadata.addWidget(self.metadataList)
        vMetadata.addWidget(infoLabel)
        vMetadata.addWidget(self.otherInfoPlainText)
        vMetadata.addWidget(hideMetadataButton)
        self.vMetadataWidget.setLayout(vMetadata)

        # Splitter (self)
        # - Layout for actions
        vActionsWidget = QWidget()
        vActions = QVBoxLayout()
        vActions.addWidget(self.renameWidget)
        vActions.addWidget(self.resampleWidget)
        vActions.addWidget(self.dropWidget)
        vActions.addWidget(self.sliceWidget)
        vActions.addStretch()
        vActionsWidget.setLayout(vActions)
        # - Add to self (splitter)
        self.addWidget(self.qcWidget)
        self.addWidget(vActionsWidget)
        self.addWidget(self.vMetadataWidget)
        self.addWidget(self.vDataSplitter)

    def dataListClick(self):
        if self.autoPlotRadioButton.isChecked():
            self.addPlot()

    def addPlot(self):
        """It creates a FigureCanvas with the input figure"""

        self.msg2Statusbar.emit("Making the figure")

        # Create key list
        keys = [item.text() for item in self.dataList.selectedItems()]

        # If nothing is selected, go out
        if not keys:
            self.msg2Statusbar.emit("Ready")
            return

        # Check if it is a QC plot
        if self.parameterQCRadioButton.isChecked():
            keys = [keys[0] + "_QC"]

        # Check if it is a correlation
        if self.correlationRadioButton.isChecked():
            plotWidget = ScatterMatrixPlotWidget(wf=self.wf, keys=keys)
            self.addWidget(plotWidget)
            return

        # Create name of the plot
        name = '_'.join(keys)

        # Check if plot is done
        new = True
        for plotWidget in self.plotWidgetList:
            if plotWidget.name == name:
                if ~plotWidget.isVisible():
                    plotWidget.refreshPlot()
                    plotWidget.show()
                new = False
                break

        # Create the plot if is new
        if new:
            if len(keys) == 1 and "_QC" in keys[0]:
                plotWidget = QCPlotWidget(wf=self.wf, key=keys[0])
            else:
                plotWidget = TSPlotWidget(wf=self.wf, keys=keys)
                plotWidget.msg2Statusbar[str].connect(self.msg2Statusbar.emit)
            self.addWidget(plotWidget)
            # Add the widget to the list
            self.plotWidgetList.append(plotWidget)

        self.msg2Statusbar.emit("Ready")

    def addQCBarPlot(self):
        """
        It creates a FigureCanvas with the input figure (QC)
        """
        self.msg2Statusbar.emit("Making the figure")
        # Check if the plot exists
        plotWidget = None
        for plotWidget_ in self.plotWidgetList:
            if plotWidget_.name == "QC":
                plotWidget = plotWidget_
                plotWidget.wf = self.wf
                plotWidget.refreshPlot()
                plotWidget.show()
                break
        if plotWidget is None:

            plotWidget = QCBarPlotWidget(wf=self.wf)
            self.addWidget(plotWidget)
            # Add the widget to the list
            self.plotWidgetList.append(plotWidget)
        self.msg2Statusbar.emit("Ready")

    def addSpectroPlot(self):
        """It ads the SpectroPlotWidget to the screen"""

        self.msg2Statusbar.emit("Making the figure")
        # Check if the plot exists
        plotWidget = None
        for plotWidget_ in self.plotWidgetList:
            if plotWidget_.name == "Spectrogram":
                plotWidget = plotWidget_
                plotWidget.wf = self.wf
                plotWidget.refreshPlot()
                plotWidget.show()
                break
        if plotWidget is None:
            plotWidget = SpectrogramPlotWidget(wf=self.wf)
            self.addWidget(plotWidget)
            # Add the widget to the list
            self.plotWidgetList.append(plotWidget)
        self.msg2Statusbar.emit("Ready")

    def openData(self, path, concat=False):
        """
        It opens the netcdf of the path.

        Parameters
        ----------
            path: str or WaterFrame
                Path where the file is or WaterFrame object.
            concat: bool, optional (concat = False)
                It adds the new dataframe to the current dataframe.

        Returns
        -------
            True/False: bool
                It indicates if the operation is ok.
        """
        self.msg2Statusbar.emit("Opening data")
        if isinstance(path, str):
            # Obtain type of file
            extension = path.split(".")[-1]
            # Init ok
            ok = False
            wf_new = WaterFrame()
            if extension == "nc":
                ok = wf_new.from_netcdf(path)
            elif extension == "pkl":
                ok = wf_new.from_pickle(path)
            if ok:
                # Check if we want actual data
                if not concat:
                    self.newWaterFrame()
                self.wf.concat(wf_new)

                self.msg2TextArea.emit("Working with file {}".format(path))
                # Add metadata information into metadataList
                self.addMetadata(self.wf.metadata)
                # Add other information
                self.otherInfoPlainText.setPlainText(repr(self.wf))
                # Add data information into dataList
                self.addData(self.wf.data)
                # Plot QC
                self.addQCBarPlot()
                self.msg2Statusbar.emit("Ready")
                return True
            else:
                self.msg2Statusbar.emit("Error opening data")
                return False
        else:
            # Path is a WaterFrame

            # Check if there is no data in the waterframe
            if path.data.empty:
                return False

            # Check if it is a dataframe of an acoustic data.
            # In this case, we are going to delete the previous dataframe.
            if "Sequence" in self.wf.data.keys():
                self.wf.clear()
            self.wf.concat(path)

            # Add data information into dataList
            self.addData(self.wf.data)
            self.addMetadata(self.wf.metadata)
            # Plot QC
            self.addQCBarPlot()
            return True

    def addMetadata(self, metadataDict):
        """
        Add Metadata information into self.metadataList
        :param metadataDict: WaterFrame Metadata Dictionary
        """
        # Clear the list
        self.metadataList.clear()

        items = []
        msg = "\nMetadata:"
        for key, value in metadataDict.items():
            items.append("{}: {}".format(key, value))
            msg += "\n- {}: {}".format(key, value)
        self.metadataList.addItems(items)
        # Send a message to the text area
        self.msg2TextArea.emit(msg)

    def addData(self, data):
        """
        Add data names into self.dataList
        :param data: WaterFrame data variable
        """

        def is_acoustic_data(a):
            # will be True also for 'NaN'
            if a == "Sequence":
                return True
            elif a == "Data Points":
                return True
            try:
                float(a)
                return True
            except ValueError:
                return False

        # Clear the list
        self.dataList.clear()
        # Parameter keys (without QC)
        # NO DEPTH in nc files, NO TIME
        keys_to_work = [key for key in data.keys() if 'TIME' not in key
                        if not is_acoustic_data(key)
                        if key + "_QC" in data.keys()]
        self.dataList.addItems(keys_to_work)
        # Add graphs
        self.graphList.clear()
        self.graphList.addItem("QC")
        # Check if we have acoustic data
        for key in data.keys():
            if is_acoustic_data(key):
                self.graphList.addItem("Spectrogram")
                break

        # Add tooltip
        msg = "\nData:"
        for i in range(self.dataList.count()):
            if "_QC" in self.dataList.item(i).text():
                self.dataList.item(i).setToolTip(
                    'QC flags of {}'.format(self.dataList.item(i).text()[:-3]))
            else:
                try:
                    self.dataList.item(i).setToolTip('{} ({})'.format(
                        self.wf.meaning[
                            self.dataList.item(i).text()]['long_name'],
                        self.wf.meaning[
                            self.dataList.item(i).text()]['units']))
                    msg += "\n- {}: {} ({})".format(
                        self.dataList.item(i).text(),
                        self.wf.meaning[
                            self.dataList.item(i).text()]['long_name'],
                        self.wf.meaning[
                            self.dataList.item(i).text()]['units'])
                except KeyError:
                    pass
        # Send a message to the text area
        self.msg2TextArea.emit(msg)
        # Send the labels to the dropWidget
        self.dropWidget.addLabels(keys_to_work)
        self.qcWidget.addLabels(keys_to_work)
        self.renameWidget.addLabels(keys_to_work)
        self.sliceWidget.refresh(self.wf.data.index[0], self.wf.data.index[-1])

    def saveData(self, path):
        """
        Save current data into a pickle file
        :param path: File path
        :return: Bool
        """
        self.msg2Statusbar.emit("Saving data")
        ok = self.wf.to_pickle(path)
        if ok:
            self.msg2TextArea.emit("Data saved on file {}".format(path))
            self.msg2Statusbar.emit("Ready")
        return ok

    def dropData(self, labels, flagList, dropNaN):
        """
        Delete some parameters from self.wf and refresh the lists
        :param labels: list of labels to drop
        :param flagList: list of flags to drop
        :return:
        """
        self.msg2TextArea.emit("Deleting data")

        # This is a trick, delete the list if is a list of None
        if flagList[0] is None:
            flagList = None

        if flagList:
            self.wf.use_only(parameters=labels, flags=[0, 1], dropnan=dropNaN)
        else:
            # Delete the parameters
            self.wf.drop(keys=labels, flags=flagList)
        # Refresh the lists
        self.addData(self.wf.data)

        # Delete plots with the key
        for label in labels:
            for plotWidget in self.plotWidgetList:
                if plotWidget.name == "QC":
                    plotWidget.refreshPlot()
                if label == plotWidget.name or label+"_" in \
                   plotWidget.name or "_"+label in plotWidget.name:
                    plotWidget.deleteLater()
                    self.plotWidgetList.remove(plotWidget)

        # Send message
        msg = ""
        if flagList is None:
            for label in labels:
                if '_QC' in label:
                    continue
                msg += "{} ".format(label)
            msg += "deleted"
        else:
            msg += "Data with QC Flags "
            for flag in flagList:
                msg += "{}, ".format(flag)
            msg += "from "
            for label in labels:
                if '_QC' in label:
                    continue
                msg += "{}, ".format(label)
            msg += "deleted"
        self.msg2TextArea.emit("\n{}".format(msg))
        self.msg2Statusbar.emit(msg)

    def applyQC(self, listQC):
        """
        Apply the QC procedures
        :param listQC:
        :return:
        """

        def doIt(key_in):
            """
            Common part, to not repeat code
            :param key_in: key to apply QC tests
            """
            if '_QC' in key_in:
                return
            if listQC[0]:
                #  Reset flags
                self.msg2Statusbar.emit(
                    "Setting flags from {} to {}".format(key_in, listQC[0]))
                self.wf.reset_flag(key=key_in, flag=int(listQC[0]))
                self.msg2Statusbar.emit("Ready")
            if listQC[3]:
                # Spike test
                threshold = float(listQC[4].replace(',', '.'))
                self.msg2Statusbar.emit(
                    "Applying spike test to "
                    "{}, with rolling window {} and threshold {}".format(
                        key_in, listQC[5], threshold))
                self.wf.spike_test(key=key_in, window=int(listQC[5]),
                                   threshold=threshold, flag=int(listQC[3]))
                self.msg2Statusbar.emit("Ready")
            if listQC[1]:
                # Range test
                self.msg2Statusbar.emit(
                    "Applying range test to {}".format(key_in))
                self.wf.range_test(key=key_in, flag=int(listQC[1]))
                self.msg2Statusbar.emit("Ready")
            if listQC[2]:
                # Flat test
                self.msg2Statusbar.emit(
                    "Applying flat test to"
                    " {}, with rolling window {}".format(key_in, listQC[5]))
                self.wf.flat_test(key=key_in, window=int(listQC[5]),
                                  flag=int(listQC[2]))
                self.msg2Statusbar.emit("Ready")
            if listQC[6]:
                # Flag to flag
                self.msg2Statusbar.emit(
                    "Changing flags of "
                    "{} from {} to {}".format(key_in, listQC[6], listQC[7]))
                self.wf.flag2flag(key=key_in, original_flag=int(listQC[6]),
                                  translated_flag=int(listQC[7]))
                self.msg2Statusbar.emit("Ready")

        self.msg2Statusbar.emit("Creating QC flags")

        if listQC[8] == 'all':
            for key in self.wf.parameters():
                doIt(key_in=key)
        else:
            for i in range(8, len(listQC)):
                key = listQC[i]
                doIt(key_in=key)

        self.msg2Statusbar.emit("Updating graphs")
        # Refresh the QC graph
        for plotWidget in self.plotWidgetList:
            if "QC" in plotWidget.name:

                if plotWidget.isVisible():
                    plotWidget.refreshPlot()
                # Show the QCBarPlot
                elif plotWidget.name == "QC":
                    plotWidget.refreshPlot()
                    plotWidget.show()
        self.msg2Statusbar.emit("Ready")

    def applyRename(self, original_key, new_key):
        """It renames keys from a WaterFrame"""
        # Rename key from the Waterframe
        self.msg2Statusbar.emit(
            "Changing name {} to {}".format(original_key, new_key))
        self.wf.rename(original_key, new_key)
        # Rename the key of the plotWidgets if it process
        for plotWidget in self.plotWidgetList:
            if isinstance(plotWidget.key, list):
                for i, key in enumerate(plotWidget.key):
                    if key == original_key:
                        plotWidget.key[i] = new_key
                        plotWidget.name = plotWidget.name.replace(original_key,
                                                                  new_key)
                        plotWidget.refreshPlot()
            else:
                if plotWidget.name == "QC":
                    plotWidget.refreshPlot()
                elif plotWidget.key == original_key:
                    plotWidget.key = new_key
                    plotWidget.name = new_key
                    plotWidget.refreshPlot()
        # Add data information into dataList
        self.addData(self.wf.data)
        self.msg2Statusbar.emit("Ready")
        self.msg2TextArea.emit(
            "Key name {} changed to {}.".format(original_key, new_key))

    def applyResample(self, rule):
        """
        It applies the resample function to  self.waterframe
        :param rule: Rule to resample.
        """
        self.msg2Statusbar.emit("Resampling data")
        self.wf.resample(rule)
        self.msg2Statusbar.emit("Ready")

    def applySlice(self, start, stop):
        """
        It applies the resample function to  self.waterframe
        :param start: Start time.
        :param stop: Stop time
        """
        self.msg2Statusbar.emit("Slicing data")

        self.wf.slice_time(start, stop)

        self.addData(self.wf.data)
        self.refreshPlots()

        self.msg2Statusbar.emit("Ready")
        self.msg2TextArea.emit(
            "Dataframe sliced from {} to {}.".format(start, stop))

    def graphClick(self, item):
        if item.text() == "QC":
            self.addQCBarPlot()
        elif item.text() == "Spectrogram":
            self.addSpectroPlot()

    def newWaterFrame(self):
        """Create a new WaterFrame object and clean all screens."""
        self.wf = WaterFrame()
        # Delete all plots
        for plotWidget in self.plotWidgetList:
            plotWidget.deleteLater()
        self.plotWidgetList.clear()
        # Hide the widget
        self.hide()

    def refreshPlots(self):
        """It refresh all plots"""
        self.msg2Statusbar.emit("Refreshing plots")

        for plotWidget in self.plotWidgetList:
            try:
                plotWidget.refreshPlot()
            except KeyError:
                self.plotWidgetList.remove(plotWidget)
                plotWidget.hide()
                plotWidget.deleteLater()

        self.msg2Statusbar.emit("Ready")
