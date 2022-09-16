from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from src.MainLayout import *
from src.config import db_anmeldung, getdbcreds
from src.db import dbopen



class BaseInfo(ArvenWidget):
    def __init__(self):
        super(BaseInfo, self).__init__('not')

        self.topdown = QVBoxLayout()
        self.topdown.setContentsMargins(40, 35, 40, 0)
        self.topdown.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.topdown)

        self.across1 = QHBoxLayout()
        self.topdown.addLayout(self.across1)
        self.topdown_left = QVBoxLayout()
        self.across1.addLayout(self.topdown_left)
        self.across1.addSpacerItem(self.spacerH)

        self.ersteinrichtung = ArvenButton('Datenbankzugang')
        self.ersteinrichtung.clicked.connect(self.openDBinfo)
        self.topdown_left.addWidget(self.ersteinrichtung)


        self.erst_hinweis = ArveLabel('notice', 'Bitte richten Sie den Datenbankzugang ein')
        self.topdown_left.addWidget(self.erst_hinweis)
        self.topdown_left.addSpacerItem(self.spacerV)

    def openDBinfo(self):
        self.DBinfo = InputDBinfo()
        self.DBinfo.show()






class InputDBinfo(ArvenWidget):
    def __init__(self):
        super(InputDBinfo, self).__init__('not')
        self.topdown = QVBoxLayout()
        self.setLayout(self.topdown)
        self.setStyleSheet('background-color:white')

        self.instruction = ArveLabel('header', 'Bitte hier die Zugangsdaten für die Datenbank eingeben, '
                                               'die Sie von Arvensteyn erhalten haben')

        self.hostname = InputArve('Hostname')
        self.dbname = InputArve('Datenbank Name')
        self.username = InputArve('Benutzername')
        self.password1 = InputArve('Passwort')
        self.password1.setClearButtonEnabled(True)
        self.password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.password2 = InputArve('Passwort wiederholen')
        self.password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.password2.textChanged.connect(self.passwordident)
        self.password1.textChanged.connect(self.passwordident)
        self.password2.setClearButtonEnabled(True)
        self.password2.setEchoMode(QLineEdit.EchoMode.Password)

        self.passwordstatus = ArveLabel('notice', '')
        self.checkdb = ArvenButton('Datenbankzugang prüfen')
        self.checkdb.setDisabled(True)
        self.checkdb.clicked.connect(self.check_connection)

        self.topdown.addWidget(self.instruction)
        self.topdown.addWidget(self.hostname)
        self.topdown.addWidget(self.dbname)
        self.topdown.addWidget(self.username)
        self.topdown.addWidget(self.password1)
        self.topdown.addWidget(self.password2)
        self.topdown.addWidget(self.passwordstatus)
        self.topdown.addWidget(self.checkdb)

    def passwordident(self):
        if not self.password1.text() == self.password2.text():
            if not self.password2.text() == '':
                self.passwordstatus.setText('Passwörter stimmen nicht überein')
                self.checkdb.setDisabled(True)  
        elif self.password1.text() == self.password2.text():
            if not self.password2.text() == '':
                self.passwordstatus.setText('Passwörter stimmen überein')
                self.checkdb.setDisabled(False)

    def check_connection(self):
        #db_anmeldung(self.hostname.text(), self.dbname.text(), self.username.text(), self.password1.text())
        dbopen()


        