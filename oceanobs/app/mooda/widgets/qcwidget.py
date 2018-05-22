from PyQt5.QtWidgets import (QWidget, QLabel, QListWidget, QPushButton,
                             QSpinBox, QHBoxLayout, QVBoxLayout, QCheckBox,
                             QDoubleSpinBox)
from PyQt5.QtCore import pyqtSignal, Qt


class QCWidget(QWidget):
    """QC Preferences Widget"""

    # Signals
    list2qc = pyqtSignal(list)

    def __init__(self):
        """Constructor"""

        super().__init__()

        self.initUI()

    def initUI(self):

        # Labels
        qcLabel = QLabel("QC procedures")
        resetLabel = QLabel("Reset QC: ")
        toLabel = QLabel("->")
        badRangeLabel = QLabel("- Bad QC: ")
        badFlatLabel = QLabel("- Bad QC: ")
        badSpikeLabel = QLabel("- Bad QC: ")
        rollingLabel = QLabel("Rolling window: ")
        thresholdLabel = QLabel("Threshold: ")
        parameterLabel = QLabel("Parameters: ")

        # Lists
        self.keyList = QListWidget(self)
        self.keyList.setEnabled(False)

        # Check Box
        self.resetCheck = QCheckBox("Reset QC", self)
        self.resetCheck.setChecked(True)
        self.rangeCheck = QCheckBox("Range test", self)
        self.rangeCheck.setChecked(True)
        self.flatCheck = QCheckBox("Flat test", self)
        self.flatCheck.setChecked(True)
        self.spikeCheck = QCheckBox("Spike test", self)
        self.spikeCheck.setChecked(True)
        self.flag2flagCheck = QCheckBox("Change flags", self)
        self.flag2flagCheck.setChecked(True)
        self.allCheck = QCheckBox("All", self)
        self.allCheck.setChecked(True)
        self.allCheck.toggled.connect(self.keyList.setDisabled)

        # Spin box
        self.originalSpinBox = QSpinBox(self)
        self.originalSpinBox.setMinimum(0)
        self.originalSpinBox.setMaximum(9)
        self.originalSpinBox.setValue(0)
        # -
        self.translatedSpinBox = QSpinBox(self)
        self.translatedSpinBox.setMinimum(0)
        self.translatedSpinBox.setMaximum(9)
        self.translatedSpinBox.setValue(1)
        # -
        self.badRangeSpinBox = QSpinBox(self)
        self.badRangeSpinBox.setMinimum(0)
        self.badRangeSpinBox.setMaximum(9)
        self.badRangeSpinBox.setMinimum(0)
        self.badRangeSpinBox.setValue(4)
        # -
        self.flatSpinBox = QSpinBox(self)
        self.flatSpinBox.setMinimum(0)
        self.flatSpinBox.setMaximum(9)
        self.flatSpinBox.setMinimum(0)
        self.flatSpinBox.setValue(4)
        # -
        self.spikeSpinBox = QSpinBox(self)
        self.spikeSpinBox.setMinimum(0)
        self.spikeSpinBox.setMaximum(9)
        self.spikeSpinBox.setMinimum(0)
        self.spikeSpinBox.setValue(4)
        # -
        self.rollingSpinBox = QSpinBox(self)
        self.rollingSpinBox.setValue(0)
        self.rollingSpinBox.setToolTip(
            "Size of the moving window.\n"
            "This is the number of observations used for calculating"
            " the mean.\n0 = Auto")
        # -
        self.resetSpinBox = QSpinBox(self)
        self.resetSpinBox.setMinimum(0)
        self.resetSpinBox.setMaximum(9)
        self.resetSpinBox.setMinimum(0)
        self.resetSpinBox.setValue(0)
        # -
        self.thresholdSpinBox = QDoubleSpinBox(self)
        self.thresholdSpinBox.setValue(2.00)
        self.thresholdSpinBox.setToolTip(
            "Maximum difference between the value analyzed and the average of"
            " the rooling window.")

        # Button
        applyButton = QPushButton("Apply")
        applyButton.clicked.connect(self.apply)
        closeButton = QPushButton("Hide")
        closeButton.clicked.connect(self.hide)

        # Layouts
        # - Horizontal Layout for reset
        hReset = QHBoxLayout()
        hReset.addWidget(resetLabel)
        hReset.addWidget(self.resetSpinBox)
        hReset.addStretch()
        # - Horizontal Layout for ranges
        hRanges = QHBoxLayout()
        hRanges.addWidget(badRangeLabel)
        hRanges.addWidget(self.badRangeSpinBox)
        hRanges.addStretch()
        # hRanges.addStretch()
        # - Horizontal Layout for flat
        hFlat = QHBoxLayout()
        hFlat.addWidget(badFlatLabel)
        hFlat.addWidget(self.flatSpinBox)
        hFlat.addStretch()
        # hFlat.addStretch()
        # - Horizontal Layout for spykes
        hSpykes = QHBoxLayout()
        hSpykes.addWidget(badSpikeLabel)
        hSpykes.addWidget(self.spikeSpinBox)
        hSpykes.addStretch()
        # - Horizontal Layout for threshold
        hThreshold = QHBoxLayout()
        hThreshold.addWidget(thresholdLabel)
        hThreshold.addWidget(self.thresholdSpinBox)
        hThreshold.addStretch()
        # - Horizontal Layout for rolling window
        hRolling = QHBoxLayout()
        hRolling.addWidget(rollingLabel)
        hRolling.addWidget(self.rollingSpinBox)
        hRolling.addStretch()
        # - Horizontal Layout for flag2flag -
        hFlag2flag = QHBoxLayout()
        hFlag2flag.addWidget(self.originalSpinBox)
        hFlag2flag.addWidget(toLabel)
        hFlag2flag.addWidget(self.translatedSpinBox)
        hFlag2flag.addStretch()
        # - Vertical Layout for the Widget
        vQC = QVBoxLayout()
        vQC.addWidget(parameterLabel)
        vQC.addWidget(self.allCheck)
        vQC.addWidget(self.keyList)
        vQC.addWidget(qcLabel)
        vQC.addWidget(self.resetCheck)
        vQC.addLayout(hReset)
        vQC.addWidget(self.rangeCheck)
        vQC.addLayout(hRanges)
        vQC.addWidget(self.flatCheck)
        vQC.addLayout(hFlat)
        vQC.addWidget(self.spikeCheck)
        vQC.addLayout(hSpykes)
        vQC.addLayout(hThreshold)
        vQC.addLayout(hRolling)
        vQC.addWidget(self.flag2flagCheck)
        vQC.addLayout(hFlag2flag)
        vQC.addWidget(applyButton)
        vQC.addWidget(closeButton)
        vQC.addStretch()
        self.setLayout(vQC)

    def apply(self):
        """
        Emit a signal with the current QC settings
        """
        settings = []
        if self.resetCheck.isChecked():
            settings.append(self.resetSpinBox.text())
        else:
            settings.append(None)
        if self.rangeCheck.isChecked():
            settings.append(self.badRangeSpinBox.text())
        else:
            settings.append(None)
        if self.flatCheck.isChecked():
            settings.append(self.flatSpinBox.text())
        else:
            settings.append(None)
        if self.spikeCheck.isChecked():
            settings.append(self.spikeSpinBox.text())
        else:
            settings.append(None)
        settings.append(self.thresholdSpinBox.text())
        settings.append(self.rollingSpinBox.text())
        if self.flag2flagCheck.isChecked():
            settings.append(self.originalSpinBox.text())
            settings.append(self.translatedSpinBox.text())
        else:
            settings.append(None)
            settings.append(None)
        if self.allCheck.isChecked():
            settings.append("all")
        else:
            for index in range(self.keyList.count()):
                item = self.keyList.item(index)
                if item.checkState():
                    settings.append(item.text())

        self.list2qc.emit(settings)

    def addLabels(self, labels):
        """
        Add items to self.dropList
        """
        # Clear the list
        self.keyList.clear()
        # Add new items
        self.keyList.addItems(labels)
        # Configure the items checkable
        for index in range(self.keyList.count()):
            item = self.keyList.item(index)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
