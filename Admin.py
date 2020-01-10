from DBAgent import DatabaseAgent
import datetime
import Exceptions 
from Authentication import Authentication
from ApplicationLogger import Logger
import sessionMange
import conf
class Admin:        
    def __init__(self):
        self.log = Logger()
        self .authen = Authentication()
    
    def addUser(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        digest = self.authen.signUp(msgDict["password"])
        msgDict["password"] = digest["hashPassword"]
        msgDict["salt"] = digest["salt"]
        print("message",msgDict)
        # admin = Admin()
        nameLs = []
        valueLs = []
        for key,val in msgDict.items():
            nameLs.append(key.lower())
            valueLs.append(val)
        print(nameLs)
        print(valueLs)
        reval = False
        try:
            if not adminDb.fetchData("clientusers",["username"],{"username":msgDict["userName"]}):
                if adminDb.pushData ("clientusers", nameLs, valueLs):
                    self.log.logEvent("Admin",1,msgDict["userName"]+" Client user registerd successfully",clientId,msgDict["userName"])
                    response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user added successfully","data":""},"Signature":{"signature":"","Key":""}}
                    return response
                else:
                    self.log.logEvent("Admin",1,msgDict["userName"]+"Client user registerd failed and eception is occured")
                    response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user can't added ","data":""},"Signature":{"signature":"","Key":""}}
                    return response
            else:
                self.log.logEvent("Admin",1,msgDict["userName"]+"Client user name alraedy exist",clientId,msgDict["userName"])
                response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user name already exixt ","data":""},"Signature":{"signature":"","Key":""}}
                return response                
                                    
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc))    
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))               
        
            
    def login(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        fileds = ["username","password"]
        con = {"clientid":clientId}
        data = masterDb.fetchData("regusers",fileds,con)
        print("........................",data)
        datalis = [clientId,clientId,data[0][1],5432]
        print("...datalis...........",datalis)
        adminDb = DatabaseAgent(clientId, clientId, conf.host,data[0][1], 5432)
        adminDb.initConnection()        
        try:
            statusFlag = masterDb.fetchData("regusers",["status"],{"clientid":clientId})
            if statusFlag[0][0] == "approved":
                #####################################################################  
                filedLs = ["password","salt","employeeid","userrole"]              
                if self.authen.login(msgDict,"clientusers",filedLs,datalis,sessionkey):
                    adminDb = DatabaseAgent(clientId, clientId, conf.host,data[0][1], 5432)
                    adminDb.initConnection()                
                    userid = adminDb.fetchData("clientusers",["employeeid"],{"username":msgDict["userName"]})
                    archiveflag = adminDb.fetchData("clientusers",["archive"],{"username":msgDict["userName"]})
                    print("boolean value",archiveflag)
                    if archiveflag:
                        self.log.logEvent("Admin",3,"user logined suceessfully",clientId,msgDict["userName"])                
                        response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user login successfully","data":userid},"Signature":{"signature":"","Key":""}}
                        return response
                    else:
                        self.log.logEvent("Admin",3,"your archived please connact to the admin",clientId,msgDict["userName"])
                        response = {"Header":{"status":"fail","module":"admin"},"Body":{"message":"your archived please connact to the admin","data":""},"Signature":{"signature":"","Key":""}}
                        return response                         
                else:
                    self.log.logEvent("Admin",3,"user logined error",clientId,msgDict["userName"])
                    response = {"Header":{"status":"fail","module":"admin"},"Body":{"message":"wrong username or password","data":""},"Signature":{"signature":"","Key":""}}
                    return response   

            elif statusFlag[0][0] == "rejected":
                self.log.logEvent("Admin",3,"comapny is rejected",clientId,msgDict["userName"])
                response = {"Header":{"status":"fail","module":"admin"},"Body":{"message":"your comapny is rejected","data":""},"Signature":{"signature":"","Key":""}}
                return response                    

            else:
                self.log.logEvent("Admin",3,"comapny has not been approved",clientId,msgDict["userName"])
                response = {"Header":{"status":"fail","module":"admin"},"Body":{"message":"your comapny has not been approved","data":""},"Signature":{"signature":"","Key":""}}
                return response                

        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,msgDict["userName"])
            # self.syslog.eventHandle("admin","exception","exception on admin module"+str(expc))               
            


    def editUser(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)   
        adminDb.initConnection()
        condition = {"employeeid": msgDict["employeeId"]}
        changDist = {}
        
        for key in msgDict:
            if key == "emplyeeId":
                continue
            else:
                changDist[key.lower()] = (msgDict[key])
        try:

            if adminDb.editData("clientusers",changDist,condition):
                self.log.logEvent("Admin",2,msgDict["employeeId"]+"user edited successfully",clientId,sessionMange.session[sessionkey]["userid"])
                # datalis = ["fullname","employeeid","designation","emailid","userrole",'archive']
                # adminDb.fetchData("clients",datalis)
                response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user deatils edited successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response

            else:
                self.log.logEvent("Admin",2,"user cant edited",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user deatils can't edited ","data":""},"Signature":{"signature":"","Key":""}}
                return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))                         


    def deleteUser(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        delete = " set delete = 'True' where "
        datdict = {"employeeid":msgDict["employeeId"]}
        try:
            if msgDict["employeeId"] == "kcemp1001":
                response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"admin can't be delete","data":""},"Signature":{"signature":"","Key":""}}
                return response       
            else:          
                if adminDb.updateTable(delete,"clientusers",datdict):
                    self.log.logEvent("Admin",2,msgDict["employeeId"]+"Client user deletd successfully",clientId,sessionMange.session[sessionkey]["userid"])
                    response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user delete successfully","data":""},"Signature":{"signature":"","Key":""}}
                    return response          #self.listClientUser()
                else:
                    self.log.logEvent("Admin",2,msgDict["employeeId"]+"Client can't user deleted ",clientId,sessionMange.session[sessionkey]["userid"])            
                    response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user can't delete","data":""},"Signature":{"signature":"","Key":""}}
                    return response 
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))               

            

    def archiveUser(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        archive = " set archive = 'True' where "
        admin = Admin()
        datdict = {"employeeid":msgDict["employeeId"]}
        try:
            if msgDict["employeeId"] == "kcemp1001":
                response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"admin can't be archived","data":""},"Signature":{"signature":"","Key":""}}
                return response    
            else:             
                if adminDb.updateTable(archive,"clientusers",datdict):
                    self.log.logEvent("Admin",2,msgDict["employeeId"]+"Client archived successfully",clientId,sessionMange.session[sessionkey]["userid"])
                    response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user archived successfully","data":""},"Signature":{"signature":"","Key":""}}
                    return response

                else:
                    self.log.logEvent("Admin",2,msgDict["employeeId"]+"Client canot archived",clientId,sessionMange.session[sessionkey]["userid"])
                    response = {"Header":{"status":"fail","module":"admin"},"Body":{"message":"user can't archived ","data":""},"Signature":{"signature":"","Key":""}}
                    return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,msgDict["employeeId"])
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc)               

    def unArchiveUser(self,clientId,msgDict,):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        archive = " set archive = 'False' where "
        admin = Admin()
        datdict = {"employeeid":msgDict["employeeId"]}
        try:        
            if adminDb.updateTable(archive,"clientusers",datdict):
                self.log.logEvent("Admin",2,msgDict["employeeId"]+"Client archived successfully",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user unarchived successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response
            else:
                self.log.logEvent("Admin",2,msgDict["employeeId"]+"Client canot archived",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"admin"},"Body":{"message":"user can't unarchived ","data":""},"Signature":{"signature":"","Key":""}}
                return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))                         

    def editList(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        condition ={"employeeid":msgDict["employeeId"]}
        datalis = ["fullname","employeeid","designation","emailid","userrole",'archive']
        cliList = adminDb.fetchData("clientusers",datalis,condition)
        infolist = []
        try:
            for info in cliList:
                for tup in info:
                    infolist.append(tup)
            role = adminDb.fetchData("permission",["rolename","roleid"])
            infolist.append(role)
            self.log.logEvent("Admin",2,"edit button wanted listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user edit list","data":infolist},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))               





    def roleList(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        self.log.logEvent("Admin",2,"total permission list listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
        try:
            responseData = adminDb.fetchData("permission",["rolename","roleid"])
            response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user role list","data":responseData},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))                     

    def listClientUser(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        print(".................",dbData)
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        datalis = ["fullname","employeeid","designation","userrole",'archive']
        self.log.logEvent("Admin",0,"Client user listed successfully",clientId,sessionMange.session[sessionkey]["userid"])
        try:
            responseData = adminDb.fetchData("clientusers",datalis)
            print("dbdata is................................",responseData)
            response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user list","data":responseData},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))               

    def userProfile(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        dbCompanyname = masterDb.fetchData("regusers",["companyname"],cond)
        print(".................",dbData)
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        conditions = {"employeeid":msgDict["employeeId"]}
        detail =["fullname","employeeid","userrole","designation"]
        self.log.logEvent("Admin",0,"user profile showed",clientId,msgDict["employeeId"])
        try:
            responseData =  adminDb.fetchData("clientusers",detail,conditions)
            print("response data",responseData)
            responseData.append(dbCompanyname[0][0])
            response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"user profile","data":responseData},"Signature":{"signature":"","Key":""}}
            return response        
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))               




