from PyQt6.QtSql import (QSqlDatabase,
                         QSqlRelationalTableModel,
                         QSqlRelation,
                         QSqlRelationalDelegate,
                         QSqlTableModel,
                         QSqlDriver,
                         QSqlQuery,
                         QSqlRecord,
                         QSqlQueryModel
                         )

from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression, QVariant, QModelIndex
from src.config import currentConfig, Anmeldung
from src.db import dbopen


db = dbopen()

class MitarbeiterCred(QSqlTableModel):
    def __init__(self):
        super(MitarbeiterCred, self).__init__()
        self.setTable('arvensteyn_dev22.mitglieder')
        self.select()

        self.role = ''
        self.setSort(0, Qt.SortOrder.AscendingOrder)

    def checkKey(self, Mitglied):
        query1 = QSqlQuery()
        query1.exec(
            f"""SELECT mitgliedernr, beruf, role FROM arvensteyn_dev22.mitglieder WHERE mitglied = '{Mitglied}';""")

        while query1.next():
            self.Beruf = query1.value('beruf')
            self.role = query1.value('role')
            self.ID = query1.value('mitgliedernr')
            Anmeldung(ID=self.ID, Kopfzeile=Mitglied, Role=self.role, Profession=self.Beruf)


    def checkpass(self, Mitglied, PW):
        query2 = QSqlQuery()
        query2.exec(f"""SELECT mitgliedernr 
                          FROM arvensteyn_dev22.mitglieder
                         WHERE mitglied = '{Mitglied}'
                           AND auth = crypt('{PW}', auth);""")
        print(query2.lastQuery())

        if query2.record().count() == 1:
            print(query2.record().value(0))
            return True
        else:
            return False


class DBModelMdt(QSqlRelationalTableModel):
    def __init__(self):
        super(DBModelMdt, self).__init__()
        self.setTable("arvensteyn_dev22.mandanten")
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.setSort(0, Qt.SortOrder.AscendingOrder)
        self.setRelation(3, QSqlRelation("arvensteyn_dev22.partner", "partnerid", "name"))
        self.select()

    def filter_mandantid(self, mandantid):
        filter = f"""'mandantid' = {mandantid}"""
        self.setFilter(filter)


class MandantListe(QSqlQueryModel):
    def __init__(self):
        super(MandantListe, self).__init__()
        query = (
            f"""select arvensteyn_dev22.mandanten.name, arvensteyn_dev22.mandanten.mandantid FROM arvensteyn_dev22.mandanten ORDER BY arvensteyn_dev22.mandanten.name ASC""")
        self.setQuery(query)

    def filter_by_name(self, input_name):
        query = f"""select arvensteyn_dev22.mandanten.name, arvensteyn_dev22.mandanten.mandantid FROM arvensteyn_dev22.mandanten WHERE arvensteyn_dev22.mandanten.name LIKE '%{input_name}%' 
        ORDER BY arvensteyn_dev22.mandanten.name ASC"""
        self.setQuery(query)
        while self.query().next():
            print(self.query().value(0))
        print(self.lastError().text())


class MandantEditmodel(QSqlRelationalTableModel):
    def __init__(self, mandantid='NULL'):
        super(MandantEditmodel, self).__init__()
        self.setTable("arvensteyn_dev22.mandanten")
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.setSort(1, Qt.SortOrder.AscendingOrder)
        self.setJoinMode(QSqlRelationalTableModel.JoinMode.LeftJoin)
        self.setRelation(3, QSqlRelation("arvensteyn_dev22.partner", "partnerid", "name"))
        filter = (f"""arvensteyn_dev22.mandanten.mandantid = {mandantid}""")
        self.setFilter(filter)
        self.select()

        print(self.lastError().text())

    def update_re(self, newperson):
        query = QSqlQuery(f"""Update arvensteyn_dev22.mandanten SET rechnungsempfaenger = {newperson}""")
        if not self.setQuery(query):
            print(self.lastError().text())


