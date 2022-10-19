from src.MainLayout import *
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QCompleter,
    QDataWidgetMapper,
    QAbstractItemView
)


from PyQt6.QtCore import QRegularExpression, QModelIndex, QItemSelection, QVariantAnimation, pyqtSlot, QEvent
from PyQt6.QtGui import QRegularExpressionValidator
from datetime import date
from src.MdtVerwaltung import SearchfieldMandanten
from src.variables import Jahr
from src.InputHumans import Human_Selection

today_date = date.today()
Jahr = today_date.strftime("%y")

from src.data import DBModelMdt, DBModelAuftraege, Auftragsauswahl, Gerichte, AuftragsauswahlNr, Auftragnummer

kollisionen = {"Kollisionsprüfung durch verantwortlichen Partner ergebnislos" : 1,
               "Strategische Kollision mit Bestandsmandat, Klärung mit verantwortlichen Partnern vor Annahme erfolgt" : 2,
               "Kollision i.e.S festgestellt, Mandat wird abgelehnt oder beendet" : 3}


class MainFrameAuftraege(ArvenWidget):
    def __init__(self):
        super(MainFrameAuftraege, self).__init__('not')

        self.setWindowTitle("Neuen Auftrag anlegen")
        self.title = ArveLabel('header', "Neuen Auftrag anlegen")
        self.title.setStyleSheet('color:rgb(9, 58, 112); font-weight: bold;')
        self.title.installEventFilter(self)

        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.title)

        self.mainHBox = QHBoxLayout()
        self.block_a = SearchfieldMandanten()
        self.block_b = DatenAuftraege()
        self.block_b.setDisabled(True)

        self.mainHBox.addWidget(self.block_a, 1)
        self.mainHBox.addWidget(self.block_b, 2)

        self.VBox.addLayout(self.mainHBox)
        self.setLayout(self.VBox)

        ##signals
        self.block_a.searchLine_mdt.returnPressed.connect(self.filtermdt)
        self.block_a.search_table.doubleClicked.connect(self.indexmap_2)

    def new_newAuftrag(self):
        self.block_b.setDisabled(True)
        self.slide_search('in')


    def slide_search(self, direction):
        self.animation1 = QVariantAnimation(self)
        self.animation1.setDuration(200)

        if direction == 'in':
            self.animation1.setStartValue(self.block_a.width())
            self.animation1.setEndValue(500)
            #self.animation1.finished.connect(self.addSearchfield(False))
            self.animation1.start()

        elif direction == 'out':
            self.animation1.setStartValue(self.block_a.width())
            self.animation1.setEndValue(0)
            self.animation1.start()
        self.animation1.valueChanged.connect(self.slide_searchII)

    def slide_searchII(self, value):
        self.block_a.setFixedWidth(value)

    def filtermdt(self):
        self.block_a.search_model.filter_by_name(self.block_a.searchLine_mdt.text())

    @pyqtSlot(QModelIndex)
    def indexmap_2(self, index):
        # central fork to change from searchfield to individual client.
        if not index.sibling(index.row(), 1).data() is None:  # no client nr. = no client fields
            self.cur_index = index.sibling(index.row(), 1).data()  # identify client nr.
            self.cur_mdt = index.sibling(index.row(), 0).data()
            self.slide_search('out')
            self.block_b.setDisabled(False)
            self.block_b.fill_initial(self.cur_index, self.cur_mdt)
            self.define_az(self.cur_index)

        else:
            self.cur_index = ''  # don't crash if no client nr., retry
            self.block_a.searchLine_mdt.clear()

    def define_az(self, cur_mdtid):

        self.mdt_az = str(cur_mdtid).zfill(4)
        self.checknr = Auftragnummer(cur_mdtid)
        self.jahr = self.checknr.max_auftragsjahr()
        self.lastnummer = self.checknr.max_auftrag()

        if not self.jahr == Jahr:
            newnummer = str(1).zfill(3)
            self.new_az = f"""{self.mdt_az}-{Jahr}-{newnummer}"""

        else:
            newnummer = self.lastnummer + 1
            newnummer = str(newnummer).zfill(3)
            self.new_az = f"""{self.mdt_az}-{Jahr}-{newnummer}"""

        self.block_b.Auftragsnummer.setText(f"""{self.new_az} (neu)""")

    def eventFilter(self, obj, event):
        if not self.isEnabled() == False:
            if event.type() == QEvent.Type.MouseButtonPress:
                if self.title is obj:
                    self.new_newAuftrag()


        return QWidget.eventFilter(self, obj, event)




