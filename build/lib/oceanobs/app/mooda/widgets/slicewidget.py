from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QDateTimeEdit,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal


class SliceWidget(QWidget):
    """Custom widget to slice data"""
    # Signals
    sliceTimes = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Labels
        sliceLabel = QLabel("Slicing")
        startLabel = QLabel("Start: ")
        endLabel = QLabel("End: ")

        # DateTimeEdit
        self.startDateTimeEdit = QDateTimeEdit()
        self.endDateTimeEdit = QDateTimeEdit()

        # Buttons
        applyButton = QPushButton("Apply")
        applyButton.clicked.connect(self.sendTimes)
        hideButton = QPushButton("Hide")
        hideButton.clicked.connect(self.hide)

        # Layouts
        # - Horizontal for start
        hStart = QHBoxLayout()
        hStart.addWidget(startLabel)
        hStart.addWidget(self.startDateTimeEdit)
        # - Horizontal for end
        hEnd = QHBoxLayout()
        hEnd.addWidget(endLabel)
        hEnd.addWidget(self.endDateTimeEdit)

        # - Vertical for self
        vWidget = QVBoxLayout()
        vWidget.addWidget(sliceLabel)
        vWidget.addLayout(hStart)
        vWidget.addLayout(hEnd)
        vWidget.addWidget(applyButton)
        vWidget.addWidget(hideButton)
        self.setLayout(vWidget)

    def sendTimes(self):
        self.sliceTimes.emit(self.startDateTimeEdit.text(),
                             self.endDateTimeEdit.text())

    def refresh(self, start, end):

        self.startDateTimeEdit.setMinimumDateTime(start)
        self.startDateTimeEdit.setMaximumDateTime(end)
        self.startDateTimeEdit.setDateTime(start)
        self.endDateTimeEdit.setMinimumDateTime(start)
        self.endDateTimeEdit.setMaximumDateTime(end)
        self.endDateTimeEdit.setDateTime(end)