class GV_model(QSqlTableModel):
    def __init__(self, gv_index ='NULL'):
        super(GV_model, self).__init__()

        self.setTable("arvensteyn_dev22.humans")
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        filter = (f"""arvensteyn_dev22.humans.index = {gv_index}""")
        self.setFilter(filter)
        self.select()

        print(self.lastError().text())


class REE_model(QSqlTableModel):
    def __init__(self, re_index ='NULL'):
        super(REE_model, self).__init__()

        self.setTable("arvensteyn_dev22.humans")
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.setSort(1, Qt.SortOrder.AscendingOrder)
        filter = (f"""arvensteyn_dev22.humans.index = {re_index}""")
        self.setFilter(filter)
        self.select()

        print(self.lastError().text())

class HumanSearch(QSqlQueryModel):
    def __init__(self):
        super(HumanSearch, self).__init__()
        query = f"""SELECT max(index) FROM arvensteyn_dev22.humans"""
        self.setQuery(query)
        print(self.rowCount())
        self.new_index = self.index(0, 0).data()
        self.result()

    def result(self):
        return self.new_index

class DBModelHumans(QSqlTableModel):
    def __init__(self):
        super(DBModelHumans, self).__init__()
        self.setTable("arvensteyn_dev22.humans")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.setSort(0, Qt.SortOrder.AscendingOrder)

    def welcome_human(self, name_full, name_prefix, name_first, name_last, birthday, organization, title, role,
                      work_address1, work_city1, work_zip1, work_phone_1, work_phone_2, work_phone_3,
                      work_fax, mobile_phone_1, work_email_1, note, url):
        list = [name_prefix, name_first, name_last, birthday, organization, title, role,
                work_address1, work_city1, work_zip1, work_phone_1, work_phone_2, work_phone_3,
                work_fax, mobile_phone_1, work_email_1, note, url]
        new_human = self.record()
        new_human.setGenerated(0, False)
        new_human.setValue(2, name_full)
        new_human.setValue(3, name_prefix)
        new_human.setValue(4, name_first)
        new_human.setValue(6, name_last)
        new_human.setValue(9, birthday)
        new_human.setValue(11, organization)
        new_human.setValue(12, title)
        new_human.setValue(13, role)
        new_human.setValue(31, work_address1)
        new_human.setValue(32, work_city1)
        new_human.setValue(33, work_zip1)
        new_human.setValue(49, work_phone_1)
        new_human.setValue(50, work_phone_2)
        new_human.setValue(51, work_phone_3)
        new_human.setValue(55, work_fax)
        new_human.setValue(58, mobile_phone_1)
        new_human.setValue(64, work_email_1)
        new_human.setValue(70, note)
        new_human.setValue(72, url)

        if not self.insertRecord(-1, new_human):
            print(self.lastError().text())

        # lastval = QSqlQuery()
        # lastval.exec("select lastval()")
        # lastval.next()
        # val = lastval.value(0)
        # return val
        #
class DBModelAuftraege(QSqlRelationalTableModel):
    def __init__(self):
        super(DBModelAuftraege, self).__init__()

        self.setTable('arvensteyn_dev22.auftraege')
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.setSort(0, Qt.SortOrder.DescendingOrder)
        self.setJoinMode(QSqlRelationalTableModel.JoinMode.LeftJoin)
        self.setRelation(1, QSqlRelation('arvensteyn_dev22.mandanten', 'mandantid', 'name'))
        self.setRelation(6, QSqlRelation('arvensteyn_dev22.gegner', 'id', 'gegner_name'))
        self.setRelation(7, QSqlRelation('arvensteyn_dev22.gegner', 'id', 'gegner_name'))
        self.setRelation(8, QSqlRelation('arvensteyn_dev22.gegner', 'id', 'gegner_name'))
        self.setRelation(9, QSqlRelation('arvensteyn_dev22.humans', 'index', 'full_name'))

        self.select()


        




