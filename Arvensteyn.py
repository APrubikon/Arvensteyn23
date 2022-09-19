from PyQt6.QtWidgets import QApplication, QProgressBar, QSystemTrayIcon, QMenu, QMainWindow, QStackedWidget, QWidget
import sys  # Only needed for access to command line arguments
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from src.MainWindow import *

from src.ArvensteynMenu import Tray
from src.config import definecfgFile
#
# from src.EditMdt import EditMdt
# from src.InputHumans import Human
# from src.auftraege import MainFrameAuftraege
#
# from src.Login import Login
# from src.Timesheet import Timeframe, New_Entry
# from src.Rechnungslauf import Rechnungslauf
# from security import LeistungenMasterView
# from src.data import Leistungen
# from src.testtable import Testtable
# from src.korrektur import Korrekturfile
# from src.variables import workdays
#

def singleton():
    apps = QApplication.topLevelWidgets()
    for i in apps:
        i.close()


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
