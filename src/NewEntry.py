from src.MainLayout import *
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QHBoxLayout, QDateEdit, QAbstractItemDelegate,  QDataWidgetMapper
from PyQt6.QtSql import QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel
from src.variables import *
from PyQt6.QtCore import Qt

from src.data import Leistungen, PreviousEntriesFileProxy
from src.config import currentConfig
from src.data import LeistungenTableModel
from src.auxiliary_gui import EmptyDelegate, CheckBoxDelegateQt, BooleanDelegateII, QTableviewEditableDelegate, CheckBoxDelegate




class NewTimeEntry(ArvenWidget):
    def __init__(self, file, az, mdt, auftrag, parent=None):
        super(NewTimeEntry, self).__init__('not')

        self.setMinimumSize(600, 400)

        self.setStyleSheet("background-color: white")
        self.setWindowTitle(f"""{mdt}: {az}""")

        self.file = file
        self.az = InputArve('Aktenzeichen')
        self.mdt = InputArve('Mandant')
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.mdt)
        self.hbox1.addWidget(self.az)


        self.Akte = InputArve('Auftrag')
        self.leistungsbeschreibung = QTextEdit(parent=self)
        self.leistungsbeschreibung.setStyleSheet("border-color:lightgray; border-style: solid; "
                                                 "border-radius: 4px; border-width:1px")

        self.label_day = ArveLabel("header", "Datum der Leistung")

        self.day_selection = ArvenDate()

        self.day_selection.setMinimumDate(firstpreviousM)

        self.day_selection.setMaximumDate(today_date)

        self.day_selection.setDate(today_date)

        self.label_duration = ArveLabel("header", "Dauer der Leistung")

        self.duration = ComboArve("Dauer")

        self.duration.setMaxVisibleItems(8)

        self.billable = ArveCheck("abrechenbar?", True)

        self.label_description = ArveLabel("header", "Beschreibung der Leistung")

        self.erfassen = ArvenButton("Leistung erfassen")

        self.erfassen.clicked.connect(self.leistungserfassung)



        self.previous = ArvenButton("Vorherige Einträge in dieser Akte")

        self.previous.clicked.connect(self.show_previous)

        self.az.setText(az)
        self.az.setReadOnly(True)
        self.mdt.setText(mdt)
        self.mdt.setReadOnly(True)
        self.Akte.setText(auftrag)
        self.Akte.setReadOnly(True)

        self.HBox = QHBoxLayout()
        self.VBox = QVBoxLayout()
        self.setLayout(self.HBox)

        self.VBox.addLayout(self.hbox1)
        self.VBox.addWidget(self.Akte)

        self.VBox.addWidget(self.label_day)
        self.VBox.addWidget(self.day_selection)
        self.VBox.addWidget(self.billable)
        self.VBox.addWidget(self.label_duration)
        self.VBox.addWidget(self.duration)
        self.VBox.addWidget(self.label_description)
        self.VBox.addWidget(self.leistungsbeschreibung)
        self.VBox.addWidget(self.erfassen)
        self.VBox.addWidget(self.previous)

        self.HBox.addLayout(self.VBox)

        self.fillduration()


    def fillduration(self):
        for key, value in intervalls15.items():
            self.duration.addItem(key, value)

    def leistungserfassung(self):
        self.ra = currentConfig.getcurrent_ra(currentConfig())
        self.lbeschreibung = self.leistungsbeschreibung.toPlainText()
        idx = self.duration.currentIndex()

        self.minutes = self.duration.itemData(idx)
        if self.billable.isChecked() == False:
            self.abrb = 0
        else:
            self.abrb = 1
        self.ldatum = self.day_selection.date().toPyDate().isoformat()
        self.stamp = datetime.now().isoformat()
        self.packet = {"file": self.file, "ra": self.ra, "lbeschreibung": self.lbeschreibung, "duration": self.minutes,
                       "l_datum": self.ldatum, "abrb": self.abrb, "stamp": self.stamp}

        Leistungen.leistungserfassung(Leistungen(), **self.packet)
        self.duration.setCurrentIndex(-1)
        self.leistungsbeschreibung.clear()
        self.billable.setChecked(True)

    def show_previous(self):
        self.korrektur = MyPreviousEntries(self.file)
        self.korrektur.show()


class MyPreviousEntries(ArvenWidget):
    def __init__(self, file):
        super(MyPreviousEntries, self).__init__('not')
        self.setStyleSheet("background-color: white")
        self.ra = currentConfig.getcurrent_ra(currentConfig())

        self.setMinimumSize(1000,800)
        self.setWindowTitle(f"""Vorherige Einträge""")
        self.warningtext = ArveLabel("notice", "Frühere Einträge können hier direkt angepasst werden")
        self.warningtext.setStyleSheet("color: darkred;")

        self.prev_entries = ArvenTable()
        self.prev_entries.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.prev_entries.setEditTriggers(QTableView.EditTrigger.AllEditTriggers)
        self.model = LeistungenTableModel()
        self.model.setTable("arvensteyn_dev22.leistungen")
        self.model.setJoinMode(QSqlRelationalTableModel.JoinMode.InnerJoin)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.model.setRelation(12, QSqlRelation("arvensteyn_dev22.auftraege", "id", "az"))
        #selfmodel.setRelation(2, QSqlRelation("arvensteyn_dev22.mandanten", "mandantid", "name"))
        self.model.setRelation(1, QSqlRelation("arvensteyn_dev22.mitglieder", "mitgliedernr", "mitglied"))
        filter = f"""arvensteyn_dev22.leistungen.ra = {self.ra} AND arvensteyn_dev22.leistungen.auftrag = {file}"""
        self.model.setFilter(filter)
        self.model.select()

        self.prev_entries.setModel(self.model)
        for i in range(14):
            self.prev_entries.setColumnHidden(i, True)
        visible = [2, 4, 5, 13]
        for i in visible:
            self.prev_entries.setColumnHidden(i, False)
        self.prev_entries.horizontalHeader().moveSection(2,0)
        self.prev_entries.horizontalHeader().moveSection(0, 1)
        self.prev_entries.horizontalHeader().moveSection(1, 2)
        self.prev_entries.setColumnWidth(2, 600)
        self.prev_entries.setColumnWidth(4, 100)
        self.prev_entries.setColumnWidth(5, 200)
        self.prev_entries.setColumnWidth(13, 50)
        self.prev_entries.resizeRowsToContents()
        self.prev_entries.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.prev_entries.horizontalHeader().show()
        self.prev_entries.horizontalHeader().setStyleSheet("background-color:lightgray")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Leistungsbeschreibung")
        self.model.setHeaderData(5, Qt.Orientation.Horizontal, "Tag der Leistung")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Dauer")
        self.model.setHeaderData(13, Qt.Orientation.Horizontal, "€")




        self.HBox = QHBoxLayout(self)
        self.vbox = QVBoxLayout()

        self.VBox = QVBoxLayout()

        self.VBox.addWidget(self.warningtext)
        self.VBox.addWidget(self.prev_entries)
        self.HBox.addLayout(self.VBox, 2)
