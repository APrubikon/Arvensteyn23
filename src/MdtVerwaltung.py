from src.data import DBModelMdt, MandantEditmodel, MandantListe, HumanSearch
from src.MainLayout import *
from PyQt6.QtCore import QEvent, QRegularExpression, QVariantAnimation, QTimer, QVariant
from PyQt6.QtGui import QRegularExpressionValidator
import PyQt6.QtSql
import time

from PyQt6.QtWidgets import (
                             QHBoxLayout,
                             QVBoxLayout,
                             QScrollArea,
                             QWidget,
                             QGridLayout,
                             QSpacerItem,
                             QSizePolicy,
                             QTextEdit,
                             QCompleter,
                             QDataWidgetMapper
                            )

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex
from src.InputHumans import Human, Human_Selection

Anreden = ["Frau", "Herr", "Frau Dr.", "Herr Dr.", "Frau Prof. Dr.", "Herr Prof. Dr."]
Positionen = ["Geschäftsführerin", "Geschäftsführer", "Mitglied des Vorstands"]
Bundeslaender = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg',
                 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen',
                 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
Staaten = {"Deutschland" : 1, "EU (außer Deutschland)" : 2, "Außerhalb EU" : 3}

gwg = {"Keine Anhaltspunkte für Geldwäscheverdacht" : 1,
       "Prüfung von Anhaltspunkten auf Geldwäscheverdacht erfolglos (Vermerk)" : 2,
       "Geldwäscheverdacht kann nicht beseitigt werden, Manda(n)t wird abgelehnt oder beendet" : 3}

kollisionspruefung = {"Kollisionsprüfung durch den mandantenverantwortlichen Partner ergebnislos" : 1,
                     "Kollisionen im weiteren Sinn denkbar; Annahme nach Rücksprache mit betroffenen Partnern" : 2,
                     "Kollision im berufsrechtlichen Sinn; Mandant wird abgelehnt" : 3}


