# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 21:01:13 2022

@author: Schmuck
"""

import pandas as pd
from BirthdayDB import BirthdayDB


# birthdays = pd.read_csv("Birthdays.csv")

db = BirthdayDB("A:\appsuser\db\EventNotifications\testMe.db")

# for i in birthdays.iterrows():
#     # print(i[1].values)
#     items = i[1].values
#     try:
#         db.AddPerson(items[0], items[1], items[2], items[3], items[4], items[5], items[6], items[7])
#     except:
#         pass

db.end()