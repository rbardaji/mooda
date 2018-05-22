from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal


class RenameWidget(QWidget):
    """Widget to rename keys from a WaterFrame"""
    # Signals
    key2change = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Labels
        renameLabel = QLabel("Rename:")
        toLabel = QLabel("to")

        # ComboBox
        self.keyComboBox = QComboBox()

        # Line edit
        self.newNameLineEdit = QLineEdit()

        # Buttons
        applyButton = QPushButton("Apply")
        applyButton.clicked.connect(self.sendLabels)
        hideButton = QPushButton("Hide")
        hideButton.clicked.connect(self.hide)

        # Layouts
        # - Horizontal for rename
        hRename = QHBoxLayout()
        hRename.addWidget(self.keyComboBox)
        hRename.addWidget(toLabel)
        hRename.addWidget(self.newNameLineEdit)
        hRename.addStretch()
        # - Vertical for self
        vWidget = QVBoxLayout()
        vWidget.addWidget(renameLabel)
        vWidget.addLayout(hRename)
        vWidget.addWidget(applyButton)
        vWidget.addWidget(hideButton)
        self.setLayout(vWidget)

    def addLabels(self, labels):
        """Add items to self.dropList"""
        # Clear the ComboBox
        self.keyComboBox.clear()
        # Clear the input box
        self.newNameLineEdit.clear()
        # Add new items
        self.keyComboBox.addItems(labels)

    def sendLabels(self):
        if self.newNameLineEdit.text():
            self.key2change.emit(self.keyComboBox.currentText(),
                                 self.newNameLineEdit.text())