class Mandantenverwaltung(ArvenWidget):
    def __init__(self):
        super(Mandantenverwaltung, self).__init__('not')

        self.setObjectName('Mandantenverwaltung')
        self.setWindowTitle("Stammblatt Mandanten bearbeiten")
        self.setStyleSheet('background-color: white')

        ## widgets
        self.new_search = ArveLabel('header', 'Mandanten verwalten')
        self.new_search.setStyleSheet('color:rgb(9, 58, 112); font-weight: bold;')
        self.new_search.installEventFilter(self)

        self.searchfield = SearchfieldMandanten()
        self.editfield = Editfield()


        ## layouts

        self.MainVerticalLayout = QVBoxLayout()
        self.setLayout(self.MainVerticalLayout)
        self.MainHorizontalLayout = QHBoxLayout()

        ## add widgets to Layouts
        self.MainVerticalLayout.addWidget(self.new_search)
        self.MainVerticalLayout.addLayout(self.MainHorizontalLayout)

        self.MainHorizontalLayout.addWidget(self.searchfield)
        self.MainHorizontalLayout.addWidget(self.editfield)
        self.MainHorizontalLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)

        ##signals
        self.searchfield.searchLine_mdt.returnPressed.connect(self.filtermdt)
        self.searchfield.search_table.doubleClicked.connect(self.indexmap_2)
        self.editfield.block_a.Intern.stateChanged.connect(self.editfield.InternalStatusChange)
        #self.editfield.block_c.GVcheck.stateChanged.connect(self.editfield.natPersonChange)
        self.editfield.block_f.Rahmenvertrag.stateChanged.connect(self.editfield.RVChange)
        self.editfield.block_a.Akquise.stateChanged.connect(self.editfield.akquiseStatusChange)
        self.editfield.block_c.GVdisplay.installEventFilter(self)
        self.editfield.block_c.RE_display.installEventFilter(self)

    def filtermdt(self):
        self.searchfield.search_model.filter_by_name(self.searchfield.searchLine_mdt.text())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def indexmap_2(self, index):
        # central fork to change from searchfield to individual client.
        if not index.sibling(index.row(), 1).data() is None:  # no client nr. = no client fields
            self.cur_index = index.sibling(index.row(), 1).data()  # identify client nr.
            self.editfield.addSearchfield(False)
            self.editfield.refresh_data(self.cur_index)
            self.slide_search('out')
        else:
            self.cur_index = ''  # don't crash if no client nr., retry
            self.searchfield.searchLine_mdt.clear()


    def slide_search(self, direction):
        self.animation1 = QVariantAnimation(self)
        self.animation1.setDuration(200)

        if direction == 'in':
            self.animation1.setStartValue(self.searchfield.width())
            self.animation1.setEndValue(500)
            #self.animation1.finished.connect(self.addSearchfield(False))
            self.animation1.start()

        elif direction == 'out':
            self.animation1.setStartValue(self.searchfield.width())
            self.animation1.setEndValue(0)
            #self.animation1.finished.connect(self.addSearchfield(True))
            self.animation1.start()


        self.animation1.valueChanged.connect(self.slide_searchII)

    def slide_searchII(self, value):
        self.searchfield.setFixedWidth(value)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if self.new_search is obj:
                self.slide_search('in')
            elif self.editfield.block_c.GVdisplay is obj:
                self.open_gv()
            elif self.editfield.block_c.RE_display is obj:
                self.open_re()

        return QWidget.eventFilter(self, obj, event)

    def open_gv(self):
        self.editfield.block_gv.tab1.block_a.Arbeitgeber.setText(self.editfield.block_a.NameMdt.text())
        self.editfield.block_gv.tab1.block_a.Position.setText(self.editfield.block_c.GVPosition.text())
        self.editfield.block_gv.tab1.block_a.Adresse1.setText(self.editfield.block_b.Sitz1.text())
        self.editfield.block_gv.tab1.block_a.Adresse2.setText(self.editfield.block_b.Sitz2.text())
        self.editfield.block_gv.tab1.block_a.PLZ.setText(self.editfield.block_b.Sitz3.text())
        self.editfield.block_gv.tab1.block_a.Ort.setText(self.editfield.block_b.Sitz4.text())
        self.editfield.block_gv.show()

    def open_re(self):
        self.editfield.block_re.tab1.block_a.Arbeitgeber.setText(self.editfield.block_a.NameMdt.text())
        self.editfield.block_re.tab1.block_a.Position.setText(self.editfield.block_c.GVPosition.text())
        self.editfield.block_re.tab1.block_a.Adresse1.setText(self.editfield.block_b.Sitz1.text())
        self.editfield.block_re.tab1.block_a.Adresse2.setText(self.editfield.block_b.Sitz2.text())
        self.editfield.block_re.tab1.block_a.PLZ.setText(self.editfield.block_b.Sitz3.text())
        self.editfield.block_re.tab1.block_a.Ort.setText(self.editfield.block_b.Sitz4.text())
        self.editfield.block_re.show()




class SearchfieldMandanten(ArvenWidget):
    def __init__(self):
        super(SearchfieldMandanten, self).__init__('not')

        self.setObjectName('searchfield')
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.setFixedWidth(500)

        self.searchLayout = QVBoxLayout()
        self.setLayout(self.searchLayout)
        self.searchLabel_mdt = ArveLabel('notice', "Bitte Mandanten auswählen...")
        self.searchLine_mdt = InputArve('hier eingeben')
        self.search_table = ArvenTable()
        self.search_model = MandantListe()
        self.search_table.setModel(self.search_model)
        self.search_table.setColumnHidden(1, True)

# layout
        self.searchLayout.addWidget(self.searchLabel_mdt)
        self.searchLayout.addWidget(self.searchLine_mdt)
        self.searchLayout.addWidget(self.search_table)

