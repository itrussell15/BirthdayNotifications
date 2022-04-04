# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 21:01:13 2022

@author: Schmuck
"""

import pandas as pd
from BirthdayDB import BirthdayDB


birthdays = pd.read_csv("Birthdays.csv")

db = BirthdayDB("A:\\appsuser\\db\\Info.db")

for i in birthdays[6:].iterrows():
    items = i[1].values
    try:
        db.AddPerson(items[0], items[1], items[2], items[3], items[4])
    except:
        pass

db.end()