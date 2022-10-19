from PyQt6.QtWidgets import QApplication, QProgressBar, QSystemTrayIcon, QMenu, QMainWindow, QStackedWidget, QWidget
import sys  # Only needed for access to command line arguments
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from src.MainWindow import *

from src.ArvensteynMenu import Tray
from src.MdtVerwaltung import Mandantenverwaltung

def main():
    app = QApplication(sys.argv)
    w = Pitch()
    w.showMaximized()
    #app.setQuitOnLastWindowClosed(False)

    QLocale.setDefault(QLocale(QLocale.Language.German))

    modul_trayII = Tray()
    modul_trayII.show()






    try:
        sys.exit(app.exec())

    except:
        print("Exiting")


if __name__ == '__main__':
    main()
