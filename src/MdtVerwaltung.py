from src.data import DBModelMdt, MandantEditmodel, MandantListe, GV_model, REE_model, HumanSearch
from src.MainLayout import *
from PyQt6.QtCore import QEvent, QRegularExpression, QVariantAnimation
from PyQt6.QtGui import QRegularExpressionValidator
import PyQt6.QtSql

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
                             QFrame,
                             QDataWidgetMapper,
                             QComboBox, QItemDelegate
                            )

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex
from src.InputHumans import Human, Human_Selection

Anreden = ["Frau", "Herr", "Frau Dr.", "Herr Dr.", "Frau Prof. Dr.", "Herr Prof. Dr."]
Positionen = ["Geschäftsführerin", "Geschäftsführer", "Mitglied des Vorstands"]
Bundeslaender = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg',
                 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen',
                 'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
Staaten = ["Deutschland", "EU (außer Deutschland)", "Außerhalb EU"]

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

        ## widgets
        self.new_search = ArveLabel('header', 'Mandanten verwalten')
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

        # init functions
        self.addSearchfield(True)

    def filtermdt(self):
        self.searchfield.search_model.filter_by_name(self.searchfield.searchLine_mdt.text())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def indexmap_2(self, index):
        # central fork to change from searchfield to individual client.
        if not index.sibling(index.row(), 1).data() is None:  # no client nr. = no client fields
            self.cur_index = index.sibling(index.row(), 1).data()  # identify client nr.
            self.editfield.refresh_data(self.cur_index)
            self.slide_search('out')

         # fetch data pertaining to client nr
        # fetch extra data re legal representative and bill
            # receiver

            #self.addSearchfield(False)  # unblock editable fields
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

        return QWidget.eventFilter(self, obj, event)

    def addSearchfield(self, searchable:bool):
        if searchable == True:
            for i in self.editfield.children():
                if isinstance(i, InputArve | ComboArve | ArveCheck | ArveLabel | ArvenButton):
                    i.setDisabled(True)
        elif searchable == False:
            for i in self.editfield.children():
                if isinstance(i, InputArve | ComboArve | ArveCheck | ArveLabel | ArvenButton):
                    i.setDisabled(False)



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

        self.setObjectName('EditfieldMandanten')
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.scrollSpace = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollGrid = QGridLayout(self.scrollWidget)
        self.scrollSpace.setWidgetResizable(True)

        self.block_a = GrundDaten()
        self.block_b = Sitz()
        self.block_c = GesVertretung()
        self.block_e = Berufsrecht()
        self.block_f = Abrechnung()
        # self.block_g = Options()
        self.humanleash = ''
        self.block_n = Human_Selection(prozess="neu")
        self.block_m = Human_Selection(prozess="neu")

        self.scrollGrid.addWidget(self.block_a, 1, 0)
        self.scrollGrid.addWidget(self.block_b, 2, 0)
        self.scrollGrid.addWidget(self.block_c, 3, 0)
        self.scrollGrid.addWidget(self.block_e, 1, 1)
        self.scrollGrid.addWidget(self.block_f, 2, 1)

        self.mapper_mdt = QDataWidgetMapper()
        self.mappermodel_mdt = MandantEditmodel('NULL')

        self.add_mapping()

        self.layouting = QVBoxLayout()
        self.setLayout(self.layouting)
        self.layouting.addWidget(self.scrollSpace)
        self.scrollSpace.setWidget(self.scrollWidget)
        self.scrollSpace.setWidgetResizable(True)


    def add_mapping(self):
        self.mapper_mdt.addMapping(self.block_a.NameMdt, 1)
        self.mapper_mdt.addMapping(self.block_a.MdtNr, 22)
        self.mapper_mdt.addMapping(self.block_a.MVP, 3)
        self.mapper_mdt.addMapping(self.block_b.Sitz1, 8)
        self.mapper_mdt.addMapping(self.block_b.Sitz2, 9)
        self.mapper_mdt.addMapping(self.block_b.Sitz3, 10)
        self.mapper_mdt.addMapping(self.block_b.Sitz4, 11)
        self.mapper_mdt.addMapping(self.block_b.Sitz5, 12)
        self.mapper_mdt.addMapping(self.block_b.Sitz5, 13)
        self.mapper_mdt.addMapping(self.block_c.GVPosition, 24)
        self.mapper_mdt.addMapping(self.block_c.GVdisplay, 6)
        self.mapper_mdt.addMapping(self.block_c.elektr_rechnung, 25)
        self.mapper_mdt.addMapping(self.block_e.GeldwaescheG, 20)

    def refresh_data(self, indexMdt):
        self.mappermodel_mdt = MandantEditmodel(indexMdt)
        self.mapper_mdt.setModel(self.mappermodel_mdt)
        self.add_mapping()
        self.mapper_mdt.toFirst()




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
        self.Sitz6 = ComboArve("Staat")
        self.Sitz6.addItems(Staaten)
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
        self.GVblind = InputArve('')

        self.GVdisplay.setReadOnly(True)
        self.GVPosition = InputArve("Position des gesetzlichen Vertreters")
        completer = QCompleter(Positionen, self)
        self.GVPosition.setCompleter(completer)
        self.GVcheck = ArveCheck("Mandant ist natürliche Person", False)
        #self.GVcheck.stateChanged.connect(self.nat_person)
        self.AddToAdressBook = ArvenButton("Adressbuch")
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)

        self.GVVBox = QVBoxLayout(self)

        self.GVVBox.addWidget(self.GVlabel)
        self.GVVBox.addWidget(self.GVcheck)
        self.GVVBox.addWidget(self.GVPosition)
        self.GVVBox.addWidget(self.GVdisplay)
        self.GVVBox.addWidget(self.AddToAdressBook)

        self.REcheck = ArveCheck("Persönlicher Rechnungsempfänger", True)
        self.RE_display = InputArve("Rechnungsempfänger")
        self.RE_display.setReadOnly(True)
        self.RE_blind = QComboBox()
        self.REE_AddToAdressBook = ArvenButton("Adressbuch")
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)

        self.elektr_rechnung_check = ArveCheck("Elektronische Rechnung", False)
        self.elektr_rechnung = InputArve("Email-Adresse für Rechnung")

        self.GVVBox.addWidget(self.REcheck)
        self.GVVBox.addWidget(self.RE_display)
        self.GVVBox.addWidget(self.REE_AddToAdressBook)
        self.GVVBox.addWidget(self.elektr_rechnung_check)
        self.GVVBox.addWidget(self.elektr_rechnung)
        self.GVVBox.addSpacerItem(self.spacerV)

