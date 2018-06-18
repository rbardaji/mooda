from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal


class ResampleWidget(QWidget):
    """
    Custom widget to resample data.
    """
    # Signals
    resampleRule = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Labels
        resampleLabel = QLabel("Resample:")

        # ComboBox
        self.ruleComboBox = QComboBox()
        self.ruleComboBox.addItems(
            ["None", "Minutely", "Hourly", "Daily", "Weekly"])

        # Buttons
        applyButton = QPushButton("Apply")
        applyButton.clicked.connect(self.sendRule)
        hideButton = QPushButton("Hide")
        hideButton.clicked.connect(self.hide)

        # Layouts
        # - Horizontal for rename
        hResample = QHBoxLayout()
        hResample.addWidget(resampleLabel)
        hResample.addWidget(self.ruleComboBox)
        # - Vertical for self
        vWidget = QVBoxLayout()
        vWidget.addLayout(hResample)
        vWidget.addWidget(applyButton)
        vWidget.addWidget(hideButton)
        self.setLayout(vWidget)

    def sendRule(self):

        rule = None
        if self.ruleComboBox.currentText() == "Minutely":
            rule = "T"
        elif self.ruleComboBox.currentText() == "Hourly":
            rule = "H"
        elif self.ruleComboBox.currentText() == "Daily":
            rule = "D"
        elif self.ruleComboBox.currentText() == "Weekly":
            rule = "W"

        self.resampleRule.emit(rule)
