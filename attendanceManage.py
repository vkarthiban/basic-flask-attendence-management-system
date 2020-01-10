from DBAgent import DatabaseAgent
import datetime
import Exceptions 
from Authentication import Authentication
from ApplicationLogger import Logger
import sessionMange

class attendanceManage:
    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()

    def getAttendace(self,clientId,sessionkey):#to be filled from the call site (module launcher)
        masterDb = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, "127.0.0.1",password, 5432)
        adminDb.initConnection()
        dataFields = ["date","labourerid","labourername","labourerclass","shiftid","intime","outtime","numberofhours","overtimeallocated" ,"overtimeworked","siteid","projectid"]
        tableName = "attendance"
        responseData = adminDb.fetchData(tableName,dataFields)
        print("dictonary",responseData)
        try:
            self.log.logEvent("Admin",2,"attendance listed success fully")
            response = {"Header":{"status":"success","module":"attendance"},"Body":{"message":"filtered attendance","data":responseData},"Signature":{"signature":"","Key":""}}
            return response 
        except Exception as expc:
            # self.syslog.eventHandle("attendanceManage","exception","exception on attendanceManage module",str(expc))
            self.log.logEvent("attendanceManage",3," all role permission listed occured "+str(expc))            
        

    def getAttendacePers(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, "127.0.0.1",password, 5432)
        adminDb.initConnection()
        dataFields = ["day","date","labourerid","labourername","labouercategory","intime","outtime","numberofhours","overtimeallocated","overtimeworked","shiftid"]
        tableName = "attendance"
        condition = {}
        try:
            for key in msgDict:
                condition[key.lower()] = (msgDict[key])
            responseData = adminDb.fetchData(tableName,dataFields,condition)
            print("dictonary",responseData)
            self.log.logEvent("Admin",2,"attendance listed success fully")
            response = {"Header":{"status":"success","module":"attendance"},"Body":{"message":"filtered attendance","data":responseData},"Signature":{"signature":"","Key":""}}
            return response 
        except Exception as expc:
            # self.syslog.eventHandle("attendanceManage","exception","exception on attendanceManage module",str(expc))
            self.log.logEvent("attendanceManage",3," all role permission listed occured "+str(expc))            

    def filterAttendance(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, "127.0.0.1",password, 5432)
        adminDb.initConnection()
        condition = {}
        for key in msgDict:
            condition[key.lower()] = msgDict(key)
        dataFields = ["day","date","labourerid","labourername","labouercategory","labourertype","intime","outtime","numberofhours","overtimeallocated","overtimeworked","siteid","projectid"]
        self.log.logEvent("Admin",2,"attendance filtering geting")
        try:
            responseData =  adminDb.fetchData("attendance",dataFields,condition)
            response = {"Header":{"status":"success","module":"attendance"},"Body":{"message":"filtered attendance","data":responseData},"Signature":{"signature":"","Key":""}}
            return response        
        except Exception as expc:
            # self.syslog.eventHandle("attendanceManage","exception","exception on attendanceManage module",str(expc))
            self.log.logEvent("attendanceManage",3," all role permission listed occured "+str(expc))            