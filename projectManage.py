from DBAgent import DatabaseAgent
import datetime
import conf
import Exceptions 
from Authentication import Authentication
from ApplicationLogger import Logger
import sessionMange

class projectManage:
    
    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()

    def projectsAdding(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        # nameLs = []
        # valueLs = []
        # sites = ""
        # labourercnt = ""
        # for key in msgDict:
        #     if key == "locations":
        #         continue
        #     else:
        #         nameLs.append(key.lower())
        #         valueLs.append(msgDict[key])            
        # print("namels............",nameLs)
        # print("valuels...............",valueLs)
        try:
            if adminDb.pushData("projects",["projectname"],[msgDict["projectName"]]):
                projectid = adminDb.fetchData("projects",["projectid"],{"projectname":msgDict["projectName"]})
                # for key in msgDict:
                #     if key == "locations":
                        # for cnt in range(len(msgDict["locations"])):
                adminDb.pushData("sites",["sitenames","numoflabourer","projectid","compensationamount","compensationdays","concreteamount","debitaccountid","creditaccountid"],[msgDict["siteNames"],msgDict["numOfLabourer"],projectid[0],msgDict["compensationAmount"],msgDict["compensationDays"],msgDict["concreteAmount"],msgDict["debitAccountId"],msgDict["creditAccountId"]])
                self.log.logEvent("projectManage",2,msgDict["projectName"]+" project added successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project added successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response             
            else:
                self.log.logEvent("Admin",2,msgDict["projectName"]+" project canot added",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"projectManage"},"Body":{"message":"project can't added","data":""},"Signature":{"signature":"","Key":""}}
                return response
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])        


    def listProjects(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        totalLs  = []
        datalis = ["projectname,projectid"]
        siteinfo = ["sitenames","siteid","numoflabourer","compensationamount","compensationdays","concreteamount","debitaccountid","creditaccountid"]
        self.log.logEvent("projectManage",0,"project listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
        try:
            projectData = adminDb.fetchData("projects",datalis) 
            print ("Project Names and ID : ", projectData)
            print ("Length od Project Data : ", len(projectData))
            for cnt in range(len(projectData)):
                print("Count: ", cnt)
                ls = adminDb.fetchData("sites",siteinfo,{"projectid":projectData[cnt][1]})
                print ("List: ", ls)

                totalLs.append([projectData[cnt][0], projectData[cnt][1]])

                totalLs[-1].append(list(ls))
                print("TotalLs: ", totalLs)

            response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project list","data":totalLs},"Signature":{"signature":"","Key":""}}
            return response     
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])            

    def editList(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        totalLs  = []
        datalis = ["projectname,projectid"]
        siteinfo = ["sitenames","siteid","numoflabourer","compensationamount","compensationdays","concreteamount"]
        self.log.logEvent("projectManage",0,"project listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
        try:
            projectData = adminDb.fetchData("projects",datalis,{"projectid":msgDict["projectId"]}) 
            print ("Project Names and ID : ", projectData)
            print ("Length od Project Data : ", len(projectData))
            for cnt in range(len(projectData)):
                print("Count: ", cnt)
                ls = adminDb.fetchData("sites",siteinfo,{"projectid":projectData[cnt][1]})
                print ("List: ", ls)

                totalLs.append([projectData[cnt][0], projectData[cnt][1]])

                totalLs[-1].append(list(ls))
                print("TotalLs: ", totalLs)

            response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project list","data":totalLs},"Signature":{"signature":"","Key":""}}
            return response     
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])            


    def editProjects(self,clientId,msgDict):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        condition = {"projectid":msgDict["projectId"]}
        changDist = {}
        for key in msgDict:
            if "projectId" == key:
                continue
            else:
                changDist[key.lowe()] = (msgDict[key])
        try:
            if adminDb.editData("projects",changDist,condition):
                self.log.logEvent("projectManage",0,"project edited successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project edited successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response 
            else:
                self.log.logEvent("projectManage",0,"project database error ",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"projectManage"},"Body":{"message":"project can't edited","data":""},"Signature":{"signature":"","Key":""}}
                return response 
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])            


    
     

    def deleteProjects(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        condition = {"projectid":msgDict["projectId"]}
        try:
            if adminDb.updateTable(delete,"projects",condition) and adminDb.updateTable(delete,"sites",condition):
                self.log.logEvent("projectManage",3,"project deleted successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project deleted successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response 
            else:
                self.log.logEvent("projectManage",3,"project deleted db error occured",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"projectManage"},"Body":{"message":"project can't deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response 
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])            

    def filterProjects(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        # condiotion ={"delete ":"False"}
        condition = {}
        try:
            for key in msgDict:
                condition[key.lower()] = msgDict(key)
            datalis = ["projectname,projectlocations,projectlabourers,projectid,siteid"]
            self.log.logEvent("projectManage",0,"project listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData =  adminDb.fetchData("projects",datalis,condition)  
            response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project filterd","data":responseData},"Signature":{"signature":"","Key":""}}
            return response 
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 

    def addSites(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        nameLs = []
        valuels = []
        try:
            for key in msgDict:
                nameLs.append(key.lower())
                valuels.append(msgDict[key])
            if adminDb.pushData("sites",nameLs,valuels):
                self.log.logEvent("projectManage",2,"project added successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"site added sucessfully","data":""},"Signature":{"signature":"","Key":""}}
                return response
            else:
                self.log.logEvent("projectManage",2,"project can't added",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"site can't added","data":""},"Signature":{"signature":"","Key":""}}
                return response

        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3," all role permission listed occured "+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 

    def  deletSites(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId,clientId,conf.host,password,5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        try:
            if adminDb.updateTable(delete,"sites",{"siteid":msgDict["siteId"]}):
                self.log.logEvent("projectManage",3,"project deleted successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"site deleted sucessfully","data":""},"Signature":{"signature":"","Key":""}}
                return response                 
            else:
                self.log.logEvent("projectManage",0,"project can't delete",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"projectManage"},"Body":{"message":"site can't deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response 
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3,str(expc),clientId,sessionMange.session[sessionkey]["userid"])

                


    def projectIdList(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId,clientId,conf.host,password,5432)
        adminDb.initConnection()
        try:
            responseData = adminDb.fetchData("projects",["projectid"]) 
            self.log.logEvent("projectManage",0,"projectId  listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"projectManage"},"Body":{"message":"project idlist","data":responseData},"Signature":{"signature":"","Key":""}}
            return response  
        except Exception as expc:
            # self.syslog.eventHandle("projectmanagement","exception","exception on projectManage module",str(expc))
            self.log.logEvent("projectManage",3,str(expc),clientId,sessionMange.session[sessionkey]["userid"])                      

        
                
            






# pro = projectManage()
# pro.listProjects("kec119","karthi007")