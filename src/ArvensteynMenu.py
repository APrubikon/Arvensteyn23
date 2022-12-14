
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, Qt
from src.data import MostRecentFiles
from src.MainWindow import Pitch
from src.Timesheet import Timeframe
from src.NewEntry import NewTimeEntry

class Tray(QSystemTrayIcon):
    def __init__(self):
        super(Tray, self).__init__()
        icon = QIcon("/Users/Shared/PycharmProjects/arvensteynIII/gui/g2045-3w.png")

        self.setIcon(icon)
        self.setVisible(True)

        # Create the menu
        self.Main_Menu = QMenu()
        self.MainMenu1 = QMenu("Zeiterfassung")
        self.MainMenu3 = QAction("Arvensteyn öffnen")
        self.MainMenu4 = QMenu("Neues Dokument erstellen")
        self.MainMenu5 = QAction("Quit")

        self.MainMenu5.triggered.connect(self.quit)
        self.MainMenu3.triggered.connect(self.maximize)

        # Populate Zeiterfassung mit früheren Eintrögen
        self.list = MostRecentFiles()
        self.indexlist = []

        for i in range(self.list.rowCount()):
            az = self.list.index(i, 1)
            self.indexlist.append(az)

       # dynamic population of Menu with previously used filenumbers
        for item in self.indexlist:
            timesheet = self.MainMenu1.addAction(item.data(Qt.ItemDataRole.DisplayRole))
            timesheet.triggered.connect(lambda triggered, a=item : self.quickOpen(a))

        # populate Auswahl von Dokumenten
        self.anschreiben = self.MainMenu4.addAction("Anschreiben")
        self.telefonvermerk = self.MainMenu4.addAction("Telefonvermerk")
        self.gerichtSS = self.MainMenu4.addAction("Gerichtlicher Schriftsatz")
        self.aktenvermerk = self.MainMenu4.addAction("Aktenvermerk")

        #self.anschreiben.triggered.connect(self.anschreiben_neu)
        #self.telefonvermerk.triggered.connect(self.telefonvermerk_neu)
        #self.gerichtSS.triggered.connect(self.aktenvermerk_neu)
        #self.aktenvermerk.triggered.connect(self.gerichtSS_neu)

        self.setContextMenu(self.Main_Menu)
        self.Main_Menu.addMenu(self.MainMenu1)
        self.Main_Menu.addAction(self.MainMenu3)
        self.Main_Menu.addMenu(self.MainMenu4)
        self.Main_Menu.addAction(self.MainMenu5)
        self.show()


    @pyqtSlot(QtCore.QModelIndex)
    def quickOpen(self, item):
        if Timeframe.openPrevTimeSheet(Timeframe(), item):
            app = QApplication.topLevelWidgets()
            print(app)
            for a in app:
                if isinstance(a, NewTimeEntry):
                    print(a)
                    a.showMaximized()



    def quit(self):
        app = QApplication.instance()
        print("exit gracefully")
        app.quit()

    def anschreiben_neu(self):
       # dokumente = DokumenteCentral(1)
        #dokumente.showMaximized()
        #dokumente.setFocus()
        pass

    def telefonvermerk_neu(self):
        #dokumente = DokumenteCentral(2)
        #dokumente.showMaximized()
        #dokumente.setFocus()
        pass

    def aktenvermerk_neu(self):
        #dokumente = DokumenteCentral(3)
        #dokumente.showMaximized()
        #dokumente.setFocus()
        pass
    def gerichtSS_neu(self):
        #dokumente = DokumenteCentral(4)
        #dokumente.showMaximized()
        #dokumente.setFocus()
        pass


    def maximize(self):
        app = QApplication.topLevelWidgets()
        for a in app:
            if isinstance(a, Pitch):
                a.showMaximized()