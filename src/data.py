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
from src.config import currentConfig


class MitarbeiterCred(QSqlTableModel):
    def __init__(self):
        super(MitarbeiterCred, self).__init__()
        self.setTable('arvensteyn_dev22.mitglieder')
        # self.select()

        self.role = ''
        self.setSort(0, Qt.SortOrder.AscendingOrder)

    def checkKey(self, Mitglied, Passtry):
        query1 = QSqlQuery()
        query1.exec(
            f"""SELECT mitgliedernr, beruf, role, auth FROM arvensteyn_dev22.mitglieder WHERE mitglied = '{Mitglied}';""")

        while query1.next():
            self.Beruf = query1.value('beruf')
            self.role = query1.value('role')
            self.Auth = query1.value('auth')
            self.ID = query1.value('mitgliedernr')
            print(Mitglied, self.Auth, Passtry, self.ID)

        from src.config import Anmeldung
        Anmeldung(ID=self.ID, Kopfzeile=Mitglied, Role=self.role, Profession=self.Beruf)

        from src.Login import Login
        if self.Auth == Passtry:

            Login.entry(self=Login, permission="granted")

        else:
            Login.entry(self=Login, permission="denied")

