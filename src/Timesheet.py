from src.MainLayout import *
from PyQt6.QtWidgets import (QVBoxLayout,
                             QHBoxLayout,
                             QAbstractItemView,
                             QCompleter)

from PyQt6 import QtCore
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from src.data import DBModelAuftraege, MostRecentFiles, DBModelMdt, Auftragsauswahl, AuftragsauswahlNr
from src.NewEntry import NewTimeEntry

from src.auxiliary_gui import EmptyDelegate
from src.Leistungserfassung import New_Entry

ergebnisModel = DBModelAuftraege()
delegate = EmptyDelegate()

def forwarding(packet:dict):
    print(packet)


class Timeframe(ArvenWidget):
    def __init__(self):
        super(Timeframe, self).__init__('not')
        self._ts = None

        self.setWindowTitle("Zeiterfassung - Startseite")
        self.timesheet = None

        self.block_a = FindAuftrag()
        self.block_a.setParent(self)
        self.block_b = CurrentFiles()
        self.block_b.setParent(self)
        #self.block_c = CurrentAffairs()

        self.block_a.ergebnisListe.clicked.connect(self.openNewTimeSheet)
        self.block_b.last_files.clicked.connect(self.openPrevTimesheetInternal)
        self.MainHBlock = QHBoxLayout()
        self.VBlock = QVBoxLayout()
        self.VBlock1 = QVBoxLayout()
        self.VBlock.addWidget(self.block_a)
        self.VBlock.addWidget(self.block_b)
        
        self.VBlock1.addSpacerItem(self.spacerV)

        self.MainHBlock.addLayout(self.VBlock, 1)
        self.MainHBlock.addLayout(self.VBlock1, 2)

        self.setLayout(self.MainHBlock)

    def openPrevTimeSheet(self, index):
        if not index.sibling(index.row(), 0).data() is None:
            self.AuftrIndex = index.sibling(index.row(), 0).data()
        else:
            self.AuftrIndex = ''

        if not index.sibling(index.row(), 1).data() is None:
            self.az = index.sibling(index.row(), 1).data()
        else:
            self.az = ''

        if not index.sibling(index.row(), 2).data() is None:
            self.mdt = index.sibling(index.row(), 2).data()
        else:
            self.mdt = ''

        if not index.sibling(index.row(), 3).data() is None:
            self.auftrag = index.sibling(index.row(), 3).data()
        else:
            self.auftrag = ''

        self.packet = {'file': self.AuftrIndex, 'az': self.az, 'mdt': self.mdt, 'auftrag': self.auftrag}
        print(self.packet)
        self.selectAuftrag()

    def openPrevTimesheetInternal(self, index):
        if not index.sibling(index.row(), 0).data() is None:
            self.AuftrIndex = index.sibling(index.row(), 0).data()
        else:
            self.AuftrIndex = ''

        if not index.sibling(index.row(), 1).data() is None:
            self.az = index.sibling(index.row(), 1).data()
        else:
            self.az = ''

        if not index.sibling(index.row(), 2).data() is None:
            self.mdt = index.sibling(index.row(), 2).data()
        else:
            self.mdt = ''

        if not index.sibling(index.row(), 3).data() is None:
            self.auftrag = index.sibling(index.row(), 3).data()
        else:
            self.auftrag = ''

        #self.packet = {'file': self.AuftrIndex, 'az': self.az, 'mdt': self.mdt, 'auftrag': self.auftrag}
        self.selectAuftragInternal()



    def selectAuftrag(self):
        if self.timesheet is None:
            self.timesheet = NewTimeEntry(file=self.AuftrIndex, az=self.az, mdt= self.mdt, auftrag=self.auftrag)
        self.timesheet.show()



    def selectAuftragInternal(self):
        if self._ts is None:
            #for i in reversed(range(self.VBlock1.count())):
            #    self.VBlock1.itemAt(i).widget().setParent(None)
            self._ts = NewTimeEntry(file=self.AuftrIndex, az=self.az, mdt=self.mdt, auftrag=self.auftrag, parent=self)
            self.VBlock1.addWidget(self._ts, 2)
        else:
            self.VBlock1.removeWidget(self._ts)
            self._ts = NewTimeEntry(file=self.AuftrIndex, az=self.az, mdt=self.mdt, auftrag=self.auftrag, parent=self)
            self.VBlock1.addWidget(self._ts, 2)



    def openNewTimeSheet(self, index):
        if not index.sibling(index.row(), 4).data() is None:
            self.AuftrIndex = index.sibling(index.row(), 4).data()
        else:
            self.AuftrIndex = ''

        if not index.sibling(index.row(), 0).data() is None:
            self.az = index.sibling(index.row(), 0).data()
        else:
            self.az = ''
        if not index.sibling(index.row(), 3).data() is None:
            self.mdt = index.sibling(index.row(), 3).data()
        else:
            self.mdt = ''
        if not index.sibling(index.row(), 1).data() is None:
            self.auftrag = index.sibling(index.row(), 1).data()
        else:
            self.auftrag = ''

        self.packet = {'file': self.AuftrIndex, 'az': self.az, 'mdt': self.mdt, 'auftrag': self.auftrag}
        self.selectAuftragInternal()

    

