from DBAgent import DatabaseAgent
import datetime
import Exceptions 
import conf
from Authentication import Authentication
from ApplicationLogger import Logger
import sessionMange
class labourerClass:

    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()

    def classList(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        labclas = ["labourerclass","wageclass","labourerclassid","compensation","retention","advance","concretecharges"]                           #,"compensation","Retention","Advance","Concrete_charges"]
        self.log.logEvent("Admin",2,"class list listed successfully",clientId,sessionMange.session[sessionkey]["userid"]) 
        try:
            responseData = adminDb.fetchData("labourerclass",labclas)
            response = {"Header":{"status":"success","module":"labourerClass"},"Body":{"message":"class list","data":responseData},"Signature":{"signature":"","Key":""}}
            return response            
            
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])     

    def classAdding(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        keyList =[]
        valList = []
        for key in msgDict:
            keyList.append(key.lower())
            valList.append(msgDict[key])
        try:
            if adminDb.pushData("labourerclass",keyList,valList):
                self.log.logEvent("Admin",2,msgDict["labourerClass"]+" class added successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labourerClass"},"Body":{"message":"class added successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                response = {"Header":{"status":"fail","module":"labourerClass"},"Body":{"message":"class can't added","data":""},"Signature":{"signature":"","Key":""}}
                return response  
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                  
                   

    def classDelete(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        condition = {"labourerclassid":msgDict["classId"]}
        reval =  False
        try:
            if adminDb.updateTable(delete,"labourerclass",condition):
                self.log.logEvent("Admin",2,msgDict["classId"]+"labourer class deleted successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labourerClass"},"Body":{"message":"class deleted succes","data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Admin",2,msgDict["classId"]+"labourer class cant deleted "+ expc + "exception is occured",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labourerClass"},"Body":{"message":"class canot deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response     
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                 