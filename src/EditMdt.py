from src.data import DBModelMdt, MandantEditmodel, MandantListe, GV_model, REE_model, HumanSearch
from src.MainLayout import *
from PyQt6.QtCore import QEvent, QRegularExpression
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

kollisionsprüfung = {"Kollisionsprüfung durch den mandantenverantwortlichen Partner ergebnislos" : 1,
                     "Kollisionen im weiteren Sinn denkbar; Annahme nach Rücksprache mit betroffenen Partnern" : 2,
                     "Kollision im berufsrechtlichen Sinn; Mandant wird abgelehnt" : 3}


class EditMdt(ArvenWidget):
    def __init__(self):
        super(EditMdt, self).__init__('not')
        self.setWindowTitle("Stammblatt Mandanten bearbeiten")

        self.new_search = ArveLabel('header', 'Mandanten verwalten')
        self.new_search.installEventFilter(self)

        # setup searchfield
        self.searchLayout = QVBoxLayout()
        self.searchLabel_mdt = ArveLabel('notice', "Bitte Mandanten auswählen...")
        self.searchLine_mdt = InputArve('hier eingeben')
        self.search_table = ArvenTable()
        self.search_model = MandantListe()
        self.search_table.setModel(self.search_model)
        self.search_table.setColumnHidden(1, True)

         # setup layout for searchfield
        self.searchLayout.addWidget(self.searchLabel_mdt)
        self.searchLayout.addWidget(self.searchLine_mdt)
        self.searchLayout.addWidget(self.search_table)

        # setup field for data-editing
        self.scrollSpace = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollGrid = QGridLayout(self.scrollWidget)
        self.scrollSpace.setWidgetResizable(True)

        self.block_a = GrundDaten()
        self.block_b = Sitz()
        self.block_c = GesVertretung()
        self.block_e = Berufsrecht()
        self.block_f = Abrechnung()
        #self.block_g = Options()
        self.humanleash = ''
        self.block_n = Human_Selection(prozess="neu")
        self.block_m = Human_Selection(prozess="neu")
        self.scrollGrid.addWidget(self.new_search, 0, 0)
        self.scrollGrid.addWidget(self.block_a, 1, 0)
        self.scrollGrid.addWidget(self.block_b, 2, 0)
        self.scrollGrid.addWidget(self.block_c, 3, 0)
        self.scrollGrid.addWidget(self.block_e, 1, 1)
        self.scrollGrid.addWidget(self.block_f, 2, 1)
        #self.scrollGrid.addWidget(self.block_g, 3, 1)

        # setup three QDataWidgetmappers and Models

        self.mapper_mdt = QDataWidgetMapper()
        self.mappermodel_mdt = MandantEditmodel('NULL')
        self.mapper_gv = QDataWidgetMapper()
        self.mappermodel_gv = GV_model('NULL')
        self.mapper_REE = QDataWidgetMapper()
        self.mappermodel_re = REE_model('NULL')
        self.add_mapping()

        self.MainHorizontalLayout = QHBoxLayout()

        self.setLayout(self.MainHorizontalLayout)

        ### SIGNALS
        self.searchLine_mdt.editingFinished.connect(self.filtermdt)
        self.search_table.doubleClicked.connect(self.indexmap_2)
        self.block_a.Intern.stateChanged.connect(self.InternalStatusChange)
        self.block_a.Akquise.stateChanged.connect(self.AkquiseStatusChange)
        self.block_c.REE_AddToAdressBook.clicked.connect(self.rechnungsempfaenger)
        self.block_n.tab1.block_a.ButtonAdd.clicked.connect(self.tetherRE)
        self.block_c.AddToAdressBook.clicked.connect(self.ges_vertreter)
        self.block_m.tab1.block_a.ButtonAdd.clicked.connect(self.tetherGV)
        self.block_c.GVcheck.stateChanged.connect(self.nat_person)
        self.block_c.REcheck.stateChanged.connect(self.no_re)
        self.block_c.elektr_rechnung_check.stateChanged.connect(self.elektr_RE)
        #self.block_g.MV_VV_ablage.stateChanged.connect(self.vv_mv_ablage_change)
        #self.block_g.MV_VV_versand.stateChanged.connect(self.vv_mv_sendung_change)
        self.block_f.Rahmenvertrag.stateChanged.connect(self.rahmenvertrag_change)

        self.addSearchfield(searchable=True)

        # must be last line of constructor
        self.scrollSpace.setWidget(self.scrollWidget)



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

    def add_extra_mapping(self):
        self.mapper_REE.addMapping(self.block_c.RE_display, 2)
        self.mapper_REE.addMapping(self.block_c.RE_blind, 1)
        self.mapper_gv.addMapping(self.block_c.GVblind, 26)
        self.mapper_gv.addMapping(self.block_c.GVdisplay, 2)

    def filtermdt(self):
        # function to filter mdt by input in search line
        self.search_model.filter_by_name(self.searchLine_mdt.text())
        print(self.search_model.lastError().text())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def indexmap_2(self, index):
    # central fork to change from searchfield to individual client.
        if not index.sibling(index.row(), 1).data() is None: # no client nr. = no client fields
            self.cur_index = index.sibling(index.row(), 1).data() # identify client nr.
            self.set_models()                                      # fetch data pertaining to client nr
            self.set_extra_models()                                 # fetch extra data re legal representative and bill
                                                                    # receiver
            self.addSearchfield(False)                              # unblock editable fields
        else:
            self.cur_index = ''                                     # don't crash if no client nr., retry
            self.searchLine_mdt.clear()


    def set_models(self):
        self.mappermodel_mdt = MandantEditmodel(self.cur_index)
        self.mapper_mdt.setModel(self.mappermodel_mdt)
        self.add_mapping()
        self.mapper_mdt.toFirst()

    def set_extra_models(self):
        self.gv_number = self.mappermodel_mdt.record(self.mapper_mdt.currentIndex()).value(6)
        self.re_number = self.mappermodel_mdt.record(self.mapper_mdt.currentIndex()).value(7)

        self.mappermodel_gv = GV_model(self.gv_number)
        self.mapper_gv.setModel(self.mappermodel_gv)
        self.mappermodel_re = REE_model(self.re_number)
        self.mapper_REE.setModel(self.mappermodel_re)

        #self.add_extra_mapping()
        self.mapper_gv.toFirst()
        self.mapper_REE.toFirst()

        self.InternalFileStatus()
        self.AkquiseFileStatus()
        self.elektr_re_status()
        self.no_re()
        #self.vv_mv_ablage()
        #self.vv_mv_sendung()
        self.rahmenvertrag()
        self.nat_person()

    def addSearchfield(self, searchable):
        if searchable == True:
            self.MainHorizontalLayout.addLayout(self.searchLayout, 1)
            self.MainHorizontalLayout.addWidget(self.scrollSpace, 3)
            self.new_search.setDisabled(True)
            self.block_a.setDisabled(True)
            self.block_b.setDisabled(True)
            self.block_c.setDisabled(True)
            self.block_e.setDisabled(True)
            self.block_f.setDisabled(True)

        if searchable == False:
            self.MainHorizontalLayout.removeItem(self.searchLayout)
            self.new_search.setDisabled(False)
            self.block_a.setDisabled(False)
            self.block_b.setDisabled(False)
            self.block_c.setDisabled(False)
            self.block_e.setDisabled(False)
            self.block_f.setDisabled(False)

    def eventFilter(self, obj, event):
        # switchboard = {'Mandanten verwalten' : EditMdt()}

        if event.type() == QEvent.Type.MouseButtonPress:
            if self.new_search is obj:
                self.addSearchfield(True)

        return QWidget.eventFilter(self, obj, event)




    def InternalStatusChange(self):
        #function checks if checkbox "intern" is checked and writes changes to db
        # first line re initialization before mappermodel_mdt is set
        InternalIndex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 4)

        if self.block_a.Intern.isChecked():
            self.mappermodel_mdt.setData(InternalIndex, True)
        else:
            self.mappermodel_mdt.setData(InternalIndex, False)

    def InternalFileStatus(self):
        # function maps db-entry for "internal file" to checkbox; todo: do this by QDataWidgetMapper?
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            InternalStatus = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 4).data(Qt.ItemDataRole.DisplayRole)

            if InternalStatus == True:
                self.block_a.Intern.setChecked(True)
            else:
                self.block_a.Intern.setChecked(False)

    def elektr_re_status(self):
        # function maps db-entry for "elektrr_rechnung" to checkbox;
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            elektr_rech_status = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 25).data(Qt.ItemDataRole.DisplayRole)

            if not elektr_rech_status == '':
                self.block_c.elektr_rechnung_check.setChecked(True)
            else:
                self.block_c.elektr_rechnung_check.setChecked(False)

    def AkquiseStatusChange(self):
        #function checks if checkbox "akquise" is checked and writes changes to db
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            akquiseindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 5)
            if self.block_a.Akquise.isChecked():
                self.mappermodel_mdt.setData(akquiseindex, True)
            else:
                self.mappermodel_mdt.setData(akquiseindex, False)

    def AkquiseFileStatus(self):
        # function maps db-entry for "akquise file" to checkbox; todo: do this by QDataWidgetMapper?
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            akquiseStatus = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 5).data(Qt.ItemDataRole.DisplayRole)
            if akquiseStatus == True:
                self.block_a.Akquise.setChecked(True)
            else:
                self.block_a.Akquise.setChecked(False)

    def ges_vertreter(self):
        self.block_m.tab1.block_a.Arbeitgeber.setText(self.block_a.NameMdt.text())
        self.block_m.tab1.block_a.Position.setText(self.block_c.GVPosition.text())
        self.block_m.tab1.block_a.Adresse1.setText(self.block_b.Sitz1.text())
        self.block_m.tab1.block_a.Adresse2.setText(self.block_b.Sitz2.text())
        self.block_m.tab1.block_a.PLZ.setText(self.block_b.Sitz3.text())
        self.block_m.tab1.block_a.Ort.setText(self.block_b.Sitz4.text())
        self.block_m.show()

    def rechnungsempfaenger(self):
        self.block_n.tab1.block_a.Arbeitgeber.setText(self.block_a.NameMdt.text())
        self.block_n.tab1.block_a.Adresse1.setText(self.block_b.Sitz1.text())
        self.block_n.tab1.block_a.Adresse2.setText(self.block_b.Sitz2.text())
        self.block_n.tab1.block_a.PLZ.setText(self.block_b.Sitz3.text())
        self.block_n.show()

    def tetherRE(self):
        # write new person into humans
        self.block_n.tab1.human_cleanup()

        # find index of newest person
        newperson = HumanSearch.result(HumanSearch())

        # write newest person in mandanten as RE
        self.mappermodel_mdt.setData(self.mappermodel_gv.index(self.mapper_mdt.currentIndex(), 7), newperson)

       # refresh models and mappers
        self.set_models()
        self.set_extra_models()

        self.block_n.tab1.clearinput()
        self.block_n.close()

    def tetherGV(self):
        # write new person into humans
        self.block_m.tab1.human_cleanup()

        # find index of newest person
        newperson = HumanSearch.result(HumanSearch())

        # write newest person in mandanten as GV
        self.mappermodel_mdt.setData(self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 6), newperson)

         # refresh models and mappers
        self.set_models()
        self.set_extra_models()

        self.block_m.tab1.clearinput()
        self.block_m.close()

    def nat_person(self):
        # disable gv if mandant = nat person
        if not self.block_c.GVcheck.isChecked():
            self.block_c.AddToAdressBook.setDisabled(False)
        else:
            self.block_c.AddToAdressBook.setDisabled(True)
            self.update_gv()

    def update_gv(self):
        # if gv is existant and mandant is set to be nat. person
        dlg = ArvenDialog("Gesetzlichen Vertreter löschen", "Der gesetzliche Vertreter wird endgültig gelöscht. \n\n(Der Eintrag"               
                                                            " im Adressbuch bleibt bestehen und \nkann jederzeit wieder mit dem Mandanten"      
                                                            " verknüpft werden.)")
        if dlg.exec():
            gv_check = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 6).data(Qt.ItemDataRole.DisplayRole)
            if self.block_c.GVcheck.isChecked():
                if not gv_check == '':
                    if self.mappermodel_mdt.setData(self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 6), None):
                       # self.set_extra_models()
                        self.block_c.GVdisplay.clear()

    def no_re(self):
        # disable re if no separate rechnungsempfänger
        if self.block_c.REcheck.isChecked():
            self.block_c.REE_AddToAdressBook.setDisabled(False)
        else:
            self.block_c.REE_AddToAdressBook.setDisabled(True)
            self.update_re()

    def update_re(self):
        # if re is existant and mandant is checked as no abw. ree
        dlg = ArvenDialog("Persönlichen Rechnungsempfänger löschen",
                          "Der abweichende Rechnungsempfänger wird endgültig gelöscht. \n\n(Der Eintrag"
                          " im Adressbuch bleibt bestehen und \nkann jederzeit wieder mit dem Mandanten"
                          " verknüpft werden.)")
        if dlg.exec():
            re_check = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 7).data(Qt.ItemDataRole.DisplayRole)
            print(re_check)
            if not self.block_c.GVcheck.isChecked():
                if not re_check == '':
                    if self.mappermodel_mdt.setData(self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 7),
                                                    None):
                        self.set_extra_models()
                        self.block_c.RE_display.clear()

    def elektr_RE(self):
        if not self.block_c.elektr_rechnung_check.isChecked():
            self.block_c.elektr_rechnung.setDisabled(True)
            self.update_elektr_RE()
        else:
            self.block_c.elektr_rechnung.setDisabled(False)

    def update_elektr_RE(self):
        dlg = ArvenDialog("Adresse für elektronischen Rechnungsempfang löschen",
                          "Die E-Mailadresse wird endgültig gelöscht. \n\n(Dieser Vorgang "
                          "kann nicht rückgängig gemacht werden.)")
        if dlg.exec():
            self.rech_check = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 25).data(Qt.ItemDataRole.DisplayRole)
            if not self.block_c.elektr_rechnung_check.isChecked():
                if not self.rech_check == '':
                    if self.mappermodel_mdt.setData(self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 25), None):
                        self.set_extra_models()
                        self.block_c.elektr_rechnung.clear()

    #def vv_mv_sendung_change(self):
    #    # function checks if checkbox "mv_vv versendet" is checked and writes changes to db
    #    # first line re initialization before mappermodel_mdt is set
    #    if not self.mapper_mdt.model() is None:
    #        mv_versandindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 18)
    #        if self.block_g.MV_VV_versand.isChecked():
    #            self.mappermodel_mdt.setData(mv_versandindex, True)
    #        else:
    #            self.mappermodel_mdt.setData(mv_versandindex, False)
    #
    #def vv_mv_sendung(self):
    #    # function maps db-entry for "mv/vv versendet" to checkbox;
    #    # first line re initialization before mappermodel_mdt is set
    #    if not self.mapper_mdt.model() is None:
    #        mv_vv_status = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 18).data(Qt.ItemDataRole.DisplayRole)
    #        if mv_vv_status == True:
    #            self.block_g.MV_VV_versand.setChecked(True)
    #        else:
    #            self.block_g.MV_VV_versand.setChecked(False)

    #def vv_mv_ablage_change(self):
    #    # function checks if checkbox "mv_vv abgelegt" is checked and writes changes to db
    #    # first line re initialization before mappermodel_mdt is set
    #    if not self.mapper_mdt.model() is None:
    #        mv_ablageindex = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 19)
    #        if self.block_g.MV_VV_ablage.isChecked():
    #            self.mappermodel_mdt.setData(mv_ablageindex, True)
    #        else:
    #            self.mappermodel_mdt.setData(mv_ablageindex, False)
    #
    #def vv_mv_ablage(self):
    #    # function maps db-entry for "mv/vv abgelegt" to checkbox;
    #    # first line re initialization before mappermodel_mdt is set
    #    if not self.mapper_mdt.model() is None:
    #        mv_vv_ablagestatus = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 19).data(
    #            Qt.ItemDataRole.DisplayRole)
    #        if mv_vv_ablagestatus == True:
    #            self.block_g.MV_VV_ablage.setChecked(True)
    #        else:
    #            self.block_g.MV_VV_ablage.setChecked(False)

    def rahmenvertrag_change(self):
        # function checks if checkbox "rahmenvertrag" is checked and writes changes to db
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            rahmenvertrag_index = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 28)
            if self.block_f.Rahmenvertrag.isChecked():
                self.mappermodel_mdt.setData(rahmenvertrag_index, True)
            else:
                self.mappermodel_mdt.setData(rahmenvertrag_index, False)

    def rahmenvertrag(self):
        # function maps db-entry for "mv/vv abgelegt" to checkbox;
        # first line re initialization before mappermodel_mdt is set
        if not self.mapper_mdt.model() is None:
            rahmenvertrag_status = self.mappermodel_mdt.index(self.mapper_mdt.currentIndex(), 28).data(
                Qt.ItemDataRole.DisplayRole)
            if rahmenvertrag_status == True:
                self.block_f.Rahmenvertrag.setChecked(True)
            else:
                self.block_f.Rahmenvertrag.setChecked(False)

    def refreshmodels(self):
        self.mappermodel_mdt.select()
        self.search_model = MandantListe()
        self.mappermodel_gv.select()
        self.mappermodel_re.select()

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
        self.KollisionMdt = ComboArve("Mandantenbezogene Kollision")
        self.GeldwaescheG = ComboArve("Geldwäschegesetz")
        #self.Drittwirkung = ComboArve("Schutzwirkung zugunsten Dritter (Konzernunternehmen)")

        self.VBox = QVBoxLayout(self)

        self.VBox.addWidget(self.BerufsrechtLabel)
        self.VBox.addWidget(self.KollisionMdt)
        self.VBox.addWidget(self.GeldwaescheG)
        #self.VBox.addWidget(self.Drittwirkung)
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)
        self.VBox.addSpacerItem(self.spacerV)
        self.fill_gwg()
        self.fill_koll()

    def fill_gwg(self):
        for key, value in gwg.items():
            self.GeldwaescheG.addItem(key)

    def fill_koll(self):
        for key, value in kollisionsprüfung.items():
            self.KollisionMdt.addItem(key)


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

#class Options(QWidget):
#    def __init__(self):
#        super(Options, self).__init__()
#
#        self.title = ArveLabel("header", "Optionen")
#        self.MVneu = ArvenButton("Mandatsvertrag erstellen")
#        self.VVneu = ArvenButton("Vergütungsvereinbarung erstellen")
#        self.MV_VV_versand = ArveCheck("Mandatsvertrag und Vergütungsvereinbarung versendet", False)
#        self.MV_VV_ablage = ArveCheck("Mandatsvertrag und Vergütungsvereinbarung unterschrieben abgelegt", False)
#        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
#                                   vPolicy=QSizePolicy.Policy.Expanding)
#        self.VBox = QVBoxLayout(self)
#        self.VBox.addWidget(self.title)
#        self.VBox.addWidget(self.MVneu)
#        self.VBox.addWidget(self.VVneu)
#        self.VBox.addWidget(self.MV_VV_versand)
#        self.VBox.addWidget(self.MV_VV_ablage)
#        self.VBox.addSpacerItem(self.spacerV)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

class ReadOnlyDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        lb = QLabel(parent)
        return lb

