from src.MainLayout import *
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QTextEdit,
    QDataWidgetMapper,
    QCalendarWidget,
    QTabWidget
)

from PyQt6.QtCore import QRegularExpression, pyqtSlot, QModelIndex, QVariant
from PyQt6.QtGui import QRegularExpressionValidator
from src.data import DBModelHumans
from src.variables import today, today_date



class Human(ArvenWidget):
    def __init__(self, prozess: str):

        super(Human, self).__init__(framed='not')
        self.url = None
        self.note = None
        self.work_email_1 = None
        self.mobile_phone_1 = None
        self.work_fax_1 = None
        self.work_phone_3 = None
        self.work_phone_2 = None
        self.work_phone_1 = None
        self.work_zip_1 = None
        self.work_city_1 = None
        self.work_address_1 = None
        self.role = None
        self.title = None
        self.birthday = None
        self.name_complete = None
        self.name_last = None
        self.name_first = None
        self.name_prefix = None
        self.organization = None
        self.setWindowTitle("Arvensteyn - Adressbuch")

        self.Titel = ArveLabel("header", "")
        self.VBox = QVBoxLayout(self)
        self.HBox1 = QHBoxLayout()
        self.HBox2 = QHBoxLayout()
        self.HBox3 = QHBoxLayout()
        self.HBox4 = QHBoxLayout()
        self.HBox5 = QHBoxLayout()
        self.HBox6 = QHBoxLayout()
        self.HBox7 = QHBoxLayout()
        self.block_a = HumanWidgets()

        self.Prozessschritt(prozess=prozess)

        self.tether = ""



    def human_cleanup(self):
        #self.index =  # todo
        #self.warning = # todo
        self.name_prefix = self.block_a.Anrede.currentText()
        self.name_first = self.block_a.Vorname.text()
        self.name_complete = f"""{self.block_a.Nachname.text()}, {self.block_a.Vorname.text()}"""

        self.name_last = self.block_a.Nachname.text()
        self.birthday = self.block_a.birthday.date()

        # self.photo =
        self.organization = self.block_a.Arbeitgeber.text()

        self.title = self.block_a.Titel.currentText()

        self.role = self.block_a.Position.text()

       # self.logo_url =

        #self.mailer =

        #self.home_address_1 =
        # =
        #self.home_city_1 =
        # =
        #self.home_state_1 =
        # =
        #self.home_zip_1 =
        # =
        #self.home_country_1 =
        #  # =
        #self.home_address_2 =
        # =
        #self.home_city_2 =
        # =
        #self.home_state_2 =
        # =
        #self.home_zip_2 =
        # =
        #self.home_country =
        # =
        #self.home_address_3 =
        # =
        #self.home_city_3 =
        # =
        #self.home_state_3 =
        # =
        #self.home_zip_3 =
        # =
        #self.home_country_2 =
        # =
        self.work_address_1 = f"""{self.block_a.Adresse1.text()} {self.block_a.Adresse2.text()}"""

        self.work_city_1 = self.block_a.Ort.text()

        #self.work_state_1 =

        self.work_zip_1 = self.block_a.PLZ.text()

        #self.work_country_1 =

        #self.work_address_2 =
        # =
        #self.work_city_2 =
        # =
        #self.work_state_2 =
        # =
        #self.work_zip_2 =
        # =
        #self.work_country_2 =
        # =
        #self.work_address_3 =
        # =
        #self.work_city_3 =
        # =
        #self.work_state_3 =
        # =
        #self.work_zip_3 =
        # =
        #self.work_country_3 =
        # =
        #self.home_phone_1 =
        # =
        #self.home_phone_2 =
        # =
        #self.home_phone_3 =

        self.work_phone_1 = self.block_a.Telefon.text()

        self.work_phone_2 = self.block_a.Telefon1.text()

        self.work_phone_3 = self.block_a.Telefon2.text()

        #self.home_fax_1 =
        # =
        #self.home_fax_2 =
        # =
        #self.home_fax_3 =

        self.work_fax_1 = self.block_a.Fax.text()

        #self.work_fax_2 =
        # =
        #self.work_fax_3 =
        # =
        self.mobile_phone_1 = self.block_a.Mobil.text()
        # =
        #self.mobile_phone_2 =
        # =
        #self.mobile_phone_3 =
        # =
        #self.home_email_1 =
        # =
        #self.home_email_2 =
        # =
        #self.home_email_3 =

        self.work_email_1 = self.block_a.Email.text()
        # =
        #self.work_email_2 = self.block_a..text()
        # =
        #self.work_email_3 =
        # =
        #self.geocode =
        # =
        #self.timezone =
        # =
        #self.agent =
        # =
        self.note = self.block_a.Kommentare.toPlainText()
        #self.rev =

        self.url = self.block_a.url.text()

       # self.uidaim =
       #  =
       # self.icq =
       #  =
       # self.msn =
       #  =
       # self.yahoo =
       #  =
       # self.jabber =
       #  =
       # self.skype =
       #  =
       # self.gadugadu =
       #  =
       # self.groupwise =


        packet = {"name_full" : self.name_complete, "name_prefix" : self.name_prefix, "name_first" : self.name_first, "name_last" : self.name_last,
                  "birthday" : self.birthday, "organization" : self.organization , "title" : self.title, "role" : self.role,
                  "work_address1" : self.work_address_1, "work_city1": self.work_city_1, "work_zip1" : self.work_zip_1,
                  "work_phone_1" : self.work_phone_1, "work_phone_2" : self.work_phone_2 , "work_phone_3" : self.work_phone_3,
                  "work_fax" : self.work_fax_1, "mobile_phone_1" : self.mobile_phone_1, "work_email_1" : self.work_email_1,
                  "note" : self.note, "url" : self.url}

        #print(packet)
        self.tether = DBModelHumans.welcome_human(DBModelHumans(), **packet)


    def leash(self):
        print(f"""{self.tether} times""")
        return self.tether


    def Prozessschritt(self, prozess: str) -> object:
        if prozess == "neu":
            self.Titel.setText("Neuen Eintrag im Adressbuch anlegen")

            self.HBox1.addWidget(self.block_a.Vorname)
            self.HBox1.addWidget(self.block_a.Nachname)
            self.VBox.addLayout(self.HBox1)
            self.HBox7.addWidget(self.block_a.Anrede)
            self.HBox7.addWidget(self.block_a.Titel)
            self.VBox.addLayout(self.HBox7)
            self.VBox.addWidget(self.block_a.Arbeitgeber)
            self.VBox.addWidget(self.block_a.Position)
            self.HBox2.addWidget(self.block_a.Adresse1)
            self.HBox2.addWidget(self.block_a.Adresse2)
            self.VBox.addLayout(self.HBox2)
            self.HBox3.addWidget(self.block_a.PLZ)
            self.HBox3.addWidget(self.block_a.Ort)
            self.VBox.addLayout(self.HBox3)
            self.HBox4.addWidget(self.block_a.Telefon, 2)
            self.HBox4.addWidget(self.block_a.extraTelefon1, 1)
            self.VBox.addLayout(self.HBox4)
            self.HBox5.addWidget(self.block_a.Telefon1, 2)
            self.HBox5.addWidget(self.block_a.extraTelefon2, 1)
            self.VBox.addLayout(self.HBox4)
            self.block_a.Telefon1.hide()
            self.block_a.extraTelefon2.hide()
            self.block_a.Telefon2.hide()
            self.VBox.addWidget(self.block_a.Telefon2)
            self.VBox.addLayout(self.HBox5)

            self.VBox.addWidget(self.block_a.Telefon2)

            self.VBox.addLayout(self.HBox4)
            self.VBox.addLayout(self.HBox4)
            self.VBox.addWidget(self.block_a.Mobil)
            self.VBox.addWidget(self.block_a.Fax)
            self.VBox.addWidget(self.block_a.Email)
            self.VBox.addWidget(self.block_a.url)
            self.VBox.addWidget(self.block_a.Kommentare)

            self.VBox.addWidget(self.block_a.PersAddBook)
            self.VBox.addWidget(self.block_a.ButtonAdd)

            self.VBox.addSpacerItem(self.spacerV)

            self.block_a.extraTelefon1.clicked.connect(self.extraTelefon1)
            self.block_a.extraTelefon2.clicked.connect(self.extraTelefon2)

        if prozess == "auswahl":
            self.Titel.setText("Eintrag aus Adressbuch auswählen")

    def extraTelefon1(self):
        self.block_a.extraTelefon2.show()
        self.block_a.Telefon1.show()

    def extraTelefon2(self):
        self.block_a.Telefon2.show()

    def clearinput(self):
        self.block_a.Vorname.clear()
        self.block_a.Nachname.clear()
        self.block_a.Anrede.clear()
        self.block_a.Titel.clear()
        self.block_a.Arbeitgeber.clear()
        self.block_a.Position.clear()
        self.block_a.Adresse1.clear()
        self.block_a.Adresse2.clear()
        self.block_a.PLZ.clear()
        self.block_a.Ort.clear()
        self.block_a.Telefon.clear()
        self.block_a.Telefon1.clear()
        self.block_a.Telefon2.clear()
        self.block_a.Fax.clear()
        self.block_a.Email.clear()
        self.block_a.birthday.clear()
        self.block_a.Kommentare.clear()
        self.block_a.url.clear()
        self.block_a.Mobil.clear()






