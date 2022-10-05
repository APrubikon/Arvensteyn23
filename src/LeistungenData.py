from PyQt6.QtSql import QSqlQueryModel, QSqlQuery
from src.db import dbopen

#editables = {1: (
#            "UPDATE arvensteyn_dev22.auftraege SET auftragsbezeichnung = '{}' WHERE arvensteyn_dev22.auftraege.id = '{}'",
#            4),
#            6: (" UPDATE arvensteyn_dev22.auftraege SET mdt = '{}' WHERE arvensteyn_dev22.auftraege.id = '{}'", 4)}
#
#        query = f"""SELECT
#                                  arvensteyn_dev22.auftraege.az, arvensteyn_dev22.auftraege.rvg, arvensteyn_dev22.auftraege.auftragsbezeichnung,
#                                  arvensteyn_dev22.auftraege.auftragsjahr, arvensteyn_dev22.mandanten.name,
#                                  arvensteyn_dev22.auftraege.id, arvensteyn_dev22.auftraege.mdt
#                                  FROM
#                                  arvensteyn_dev22.auftraege
#                                  INNER JOIN arvensteyn_dev22.mandanten ON arvensteyn_dev22.mandanten.mandantid =
#                                  arvensteyn_dev22.auftraege.mdt AND arvensteyn_dev22.mandanten.name = 'Abbas Nasrallah'"""
#
#
#
dbopen()
class LeistungenData(QSqlQueryModel):
    def __init__(self):
        super(LeistungenData, self).__init__()

        # this is an editable query model with multiple inner joins, functions to insert new entries and
        # checkable boxes for boolean values
        query = QSqlQuery("Select * "
        "from arvensteyn_dev22.leistungen" 
        "inner join arvensteyn_dev22.auftraege on arvensteyn_dev22.auftraege.id = arvensteyn_dev22.leistungen.auftrag" 
        "inner join arvensteyn_dev22.mandanten on arvensteyn_dev22.mandanten.mandantid = arvensteyn_dev22.auftraege.mdt")


        self.setQuery(query)

        print(self.lastError().text())

LeistungenData()