class Auftragsauswahl(QSqlQueryModel):
    def __init__(self, MdtName):
        super(Auftragsauswahl, self).__init__()

        query = QSqlQuery(f"""SELECT
                          arvensteyn_dev22.auftraege.az, arvensteyn_dev22.auftraege.auftragsbezeichnung, 
                          arvensteyn_dev22.auftraege.auftragsjahr, arvensteyn_dev22.mandanten.name, 
                          arvensteyn_dev22.auftraege.id
                          FROM 
                          arvensteyn_dev22.auftraege
                          INNER JOIN arvensteyn_dev22.mandanten ON arvensteyn_dev22.mandanten.mandantid = 
                          arvensteyn_dev22.auftraege.mdt AND arvensteyn_dev22.mandanten.name = '{MdtName}'""")
        self.setQuery(query)


class AuftragsauswahlNr(QSqlQueryModel):
    def __init__(self, MdtNr):
        super(AuftragsauswahlNr, self).__init__()

        query = QSqlQuery(f"""SELECT                                                                             
                          arvensteyn_dev22.auftraege.az, arvensteyn_dev22.auftraege.auftragsbezeichnung,         
                          arvensteyn_dev22.auftraege.auftragsjahr, arvensteyn_dev22.mandanten.name,              
                          arvensteyn_dev22.auftraege.id                                                          
                          FROM                                                                                   
                          arvensteyn_dev22.auftraege                                                             
                          INNER JOIN arvensteyn_dev22.mandanten ON arvensteyn_dev22.mandanten.mandantid =        
                          arvensteyn_dev22.auftraege.mdt AND arvensteyn_dev22.mandanten.mdt_id_lz = '{MdtNr}'""")
        self.setQuery(query)

class Gerichte(QSqlTableModel):
    def __init__(self):
        super(Gerichte, self).__init__()
        self.setTable('arvensteyn_dev22.gerichte')
        self.select()
        if not self.select() == True:
            print(f"""{self.lastError().text()}""")

class Leistungen(QSqlRelationalTableModel):
    def __init__(self):
        super(Leistungen, self).__init__()

        self.setTable("arvensteyn_dev22.leistungen")
        self.setJoinMode(QSqlRelationalTableModel.JoinMode.InnerJoin)
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.setRelation(12, QSqlRelation("arvensteyn_dev22.auftraege", "id", "az"))
        # self.setRelation(2, QSqlRelation("arvensteyn_dev22.mandanten", "mandantid", "name"))
        self.setRelation(1, QSqlRelation("arvensteyn_dev22.mitglieder", "mitgliedernr", "mitglied"))
        self.select()

    def leistungserfassung(self, file: int, ra: int, lbeschreibung: str, duration: int, abrb: bool, l_datum: str,
                           stamp: str):
        if abrb == 0:
            abrb = False
        elif abrb == 1:
            abrb = True
        self.neue_leistung = self.record()
        self.neue_leistung.setGenerated(0, False)
        self.neue_leistung.setValue(1, ra)
        self.neue_leistung.setValue(2, lbeschreibung)
        self.neue_leistung.setValue(4, duration)
        self.neue_leistung.setValue(5, l_datum)
        self.neue_leistung.setValue(8, stamp)
        self.neue_leistung.setValue(12, file)
        self.neue_leistung.setValue(13, abrb)
        if not self.insertRecord(-1, self.neue_leistung):
            print(self.lastError().text())

    def ra_filter(self, file):
        filter = f"""auftrag = {file} AND ra = {self.ra}"""
        self.setFilter(filter)
        print(self.lastError().text())

class PreviousEntriesFileProxy(QSortFilterProxyModel):
    def __init__(self, file):
        super(PreviousEntriesFileProxy, self).__init__()
        self.setSourceModel(Leistungen())

        filter = f"""{file}"""

        self.setFilterKeyColumn(13)

        self.setFilterFixedString(filter)