class CurrentFiles(ArvenWidget):
    def __init__(self):
        super(CurrentFiles, self).__init__(framed="not")

        self.last_files = ArvenTable()
        model = MostRecentFiles()
        self.last_files.setModel(model)
        self.last_files.setColumnHidden(0, True)
        self.last_files.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.last_files.resizeRowsToContents()

        self.last_files.setItemDelegate(delegate)
        self.title = ArveLabel("header", "Meine zuletzt verwendeten Akten")

        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.title)
        self.VBox.addWidget(self.last_files)

        self.setLayout(self.VBox)


class CurrentAffairs(ArvenWidget):
    def __init__(self):
        super(CurrentAffairs, self).__init__("not")

        pass

class FindAuftrag(ArvenWidget):
    def __init__(self):
        super(FindAuftrag, self).__init__(framed="framed")

        self.searchMode1 = ArvenRadio("Mandant nach Namen auswählen", "checked")
        self.searchMode1.toggled.connect(self.searchModeSelect)

        self.searchMode2 = ArvenRadio("Mandant nach Nummer auswählen (vierstellig", "not")
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
        self.ergebnisListe.setParent(self)

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
            self.search_line.returnPressed.connect(self.auftragsliste_num)

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
        self.auftragsliste(self.MdtName)
        print(DBModelAuftraege.lastError(DBModelAuftraege()).text())


    def auftragsliste(self, MdtName:str):
        self.model = Auftragsauswahl(MdtName)
        self.ergebnisListe.setModel(self.model)
        self.ergebnisListe.verticalHeader().hide()
        self.ergebnisListe.horizontalHeader().setStretchLastSection(True)
        self.ergebnisListe.horizontalHeader().hide()

        self.ergebnisListe.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.ergebnisListe.resizeRowsToContents()
        self.ergebnisListe.setColumnHidden(2, True)
        self.ergebnisListe.setColumnHidden(3, True)
        self.ergebnisListe.setColumnHidden(4, True)

    def auftragsliste_num(self):
        MdtNr = self.search_line.text()
        print(MdtNr)
        model = AuftragsauswahlNr(MdtNr)
        self.ergebnisListe.setModel(model)
        self.ergebnisListe.verticalHeader().hide()
        self.ergebnisListe.horizontalHeader().setStretchLastSection(True)
        self.ergebnisListe.horizontalHeader().hide()

        self.ergebnisListe.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.ergebnisListe.resizeRowsToContents()
        self.ergebnisListe.setColumnHidden(2, True)
        self.ergebnisListe.setColumnHidden(3, True)
        self.ergebnisListe.setColumnHidden(4, True)
