# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 21:01:13 2022

@author: Schmuck
"""

import pandas as pd
from BirthdayDB import BirthdayDB


birthdays = pd.read_csv("A:\\appsuser\\db\\EventNotifications\\Birthdays.csv")

db = BirthdayDB("A:\\appsuser\\db\\Test.db")

for i in birthdays.iterrows():
    items = i[1].values
    # print(items)
    db.AddPerson(items[0], items[1], items[2], items[3], items[4], items[5])

db.end()