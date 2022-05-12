#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:27:48 2022

@author: schmuck
"""

import sqlite3


con = sqlite3.connect('Test.db')
cur = con.cursor()

# command = '''ALTER TABLE Birthdays ADD COLUMN messageNumber TEXT'''
command = '''SELECT * FROM Birthdays'''
print(cur.execute(command).fetchall())

con.commit()
cur.close()    
