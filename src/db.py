from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox
from src.config import getdbcreds





def dbopen():
    creds = getdbcreds()
    print(creds)

    db = QSqlDatabase.addDatabase('QPSQL')

    db.setHostName(creds['host'])
    db.setDatabaseName(creds['database'])
    db.setUserName(creds['user'])
    db.setPassword(creds['pw'])

#
        #ToDo: check to see if internet connection is available

    if not db.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % db.lastError().databaseText(),
        )
    else:
        return db