class Editfield(ArvenWidget):
    def __init__(self):
        super(Editfield, self).__init__('not')
        self.mandantid = ''

        self.setObjectName('EditfieldMandanten')
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.scrollSpace = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollGrid = QGridLayout(self.scrollWidget)
        self.scrollSpace.setWidgetResizable(True)

        self.block_a = GrundDaten()
        self.block_b = Sitz()
        self.block_b.Sitz6.installEventFilter(self)
        self.block_c = GesVertretung()
        self.block_e = Berufsrecht()
        self.block_e.KollisionMdt.installEventFilter(self)
        self.block_e.GeldwaescheG.installEventFilter(self)
        self.block_f = Abrechnung()
        # self.block_g = Options()
        self.block_gv = Human_Selection(prozess="neu")
        self.block_re = Human_Selection(prozess="neu")
        self.addSearchfield(True)

        self.scrollGrid.addWidget(self.block_a, 1, 0)
        self.scrollGrid.addWidget(self.block_b, 2, 0)
        self.scrollGrid.addWidget(self.block_c, 3, 0)
        self.scrollGrid.addWidget(self.block_e, 1, 1)
        self.scrollGrid.addWidget(self.block_f, 2, 1)

        self.mapper_mdt = QDataWidgetMapper(self)
        self.mappermodel_mdt = MandantEditmodel('NULL')

        self.add_mapping()

        self.layouting = QVBoxLayout()
        self.setLayout(self.layouting)
        self.layouting.addWidget(self.scrollSpace)
        self.scrollSpace.setWidget(self.scrollWidget)
        self.scrollSpace.setWidgetResizable(True)

        ## signals fr check boxes and subwindows
        self.block_c.GVcheck.stateChanged.connect(self.update_nat_person)
        self.block_gv.tab1.block_a.ButtonAdd.clicked.connect(self.write_gv)
        self.block_re.tab1.block_a.ButtonAdd.clicked.connect(self.write_re)
        self.block_gv.tab2.uebernehmen.clicked.connect(self.add_gv)
        self.block_re.tab2.uebernehmen.clicked.connect(self.add_re)


    def add_mapping(self):
        self.mapper_mdt.addMapping(self.block_a.NameMdt, 1)
        self.mapper_mdt.addMapping(self.block_a.MdtNr, 22)
        self.mapper_mdt.addMapping(self.block_a.MVP, 3)
        self.mapper_mdt.addMapping(self.block_c.RE_display, 7)
        self.mapper_mdt.addMapping(self.block_b.Sitz1, 8)
        self.mapper_mdt.addMapping(self.block_b.Sitz2, 9)
        self.mapper_mdt.addMapping(self.block_b.Sitz3, 10)
        self.mapper_mdt.addMapping(self.block_b.Sitz4, 11)
        self.mapper_mdt.addMapping(self.block_b.Sitz5, 12)
        self.mapper_mdt.addMapping(self.block_b.Sitz6, 13)
        self.mapper_mdt.addMapping(self.block_c.GVPosition, 30)
        self.mapper_mdt.addMapping(self.block_c.GVdisplay, 6)
        self.mapper_mdt.addMapping(self.block_c.elektr_rechnung, 24)
        self.mapper_mdt.addMapping(self.block_f.Stundensatz1, 14)
        self.mapper_mdt.addMapping(self.block_f.MVPAnteil, 21)
        self.mapper_mdt.addMapping(self.block_f.SonstigesVerguetung, 16)
        self.mapper_mdt.addMapping(self.block_e.GeldwaescheG, 19, b'text')
        self.mapper_mdt.addMapping(self.block_e.KollisionMdt, 20, b'text')

    def refresh_data(self, indexMdt):
        self.mandantid = indexMdt
        self.mappermodel_mdt = MandantEditmodel(indexMdt)
        self.mapper_mdt.setModel(self.mappermodel_mdt)
        self.add_mapping()
        self.mapper_mdt.toFirst()
        self.InternalFileStatus()
        self.AkquiseFileStatus()
        self.natPersonStatus()
        self.RVStatus()

    def fill_gwg(self):
        dlg = ComboDialog('Geldwäscheprüfung', 'Bitte Ergebnis der Prüfung nach Geldwäschegesetz auswählen', gwg)

        if dlg.exec():
            self.GeldwaescheGErg = dlg.combobox.currentText()
            gwg_index = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 19)
            self.mappermodel_mdt.setData(gwg_index, self.GeldwaescheGErg)

    def fill_staat(self):
        dlg = ComboDialog('Staat auswählen', 'Bitte den Staat des Sitzes auswählen', Staaten)


        if dlg.exec():
            self.block_b.sitz_staat = dlg.combobox.currentText()
            staat_index = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 13)
            self.mappermodel_mdt.setData(staat_index, self.block_b.sitz_staat)

    def fill_koll(self):
        dlg = ComboDialog('Kollisionsprüfung', 'Bitte Ergebnis der Kollisionsprüfung auswählen', kollisionspruefung)

        if dlg.exec():
            self.KollisionErg = dlg.combobox.currentText()
            kol_index = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 20)
            self.mappermodel_mdt.setData(kol_index, self.KollisionErg)

    def eventFilter(self, obj, event):
        if not self.block_a.NameMdt.isEnabled() == False:
            if event.type() == QEvent.Type.MouseButtonPress:
                if self.block_e.KollisionMdt is obj:
                    self.fill_koll()
                elif self.block_e.GeldwaescheG is obj:
                    self.fill_gwg()
                elif self.block_b.Sitz6 is obj:
                    self.fill_staat()

        return QWidget.eventFilter(self, obj, event)

    def addSearchfield(self, searchable: bool):

        if searchable == True:

            self.setDisabled(True)
        elif searchable == False:
            self.setDisabled(False)

    def InternalFileStatus(self):
        # function maps db-entry for "internal file" to checkbox;
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            InternalStatus = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 4).data(Qt.ItemDataRole.DisplayRole)

            if InternalStatus == True:
                self.block_a.Intern.setChecked(True)
            else:
                self.block_a.Intern.setChecked(False)

    def AkquiseFileStatus(self):
        # function maps db-entry for "akquise file" to checkbox;
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            akquiseStatus = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 5).data(Qt.ItemDataRole.DisplayRole)
            if akquiseStatus == True:
                self.block_a.Akquise.setChecked(True)
            else:
                self.block_a.Akquise.setChecked(False)

    def InternalStatusChange(self):
        # function checks if checkbox "intern" is checked and writes changes to db
        # first line re initialization before mappermodel_mdt is set
        InternalIndex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 4)

        if self.block_a.Intern.isChecked():
            self.mappermodel_mdt.setData(InternalIndex, True)
        else:
            self.mappermodel_mdt.setData(InternalIndex, False)

    def akquiseStatusChange(self):
        # function checks if checkbox "akquise" is checked and writes changes to db
        # first line re initialization before mappermodel_mdt is set
        akquiseIndex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 5)

        if self.block_a.Akquise.isChecked():
            self.mappermodel_mdt.setData(akquiseIndex, True)
        else:
            self.mappermodel_mdt.setData(akquiseIndex, False)


    def natPersonStatus(self):
        if not self.mapper_mdt.model() is None:
            self.natPersonStatusdata = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 28).data(Qt.ItemDataRole.DisplayRole)

            if self.natPersonStatusdata == True:
                self.block_c.GVcheck.setChecked(True)
            else:
                self.block_c.GVcheck.setChecked(False)

    def RVChange(self):
        ## see internalstatuschange and akquiseStatuschange
        RVIndex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 27)

        if self.block_f.Rahmenvertrag.isChecked():
            self.mappermodel_mdt.setData(RVIndex, True)
        else:
            self.mappermodel_mdt.setData(RVIndex, False)

    def RVStatus(self):
        # function maps db-entry for "Rahmenvertrag" to checkbox;
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            RVStatus = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 27).data(Qt.ItemDataRole.DisplayRole)

            if RVStatus == True:
                self.block_f.Rahmenvertrag.setChecked(True)
            else:
                self.block_f.Rahmenvertrag.setChecked(False)

    def write_gv(self):
        # write new person into humans
        self.newperson = 0
        self.block_gv.tab1.human_cleanup()

        # find index of newest person
        self.newperson = HumanSearch.result(HumanSearch())
        self.refresh_data(self.mandantid)
        # write newest person in mandanten as GV

        if not self.newperson == 0:
            gvindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 6)
            self.mappermodel_mdt.setData(gvindex, self.newperson)

            # cleanup and close adressbook
            self.block_gv.tab1.clearinput()
            self.block_gv.close()



    def write_re(self):
        self.newperson = 0
        # write new person into humans
        self.block_re.tab1.human_cleanup()

        # find index of newest person
        self.newperson = HumanSearch.result(HumanSearch())
        self.refresh_data(self.mandantid)

        # write newest person in mandanten as RE
        if not self.newperson == 0:
            REindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 7)
            self.mappermodel_mdt.setData(REindex, self.newperson)

            self.block_re.tab1.clearinput()
            self.block_re.close()

    def update_nat_person(self):
        natPersonIndex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 28)

        if self.block_c.GVcheck.isChecked():
            self.mappermodel_mdt.setData(natPersonIndex, True)

        elif not self.block_c.GVcheck.isChecked():
            self.mappermodel_mdt.setData(natPersonIndex, False)

    def add_gv(self):
        entry = self.block_gv.tab2.NrHuman
        print(entry)

        gvindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 6)
        self.mappermodel_mdt.setData(gvindex, entry)

        # cleanup and close adressbook
        self.block_gv.close()


    def add_re(self):
        entry = self.block_re.tab2.NrHuman
        reindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 7)
        self.mappermodel_mdt.setData(reindex, entry)

        # cleanup and close adressbook
        self.block_re.close()




