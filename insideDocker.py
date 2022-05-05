#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:27:48 2022

@author: schmuck
"""

import os

if os.environ.get("INSIDE_DOCKER"):
    print("INSIDE DOCKER!")
else:
    print("OUTSIDE DOCKER :(")
