# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 14:34:13 2022

@author: Schmuck
"""

from BirthdayDB import BirthdayDB, Notifications
from Systems import SystemInformation, loggingSetup
import datetime, os


sysInfo = SystemInformation()
log = loggingSetup(sysInfo.logging)
notify = Notifications(sysInfo.notificationSecretLocation)

# Add the new modifications into the database.
if sysInfo.getLastRunTime() < sysInfo.getBirthdayModificationTime():
    print("New Modifications!")
    sysInfo.createDBBackup()
    
    log.info("Birthday file modifications detected. Database updated and backup created")
    
# REMOVE WHEN CONFIDENT THE PROGRAM RUNS WHEN SUPPOSED TO
# notify.sendNotification("System Ran", "Your program ran successfully!")
# print("PROGRAM RAN")


# log.info("Program started")

# print("Script running @ {}".format(datetime.datetime.now()))

# try:
#     run_time = datetime.datetime.now()
    
    
#     db = BirthdayDB(sysInfo.databaseLocation)
#     for i in [0, 7, 30]:
#         date = datetime.date.today()
#         out = db.Query(i, date = date)
#         if len(out) >= 1:
#             # Send notification to phone about birthday upcoming
#             [notify.GenerateMessage(j, i) for j in out]
#     db.end()
#     log.info("{} messages sent from {} {} docker".format(notify.sent_messages, sysInfo.os, "inside" if sysInfo.docker else "outside"))
# except Exception as e:
#     log.error(str(e))
#     # print(str(e))