class MostRecentFiles(QSqlQueryModel):
    def __init__(self):
        super(MostRecentFiles, self).__init__()
        self.ra = currentConfig.getcurrent_ra(self=currentConfig())

        query = QSqlQuery(f"""select
                          arvensteyn_dev22.auftraege.id, arvensteyn_dev22.auftraege.az,
                          arvensteyn_dev22.mandanten.name, arvensteyn_dev22.auftraege.auftragsbezeichnung   
                          from 
                          arvensteyn_dev22.auftraege
                          inner join arvensteyn_dev22.leistungen ON arvensteyn_dev22.leistungen.auftrag = 
                          arvensteyn_dev22.auftraege.id AND arvensteyn_dev22.leistungen.ra = {self.ra}
                          inner join arvensteyn_dev22.mandanten ON arvensteyn_dev22.auftraege.mdt = 
                          arvensteyn_dev22.mandanten.mandantid
                          group by arvensteyn_dev22.auftraege.id, arvensteyn_dev22.mandanten.name LIMIT 10""")

        print(self.ra)
        self.setQuery(query)
        print(self.lastError().text())


editables = {1: (
"UPDATE arvensteyn_dev22.auftraege SET auftragsbezeichnung = '{}' WHERE arvensteyn_dev22.auftraege.id = '{}'", 4),
             6: (" UPDATE arvensteyn_dev22.auftraege SET mdt = '{}' WHERE arvensteyn_dev22.auftraege.id = '{}'", 4)}

query = f"""SELECT
                          arvensteyn_dev22.auftraege.az, arvensteyn_dev22.auftraege.rvg, arvensteyn_dev22.auftraege.auftragsbezeichnung, 
                          arvensteyn_dev22.auftraege.auftragsjahr, arvensteyn_dev22.mandanten.name, 
                          arvensteyn_dev22.auftraege.id, arvensteyn_dev22.auftraege.mdt
                          FROM 
                          arvensteyn_dev22.auftraege
                          INNER JOIN arvensteyn_dev22.mandanten ON arvensteyn_dev22.mandanten.mandantid = 
                          arvensteyn_dev22.auftraege.mdt AND arvensteyn_dev22.mandanten.name = 'Abbas Nasrallah'"""


## todo revise whole odel
class LeistungenTableModel(QSqlRelationalTableModel):
    # source : https://stackoverflow.com/questions/49752388/editable-qtableview-of-complex-sql-query
    def __init__(self, *args, **kwargs):
        super(QSqlRelationalTableModel, self).__init__(*args, **kwargs)
        self.booleanSet = [9, 10, 13]  # columns with checkboxes
        self.setTable("arvensteyn_dev22.leistungen")
        self.setRelation(3, QSqlRelation("arvensteyn_dev22.partner", "partnerid", "name"))

        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.select()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        if index.column() in self.booleanSet:
            fl = QSqlRelationalTableModel.flags(self, index)
            fl |= Qt.ItemFlag.ItemIsUserCheckable
            return fl
        else:
            return QSqlRelationalTableModel.flags(self, index)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        value = QSqlRelationalTableModel.data(self, index)
        if role == Qt.ItemDataRole.CheckStateRole:
            if index.column() in self.booleanSet:
                return Qt.CheckState.Unchecked if value == 0 else Qt.CheckState.Checked
            else:
                return QVariant()
        return QSqlRelationalTableModel.data(self, index, role)

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False
        if index.column() in self.booleanSet:
            if role == Qt.ItemDataRole.CheckStateRole:
                val = True if value == Qt.CheckState.Unchecked.value else False
                self.dataChanged.emit(index, index, (role,))
                print(self.lastError().text())
                return QSqlRelationalTableModel.setData(self, index, val, Qt.ItemDataRole.EditRole)

            else:
                #self.data(index, Qt.ItemDataRole.CheckStateRole)
                return QSqlRelationalTableModel.setData(self, index, value, Qt.ItemDataRole.EditRole)
