from src.MainLayout import *
from PyQt6.QtCore import QEvent
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

from src.InputHumans import Human, Human_Selection
from src.EditMdt import GrundDaten, Sitz, GesVertretung, Berufsrecht, Abrechnung # Options
from src.data import MandantEditmodel, MVP, HumanSearch
from src.variables import Jahr


class New_Mandant(ArvenWidget):
    def __init__(self):
        super(New_Mandant, self).__init__('not')
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.scrollSpace = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollGrid = QGridLayout(self.scrollWidget)
        self.scrollSpace.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scrollSpace)

        self.hbox_title = QHBoxLayout()
        self.title = ArveLabel('header', 'Neuen Mandanten anlegen')
        self.new_mvp = ComboArve("Mandantenverantwortlichen Partner auswählen")
        self.hbox_title.addWidget(self.title)
        self.hbox_title.addWidget(self.new_mvp)

        self.mdt_anlegen = ArvenButton("Neuen Mandanten anlegen")
        self.block_a = GrundDaten()
        self.block_a.MdtNr.setPlaceholderText("Wird automatisch vergeben")
        self.block_a.MVP.hide()
        self.block_a.MVPLabel.hide()
        self.block_b = Sitz()
        self.block_c = GesVertretung()
        self.block_e = Berufsrecht()
        self.block_f = Abrechnung()
        #self.block_g = Options()
        self.humanleash = ''
        self.block_n = Human_Selection(prozess="neu")
        self.block_m = Human_Selection(prozess="neu")

        self.scrollGrid.addLayout(self.hbox_title, 0, 0)
        self.scrollGrid.addWidget(self.block_a, 1, 0)
        self.scrollGrid.addWidget(self.block_b, 2, 0)
        self.scrollGrid.addWidget(self.block_c, 3, 0)
        self.scrollGrid.addWidget(self.block_e, 1, 1)
        self.scrollGrid.addWidget(self.block_f, 2, 1)
        #self.scrollGrid.addWidget(self.block_g, 3, 1)
        self.scrollGrid.addWidget(self.mdt_anlegen, 3, 1)
        self.RE = None
        self.GV = None


        self.mvp_model = MVP()
        self.set_mvp()
        self.noRE()
        self.nat_person()
        self.elektrRechnung()

        # signals
        self.block_c.AddToAdressBook.clicked.connect(self.ges_vertreter)
        self.block_c.REE_AddToAdressBook.clicked.connect(self.rechnungsempfaenger)
        self.mdt_anlegen.clicked.connect(self.warnings)
        self.block_m.tab1.block_a.ButtonAdd.clicked.connect(self.write_gv)
        self.block_n.tab1.block_a.ButtonAdd.clicked.connect(self.writeREE)
        self.block_c.GVcheck.stateChanged.connect(self.nat_person)
        self.block_c.REcheck.stateChanged.connect(self.noRE)
        self.block_c.elektr_rechnung_check.stateChanged.connect(self.elektrRechnung)

        self.scrollSpace.setWidget(self.scrollWidget)

    def set_mvp(self):
        self.new_mvp.setModel(self.mvp_model)
        self.new_mvp.setModelColumn(2)
        self.new_mvp.setCurrentIndex(-1)

    def ges_vertreter(self):
        self.block_m.tab1.block_a.Arbeitgeber.setText(self.block_a.NameMdt.text())
        self.block_m.tab1.block_a.Position.setText(self.block_c.GVPosition.text())
        self.block_m.tab1.block_a.Adresse1.setText(self.block_b.Sitz1.text())
        self.block_m.tab1.block_a.Adresse2.setText(self.block_b.Sitz2.text())
        self.block_m.tab1.block_a.PLZ.setText(self.block_b.Sitz3.text())
        self.block_m.tab1.block_a.Ort.setText(self.block_b.Sitz4.text())
        self.block_m.show()


    def warnings(self):
        if self.block_a.NameMdt.text() == '':
            dlg = ArvenDialog("Bitte Namen des neuen Mandanten eingeben",
                              f"""Bitte Namen des neuen Mandanten eingeben""")
            dlg.exec()
        elif self.new_mvp.currentIndex() == -1:
            dlg = ArvenDialog("Bitte mandantenverantwortlichen Partner angeben",
                              f"""Bitte einen mandantenverantwortlichen Partner angeben""")
            dlg.exec()
        else:
            self.new_mandant()

    def new_mandant(self):

        internal = True if self.block_a.Intern.isChecked() == True else False
        akquise = True if self.block_a.Akquise.isChecked() == True else False
        ges_vertreter = self.block_m.tab1.block_a.Nachname.text()
        rv = True if self.block_f.Rahmenvertrag.isChecked() == True else False
        mvp = self.mvp_model.record(self.new_mvp.currentIndex()).value(0)
        nat_person = True if self.block_c.GVcheck.isChecked() == True else False


        new_mandant = {'name' : self.block_a.NameMdt.text(), 'Anlagejahr' : Jahr, 'internal' :
                        internal, 'akquise' : akquise, 'sitz_strasse' : self.block_b.Sitz1.text(), 'sitz_hausnummer' : self.block_b.Sitz2.text(),
                       'sitz_plz' : self.block_b.Sitz3.text(), 'sitz_ort' : self.block_b.Sitz4.text(), 'sitz_bundesland' : self.block_b.Sitz5.text(),
                       'sitz_staat' : self.block_b.Sitz6.currentText(), 'rv' : rv, 'stundensatz1' : self.block_f.Stundensatz1.text(),
                        'stundensatz2' : self.block_f.Stundensatz2.text(), 'bemerkungen' : self.block_f.SonstigesVerguetung.toPlainText(),
                        'gwg' : self.block_e.GeldwaescheG.currentText(), 'koll' : self.block_e.KollisionMdt.currentText(),
                       'mvp' : mvp, 'mvp_anteil' : self.block_f.MVPAnteil.text(),   'gv_position' : self.block_c.GVPosition.text(),
                       'nat_person' : nat_person, 'elektr-rechnung' : self.block_c.elektr_rechnung.text(), 're' : self.RE, 'gv' : self.GV
                       }

        MandantModel = MandantEditmodel()
        MdtNr = MandantModel.addnew(new_mandant)
        if not MdtNr is None:
            dlg = ArvenDialog("Neuer Mandant erfolgreich angelegt", f"""Neuer Mandant {self.block_a.NameMdt.text()} hat die Mandantennummer {MdtNr}.""")
            dlg.exec()

        else:
            dlg = ArvenDialog("Fehler", f"""Neuer Mandant {self.block_a.NameMdt.text()} konnte nicht eingetragen werden. \n\n
                                Fehler: {MandantModel.lastError().text()}""")
            dlg.exec()


    def rechnungsempfaenger(self):
        self.block_n.tab1.block_a.Arbeitgeber.setText(self.block_a.NameMdt.text())
        self.block_n.tab1.block_a.Adresse1.setText(self.block_b.Sitz1.text())
        self.block_n.tab1.block_a.Adresse2.setText(self.block_b.Sitz2.text())
        self.block_n.tab1.block_a.PLZ.setText(self.block_b.Sitz3.text())
        self.block_n.show()

    def write_gv(self):
        # write new person into humans
        self.block_m.tab1.human_cleanup()

        # find index of newest person
        newperson = HumanSearch.result(HumanSearch())

        self.block_c.GVdisplay.setText(
            f"""{self.block_m.tab1.block_a.Nachname.text()}, {self.block_m.tab1.block_a.Vorname.text()}""")

        # write newest person in mandanten as RE
        self.GV = newperson

        self.block_m.close()

    def writeREE(self):
        # write new person into humans
        self.block_n.tab1.human_cleanup()

        # find index of newest person
        newperson = HumanSearch.result(HumanSearch())
        self.block_c.RE_display.setText(f"""{self.block_n.tab1.block_a.Nachname.text()}, {self.block_n.tab1.block_a.Vorname.text()}""")

        # write newest person in mandanten as RE
        self.RE = newperson

        self.block_n.close()

    def nat_person(self):
        # disable gv if mandant = nat person
        if not self.block_c.GVcheck.isChecked():
            self.block_c.AddToAdressBook.setDisabled(False)
        else:
            self.block_c.AddToAdressBook.setDisabled(True)
            self.block_c.GVPosition.setDisabled(True)
            self.block_c.GVdisplay.clear()
            self.GV = None

    def noRE(self):
        if self.block_c.REcheck.isChecked():
            self.block_c.REE_AddToAdressBook.setDisabled(False)
        else:
            self.block_c.REE_AddToAdressBook.setDisabled(True)
            self.block_c.RE_display.clear()
            self.RE = None

    def elektrRechnung(self):
        if not self.block_c.elektr_rechnung_check.isChecked():
            self.block_c.elektr_rechnung.setDisabled(True)
            self.block_c.elektr_rechnung.clear()
        else:
            self.block_c.elektr_rechnung.setDisabled(False)
