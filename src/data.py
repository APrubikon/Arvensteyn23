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
    def __init__(self, gv_index):
        super(GV_model, self).__init__()

        self.setTable("arvensteyn_dev22.humans")
        self.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        filter = (f"""arvensteyn_dev22.humans.index = {gv_index}""")
        self.setFilter(filter)
        self.select()

        print(self.lastError().text())


class REE_model(QSqlTableModel):
    def __init__(self, re_index):
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

class Gerichte(QSqlTableModel):
    def __init__(self):
        super(Gerichte, self).__init__()
        self.setTable('arvensteyn_dev22.gerichte')
        self.select()
        if not self.select() == True:
            print(f"""{self.lastError().text()}""")
