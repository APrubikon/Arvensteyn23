from PyQt6 import uic, QtGui
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QLineEdit,
                             QLabel,
                             QSizePolicy,
                             QComboBox,
                             QPushButton,
                             QSpacerItem,
                             QCheckBox,
                             QRadioButton,
                             QDateEdit,
                             QSpinBox,
                             QTableView,
                             QAbstractItemView,
                             QTextEdit,
                             QDialog,
                             QDialogButtonBox,
                             QVBoxLayout,
                             QFrame
                             )
from PyQt6.QtCore import Qt, QLocale

# todo
#from src.config import currentConfig as curr

import datetime

today = datetime.datetime.today()
today = today.strftime("%d.%m.%Y")





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("Arvensteyn_Frame")

        # open main layout
        self.ui = uic.loadUi(
            '/Users/christophengel/Library/Mobile Documents/com~apple~CloudDocs/Arvensteyn22/media/QWidgetVorlage.ui',
            self)

        # establish Keyboard Shortcuts
        self.quitSc = QShortcut(QKeySequence('command+Q'), self)
        self.quitSc.activated.connect(self.quit)

        # kopfzeile = f"""{self.Beruf} {self.Name}"""
        # self.Kopfzeile.setText(kopfzeile)
        # self.Kopfzeile.setStyleSheet("font: bold;")
        #
        # self.setStyleSheet("background-color:white")
        # pixmap = QtGui.QPixmap('/Users/Shared/PycharmProjects/arvensteynIII/gui/g2046-2.png')
        # self.labelLogo.setPixmap(pixmap)
        #
        # self.Arve = QtGui.QIcon("/Users/Shared/PycharmProjects/arvensteynIII/gui/g2045-3t.png")
        # self.ButtonZurueck = ArvenButton('zurück')
        # self.ButtonZurueck.setIcon(self.Arve)
        # self.labelDatum.setText(today)
        # self.distanz = ArveLabel("notice", "")

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
        # from src.desktop import Desktop
        # Desktop().showMaximized()

    def quit(self):
        app = QApplication.instance()
        print("properly quit")
        app.quit()
