from PyQt5.QtWidgets import (QFrame, QPlainTextEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFileDialog)
from PyQt5.QtCore import pyqtSignal


class TextFrame(QFrame):
    """Pyqt5 widget to write info. It is used as a datalog."""
    # Signals
    msg2Statusbar = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Create text entry box
        self.text = QPlainTextEdit()

        # Buttons
        hideButton = QPushButton("Hide", self)
        hideButton.clicked.connect(self.hide)
        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.save)

        # Layout
        # - Vertical layout for buttons -
        vButton = QVBoxLayout()
        vButton.addWidget(saveButton)
        vButton.addWidget(hideButton)
        vButton.addStretch()
        # - Layout of the frame -
        hFrame = QHBoxLayout()
        hFrame.addWidget(self.text)
        hFrame.addLayout(vButton)
        self.setLayout(hFrame)

    def write(self, message):
        """
        It appends on the QPlainTextEdit element the "message".

        Parameters
        ----------
            message: str
                Message to write.
        """
        self.text.appendPlainText(message)

    def save(self):
        """
        It opens a SaveFileDialog and save the text of the QPlainTextEdit on
        the path.
        """
        # Open the save file dialog
        fileName, _ = QFileDialog.getSaveFileName(
            caption="Save text as...",
            directory="",
            filter="Text File (*.txt)")
        if fileName:
            # Read the content of the QPlainTextEdit
            content = self.text.toPlainText()
            # Save the content
            with open(fileName, "w") as text_file:
                text_file.write(content)
                self.msg2Statusbar.emit("Datalog saved on {}".format(fileName))
