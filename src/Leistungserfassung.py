from src.MainLayout import *
from PyQt6.QtWidgets import (QVBoxLayout,
                             QHBoxLayout,
                             QTableView,
                             QAbstractItemView,
                             QScrollArea,
                             QCalendarWidget,
                             QTextEdit,
                             QSpinBox)



from src.config import currentConfig
from src.data import Leistungen, PreviousEntriesFileProxy

from src.auxiliary_gui import EmptyDelegate
from src.variables import *

delegate = EmptyDelegate()



class New_Entry(ArvenWidget):
    def __init__(self, file=None, az=None, mdt=None, auftrag=None, parent=None):
        super(New_Entry, self).__init__("not")

        # variables
        self.file = file
        self.az = az
        self.mdt = mdt
        self.auftrag = auftrag


        # window
        self.setWindowTitle("Arvensteyn - Leistungserfassung")
        self.setObjectName('Leistungserfassung')


        # buttons



        self.block_a = EntryWidgets()
        self.block_a.setParent(self)
        self.block_b = PreviousEntriesToFile(file=self.file)

        self.MainHBox = QHBoxLayout()
        self.MainHBox.addWidget(self.block_b)
        self.MainHBox.addWidget(self.block_a)

        self.block_a.az.setText(self.az)
        self.block_a.mdt.setText(self.mdt)
        self.block_a.auftragsbezeichnung.setText(self.auftrag)

        self.MainVerticalLayout = QVBoxLayout()
        self.setLayout(self.MainVerticalLayout)
        self.MainVerticalLayout.addLayout(self.MainHBox)
        self.MainVerticalLayout.addLayout(self.block_a.vbox2)

        self.block_a.description.setStyleSheet("border-color:lightgray; border-style: solid; border-radius:4px;"
                                                        " border-width:1px")
        self.block_a.erfassen.clicked.connect(self.leistungserfassung)

    def closing(self):
        self.close()

    def leistungserfassung(self):
        self.ra = currentConfig.getcurrent_ra(currentConfig())
        self.lbeschreibung = self.block_a.description.toPlainText()
        idx = self.block_a.duration.currentIndex()

        self.minutes = self.block_a.duration.itemData(idx)
        if self.block_a.billable.isChecked() == False:
            self.abrb = False
        else:
            self.abrb = True
        self.ldatum = self.block_a.day_selection.date().toPyDate().isoformat()
        self.stamp = datetime.now().isoformat()
        self.packet = {"file": self.file, "ra": self.ra, "lbeschreibung": self.lbeschreibung, "duration": self.minutes,
                       "l_datum": self.ldatum, "abrb": self.abrb, "stamp": self.stamp}

        Leistungen.leistungserfassung(Leistungen(), **self.packet)
        self.block_a.duration.setCurrentIndex(-1)
        self.block_a.description.clear()
        self.block_a.billable.setChecked(True)


class PreviousEntriesToFile(ArvenWidget):
    def __init__(self, file):
        self.file = file
        super(PreviousEntriesToFile, self).__init__("not")
        self.title = ArveLabel("header", "Vorherige Einträge in dieser Akte")
        self.file_entries = ArvenTable()

        self.file_entries.setStyleSheet("border-style: solid; border-radius: 4px; border-color: lightgray")
        model = PreviousEntriesFileProxy(file=self.file)
        self.file_entries.setModel(model)
        for i in range(0, 14):
            self.file_entries.setColumnHidden(i, True)
        self.file_entries.setColumnHidden(5, False)
        self.file_entries.setColumnHidden(4, False)
        self.file_entries.setColumnHidden(1, False)
        self.file_entries.verticalHeader().hide()
        self.file_entries.horizontalHeader().setStretchLastSection(True)
        self.file_entries.horizontalHeader().hide()
        self.file_entries.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.file_entries.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.file_entries.setWordWrap(True)


        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.title)
        self.VBox.addWidget(self.file_entries)
        self.setLayout(self.VBox)


class EntryWidgets(ArvenWidget):
    def __init__(self):
        super(EntryWidgets, self).__init__("not")

        self.titel = ArveLabel("header", "Neue Leistung erfassen")
        self.space = ArveLabel("header", "")
        self.mdt = InputArve("Mandant")
        self.mdt.setReadOnly(True)
        self.az = InputArve("Aktenzeichen")
        self.az.setReadOnly(True)
        self.auftragsbezeichnung = InputArve("Auftragsbezeichnung")
        self.auftragsbezeichnung.setReadOnly(True)
        self.label_day = ArveLabel("header", "Datum der Leistung")
        self.day_selection = ArvenDate()

        self.day_selection.setDisplayFormat("dddd, dd. MMMM yyyy")
        self.day_selection.setMinimumDate(firstpreviousM)
        self.day_selection.setMaximumDate(today_date)

        self.label_duration = ArveLabel("header", "Dauer der Leistung")
        self.duration = ComboArve("Dauer")
        self.duration.setMaxVisibleItems(8)

        self.billable = ArveCheck("abrechenbar?", True)
        self.label_description = ArveLabel("header", "Beschreibung der Leistung")
        self.description = QTextEdit()

        self.erfassen = ArvenButton("Leistung erfassen")

        # entry-widgets in vbox (if needed in nested hboxes)
        self.VBox = QVBoxLayout()
        self.HBox1 = QHBoxLayout()
        self.HBox2 = QHBoxLayout()
        self.HBox3 = QHBoxLayout()
        self.HBox4 = QHBoxLayout()
        self.HBox5 = QHBoxLayout()
        self.HBox6 = QHBoxLayout()
        self.HBox7 = QHBoxLayout()

        # vbox in scrollspace
        self.scrollSpace = QScrollArea()
        self.scrollSpace.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollSpace.setWidget(self.scrollWidget)
        self.scrollGrid = QHBoxLayout(self.scrollWidget)

        self.canvas()

    def canvas(self):
        self.VBox.addWidget(self.titel)
        self.HBox1.addWidget(self.mdt)
        self.HBox1.addWidget(self.az)
        self.VBox.addLayout(self.HBox1)
        self.VBox.addWidget(self.auftragsbezeichnung)
        self.VBox.addWidget(self.space)
        self.HBox2.addWidget(self.label_day)
        self.HBox2.addWidget(self.day_selection)
        self.HBox2.addSpacerItem(self.spacerH)
        self.HBox2.addWidget(self.label_duration)
        self.HBox2.addWidget(self.duration)
        self.VBox.addLayout(self.HBox2)
        self.VBox.addWidget(self.billable)
        self.VBox.addWidget(self.space)
        self.VBox.addWidget(self.erfassen)

        self.scrollGrid.addSpacerItem(self.spacerH)
        self.scrollGrid.addLayout(self.VBox)
        # self.scrollGrid.addSpacerItem((self.spacerH))

        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.label_description)
        self.vbox2.addWidget(self.description)
        self.vbox2.addWidget(self.space)
        self.vbox2.addSpacerItem(self.spacerH)

        self.setLayout(self.scrollGrid)
        self.fillduration()

    def fillduration(self):
        for key, value in intervalls15.items():
            self.duration.addItem(key, value)