class GrundDaten(QWidget):
    def __init__(self):
        super(GrundDaten, self).__init__()

        self.VBox = QVBoxLayout(self)
        self.HBox2 = QHBoxLayout()
        self.HBox3 = QHBoxLayout()
        self.HBox4 = QHBoxLayout()
        self.Titel = ArveLabel('header', 'Grunddaten')

        self.NameMdt = InputArve("Name bzw. Firma des Mandanten")
        self.NameMdt.setToolTip("Änderung nur durch Administrator")
        self.NameMdt.setBaseSize(350, 35)
        self.MdtNrLabel = ArveLabel("notice", "Mandantennummer:")
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)

        self.MdtNrLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.MdtNr = InputArve("Mandantennummer")
        self.MdtNr.setReadOnly(True)
        self.MdtNr.setStyleSheet(
            "border: 1px #8f8f91; border-radius:4px; background-color:rgb(241,241,241); color:darkred")


        self.MVP = InputArve("Mandantenverantwortlicher Partner")
        self.MVP.setToolTip("Änderung nur durch Administrator")
        self.MVP.setReadOnly(True)
        self.MVPLabel = ArveLabel("notice", "Mandantenverantwortlich:")
        self.MVPLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.AkquiseData = ''
        self.InternData = ''
        self.Intern = ArveCheck("Interner Mandant", False)
        self.Akquise = ArveCheck("Akquise - noch kein Mandatsvertrag", False)

        self.VBox.addWidget(self.Titel)

        self.VBox.addWidget(self.NameMdt)
        self.HBox2.addWidget(self.MdtNrLabel)
        self.HBox2.addWidget(self.MdtNr)
        self.HBox3.addWidget(self.MVPLabel)
        self.HBox3.addWidget(self.MVP)
        self.HBox4.addWidget(self.Intern)
        self.HBox4.addWidget(self.Akquise)
        self.VBox.addLayout(self.HBox2)
        self.VBox.addLayout(self.HBox3)
        self.VBox.addLayout(self.HBox4)
        self.VBox.addSpacerItem(self.spacerV)