######################################################companyprofile#######################################################
        
    def companyProfile(self,clientId,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        try:
            compnydata = self.fetchCompanySummary(adminDb)

            projectsColl = self.fetchProjectsSummary(adminDb)

            finalList = []
            finalList.append(list(compnydata))
            finalList.append(list(projectsColl))
            self.log.logEvent("Admin", 2, "Company pofile sended successfully",clientId,sessionMange.session[sessionkey]["userid"])
            print("final list is...",finalList)
            response = {"Header":{"status":"success","module":"admin"},"Body":{"message":"companyprile","data":finalList},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))                     

    def fetchCompanySummary(self,dbAgent):
        condition = {"userrole":"Admin"}
        dataList = ["fullname", "employeeid", "designation","companyname"]
        try:
            return dbAgent.fetchData("clientusers", dataList,condition)
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))                          

    def fetchProjectsSummary(self,dbAgent):
        projCollection = []
        projectData= dbAgent.fetchData("projects", ["Projectname","projectid"])
        # print("\n\n\n")
        try:
            for i in range(len(projectData)):
                cond ={"projectid":projectData[i][1]}
                curSite = dbAgent.fetchData("sites", ["sitenames"], cond)
                lCount = dbAgent.fetchData("sites", ["numOfLabourer"], cond)
                # print("\n\n\nSites:::::::::::: ", curSite)
                # print("\nSites:::::::::::::: ", curSite[0])
                # print("\nSites:::::::::::::: ", curSite[0][0])
                projectSummary = [[], []]

                for j in range(len(curSite)):
                    # print ("\n\n\n\nJ:::::::    ", j)
                    sitesList = curSite[j][0]
                    labourerList = lCount[j][0]
                    projectSummary[-1].append(sitesList)
                    projectSummary[-2].append(labourerList)

                projectSummary.insert(0, projectData[i][0])            
                projCollection.append(projectSummary)
                #del labourerList[:]
                #del sitesList[:]
                # print("Project Summary:::::::::::::::::::::::::::::::: ", projectSummary)
                # print("sites..........  ",sitesList)
                # print("lab........................  ",labourerList)
                # print("\n\n\n")

            print("PROJECTS CONTAINER:::::::::::::::::::::::::: ", projCollection)

            return projCollection
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),clientId,sessionMange.session[sessionkey]["userid"])    
            # self.syslog.eventHandle("admin","exception","exception on admin module",str(expc))                   


