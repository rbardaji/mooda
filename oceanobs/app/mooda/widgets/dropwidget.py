from PyQt5.QtWidgets import (QWidget, QLabel, QListWidget, QPushButton,
                             QRadioButton, QSpinBox, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal, Qt


class DropWidget(QWidget):
    """
    Pyqt5 widget to show items in a QListWidget with Checks. It is used in
    PlotSplitter.
    """
    # Signals
    list2drop = pyqtSignal(list, list)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Labels
        dropLabel = QLabel("Delete parameter")

        # Lists
        self.dropList = QListWidget(self)

        # Buttons
        applyDropButton = QPushButton("Apply")
        applyDropButton.clicked.connect(self.sendLabels)
        hideDropButton = QPushButton("Hide")
        hideDropButton.clicked.connect(self.hide)

        # Radio buttons
        self.allRadio = QRadioButton("All", self)
        self.allRadio.setChecked(True)
        self.goodRadio = QRadioButton("Use QC Flags = 0 and 1", self)
        self.oneRadio = QRadioButton("Remove QC flag: ", self)

        # Spin inputs
        self.qcSpinBox = QSpinBox(self)
        self.qcSpinBox.setMinimum(0)
        self.qcSpinBox.setMaximum(9)
        self.qcSpinBox.setValue(0)

        # Layout
        # - Horizontal Layout for oneRadioButton -
        hOne = QHBoxLayout()
        hOne.addWidget(self.oneRadio)
        hOne.addWidget(self.qcSpinBox)
        # - General layout -
        vDrop = QVBoxLayout()
        vDrop.addWidget(dropLabel)
        vDrop.addWidget(self.dropList)
        vDrop.addWidget(self.allRadio)
        vDrop.addWidget(self.goodRadio)
        vDrop.addLayout(hOne)
        vDrop.addWidget(applyDropButton)
        vDrop.addWidget(hideDropButton)
        self.setLayout(vDrop)

    def addLabels(self, labels):
        """Add items to self.dropList"""
        # Clear the list
        self.dropList.clear()
        # Add new items
        self.dropList.addItems(labels)

        # Configure the items checkable
        for index in range(self.dropList.count()):
            item = self.dropList.item(index)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

    def sendLabels(self):
        """
        It returns the list of checked items from self.dropList. It also send
        the signal list2drop with the list.

        Returns
        -------
            (labels, flagList): (list of str, list of int)
                (List with checked labels from self.dropList, List of flags)
        """
        # Look for checked items and create the list
        labels = []
        for index in range(self.dropList.count()):
            item = self.dropList.item(index)
            if item.checkState():
                labels.append(item.text())

        # Flag lists
        flagList = []
        if self.allRadio.isChecked():
            flagList = [None]
        elif self.goodRadio.isChecked():
            flagList = [2, 3, 4, 5, 6, 7, 8, 9]
        elif self.oneRadio.isChecked():
            flagList = [self.qcSpinBox.value()]
        # Send the signal
        if len(labels) > 0:
            self.list2drop.emit(labels, flagList)
        return labels, flagList