class Human_Selection(ArvenWidget):
    def __init__(self, prozess:str):
        super(Human_Selection, self).__init__('not')

        self.setWindowTitle("Arvensteyn Adressbuch")
        self.setStyleSheet('background-color:white')


        self.setBaseSize(800, 800)

        self.zurueck = ArvenButton("Schließen!")
        self.zurueck.clicked.connect(self.closing)


        self.tabs = QTabWidget(self)
        self.tab1 = Human("neu")
        self.tab2 = HumanAuswahl()
        self.tabs.addTab(self.tab1, "Neuen Kontakt eintragen")
        self.tabs.addTab(self.tab2, "Kontakt aus Adressbuch wählen")

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.zurueck)
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.tabs)


    def closing(self):
        self.close()

class HumanWidgets(ArvenWidget):
    def __init__(self):
        super(HumanWidgets, self).__init__(framed="framed")

        Anreden = ["Frau", "Herr", "Ms", "Mr"]
        Titel = ["Dr.", "Prof. Dr."]
        limit = QRegularExpression("[0-9]*")
        limiter = QRegularExpressionValidator(limit)

        self.PersAddBook = ArveCheck("Zu meinem persönlichen Adressbuch hinzufügen", False)
        self.Nachname = InputArve("Name")
       # self.Nachname.setFixedWidth(250)
        self.Vorname = InputArve("Vorname")
        #self.Vorname.setFixedWidth(250)
        self.Anrede = ComboArve("Anrede auswählen")
        self.Anrede.addItems(Anreden)
        self.Titel = ComboArve("Titel auswählen")
        self.Titel.addItems(Titel)
        self.birthday = ArvenDate()
        #self.birthday.setDate(today_date)
        self.url = InputArve("Website")
        self.url.setFixedWidth(250)
        self.Arbeitgeber = InputArve("Unternehmen")
        self.Position = InputArve("Position im Unternehmen")
        self.Adresse1 = InputArve("Straße")
        self.Adresse2 = InputArve("Hausnummer")
        self.Adresse2.setFixedWidth(100)
        self.PLZ = InputArve("PLZ")
        self.PLZ.setFixedWidth(100)
        self.Ort = InputArve("Ort")
        self.Telefon = InputArve("Telefon")
        self.Telefon.setValidator(limiter)
        self.Telefon.setToolTip(
            "Deutsche Telefonnummern bitte ohne Länderkennziffer aber mit Vorwahl eingeben")
        self.extraTelefon1 = ArvenButton("weitere Telefonnummer hinzufügen")

        self.Telefon1 = InputArve("Telefon")
        self.Telefon1.setValidator(limiter)
        self.Telefon1.setToolTip(
            "Deutsche Telefonnummern bitte ohne Länderkennziffer aber mit Vorwahl eingeben")
        self.extraTelefon2 = ArvenButton("weitere Telefonnummer hinzufügen")

        self.Telefon2 = InputArve("Telefon")
        self.Telefon2.setValidator(limiter)
        self.Telefon2.setToolTip(
            "Deutsche Telefonnummern bitte ohne Länderkennziffer aber mit Vorwahl eingeben")

        self.Mobil = InputArve("Mobiltelefon")
        self.Mobil.setToolTip("Deutsche Mobilnummern bitte ohne Länderkennziffer aber mit Vorwahl eingeben")
        self.Mobil.setValidator(limiter)
        self.Fax = InputArve("Faxnummer")
        self.Fax.setValidator(limiter)
        self.Fax.setToolTip("Deutsche Faxnummern bitte ohne Länderkennziffer aber mit Vorwahl eingeben")
        self.Email = InputArve("E-Mail-Adresse")
        self.Kommentare = QTextEdit()
        self.Kommentare.setStyleSheet("border-radius:4px; background-color: rgb(241,241,241);")
        self.Kommentare.setPlaceholderText("Anmerkungen zu dem Kontakt")

        self.NeuesAnschreiben = ArvenButton("Neues Anschreiben in MS Word anlegen")
        self.ButtonAdd = ArvenButton("Zum Adressbuch hinzufügen")

