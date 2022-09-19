import configparser
import os

basedir = os.path.dirname(__file__)


# Add the structure to the file we will create

def definecfgFile():
    config = configparser.ConfigParser()
    config.add_section('user_info')
    config.set('user_info', 'Mitglied', '')
    config.set('user_info', 'user_role', '')
    config.set('user_info', 'user_profession', '')
    config.set('user_info', 'user_id', '')

    config.add_section('database_connection')
    config.set('database_connection', 'host', '')
    config.set('database_connection', 'database', '')
    config.set('database_connection', 'user', '')
    config.set('database_connection', 'pw', '')

    config.add_section('used local data')
    config.set('used local data', 'Az', '')
    config.set('used local data', 'filepath', '')

    # Write the new structure to the new file
    with open(os.path.join(basedir, "configfile.ini"), 'w') as configfile:
        config.write(configfile)


def add_filepaths():
    config = configparser.ConfigParser()
    config.set('used_data', 'filepaths', '')
    with open(r"/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini", 'w') as configfile:
        config.write(configfile)


def db_anmeldung(host='', database='', user='', pw=''):
    edit = configparser.ConfigParser()
    edit.read(os.path.join(basedir, "configfile.ini"))

    database_connection = edit["database_connection"]
    database_connection['host'] = host
    database_connection['database'] = database
    database_connection['user'] = user
    database_connection['pw'] = pw

    with open(os.path.join(basedir, "configfile.ini"), 'w') as configfile:
        edit.write(configfile)


def getdbcreds():
    content = configparser.ConfigParser()
    content.read(os.path.join(basedir, "configfile.ini"))

    db_info = content['database_connection']
    creds = {'host': db_info['host'], 'database': db_info['database'], 'user': db_info['user'], 'pw': db_info['pw']}

    return creds


def initialcheck():
    content = configparser.ConfigParser()
    content.read(os.path.join(basedir, "configfile.ini"))

    db_info = content['database_connection']
    dbcheck = db_info['database']
    return dbcheck

def get_headline():
    content = configparser.ConfigParser()
    content.read(os.path.join(basedir, "configfile.ini"))

    headline_info = content['user_info']
    headline1 = headline_info['user_profession']
    headline2 = headline_info['mitglied']
    headline = f"""{headline1} {headline2}"""
    return headline






def Anmeldung(ID, Kopfzeile, Role, Profession):
    edit = configparser.ConfigParser()
    edit.read(os.path.join(basedir, "configfile.ini"))

    ID = str(ID)

    # Get the userinfo section
    Benutzerinfo = edit["user_info"]
    # Update the password
    Benutzerinfo["Mitglied"] = Kopfzeile
    Benutzerinfo["user_role"] = Role
    Benutzerinfo["user_profession"] = Profession
    Benutzerinfo["user_id"] = ID

    if not Benutzerinfo == '':
        with open(os.path.join(basedir, "configfile.ini"), 'w') as configfile:
            edit.write(configfile)
    else:
        pass
    print('plz check')


def update_filepaths(az, filepath):
    # update config.ini (= string)
    edit = configparser.ConfigParser()
    edit.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

    lexikon = currentConfig.getfilepaths(self=currentConfig())  # get 'str from .ini, not dict
    data_section = edit["used_data"]
    if lexikon == '':
        data_section["filepaths"] = f"""{az} : {filepath}"""
    else:
        data_section["filepaths"] = f"""{lexikon}, {az} : {filepath}"""

    if not filepath == '':
        with open('/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini', 'w') as configfile:
            edit.write(configfile)
    else:
        pass


class currentConfig():
    def __init__(self):
        self.content = configparser.ConfigParser()
        self.content.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

        self.user_info = self.content["user_info"]
        self.Name = self.user_info["Mitglied"]
        self.Beruf = self.user_info["user_profession"]
        self.user_id = self.user_info["user_id"]

    def getcurrentfiles(self):
        self.content = configparser.ConfigParser()
        self.content.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

        self.lastFiles = self.content["used_data"]
        self.list_of_files = self.lastFiles["last_files"]
        self.list_of_files = [str(x) for x in self.list_of_files.split(",")]
        return self.list_of_files

    def getcurrent_ra(self):
        self.content = configparser.ConfigParser()
        self.content.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

        self.user_info = self.content["user_info"]
        self.user_id = self.user_info["user_id"]

        if not self.user_id == '':
            self.user_id = int(self.user_id)
        else:
            self.user_id = 0
        return self.user_id

    def getcurrent_tier(self):
        self.content = configparser.ConfigParser()
        self.content.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

        self.user_info = self.content["user_info"]
        self.user_tier = self.user_info["user_role"]

        if not self.user_tier == '':
            self.user_id = str(self.user_tier)
        else:
            self.user_id = 'default'
        return self.user_tier

    def getfilepaths(self):
        self.content = configparser.ConfigParser()
        self.content.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

        self.data_section = self.content["used_data"]
        self.filepaths = self.data_section["filepaths"]
        return self.filepaths  # string, even if empty

    def getfilepathsdict(self):
        # fetch content of config.ini, output dict.

        self.filepaths = self.getfilepaths()
        print(self.filepaths)  # string
        if self.filepaths != '':
            self.lexikon_list = [str(x) for x in self.filepaths.split(", ")]
            self.lexikon_t = tuple(self.lexikon_list)  # tuple
            self.list = []
            for i in self.lexikon_list:
                element = tuple(i.split(" : "))
                self.list.append(element)
            self.lexikon = tuple(self.list)
            self.lexikon = dict(self.lexikon)

        else:
            self.lexikon = {}  # empty dict.
        print(self.lexikon)
        return self.lexikon


def last_files_update(most_current):
    edit = configparser.ConfigParser()
    edit.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

    LastFiles = edit["used_data"]
    if LastFiles["last_files"] == "":
        LastFiles["last_files"] = most_current
        with open('/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini', 'w') as configfile:
            edit.write(configfile)
    else:
        print("no sweat")

    prev_list = LastFiles["last_files"]
    prev_list = [str(x) for x in prev_list.split(", ")]

    if most_current in prev_list:
        print("Nothing new")
    else:
        if len(prev_list) >= 10:
            prev_list = prev_list[1:]
        else:
            pass
        prev_list.append(most_current)
        new_list = ','.join(prev_list)
        LastFiles["last_files"] = new_list

        with open('/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini', 'w') as configfile:
            edit.write(configfile)


def check_template_anschreiben(az, filepath):
    lexikon = currentConfig.getfilepathsdict(self=currentConfig())

    if az in lexikon.keys():
        if filepath == lexikon.__getitem__(az):
            pass  # wait for click on 'neues Dokument erstellen
        else:
            pre_lexikon = currentConfig.getfilepaths(self=currentConfig())
            print(lexikon.__getitem__(az))
            new_lexikon = pre_lexikon.replace(f"""{az} : {lexikon.__getitem__(az)}""", f"""{az} : {filepath}""")
            update_filepaths_anschreiben(new_lexikon)
    else:
        pre_lexikon = currentConfig.getfilepaths(self=currentConfig())
        new_lexikon = f"""{pre_lexikon}, {az} : {filepath}"""
        update_filepaths_anschreiben(new_lexikon)


def update_filepaths_anschreiben(newfp):
    edit = configparser.ConfigParser()
    edit.read("/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini")

    data_section = edit["used_data"]
    if newfp != '':
        data_section["filepaths"] = newfp
    with open('/Users/Shared/PycharmProjects/arvensteynIII/configfile.ini') as configfile:
        edit.write(configfile)
