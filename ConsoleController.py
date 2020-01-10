'''    
This is the starting point of the software. It has 3 primary functions:
1. Start the program and load the default configurations                        
2. Initialize and test the database connection                                  
3. Start the server module with the required parameters
'''

import conf 
import db_conf
import lang_conf
import Server
from Exceptions import DbException, LangException
from DbController import DbController
import sys
from Communication import Communication
from flask import Flask
import sessionMange
# sessions = {}
host = "127.0.0.1"

def loadConfig():
    '''
    The starting configuration for the software to run are loaded here. The Python file 
    conf.py is loaded. If there is a user-defined configuration, it is loaded into the 
    program. Else the default configuration is used.
    '''

    if "usr-def" in conf.confTypes:
        return conf.confTypes["usr-def"]
    else:
        return conf.confTypes["default"]

def loadLanguage(langName):
    '''
    The language configured for use with the software is loaded, once it is read from the 
    initial configuration file. English (US) is the default language choice in case all 
    else fails or no choice has been made.
    '''
    try:
        if langName in lang_conf.languages:
            return lang_conf.languages[langName]
        else:
            raise LangException
    except LangException as langEx:
        print("The selected language was not found. Using English as default language")
        return lang_conf.languages["en-us"]

def loadDbConf():
    return db_conf.masterDbConn

if __name__ == "__main__":
    CmdArgs = sys.argv
    if len(CmdArgs) > 1:
        #################################################################################
        #       Check whether there are any command line arguments. In case there       #
        #       are any, process them. Needs to be looked into once the arguments       #
        #       are considered.                                                         #
        #################################################################################
        pass
    #####################################################################################
    #       Load the configuration file, db configuration file, language                #
    #       configuration file, test the database, and if all operations                #
    #       are successful, start the server with the configurations specified          #
    #####################################################################################
    try:
        config        = loadConfig()
        print(config)
        chLang    = loadLanguage(config["lang"])
        dbConf        = loadDbConf()
        dbConn        = DbController(dbConf)
        dbCheck       = True#dbConn.testDb()
        if not dbCheck:
            raise DbException
        else:
            #server = Server(config, dbConf, chLang)
            Server.startServer()
    except DbException as dbError:
        print(chLang["MSG0001"])
        comm = Communication(chLang)