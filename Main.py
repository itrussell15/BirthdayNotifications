# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:39:17 2022

@author: Schmuck
"""

from BirthdayDB import BirthdayDB, Notifications
from Systems import FileManager, Logging
import datetime, os
import traceback

files = FileManager()
log = Logging(files.sysInfo.logging)
notify = Notifications(files.sysInfo.notificationSecretLocation)
db = BirthdayDB(files.sysInfo.databaseLocation)

#### REMOVE WHEN CONFIDENT THE PROGRAM RUNS WHEN SUPPOSED TO
notify.sendNotification("System Ran", "Your program ran successfully!")

print("Script running @ {}".format(datetime.datetime.now()))
try:
    # Add the new modifications into the database.
    if files.hasUpdates():
        print("New Modifications!")
        files.createDBBackup()
        db.DeleteRows()
        for item in files.loadCsv():
            db.AddPerson(fname = item[0],
                         lname = item[1],
                         birthday = item[2],
                         relationship=item[3],
                         customMessage=item[4],
                         day30Not=item[5],
                         day7Not=item[6],
                         birthdayNot=item[7]
                         )
        log.info("Birthday file modifications detected. Database updated and backup created")

    date = datetime.date.today()
    # Check for any upcoming birthdays and send notification
    for n, i in enumerate([0, 7, 30]):
        out = db.Query(i, date = date)
        # print([i.fname for i in out])
        # If the query came back with atleast 1
        if len(out) >= 1:
            # For all people that have were queried
            for j in out:
                # print("Name: {} {}, Notification: {}".format(j.fname, j.lname, j.notifications))
                if j.notifications[-n-1]:
                    # Send message to phone
                    notify.GenerateMessage(j, i)
                else:
                    # Divert message to logs
                    log.filterNotification(j, i)
    db.end()

    # Log outcomes
    log.info("{} messages sent from {} {} docker".format(
        notify.sent_messages,
        files.sysInfo.os,
        "inside" if files.sysInfo.docker else "outside"))

except Exception as e:
    db.end()
    traceback.format_exc()
    log.error(traceback.format_exc())
    notify.sendNotification("ERROR", str(e))
    print(traceback.format_exc())
