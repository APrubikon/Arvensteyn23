from PyQt6 import QtWidgets
from PyQt6 import QtCore
from src.MainLayout import MainWindow, ArvenButton, InputArve, ArveLabel


class Login(MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        # Login page
        #self.Kopfzeile.hide()
        #self.labelDatum.hide()
        self.ButtonZurueck.hide()
        self.setWindowTitle("Arvensteyn - Login")


        # individual Widgets

        self.MitgliederName = InputArve('Benutzer')
        self.MitgliederName.setFocus()
        self.Password = InputArve('Bitte Passwort eingeben')
        self.Password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.LoginButton = ArvenButton("Login")
       # self.completer = QtWidgets.QCompleter()
       #
       # self.completer.setModel(DBModel1())
       # self.completer.setCompletionColumn(1)
       # self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
      #  self.MitgliederName.setCompleter(self.completer)
        self.LoginNotice = ArveLabel("notice", "")


        # individual layouts

        self.vBox = QtWidgets.QVBoxLayout()
        self.vBox.addSpacerItem(self.spacerV)
        self.vBox.addWidget(self.MitgliederName)
        self.vBox.addWidget(self.Password)
        self.vBox.addWidget(self.LoginButton)
        self.vBox.addWidget(self.LoginNotice)
        self.vBox.addSpacerItem(self.spacerV)

        self.hBox = QtWidgets.QHBoxLayout()
        self.hBox.addSpacerItem(self.spacerH)
        self.hBox.addLayout(self.vBox)
        self.hBox.addSpacerItem(self.spacerH)

        # add individual Gui elements to MainWindow
       # self.MainVerticalLayout.addLayout(self.hBox)

        # signal for LoginButton
        self.LoginButton.clicked.connect(self.knock)

        self.MitgliederName.setFocus()


    def knock(self):
        # pass input to DB
        Mitglied = self.MitgliederName.text()
        PW = self.Password.text()
        if not Mitglied == "":
           print('CHA')
           # DBModel1.checkKey(self=DBModel1, Mitglied=Mitglied, Passtry=PW)
        else:
            pass


    def entry(self, permission:str):
        # receive input from DB/controller and act GUI
        if permission == "granted":
            from Arvensteyn import Switch
            Switch.pageNr(self=Switch(), extension=1)
        else:
            self.loginNotice()

    def loginNotice(self):
        self.LoginNotice.setText("receptor")
                                                  

def shut(self):
        self.close()





