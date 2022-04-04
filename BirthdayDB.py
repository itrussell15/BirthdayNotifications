# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 23:03:46 2022

@author: Schmuck
"""

import sqlite3, requests
import os
import datetime
import time
import logging

class DBManage:

    def __init__(self, location):
        self._isEmpty = self._checkExistence(location)
        # if not self._isEmpty:
        self._con = sqlite3.connect(location)
        self._cur = self._con.cursor()

    def query(self, columns, table, **kwargs):
        command = '''SELECT {} FROM {}\n'''.format(columns, table)
        for i in kwargs.values():
            command += " "
            command += i
        return self._cur.execute(command).fetchall()

    def create(self, name, fields, primaryKey = None):

        def listKey(key):
            key = list(key)
            return "({})".format(", ".join(key))

        def strKey(key):
            return key

        options = {
            str: strKey,
            list: listKey,
            set: listKey,
            tuple: listKey,
            }

        command = '''CREATE TABLE IF NOT EXISTS {} (\n'''.format(name)

        for n, v in enumerate(fields.items()):
            command += '''"{}"'''.format(v[0])
            command += " "
            command += v[1]
            # if n != len(v):
            command += ",\n"
        if primaryKey:
            command += "PRIMARY KEY "
            try:
                command += options[type(primaryKey)](primaryKey)
            except:
                print('Invalid Primary Key Type')
        command += ")"
        # print(command)
        self._cur.execute(command)

    def _checkExistence(self, path):
        return os.path.isfile(path)

    def end(self):
        self._con.commit()
        self._con.close()

class BirthdayDB(DBManage):

    def __init__(self, location):
        super().__init__(location)
        self._tableName = "Birthdays"
        self._CreateTable()

    def AddPerson(self, fname, lname, birthday, birthLocation = None, relationship= None, sendMessage = None, customMessage = None, phoneNumber = None):
        command = '''
            INSERT INTO {}(FirstName, LastName, Birthday, BirthLocation, Relationship) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, )'''.format(self._tableName)
        self._cur.execute(command, (fname, lname, birthday, birthLocation, relationship, sendMessage, customMessage, phoneNumber))

    def _CreateTable(self):
        self.create(self._tableName,
                    {"FirstName": "TEXT NOT NULL",
                    "LastName": "TEXT NOT NULL",
                    "Birthday": "TEXT NOT NULL",
                    "BirthLocation": "TEXT",
                    "Relationship": "TEXT",
                    "sendMessage": "TEXT DEFAULT 0",
                    "customMessage": "TEXT",
                    "phoneNumber": "TEXT"},
                    primaryKey = ["FirstName", "LastName"]
                    )

    def Query(self, length, date = datetime.date.today(), **kwargs):
        future = date + datetime.timedelta(days = length)
        out = super().query("*",
                  self._tableName,
                  where = '''WHERE Birthday = "{}"'''.format(self.NoYear(future)))
        return [self.Person(i) for i in out]

    NoYear = lambda self, x: "-".join(str(x).split("-")[1:])

    def DeleteRows(self):
        self._cur.execute('''DELETE FROM {}'''.format(self._tableName))

    class Person:

        def __init__(self, row):
            self.fname = row[0]
            self.lname = row[1]
            self.birthday = row[2]
            self.birthplace = row[3]
            self.relationship = row[4]

class Notifications:

    def __init__(self):
        self._apiKey, self._userKey = self._loadKey()
        self.sent_messages = 0

    def _loadKey(self):
        with open("/home/schmuck/Secret.txt", 'r') as f:
            out = f.readlines()
        return out[0].strip(), out[1].strip()

    def GenerateMessage(self, out, time):
        title = "Birthday Alert! 🎂🎉"
        body = "Your {} {} {} has a birthday ".format(out.relationship, out.fname, out.lname)
        if time == 0:
            body += "today!"
        else:
            body += "{} days from now!".format(time)
        self.sent_messages +=1
        self.sendNotification(title, body)

    def sendNotification(self, title, message):
        print(message)
        print(title)
        r = requests.post('https://api.pushover.net/1/messages.json', {
              "token": self._apiKey,
              "user": self._userKey,
              "title": title,
              "message": message,
              })
        
def setupLogging():
    log_format = '%(asctime)s %(message)s'
    logging.basicConfig(filename='birthdays.log',
                        format = log_format,
                        filemode = "a",
                        level = logging.INFO)    
    return logging.getLogger("DiscordBotLogger")
    
if __name__ == "__main__":
    notify = Notifications()
    db = BirthdayDB("/home/schmuck/Info.db")
    for i in [0, 7, 30]:
        date = datetime.date.today()
        out = db.Query(i, date = date)
        if len(out) >= 1:
            # Send notification to phone about birthday upcoming
            [notify.GenerateMessage(j, i) for j in out]
    db.end()
    
    log = setupLogging()
    log.info("{} messages sent".format(notify.sent_messages))
    # print("Script Complete @ {}, {} messages sent".format(datetime.datetime.today(), notify.sent_messages))