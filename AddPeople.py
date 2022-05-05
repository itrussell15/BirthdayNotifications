# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 21:01:13 2022

@author: Schmuck
"""

import pandas as pd
from BirthdayDB import BirthdayDB

# birthdays = pd.read_csv("Birthdays.csv")

db_path = "A:\\appsuser\\db\\EventNotifications\\Test.db"
csv_path = "A:\\appsuser\\db\\EventNotifications\\Birthdays.csv"

db = BirthdayDB(db_path)
csv = pd.read_csv(csv_path)

# If there is a mismatch from the db and the csv
if len(csv) != db.CountRows():
    ## Delete and re add all rows from CSV
    db.DeleteRows()

    # Add back all the rows that exist in the db
    for i in csv.iterrows():
        items = i[1].values
        # print(items)
        db.AddPerson(items[0], items[1], items[2], items[3], items[4], items[5])

db.end()
