import sys
from PyQt5.QtWidgets import QApplication
from mooda.app.mooda_gui.widgets import MOODA


def main():
    app = QApplication(sys.argv)
    md = MOODA()
    md.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
