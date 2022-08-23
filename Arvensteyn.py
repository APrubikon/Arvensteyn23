from PyQt6.QtWidgets import QApplication, QProgressBar, QSystemTrayIcon, QMenu, QMainWindow, QStackedWidget
import sys  # Only needed for access to command line arguments
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from src.global_stylesheet import arvensteyn_style

#from src.desktop import Desktop
#from src.ArvensteynMenu import Tray
#
#from src.EditMdt import EditMdt
#from src.InputHumans import Human
#from src.auftraege import MainFrameAuftraege
#
#from src.Login import Login
#from src.Timesheet import Timeframe, New_Entry
#from src.Rechnungslauf import Rechnungslauf
#from security import LeistungenMasterView
#from src.data import Leistungen
#from src.testtable import Testtable
#from src.korrektur import Korrekturfile
#from src.variables import workdays
#

def singleton():
    apps = QApplication.topLevelWidgets()
    for i in apps:
        i.close()


class ArvensteynMain(QMainWindow):
    def __init__(self):
        super(ArvensteynMain, self).__init__()

        self.ui = uic.loadUi('/Users/Shared/PycharmProjects/arvensteynIII/gui/QWidgetVorlage.ui', self)

        self.quitSc = QShortcut(QKeySequence('command+Q'), self)
        self.quitSc.activated.connect(self.quit)

        kopfzeile = f"""{self.Beruf} {self.Name}"""
        self.Kopfzeile.setText(kopfzeile)
        self.Kopfzeile.setStyleSheet("font: bold;")

        self.setStyleSheet("background-color:white")
        pixmap = QtGui.QPixmap('/Users/Shared/PycharmProjects/arvensteynIII/gui/g2046-2.png')
        self.labelLogo.setPixmap(pixmap)

        self.Arve = QtGui.QIcon("/Users/Shared/PycharmProjects/arvensteynIII/gui/g2045-3t.png")
        self.ButtonZurueck = ArvenButton('zurück')
        self.ButtonZurueck.setIcon(self.Arve)
        self.labelDatum.setText(today)
        self.distanz = ArveLabel("notice", "")

        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)
        self.spacerH = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Expanding,
                                   vPolicy=QSizePolicy.Policy.Minimum)

        self.ButtonZurueck.clicked.connect(self.returnDesktop)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def returnDesktop(self):
        apps = QApplication.topLevelWidgets()
        for i in apps:
            i.close()
        from src.desktop import Desktop
        Desktop().showMaximized()

    def quit(self):
        app = QApplication.instance()
        print("outta here")
        app.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(arvensteyn_style)




    try:
        sys.exit(app.exec())

    except:
        print("Exiting")


if __name__ == '__main__':
    main()
