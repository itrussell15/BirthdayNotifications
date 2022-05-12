# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:39:17 2022

@author: Schmuck
"""

from BirthdayDB import BirthdayDB, Notifications
from Systems import FileManager, loggingSetup
import datetime, os

files = FileManager()
log = loggingSetup(files.sysInfo.logging)
notify = Notifications(files.sysInfo.notificationSecretLocation)
db = BirthdayDB(files.sysInfo.databaseLocation)
    
#### REMOVE WHEN CONFIDENT THE PROGRAM RUNS WHEN SUPPOSED TO
# notify.sendNotification("System Ran", "Your program ran successfully!")

print("Script running @ {}".format(datetime.datetime.now()))
try:
    # Add the new modifications into the database.
    if files.hasUpdates():
        print("New Modifications!")
        files.createDBBackup()
        db.DeleteRows()
        for item in files.loadCsv():
            db.AddPerson(item[0], item[1], item[2], item[3], item[4], item[5])
        log.info("Birthday file modifications detected. Database updated and backup created")

    # Check for any upcoming birthdays and send notification
    for i in [0, 7, 30]:
        date = datetime.date.today()
        out = db.Query(i, date = date)
        if len(out) >= 1:
            # Send notification to phone about birthday upcoming
            [notify.GenerateMessage(j, i) for j in out]
    db.end()
    # Log outcomes
    log.info("{} messages sent from {} {} docker".format(
        notify.sent_messages,
        files.sysInfo.os,
        "inside" if files.sysInfo.docker else "outside"))
    
except Exception as e:
    log.error(str(e))
    # print(str(e))