class Sitz(QWidget):
    def __init__(self):
        super(Sitz, self).__init__()
        self.SitzLabel = ArveLabel("header", "Sitz des Mandanten")
        self.Sitz1 = InputArve("Straße")
        self.Sitz2 = InputArve("Hausnummer")
        self.Sitz2.adjustSize()
        self.Sitz3 = InputArve("PLZ")
        self.Sitz4 = InputArve("Ort")
        self.Sitz5 = InputArve("Bundesland")
        completer = QCompleter(Bundeslaender, self)
        self.Sitz5.setCompleter(completer)
        self.Sitz6 = InputArve("Staat")
        self.sitz_staat = ''
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)
        self.HBox = QHBoxLayout()

        self.HBox.addWidget(self.Sitz1, 2)
        self.HBox.addWidget(self.Sitz2, 1)

        self.VBox = QVBoxLayout(self)
        self.VBox.addWidget(self.SitzLabel)
        self.VBox.addLayout(self.HBox)
        self.VBox.addWidget(self.Sitz3)
        self.VBox.addWidget(self.Sitz4)
        self.VBox.addWidget(self.Sitz5)
        self.VBox.addWidget(self.Sitz6)
        self.VBox.addSpacerItem(self.spacerV)


class GesVertretung(QWidget):
    def __init__(self):
        super(GesVertretung, self).__init__()

        self.GVlabel = ArveLabel("header", "Gesetzliche Vertretung des Mandanten")
        self.GVdisplay = InputArve("Gesetzlicher Vertreter")

        self.GVdisplay.setReadOnly(True)
        self.GVPosition = InputArve("Position des gesetzlichen Vertreters")
        completer = QCompleter(Positionen, self)
        self.GVPosition.setCompleter(completer)
        self.GVcheck = ArveCheck("Mandant ist natürliche Person", False)

        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)

        self.GVVBox = QVBoxLayout(self)

        self.GVVBox.addWidget(self.GVlabel)
        self.GVVBox.addWidget(self.GVPosition)
        self.GVVBox.addWidget(self.GVdisplay)


        self.RE_display = InputArve("Rechnungsempfänger")
        self.RE_display.setReadOnly(True)

        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)


        self.elektr_rechnung = InputArve("Email-Adresse für Rechnung")


        self.GVVBox.addWidget(self.RE_display)

        self.GVVBox.addWidget(self.elektr_rechnung)
        self.GVVBox.addSpacerItem(self.spacerV)