class Berufsrecht(QWidget):
    def __init__(self):
        super(Berufsrecht, self).__init__()
        self.BerufsrechtLabel = ArveLabel("header", "Berufsrechtliche Sorgfalt")
        self.KollisionMdt = InputArve("Mandantenbezogene Kollision")
        self.KollisionMdt.setReadOnly(True)
        self.KollisionMdt.installEventFilter(self)
        self.KollisionErg = ''
        self.GeldwaescheG = InputArve("Geldwäschegesetz")
        self.GeldwaescheG.setReadOnly(True)
        self.GeldwaescheG.installEventFilter(self)
        self.GeldwaescheGErg = ''
        #self.Drittwirkung = ComboArve("Schutzwirkung zugunsten Dritter (Konzernunternehmen)")
        #self.installEventFilter(self)
        self.VBox = QVBoxLayout(self)

        self.VBox.addWidget(self.BerufsrechtLabel)
        self.VBox.addWidget(self.KollisionMdt)
        self.VBox.addWidget(self.GeldwaescheG)
        #self.VBox.addWidget(self.Drittwirkung)
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)
        self.VBox.addSpacerItem(self.spacerV)


    def fill_gwg(self):
        dlg = ComboDialog('Geldwäscheprüfung', 'Bitte Ergebnis der Prüfung nach Geldwäschegesetz auswählen', gwg)

        if dlg.exec():
            self.GeldwaescheGErg = dlg.combobox.currentText()
            self.GeldwaescheG.setText(self.GeldwaescheGErg)

    def fill_koll(self):
        dlg = ComboDialog('Kollisionsprüfung', 'Bitte Ergebnis der Kollisionsprüfung auswählen', kollisionspruefung)

        if dlg.exec():
            self.KollisionErg = dlg.combobox.currentText()
            self.KollisionMdt.setText(self.KollisionErg)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if self.KollisionMdt is obj:
                self.fill_koll()
            elif self.GeldwaescheG is obj:
                self.fill_gwg()

        return QWidget.eventFilter(self, obj, event)



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