from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QCompleter
import nacl.pwhash
from PyQt6 import QtCore
from src.MainLayout import *
from src.config import db_anmeldung, getdbcreds, initialcheck, get_headline
from src.db import dbopen
from src.data import MitarbeiterCred



class BaseInfo(ArvenWidget):
    def __init__(self):
        super(BaseInfo, self).__init__('not')

        self.initial = initialcheck()
        self.headline = get_headline()

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

        self.anmeldung = ArvenButton('Arvensteyn Login')
        self.zweit_hinweis = ArveLabel('notice', 'Bitte Arvensteyn Mitarbeiter einrichten')

        self.anmeldung.clicked.connect(self.openanmeldung)
        
        self.topdown_left.addWidget(self.anmeldung)
        self.topdown_left.addWidget(self.zweit_hinweis)



        self.topdown_left.addSpacerItem(self.spacerV)

        self.activateinitialcheck()

    def openDBinfo(self):
        self.DBinfo = InputDBinfo()
        self.DBinfo.show()

    def activateinitialcheck(self):
        # check if db credentials
        if not self.initial == '':
            print('8')
        else:
            print('9')

    def openanmeldung(self):
        self.anmeldung_input = Login()
        self.anmeldung_input.show()







class InputDBinfo(ArvenWidget):
    def __init__(self):
        super(InputDBinfo, self).__init__('not')
        self.setWindowTitle('Datenbank Zugriff')
        self.topdown = QVBoxLayout()
        self.setLayout(self.topdown)
        self.setStyleSheet('background-color:white')

        self.instruction = ArveLabel('header', 'Bitte hier die Zugangsdaten f??r die Datenbank eingeben, '
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
        self.checkdb = ArvenButton('Datenbankzugang pr??fen')
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
        self.setData()   

    def passwordident(self):
        if not self.password1.text() == self.password2.text():
            if not self.password2.text() == '':
                self.passwordstatus.setText('Passw??rter stimmen nicht ??berein')
                self.checkdb.setDisabled(True)  
        elif self.password1.text() == self.password2.text():
            if not self.password2.text() == '':
                self.passwordstatus.setText('Passw??rter stimmen ??berein')
                self.checkdb.setDisabled(False)

    def check_connection(self):
        db_anmeldung(self.hostname.text(), self.dbname.text(), self.username.text(), self.password1.text())
        if dbopen():
            self.close()

    def setData(self):
        creds = getdbcreds()
        self.hostname.setText(creds['host'])
        self.dbname.setText(creds['database'])
        self.username.setText(creds['user'])
        self.password1.setText(creds['pw'])
        self.password2.setText(creds['pw'])

class Login(ArvenWidget):
    def __init__(self):
        super(Login, self).__init__('not')
        self.setWindowTitle('Arvensteyn Login')

        self.topdown = QVBoxLayout()
        self.setLayout(self.topdown)
        self.setStyleSheet('background-color:white')

        self.instruction = ArveLabel('header', 'Arvensteyn Login f??r Mitarbeiter')



        self.username = InputArve('Mitarbeiter Name')
        self.password1 = InputArve('Passwort')
        self.password1.setClearButtonEnabled(True)
        self.password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.password2 = InputArve('Passwort wiederholen')
        self.password1.setEchoMode(QLineEdit.EchoMode.Password)
        self.password2.textChanged.connect(self.passwordident)
        self.password1.textChanged.connect(self.passwordident)
        self.password2.setClearButtonEnabled(True)
        self.password2.setEchoMode(QLineEdit.EchoMode.Password)
        self.completer = QCompleter()
        self.completer.setModel(MitarbeiterCred())
        self.completer.setCompletionColumn(1)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.username.setCompleter(self.completer)

        self.passwordstatus = ArveLabel('notice', '')
        self.login_click = ArvenButton('Arvensteyn Login')
        self.login_click.setDisabled(True)
        self.login_click.clicked.connect(self.login)

        self.topdown.addWidget(self.instruction)
        self.topdown.addWidget(self.username)
        self.topdown.addWidget(self.password1)
        self.topdown.addWidget(self.password2)
        self.topdown.addWidget(self.passwordstatus)
        self.topdown.addWidget(self.login_click)
        #self.setData()

    def login(self):
        MitarbeiterCred.checkKey(MitarbeiterCred(), self.username.text())
        print(MitarbeiterCred.checkpass(MitarbeiterCred(), self.username.text(), self.password1.text()))
        #    self.close()
        #else:
        #    self.passwordstatus.setText("Falsche Logindaten")
        #

    def encryptpw(self):
        orig_password = self.password1.text().encode('utf-8')

        # Hashing the password
        hashed_data = nacl.pwhash.str(orig_password)

        # The result will be True on password match.
        res = nacl.pwhash.verify(hashed_data, orig_password)
        print(res)
       
        # On mismatch an exception will be raised
       # wrong_password = b'My password'
       # res2 = nacl.pwhash.verify(hashed_data, wrong_password)









    def passwordident(self):
        if not self.password1.text() == self.password2.text():
            if not self.password2.text() == '':
                self.passwordstatus.setText('Passw??rter stimmen nicht ??berein')
                self.login_click.setDisabled(True)
        elif self.password1.text() == self.password2.text():
            if not self.password2.text() == '':
                self.passwordstatus.setText('Passw??rter stimmen ??berein')
                self.login_click.setDisabled(False)