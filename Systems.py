# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:53:18 2022

@author: Schmuck
"""

import os, platform
import datetime
import shutil
import logging

class FileManager:
    
    def __init__(self):
        self.sysInfo = self.SystemInformation()
        
    
    # def createDBBackup(self):
    #     filename = datetime.datetime.now().strftime("%m-%d-%y_%H.%M")
    #     # print(filename)
    #     shutil.copyfile(self.databaseLocation, self._getFilePath("backups/{}.db".format(filename)))

    class SystemInformation:
    
    
        def __init__(self, devMode = False):
            self.docker = True if os.environ.get("INSIDE_DOCKER") else False
            self.os = platform.system()
            self._basePath = self.determineBasePath(devMode)
            
            self._dbFile = "Info.db"
            self._loggingFile = "birthday.log"
            self._secretFile = "Secret.txt"
    
            self.databaseLocation = self._getFilePath(self._dbFile)
            self.logging = self._getFilePath(self._loggingFile) 
            self.notificationSecretLocation = self._getFilePath(self._secretFile)
    
        def determineBasePath(self, devMode):
            if not self.docker:
                if self.os == "Windows":
                    return "A:/appsuser/db/EventNotifications"
                elif self.os == "Linux":
                    return "/mnt/apps/appsuser/db/EventNotifications"
                    # return "/run/user/1000/gvfs/smb-share:server=truenas.local,share=applications/appsuser/db/EventNotifications"
                else:
                    pass
            else:
                # If it is running in docker
                return "/home/schmuck"
        
        _getFilePath = lambda self, x: "{}/{}".format(self._basePath, x)
        
        def _getModifiedTime(self, file):
            return datetime.datetime.fromtimestamp(os.path.getmtime(self._basePath + "/{}".format(file)))
        
        def getLastRunTime(self):
            return self._getModifiedTime("birthday.log")
        
        def getBirthdayModificationTime(self):
            return self._getModifiedTime("Birthdays.csv")
        
       


        

def loggingSetup(path):
    log_format = '%(asctime)s %(message)s'
    logging.basicConfig(filename = path,
                        format = log_format,
                        filemode = "a",
                        level = logging.INFO,
                        force = True)
    return logging.getLogger("BirthdayLogger")