class HumanAuswahl(ArvenWidget):
    def __init__(self):
        super(HumanAuswahl, self).__init__('not')

        self.NrHuman = 0

        self.auswahl = InputArve('Nach Namen suchen')
        self.auswahl.returnPressed.connect(self.select)
        self.liste = ArvenTable()
        self.liste.clicked.connect(self.selectfromliste)
        self.uebernehmen = ArvenButton("Übernehmen")

        self.fullname = ArveLabel('header', '')

        self.arbeitgeber = ArveLabel('notice', '')
        self.position = ArveLabel('notice', '')
        self.adress1 = ArveLabel('notice', '')
        self.adress2 = ArveLabel('notice', '')

        self.telephone1 = ArveLabel('notice', '')
        self.telephone2 = ArveLabel('notice', '')
        self.telefax = ArveLabel('notice', '')
        self.email = ArveLabel('notice', '')

        self.MainVertical = QVBoxLayout()
        self.setLayout(self.MainVertical)
        self.MainVertical.addWidget(self.auswahl)
        self.MainVertical.addWidget(self.liste)
        self.MainVertical.addWidget(self.fullname)
        self.MainVertical.addWidget(self.arbeitgeber)
        self.MainVertical.addWidget(self.position)
        self.MainVertical.addWidget(self.adress1)
        self.MainVertical.addWidget(self.adress2)
        self.MainVertical.addWidget(self.telephone1)
        self.MainVertical.addWidget(self.telephone2)
        self.MainVertical.addWidget(self.telefax)
        self.MainVertical.addWidget(self.email)
        self.MainVertical.addSpacerItem(self.spacerV)
        self.MainVertical.addWidget(self.uebernehmen)

    def select(self):
        selectionmodel = DBModelHumans()
        selectionmodel.filter_name(self.auswahl.text())
        self.liste.setModel(selectionmodel)
        for i in range(selectionmodel.columnCount()):
            self.liste.setColumnHidden(i, True)
        self.liste.setColumnHidden(2, False)

    @pyqtSlot(QModelIndex)
    def selectfromliste(self, index):
        self.NrHuman: int = index.sibling(index.row(), 0).data()
        self.NameHuman = index.sibling(index.row(), 2).data()
        self.TitleHuman = index.sibling(index.row(), 12).data()
        self.GenderHuman = index.sibling(index.row(), 3).data()
        self.Organization = index.sibling(index.row(), 11).data()
        self.Position = index.sibling(index.row(), 13).data()
        self.adressdata1 = index.sibling(index.row(), 31).data()
        self.adressdata2 = index.sibling(index.row(), 34).data()
        self.adressdata3 = index.sibling(index.row(), 32).data()
        self.telephonedata1 = index.sibling(index.row(), 49).data()
        self.telephonedata2 = index.sibling(index.row(), 58).data()
        self.telephaxdata3 = index.sibling(index.row(), 55).data()
        self.emaildata1 = index.sibling(index.row(), 64).data()

        self.fullname.setText(f"""{self.GenderHuman} {self.TitleHuman} {self.NameHuman}""")
        self.arbeitgeber.setText(f"""{self.Organization}""")
        self.position.setText(self.Position)
        self.adress1.setText(self.adressdata1)
        self.adress2.setText(f"""{self.adressdata2} {self.adressdata3}""")
        self.telephone1.setText(self.telephonedata1)
        self.telephone2.setText(self.telephonedata2)
        self.telefax.setText(self.telephaxdata3)
        self.telephone1.setText(self.emaildata1)
