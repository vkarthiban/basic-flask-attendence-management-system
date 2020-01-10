from DBAgent import DatabaseAgent
import datetime
import Exceptions 
import conf
from Authentication import Authentication
from ApplicationLogger import Logger
import sessionMange
class roleManage:

    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()

    def createRoles(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        valuelist = []
        templist = []
        valuelist.append(msgDict["roleName"])
        for key in msgDict:
            if key  == "roleName":
                continue
            else:
                templist.append(msgDict[key])
        bigstr = ""
        for val in templist:
            bigstr += val+"&&" 
        valuelist.append(bigstr)
        try:
            if adminDb.pushData("permission",["rolename","permissions"],valuelist):
                self.log.logEvent("roleManage",2,"Client role created successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"roleMange"},"Body":{"message":"role created successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response
            else:
                self.log.logEvent("roleManage",2,"Client role creation db error occured",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"roleManage"},"Body":{"message":"role can't created","data":""},"Signature":{"signature":"","Key":""}}
                return response
        except Exception as expc:
            # self.syslog.eventHandle("rolemanagement","exception","exception on rolemanage module",str(expc))               
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])

    def editRoles(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        changDict = {}
        templist = []
        valueList = []
        for key in msgDict:
            if key  == "roleName":
                continue
            elif key == "roleId":
                continue
            else:
                templist.append(msgDict[key])
        bigstr = ""
        for val in templist:
            bigstr += val+"&&" 
        # valuelist.append(bigstr)
        changDict["rolename"] = (msgDict["roleName"])
        changDict["roleid"] = (msgDict["roleId"])
        changDict["permissions"] = (bigstr)
        condition ={"roleid":msgDict["roleId"]}
        print("total.......................................",changDict)
        reval = False
        try:
            if adminDb.editData("permission",changDict,condition):
                self.log.logEvent("roleManage",3,msgDict["roleId"]+"role permission edited successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"roleManage"},"Body":{"message":"user role edited successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response
            else:
                self.log.logEvent("roleManage",3,msgDict["roleId"]+"role permission canot edited ",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"roleManage"},"Body":{"message":"uerer role canot edit","data":""},"Signature":{"signature":"","Key":""}}
                return response
        except Exception as expc:
            # self.syslog.eventHandle("rolemanagement","exception","exception on rolemanage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])


    def listRoles(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        permiSdata = []
        try:
            permiSdata = adminDb.fetchData("permission",["rolename","roleid","permissions"])


            # out = [item for t in permiSdata for item in t] 
            print("database value is",permiSdata)
            out = []
            for t in permiSdata:
                out.append(list(t))

            # for cnt in range(2,len(out),+3):
            print("out",out)
            for cnt in range(len(out)):
                data = bytes(out[cnt][2])
                data1 = data.decode("utf-8")
                data2 = str(data1).split('&&')
                out[cnt][2] = data2
            self.log.logEvent("roleManage",3," all role permission listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"roleManage"},"Body":{"message":"uerer role list","data":out},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            # self.syslog.eventHandle("rolemanagement","exception","exception on rolemanage module",str(expc))
            self.log.logEvent("roleManage",3," all role permission listed occured exception is = "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])        


    def deleteRole(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        condition = {"roleid":msgDict["roleId"]}
        try:
            if self.adminDb.updateTable(delete,"permission",condition):
                self.log.logEvent("roleManage",3,msgDict["roleId"]+"role deleted  successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"roleManage"},"Body":{"message":"uerer role deleted successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response
            else:
                self.log.logEvent("roleManage",3,msgDict["roleId"]+"user prmiisson database error",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"roleManage"},"Body":{"message":"uerer role canot deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response
        except Exception as expc:
            # self.syslog.eventHandle("rolemanagement","exception","exception on rolemanage module",str(expc))
            self.log.logEvent("roleManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                