class DatenAuftraege(ArvenWidget):
    def __init__(self):
        super(DatenAuftraege, self).__init__(framed="not")

        self.VBox = QVBoxLayout(self)
        self.HBox = QHBoxLayout()
        self.HBox1 = QHBoxLayout()
        self.HBox2 = QHBoxLayout()
        self.HBox3 = QHBoxLayout()
        self.HBox4 = QHBoxLayout()
        self.HBox5 = QHBoxLayout()
        self.HBox6 = QHBoxLayout()

        self.Auftragsjahr = Jahr

        self.mandant = InputArve('Mandant')
        self.Auftragsname = InputArve("Neue Auftragsbezeichnung")
        # to automatische AZ-Vergabe
        self.Auftragsnummer = InputArve("Aktenzeichen wird automatisch vergeben")
        self.Auftragsnummer.setReadOnly(True)
        self.Gegner = InputArve("Gegner")
        self.Gegner.installEventFilter(self)
        self.Gegner2 = InputArve("weiterer Gegner")
        self.Gegner2.installEventFilter(self)
        self.Gegner3 = InputArve("sonstiger Beteiligter")
        self.Gegner3.installEventFilter(self)
        self.rvg = ArveCheck("Abrechnung nach RVG", False)
        self.anmerkungen = ArvenText("Bemerkungen")

        self.kollisionAuftr = InputArve("Auftragsbezogene Kollisionsprüfung")
        self.kollisionAuftr.setReadOnly(True)
        self.kollisionAuftr.installEventFilter(self)
        self.Gerichte = InputArve("Gericht")

        self.gerichtAz = InputArve("Gerichtliches Az.")

        self.streitwert = InputArve("Streitwert")

        limit = QRegularExpression("[0-9]*")
        limiter = QRegularExpressionValidator(limit)
        self.streitwert.setValidator(limiter)




        self.HBox.addWidget(self.Auftragsname, 2)
        self.HBox.addWidget(self.Auftragsnummer, 1)
        self.HBox1.addWidget(self.Gegner)
        self.HBox2.addWidget(self.Gegner2)
        self.HBox3.addWidget(self.Gegner3)
        self.HBox4.addSpacerItem(self.spacerH)

        self.HBox5.addWidget(self.streitwert)
        self.HBox5.addWidget(self.rvg)
        self.HBox6.addWidget(self.Gerichte, 2)
        self.HBox6.addWidget(self.gerichtAz, 1)

        self.VBox.addWidget(self.mandant)
        self.VBox.addLayout(self.HBox)
        self.VBox.addLayout(self.HBox1)
        self.VBox.addLayout(self.HBox2)
        self.VBox.addLayout(self.HBox3)
        self.VBox.addLayout(self.HBox4)
        self.VBox.addWidget(self.kollisionAuftr)
        self.VBox.addLayout(self.HBox6)
        self.VBox.addLayout(self.HBox5)
        self.VBox.addWidget(self.anmerkungen)

        self.VBox.addSpacerItem(self.spacerV)

        ## subwindows
        self.gegner1 = Human_Selection(prozess="neu")
        self.gegner1.setWindowTitle('Gegner eintragen')
        self.gegner2 = Human_Selection(prozess="neu")
        self.gegner2.setWindowTitle('Weiteren Gegner eintragen')
        self.sonstBet = Human_Selection(prozess="neu")
        self.sonstBet.setWindowTitle('Sonstigen Beteiligten eintragen')



        self.gegner1.tab1.block_a.ButtonAdd.clicked.connect(self.write_gegner1)
        self.gegner1.tab2.uebernehmen.clicked.connect(self.add_gegner1)
        self.gegner2.tab1.block_a.ButtonAdd.clicked.connect(self.write_gegner2)
        self.gegner2.tab2.uebernehmen.clicked.connect(self.add_gegner2)
        self.sonstBet.tab1.block_a.ButtonAdd.clicked.connect(self.write_sonstBet)
        self.sonstBet.tab2.uebernehmen.clicked.connect(self.add_sonstBet)

    def fill_initial(self, mandantid, MandantName):
        self.mandant.setText(MandantName)
        self.mandantid = mandantid


    def eventFilter(self, obj, event):
        if not self.isEnabled() == False:
            if event.type() == QEvent.Type.MouseButtonPress:
                if self.kollisionAuftr is obj:
                    self.fill_koll()
                elif self.Gegner is obj:
                    self.open_gegner1()
                elif self.Gegner2 is obj:
                    self.open_gegner2()
                elif self.Gegner3 is obj:
                    self.open_sonstBet()

        return QWidget.eventFilter(self, obj, event)

    def fill_koll(self):
        dlg = ComboDialog('Kollisionsprüfung', 'Bitte Ergebnis der Kollisionsprüfung auswählen', kollisionen)

        if dlg.exec():
            self.KollisionErg = dlg.combobox.currentText()
            self.kollisionAuftr.setText(self.KollisionErg)

    def open_gegner1(self):
        self.gegner1.show()

    def open_gegner2(self):
        self.gegner2.show()

    def open_sonstBet(self):
        self.sonstBet.show()

    def write_gegner1(self):
        pass

    def add_gegner1(self):
        pass

    def write_gegner2(self):
        pass

    def add_gegner2(self):
        pass

    def write_sonstBet(self):
        pass

    def add_sonstBet(self):
        pass

    def write_gegnerRAe(self):
        pass

    def add_gegnerRAe(self):
        pass
