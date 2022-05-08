# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:39:17 2022

@author: Schmuck
"""

from BirthdayDB import SystemInformation, Notifications, BirthdayDB, loggingSetup
import datetime

sysInfo = SystemInformation()
log = loggingSetup(sysInfo.logging)
notify = Notifications(sysInfo.notificationSecretLocation)

#REMOVE WHEN CONFIDENT THE PROGRAM RUNS WHEN SUPPOSED TO
notify.sendNotification("System Ran", "Your program ran successfully!")
print("PROGRAM RAN")

log.info("Program started")

try:
    run_time = datetime.datetime.now()
    
    
    db = BirthdayDB(sysInfo.databaseLocation)
    for i in [0, 7, 30]:
        date = datetime.date.today()
        out = db.Query(i, date = date)
        if len(out) >= 1:
            # Send notification to phone about birthday upcoming
            [notify.GenerateMessage(j, i) for j in out]
    db.end()
    log.info("{} messages sent from {} {} docker".format(notify.sent_messages, sysInfo.os, "inside" if sysInfo.docker else "outside"))
except Exception as e:
    log.error(str(e))
    # print(str(e))