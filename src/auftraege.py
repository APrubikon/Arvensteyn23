from src.MainLayout import *
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QCompleter,
    QDataWidgetMapper,
    QAbstractItemView
)

from PyQt6 import QtCore
from PyQt6.QtCore import QRegularExpression, QModelIndex, QItemSelection
from PyQt6.QtGui import QRegularExpressionValidator
from datetime import date

today_date = date.today()
Jahr = today_date.strftime("%y")

from src.data import DBModelMdt, DBModelAuftraege, Auftragsauswahl, Gerichte

kollisionen = {"Kollisionsprüfung durch verantwortlichen Partner ergebnislos" : 1,
               "Strategische Kollision mit Bestandsmandat, Klärung mit verantwortlichen Partnern vor Annahme erfolgt" : 2,
               "Kollision i.e.S festgestellt, Mandat wird abgelehnt oder beendet" : 3}







mapper = QDataWidgetMapper()
ergebnisModel = DBModelAuftraege()
ergebnisModel.sort(0, Qt.SortOrder.AscendingOrder)
mapper.setModel(ergebnisModel)


def setMapper(current):
    mapper.setCurrentIndex(current)
    print(mapper.currentIndex())
    print(current)


class MainFrameAuftraege(ArvenWidget):
    def __init__(self):
        super(MainFrameAuftraege, self).__init__('not')

        self.setWindowTitle("Aufträge bearbeiten")

        self.mainHBox = QHBoxLayout()
        self.block_a = SearchfieldAuftraege()
        self.block_b = DatenAuftraege()

        self.mainHBox.addWidget(self.block_a, 1)
        self.mainHBox.addWidget(self.block_b, 2)

        self.setLayout(self.mainHBox)




class SearchfieldAuftraege(ArvenWidget):
    def __init__(self):
        super(SearchfieldAuftraege, self).__init__(framed="framed")

        self.searchMode1 = ArvenRadio("Mandant nach Namen auswählen", "checked")
        self.searchMode1.toggled.connect(self.searchModeSelect)

        self.searchMode2 = ArvenRadio("Mandant nach Nummer auswählen", "not")
        self.searchMode2.toggled.connect(self.searchModeSelect)

        self.searchModes = QHBoxLayout()
        self.searchModes.addWidget(self.searchMode1)
        self.searchModes.addWidget(self.searchMode2)

        self.search_line = InputArve("Bitte Mandanten auswählen")
        self.completer = QCompleter()
        self.completer.setModel(DBModelMdt())
        self.completer.setCompletionColumn(1)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)

        self.completer.activated[QtCore.QModelIndex].connect(self.indexmap)

        self.ergebnisListe = ArvenTable()
        self.ergebnisListe.clicked.connect(self.indexmap_2)
        self.ergebnisListe.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.ergebnisListe.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.vBox = QVBoxLayout(self)
        self.vBox.addLayout(self.searchModes)
        self.vBox.addWidget(self.search_line)
        self.vBox.addWidget(self.ergebnisListe)
        self.searchModeSelect()

    def searchModeSelect(self):
        if self.searchMode2.isChecked():
            self.search_line.clear()
            self.search_line.setPlaceholderText("Mandant nach Nummer auswählen")
            limit = QRegularExpression("[0-9]*")
            limiter = QRegularExpressionValidator(limit)
            self.search_line.setValidator(limiter)
            self.search_line.setCompleter(self.completer)
            self.completer.setCompletionColumn(0)

        else:
            self.search_line.clear()
            self.search_line.setCompleter(self.completer)
            self.completer.setCompletionColumn(1)
            self.search_line.setPlaceholderText("Bitte Mandanten auswählen")
            self.search_line.setValidator(None)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def indexmap(self, index):
        self.MdtNrInt:int = index.sibling(index.row(), 0).data()
        self.MdtName:str = index.sibling(index.row(), 1).data()
        self.Auftragsliste(self.MdtName)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def indexmap_2(self, index):
        self.AuftrID: int = index.sibling(index.row(), 4).data()
        for i in range(ergebnisModel.rowCount()):
                if ergebnisModel.record(i).value(0) == self.AuftrID:
                    print(ergebnisModel.record(i).value(0))
                    mapper.setCurrentIndex(i)


        print(DBModelAuftraege.lastError(DBModelAuftraege()).text())


    def Auftragsliste(self, MdtName:str):
        model = Auftragsauswahl(MdtName)
        self.ergebnisListe.setModel(model)
        self.ergebnisListe.verticalHeader().hide()
        self.ergebnisListe.horizontalHeader().setStretchLastSection(True)
        self.ergebnisListe.horizontalHeader().hide()

        self.ergebnisListe.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.ergebnisListe.resizeRowsToContents()
        self.ergebnisListe.setColumnHidden(2, True)
        self.ergebnisListe.setColumnHidden(3, True)
        self.ergebnisListe.setColumnHidden(4, True)


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

        self.Auftragsname = InputArve("Auftragsbezeichnung")
        self.Auftragsnummer = InputArve("Auftragsnummer")
        self.Auftragsnummer.setReadOnly(True)
        self.Gegner = InputArve("Gegner")
        self.AddGegner = ArvenButton("Gegner zur Datenbank hinzufügen")
        self.Gegner2 = InputArve("weiterer Gegner")
        self.AddGegner2 = ArvenButton("weiteren Gegner zur Datenbank hinzufügen")
        self.Gegner3 = InputArve("sonstiger Beteiligter")
        self.AddGegner3 = ArvenButton("sonstigen Beteiligten zur Datenbank hinzufügen")
        self.rvg = ArveCheck("Abrechnung nach RVG", False)
        self.anmerkungen = ArvenText("Bemerkungen")

        self.kollisionAuftr = ComboArve("Auftragsbezogene Kollisionsprüfung")
        self.Gerichte = InputArve("Gericht")
        self.completer_ger = QCompleter()
        self.completer_ger.setModel(Gerichte())
        self.completer_ger.setCompletionColumn(1)
        self.completer_ger.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.Gerichte.setCompleter(self.completer_ger)
        self.completer_ger.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.gerichtAz = InputArve("Gerichtliches Az.")

        self.streitwert = InputArve("Streitwert")
 
        limit = QRegularExpression("[0-9]*")
        limiter = QRegularExpressionValidator(limit)
        self.streitwert.setValidator(limiter)

        self.addRae = ArvenButton("Gegnerische Rechtsanwälte hinzufügen")

        mapper.addMapping(self.Auftragsname, 5)
        mapper.addMapping(self.Auftragsnummer, 4)

        # Todo add mapping
        self.HBox.addWidget(self.Auftragsname, 2)
        self.HBox.addWidget(self.Auftragsnummer, 1)
        self.HBox1.addWidget(self.Gegner, 2)
        self.HBox1.addWidget(self.AddGegner, 1)
        self.HBox2.addWidget(self.Gegner2, 2)
        self.HBox2.addWidget(self.AddGegner2, 1)
        self.HBox3.addWidget(self.Gegner3, 2)
        self.HBox3.addWidget(self.AddGegner3, 1)
        self.HBox4.addSpacerItem(self.spacerH)
        self.HBox4.addWidget(self.addRae)
        self.HBox5.addWidget(self.streitwert)
        self.HBox5.addWidget(self.rvg)
        self.HBox6.addWidget(self.Gerichte, 2)
        self.HBox6.addWidget(self.gerichtAz, 1)

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
        self.fill_kollision()


    def fill_kollision(self):
        for key, value in kollisionen.items():
            self.kollisionAuftr.addItem(str(key), value)