#################################################################permissions#########################################



##################################################################attendance############################################################################


######################################################################company management################################################


        
            












        # try:
        #     reval
            
        # except Exception as expc:
        #     print("oocured exception is",expc)
        


# admin = Admin()
# print("companyprofile.....",admin.companyProfile("kec119","karthiban"))

# # print(admin.classList("sessionkey"))
# # # print("....................",admin.labbourerAddlist("karthiban"))
# # admin.roleList("sessionkey")
# # print("list is..........",admin.listRoles("sessionkey"))
# # print("datasss.....................................",admin.listRoles())

# # sessions["xyzabcd"] = ["karthiban","karthi007"]

# # # admin.adminRegister({"userName":"karthiban","fullName":"karthibanvediraj","emailId":"karthiban1234@gmail.com","companyName":"admin","employId":"k1551","designation":"softwaredeveloper","password":"karthi567"})
# # admin.createRoles()
# # ###################labourer reg###################################
# # data = {"labourername":"spartan","callbyname":"spartan","gender":"male","dateofbirth":"07/07/1997","fathername":"spartan","bloodgroup":"a1+","nextofkin":"ben","contactnumberofnextofkin":"155525145522","mothertounge":"tamil","addressline1":"address","addressline2":"somthing2","addressline3":"somthing","village":"newyear","state":"newyark","country":"usa","pincode":"600000" ,"mobilenumber":"666575454654656","residancephonenumber":"456518555472320","emergencyphonenumber":"45545554360","dateofjoining":"09/04/1993" ,"migrantworker":"yes" ,"siteid":"usa" ,"siteofjoining":"05/03/2019","designation":"admin","labourerclass":"best","wageclass":"good","documenttype":"adhar","documentnumber":"2585685758120","nameasperdoc":"spartan","bankname":"national","ifsccode":"55365845435520","backaccountnumber":"546546544420","brancname":"usa","nameinbank":"indian"}
# # print("datais",admin.labourerReg(data))
# ###############################################labourerlist########################################
# #print("list labourer",admin.labourerInfo())
# ######################labourer change##############################################################
# # data = {"labourerId":""}
# shift = {"shiftstart":"12:00","shiftend":"07:00","break1start":"00:00","break1end":"04:00","lunchbreakstart":"03:00","lunchbreakend":"00:00","break2start":"00:00","break2end":"04:00"}
# # admin.labourerChange()
# admin.shiftCreation(shift,"sessionkey")
# #print("list of shift",admin.shiftList())
# # shiftedit = {"shiftId":"shift1001","lunchstart":"07:00"}
# # print("list of shift",admin.shiftEdit(shiftedit))
# # shiftdelete = {"shiftId":"shift1003"}
# # print("list of shift",admin.shiftDeleted(shiftdelete))
# # print("company profile page",admin.shiftAssingn(shiftdelete))
# # print("njnkjnbkjbkjbkj",admin.companyProfile())
# # 