class Berufsrecht(QWidget):
    def __init__(self):
        super(Berufsrecht, self).__init__()
        self.BerufsrechtLabel = ArveLabel("header", "Berufsrechtliche Sorgfalt")
        self.KollisionMdt = InputArve("Mandantenbezogene Kollision")
        self.KollisionMdt.setReadOnly(True)
        self.Kollision_hidden = InputArve('')
        self.KollisionMdt.installEventFilter(self)
        self.KollisionErg = ''
        self.GeldwaescheG = InputArve("Geldwäschegesetz")
        self.GeldwaescheG.setReadOnly(True)
        self.GeldwaescheG.installEventFilter(self)
        self.GeldwaescheGErg = ''
        self.VBox = QVBoxLayout(self)

        self.VBox.addWidget(self.BerufsrechtLabel)
        self.VBox.addWidget(self.KollisionMdt)
        self.VBox.addWidget(self.GeldwaescheG)
        #self.VBox.addWidget(self.Drittwirkung)
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)
        self.VBox.addSpacerItem(self.spacerV)


class Abrechnung(QWidget):
    def __init__(self):
        super(Abrechnung, self).__init__()
        limit = QRegularExpression("[0-9]*")
        limiter = QRegularExpressionValidator(limit)


        self.AbrechnungLabel1 = ArveLabel('header', 'Vergütung')
        self.Rahmenvertrag = ArveCheck('Rahmenvertrag', True)
        self.Stundensatz1 = InputArve("Stundensatz")
        self.Stundensatz1.setValidator(limiter)
        self.Stundensatz2 = InputArve("Stundensatz 2")
        self.Stundensatz2.setValidator(limiter)
        self.Stundensatz2.setDisabled(True)
        self.MVPAnteil = InputArve('Anteil des MVP in %')
        self.MVPAnteil.setValidator(limiter)
        self.SonstigesVerguetung = QTextEdit()
        self.SonstigesVerguetung.setFixedHeight(100)
        self.SonstigesVerguetung.setStyleSheet("background-color:rgb(241, 241, 241); border-radius:4px;")
        self.SonstigesVerguetung.setPlaceholderText("Anmerkungen zur Abrechnung")

        self.VBox = QVBoxLayout(self)
        self.VBox.addWidget(self.AbrechnungLabel1)
        self.VBox.addWidget(self.Rahmenvertrag)
        self.VBox.addWidget(self.Stundensatz1)
        self.VBox.addWidget(self.Stundensatz2)
        self.VBox.addWidget(self.MVPAnteil)
        self.VBox.addWidget(self.SonstigesVerguetung)