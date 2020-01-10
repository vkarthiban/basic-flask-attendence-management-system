from DBAgent import DatabaseAgent
import datetime
import Exceptions 
from Authentication import Authentication
from ApplicationLogger import Logger
import sessionMange
import conf

class labbourerManage:

    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()


    def labourerReg(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        nameLs = []
        valueLs = []
        for key,val in msgDict.items():
            nameLs.append(key.lower())
            valueLs.append(val)
        try:
            siteid = adminDb.fetchData("sites",["siteid"],{"sitenames":msgDict["siteOfJoining"]})
            nameLs.append("siteid")
            valueLs.append(siteid[0])
            if adminDb.pushData("labourer",nameLs,valueLs):
                self.log.logEvent("labourerManage",2,"labourer added successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer added successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response            

            else:
                self.log.logEvent("labourerManage",2,"labourer can't added",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labourerManage"},"Body":{"message":"labourer can't added","data":""},"Signature":{"signature":"","Key":""}}
                return response   
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])

        
    def labouerList(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        try:
            labourerData = ["labourername","labourerid","projectname","siteid","labourerclass","shiftid"]
            self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData =  adminDb.fetchData("labourer",labourerData )
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer list","data":responseData},"Signature":{"signature":"","Key":""}}
            return response              
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])        



    def labourerInfo(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        conditiond = {"labourerid":msgDict["labourerId"]}
        try:
            labourdata = ["labourername","callbyname","gender","dateofbirth","fathername","bloodgroup","nextofkin","contactnumberofnextofkin","mothertounge","addressline1","addressline2","addressline3","village","state","country","pincode" ,"mobilenumber","residancephonenumber","emergencyphonenumber","dateofjoining" ,"migrantworker","designation","projectname" ,"siteid" ,"siteofjoining","labourerclass","shiftid","documenttype","documentnumber","nameasperdoc","bankname","ifsccode","branchname","bankaccountnumber","nameinbank","labourerid"]
            self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData = adminDb.fetchData("labourer",labourdata,conditiond)
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer info","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                 


    # def editList(self,clientId,msgDict,sessionkey):
    #     masterDb = DatabaseAgent("kunnel", "kunnel", conf.host, "kunnel123", conf.port)
    #     masterDb.initConnection()
    #     cond = {"clientid":clientId}
    #     dbData = masterDb.fetchData("regusers",["password"],cond)
    #     password = dbData[0][0]
    #     adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
    #     adminDb.initConnection()
    #     conditiond = {"labourerid":msgDict["labourerId"]}
    #     try:
    #         labourdata = ["labourername","callbyname","gender","dateofbirth","fathername","bloodgroup","nextofkin","contactnumberofnextofkin","mothertounge","addressline1","addressline2","addressline3","village","state","country","pincode" ,"mobilenumber","residancephonenumber","emergencyphonenumber","dateofjoining" ,"migrantworker","designation","projectname" ,"siteid" ,"siteofjoining","labourerclass","shiftid","documenttype","documentnumber","nameasperdoc","bankname","ifsccode","branchname","bankaccountnumber","nameinbank","labourerid"]
    #         self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
    #         responseData = adminDb.fetchData("labourer",labourdata,conditiond)
    #         response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer info","data":responseData},"Signature":{"signature":"","Key":""}}
    #         return response       
    #     except Exception as expc:
    #         # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
    #         self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  


    def personalInfo(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        conditiond = {"labourerid":msgDict["labourerId"]}
        try:
            personaldata = ["labourername","callbyname","gender","dateofbirth","fathername","bloodgroup","nextofkin","contactnumberofnextofkin","mothertounge","addressline1","addressline2","addressline3","village","state","country","pincode" ,"mobilenumber","residancephonenumber","emergencyphonenumber"]
            self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData = adminDb.fetchData("labourer",personaldata,conditiond)
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer info","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  


    def employeeInfo(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        conditiond = {"labourerid":msgDict["labourerId"]}
        try:
            employeedata = ["dateofjoining" ,"migrantworker","designation","projectname" ,"siteid" ,"siteofjoining","labourerclass","shiftid"]
            self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData = adminDb.fetchData("labourer",employeedata,conditiond)
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer info","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  


    def identityInfo(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        conditiond = {"labourerid":msgDict["labourerId"]}
        print("what is the exception/.............")
        try:
            identitydata = ["documenttype","documentnumber","nameasperdoc"]
            self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData = adminDb.fetchData("labourer",identitydata,conditiond)
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer info","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  


    def bankInfo(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        conditiond = {"labourerid":msgDict["labourerId"]}
        try:
            bankdata = ["bankname","ifsccode","branchname","bankaccountnumber","nameinbank"]
            self.log.logEvent("labourerManage",2,"labourer info showed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            responseData = adminDb.fetchData("labourer",bankdata,conditiond)
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer info","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                                               


    def editLabourer(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        condition = {"labourerid": msgDict["labourerId"]}
        changDist = {}
        for key in msgDict:
            if key == "labourerId":
                continue
            else:
                changDist[key.lower()] = (msgDict[key])

        try:
            if adminDb.editData("labourer",changDist,condition):
                self.log.logEvent("labourerManage",2,"labourer Edited success",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer edited successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response              

            else:
                self.log.logEvent("labourerManage",2,"labourer labourer can't ediot",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labourerManage"},"Body":{"message":"labourer canot edited","data":""},"Signature":{"signature":"","Key":""}}
                return response   
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                  

    def deleteLabourer(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        condition = {"labourerid": msgDict["labourerId"]}
        try:
            if adminDb.updateTable(delete,"labourer",condition):
                self.log.logEvent("labourerManage",2,"labourer deleted successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer deleted successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("labourerManage",2,"labourer deletd successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labourerManage"},"Body":{"message":"labouer cant deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response           
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])               
            

    def labourerChange(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        condition = {"labourerid":msgDict["labouerId"]}
        dataDict = {}
        try:        
            for key,val in msgDict:
                dataDict[key.lower()] = (msgDict[key])
            if adminDb.editData("labourer",dataDict,condition):
                self.log.logEvent("labourerManage",2,"labourer changed successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer changed successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response             
            else:
                self.log.logEvent("labourerManage",2,"labourer can't changed",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labourerManage"},"Body":{"message":"labbourer can't changed","data":""},"Signature":{"signature":"","Key":""}}
                return response  
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])                       
            
            
    def labbourerAddlist(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        total = []
        final = []
        projectData = adminDb.fetchData("projects",["projectname","projectid"]) 
        shiftList =[]
        proLs = []
        try:
            for cnt in range(len(projectData)):
                sitedb = adminDb.fetchData("sites",["sitenames"],{"projectid":projectData[cnt][1]}) 
                total.append([projectData[cnt][0],sitedb])
                # total.append(sitedb)
            final.append(list(total))
            print("projects",total)
            classdb = adminDb.fetchData("labourerclass",["labourerclass "])     #"compensation","Retention","Advance","Concrete_charges"
            final.append(classdb)
            print("\n\n\nclass",final)
            shiftdb = adminDb.fetchData("shift",["shiftid"])
            final.append(shiftdb)
            print("\n\n\n.......total",final)
            self.log.logEvent("labourerManage",0,"labourer addlist listed sucessfully",clientId,sessionMange.session[sessionkey]["userid"])                
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labbouerAddlist","data":final},"Signature":{"signature":"","Key":""}}
            return response 
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerMange",2,str(expc),clientId,sessionMange.session[sessionkey]["userid"])


            
# lab = labbourerManage()
# print("ststus",lab.advanceRespo("kec166",{"labourerId":"lab1001"}))age",2,"occured expection is"+str(expc))    


