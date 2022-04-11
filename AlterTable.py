#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:27:48 2022

@author: schmuck
"""

import sqlite3


con = sqlite3.connect('Testing.db')
cur = con.cursor()

command = '''ALTER TABLE Birthdays ADD COLUMN messageNumber TEXT'''
cur.execute(command)

con.commit()
cur.close()    
