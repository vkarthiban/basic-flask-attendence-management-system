from DBAgent import DatabaseAgent
import datetime
import Exceptions 
from Authentication import Authentication
import conf
from ApplicationLogger import Logger
import sessionMange

class shiftManage:

    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()

############################################################################shift management#############################################################
    def shiftCreation(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        nameLs = []
        valueLs = []
        for key in msgDict:
            nameLs.append(key)
            valueLs.append(msgDict[key])
        curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nameLs.append("shiftcreatedon")
        valueLs.append(curTime)
        reval = False
        try:
            reval = adminDb.pushData("shift",nameLs,valueLs)
            if reval:
                self.log.logEvent("shiftManage",2,"labourer shift created successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"ShiftManage"},"Body":{"message":"shift Added successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response                  
            else:
                self.log.logEvent("shiftManage",2,"labourer shift creation error",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"ShiftManage"},"Body":{"message":"shift can't created","data":""},"Signature":{"signature":"","Key":""}}
                return response      
        except Exception as expc:
            print("oocured exception is",expc)
            self.log.logEvent("shiftmanage",2,str(expc),clientId,sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("shiftmanage","exception","exception on shiftManage module",str(expc))          

    def shiftList(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        try:
            responseData =  adminDb.fetchData("shift","*")
            self.log.logEvent("shiftmanage",2,"labourer shift list",clientId,sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"ShiftManage"},"Body":{"message":"shift can't created","data":responseData},"Signature":{"signature":"","Key":""}}
            return response            
            
        except Exception as expc:
            # self.syslog.eventHandle("shiftmanage","exception","exception on shiftManage module",str(expc))          
            print("oocured exception is",expc)
        
        self.log.logEvent("shiftmanage",2,"labourer shift listed successfully",clientId,sessionMange.session[sessionkey]["userid"])

    # def shiftEdit(self,msgDict):
    #     adminDb = DatabaseAgent("admin", "admin", conf.host, "admin123", 5432)
    #     adminDb.initConnection()
    #     admin = Admin()
    #     condition = {"shiftid":msgDict["shiftId"]}
    #     changDict = {}
    #     for key in msgDict:
    #         if key == "shiftId":
    #             continue
    #         else:
    #             changDict[key.lower()] = (msgDict[key])
    #             print("conditon",condition)
    #             print("datas",changDict)
    #     if adminDb.editData("shift",changDict,condition):
    #         self.log.logEvent("Admin",2,"labourer shift edited successfully")
    #         return admin.shiftList()

    #     else:
    #         self.log.logEvent("Admin",2,"labourer shift cant edited")
    #         return "shift creation error"
            
    def shiftDeleted(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        condition = {"shiftid":msgDict["shiftId"]}
        reval = False
        try:
            if adminDb.updateTable(delete,"shift",condition):
                self.log.logEvent("shiftManage",2,msgDict["shiftId"]+"labourer shift deleted successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"ShiftManage"},"Body":{"message":"shift deleted succes","data":""},"Signature":{"signature":"","Key":""}}
                return response            
            else:
                self.log.logEvent("shiftManage",2,msgDict["shiftId"]+"labourer shift cant deleted",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"ShiftManage"},"Body":{"message":"shift canot deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response     
        except Exception as expc: 
            print("oocured exception is",expc) 
            self.log.logEvent("shiftmanage",2,"labourer shift delete successfully",clientId,sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("shiftmanage","exception","exception on shiftManage module",str(expc))    

    def shiftAssingn(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        changDict = {"shiftid":msgDict["shiftId"]}
        condition = {}
        for key in msgDict:
            condition[key.lower()] = (msgDict[key])
            self.log.logEvent("shiftManage",2,"shift assigned successfully",clientId,sessionMange.session[sessionkey]["userid"])
        reval = False
        try:
            reval = adminDb.editData("labourer",changDict,condition)
            
        except Exception as expc:
            # self.syslog.eventHandle("shiftmanage","exception","exception on shiftManage module",str(expc))    
            print("oocured exception is",expc)

        if reval:
            self.log.logEvent("shiftManage",2,"shift can't assigned ",clientId,sessionMange.session[sessionkey]["userid"]) 
            return "shift assingend successfully"                  #admin.labouerList()

