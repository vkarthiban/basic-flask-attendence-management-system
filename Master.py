from DBAgent import DatabaseAgent
from ApplicationLogger import Logger
from Authentication import Authentication
import sessionMange
# from sysloggeer import syslogger
import json
import random
import conf
import uuid
class Master:

    def __init__(self):
        self.masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        self.masterDb.initConnection()
        self.log = Logger()
        self.authen = Authentication()
        # self.syslog = syslogger()



    def createMaster(self, msgDict,sessionkey):
        digest = self.authen.signUp(msgDict["password"])
        msgDict["password"] = digest["hashPassword"]
        msgDict["salt"] = digest["salt"]
        print("message",msgDict)
        nameLs = []
        valueLs = []
        for key,val in msgDict.items():
            nameLs.append(key.lower())
            valueLs.append(val)
        print(nameLs)
        print(valueLs)
        nameLs.append("userrole")
        valueLs.append("Admin")
        try:
            if self.masterDb.pushData("master", nameLs, valueLs):
                self.log.logEvent("Master",1,msgDict["userName"]+"master registerd successfully","master","mater register")
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"master signuped successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response            
            else:
                self.log.logEvent("Master",1,msgDict["username"]+"master registerd faild","master","mater register")
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"master signup error","data":""},"Signature":{"signature":"","Key":""}}
                return response    
        except Exception as excp:
            self.log.logEvent("Master",3,"occured exception is "+str(excp),"master","mater register")  
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))          
            print("occured expection is",excp)

    def login(self,msgDict,sessionkey):
        print("sesssion.............................................",msgDict)
        dbConfig = [conf.mdbName,conf.muserName,conf.mdbPassword,conf.port] 
        try:
            filedLs = ["password","salt","userid","userrole"]
            if self.authen.login(msgDict,"master",filedLs,dbConfig,sessionkey):
                self.log.logEvent("Master",1,msgDict["userName"]+"login successed","master",sessionMange.session[sessionkey]["userid"])
                print("login userid.....",sessionMange.session[sessionkey]["userid"])
                userid = self.masterDb.fetchData('master',['userid'],{'username':msgDict['userName']})
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"login successfully","data":userid},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Master",1,msgDict["userName"]+"login error","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":" wrong username or password","data":""},"Signature":{"signature":"","Key":""}}
                return response     
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])        
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))       
            print("occured expection is",excp)                      


        

    def addUser(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        digest = self.authen.signUp(msgDict["password"])
        msgDict["password"] = digest["hashPassword"]
        msgDict["salt"] = digest["salt"]
        print("message",msgDict)
        ma = Master()
        nameLs = []
        valueLs = []
        for key,val in msgDict.items():
            nameLs.append(key.lower())
            valueLs.append(val)
        print(nameLs)
        print(valueLs)
        try:
            if not self.masterDb.fetchData("master",["username"],{"username":msgDict["userName"]}): 
                if self.masterDb.pushData("master", nameLs, valueLs):
                    self.log.logEvent("Master",1,msgDict["userName"]+"master user added successfully","master",sessionMange.session[sessionkey]["userid"])
                    response = {"Header":{"status":"success","module":"master"},"Body":{"message":"useradded successfully","data":""},"Signature":{"signature":"","Key":""}}
                    return response              
                else:
                    self.log.logEvent("Master",1,msgDict["userName"]+"Master user Addeding error","master",sessionMange.session[sessionkey]["userid"])
                    response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user canot added","data":""},"Signature":{"signature":"","Key":""}}
                    return response
            else:
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user name already exist","data":""},"Signature":{"signature":"","Key":""}}
                return response                

        except Exception as excp:
            self.log.logEvent("Master",3,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])     
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))          
            print("occured expection is",excp)                          

            
        


    def editUser(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        condition = {"userid": msgDict["userId"]}
        changDist = {}
        for key in msgDict:
            if key == "userId":
                continue
            else:
                changDist[key.lower()] = (msgDict[key])
        try:

            if self.masterDb.editData("master",changDist,condition):
                ma = Master()
                self.log.logEvent("Master",2,msgDict["userId"]+"User_details Edited","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"userdetails edited successfully" ,"data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Master",2,msgDict["userId"]+"User_details canot Edited","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user details canot be edited","data":""},"Signature":{"signature":"","Key":""}}
                return response     
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])     
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))          
            print("occured expection is",excp)                   

    def mastereditList(self,msgDict,sessionkey):
        try:
            masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterDb.initConnection()
            condition ={"userid":msgDict["userId"]}
            datalis = ["fullname","userid","emailid","userrole",'archive']
            cliList = masterDb.fetchData("master",datalis,condition)
            print("clilsit",msgDict)
            infolist = []
            self.log.logEvent("master",2,"edit button wanted listed successfully","master",sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"master"},"Body":{"message":"user edit list","data":cliList},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            self.log.logEvent("Admin",0,"occured exception is "+str(expc),"master",sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   



    def listUser(self,sessionkey):
        print("sesssion.............................................",sessionkey)
        datalis = ["fullname","userid","userrole","archive"]
        #print("............................................................................./////////////////////",sessionMange.session["username"])
        try:
            responseData = self.masterDb.fetchData("master",datalis)
            self.log.logEvent("Master",0,"listed all comaster details","master",sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"master"},"Body":{"message":"userlist","data":responseData},"Signature":{"signature":"","Key":""}}
            return response          
        except Exception as excp:
            self.log.logEvent("Master",0,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])    
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))           
            print("occured expection is",excp) 
                                 



    def deleteUser(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        datdict = {}
        delete = " set delete = 'True' where " 
        for key in msgDict:
            datdict[key.lower()] = (msgDict[key])

        try:

            if self.masterDb.updateTable(delete,"master",datdict):
                ma = Master()
                self.log.logEvent("Master",2,msgDict[key]+"master user deleted successfully","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"user deleted successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:

                self.log.logEvent("Master",2,msgDict[key]+" canot masteruser deleted","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user cant deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response    
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"]) 
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))              
            print("occured expection is",excp)                



    def archiveUser(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        archive = " set archive = 'True' where " 
        datdict = {"userid":msgDict["userId"]}
        try:
            if self.masterDb.updateTable(archive,"master",datdict):
                self.log.logEvent("Master",2,msgDict["userId"]+"master user is archived","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"user archived successfully" ,"data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Master",2,msgDict["userId"]+"master user is canot archived","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user canot archived","data":""},"Signature":{"signature":"","Key":""}}
                return response       
        except Exception as excp:
            print("occured expection is",excp)  
            self.log.logEvent("Master",2,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))             

    def unArchiveUser(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        archive = " set archive = 'False' where " 
        datdict = {"userid":msgDict["userId"]}
        try:
            if self.masterDb.updateTable(archive,"master",datdict):
                self.log.logEvent("Master",2,msgDict["userId"]+"master user is archived","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"user unarchived successfully" ,"data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Master",2,msgDict["userId"]+"master user is canot archived","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user canot unarchived","data":""},"Signature":{"signature":"","Key":""}}
                return response       
        except Exception as excp:
            print("occured expection is",excp)  
            self.log.logEvent("Master",2,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])   
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))     


##############################################client users##################################################################################

    def adminRegister(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        digest = self.authen.signUp(msgDict["password"])
        msgDict["password"] = digest["hashPassword"]
        msgDict["salt"] = digest["salt"]
        print("message",msgDict)
        nameLs = []
        valueLs = []
        name =""
        for key,val in msgDict.items():
            if key == "employeeId":
                continue
            else:
                nameLs.append(key.lower())
                valueLs.append(val)
        nameLs.append("userrole")
        valueLs.append("Admin")
        print(nameLs)
        print(valueLs)
        self.log.logEvent("Admin",1,msgDict["userName"]+"Client Admin registerd successfully","master","adminregister")
        dbcondtion = {"username":msgDict["userName"]}
        uslist = ["username"]
        password1 = str(random.randint(100000000,10000000000))
        password = "kec"+password1
        reglist = ["username","fullname","password","companyname","employeeid"]
        regval = [msgDict["userName"],msgDict["fullName"],password,msgDict["companyName"],msgDict["employeeId"]] 
        # try:
        if not self.masterDb.fetchData("regusers",uslist,dbcondtion):
            if self.masterDb.pushData("regusers",reglist,regval):
                condition = {"username":msgDict["userName"]}
                clidbnamedb = self.masterDb.fetchData("regusers",["clientid"],condition)
                print("db..........................................................................",clidbnamedb)
                clidbname = clidbnamedb[0][0]
                userid = self.admintablecreation(clidbname,password,nameLs,valueLs,msgDict["userName"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"admin signuped successfully","data":userid},"Signature":{"signature":"","Key":""}}
                return response                     
            else:
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"admin can't registerd","data":""},"Signature":{"signature":"","Key":""}}
                return response  
        else:
            response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user is alraeday existdb level","data":""},"Signature":{"signature":"","Key":""}}
            return response  
        # except Exception as excp:
        #     print("occured expection is ",excp)
        #     self.log.logEvent("Master",3,"occured exception is "+str(excp))   
        #     # self.syslog.eventHandle("master","exception","exception on master module",str(excp))            

    def admintablecreation(self,clidbname,password,nameLs,valueLs,userName):
        # try:
        if self.masterDb.createDatabase(clidbname):
            print("pasword...................................................",password)
            if self.masterDb.roleCreate(clidbname,password):
                localdb = DatabaseAgent(clidbname,clidbname,conf.host,password,"5432")
                localdb.initConnection()
#######################################################clinetusers####################################################                            
                localdb.createSequnce("cliusersxx")
                clientusers = ["username","fullname","emailid","designation","userrole","companyname"]
                extracontent = ",id serial,password bytea,salt bytea,employeeid text default 'user' ||nextval('cliusersxx'),delete boolean default False,archive boolean default False,suspend boolean default False "                                                                                                      
                localdb.createTable("clientusers",clientusers,extracontent)
########              ###########################################################################shift table###############################################################
                localdb.createSequnce("shiftxxx")
                shiftcont = ",id serial,shiftid text default 'shift' ||nextval('shiftxxx'),delete boolean default False"
                shiftlist = ["shiftstart","shiftend","break1start","break1end","lunchbreakstart","lunchbreakend","break2start","break2end","shiftcreatedon"]
                localdb.createTable("shift",shiftlist,shiftcont)
########              #########################################################################labourerdatas########################################################################                
                localdb.createSequnce("labourerxx")
                extracon2 = ",id serial,labourerid text default 'labourer' ||nextval('labourerxx'),delete boolean default False"
                labourdata = ["labourername","callbyname","gender","dateofbirth","fathername","bloodgroup","nextofkin","contactnumberofnextofkin","mothertounge","addressline1","addressline2","addressline3","village","state","country","pincode" ,"mobilenumber","residancephonenumber","emergencyphonenumber","dateofjoining" ,"migrantworker" ,"siteid" ,"siteofjoining","projectname","designation","labourerclass","documenttype","documentnumber","nameasperdoc","bankname","ifsccode","bankaccountnumber","branchname","nameinbank","shiftid"]     #,"compensation","retention","advance","concreteCharges"]
                localdb.createTable("labourer",labourdata,extracon2)
########   #####################################################################labourerclass############################################################
                localdb.createSequnce("labclassxx")
                labclass = ["labourerclass","wageclass"]
                labclasscon = ",id serial,labourerclassid text default 'labclass' ||nextval('labclassxx'),delete boolean default False,compensation  boolean default False,Retention boolean default False,Advance boolean default False,Concretecharges boolean default False"
                localdb.createTable("labourerclass",labclass,labclasscon)
########              #################################################################attendance###############################################################################
                execon = ",delete boolean default False "
                attendance = ["day","date","labourerid","labourername","labourerclass","shiftid","labouercategory","labourertype","intime","outtime","numberofhours","overtimeallocated" ,"overtimeworked","siteid","projectid"]
                localdb.createTable("attendance",attendance,execon)
########              ####################################################################project####################################################
                localdb.createSequnce("projectxx")
                companyls = ["projectname"]
                execon1 = ",id serial,projectid text default 'proj' ||nextval('projectxx'),delete boolean default False"
                localdb.createTable("projects",companyls,execon1)
########   #################################################################sites###########################################################################
                localdb.createSequnce("sitexx")
                siteLs = ["sitenames","numoflabourer","projectid","compensationamount","compensationDays","concreteAmount","creditaccountid","debitaccountid"]
                siteCon = ",id serial,siteid text default 'site' || nextval('sitexx'),delete boolean default False"
                localdb.createTable("sites",siteLs,siteCon)
##############################################################################payment_transation#############################################################################                            
                
                # localdb.createSequnce("paymentxx")
                paylist = ["transationid","timestamp","projectid","siteid","amount","debitaccountid","creditaccountid","issuer","reciverid","details","resontype"]
                paycon = ",id serial,payflag boolean default False,delete boolean default False"
                localdb.createTable("payment",paylist,paycon)
################################################################################Accounts###############################################
                accountls = ["transationid","timestamp","projectid","siteid","creditaccountid","debitaccountid"] 
                acccont = ",delete boolean default False"                               
                localdb.createTable("account",accountls,acccont)
################################################################################################AccounrtrInfo###############################################
                AccountInfoLs = ["labourerid","timestamp","phonenumber","siteid","recoveryperiod","reson","approveid"]
                accInfocont = ",id serial,approvestatus text default 'unapprove',paystatus text default 'unpaied',delete boolean default False"
                localdb.createTable("accountinfo",AccountInfoLs,accInfocont)
#################################################permission########################################################################permissions################################################ 
                localdb.createSequnce("permxx")
                permissions = ["rolename"]
                permcont = ",id serial,permissions bytea,roleid text default 'role' ||nextval('permxx'),delete boolean default false"
                localdb.createTable("permission",permissions,permcont)
############################################clientusers datapush########################################################################reguersdatapushing#######################################################
                if localdb.pushData("clientusers",nameLs,valueLs): #and localdb.pushData("company",compyFileds,compyDatas):
                    print("success")
                    con0 = {" username":userName}
                    clientid =  self.masterDb.fetchData("regusers",["clientid",],con0)                    
                    userid = localdb.fetchData("clientusers",["employeeid"])
                    print("userrid is .................",userid[0])
                    upcont =" set userid = '"+userid[0][0] + "' where "
                    self.masterDb.updateTable(upcont,"regusers",con0)
                    return clientid
                else:
                    response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"admin cant created","data":""},"Signature":{"signature":"","Key":""}}
                    return response  
            else:
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"client tables canot createds ","data":""},"Signature":{"signature":"","Key":""}}
                return response  
        else:
            response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"admin database canot created","data":""},"Signature":{"signature":"","Key":""}}
            return response  
        # except Exception as excp:
        #     print("occured expection is ",excp)
        #     self.log.logEvent("Master",3,"occured exception is "+str(excp))   
        #     # self.syslog.eventHandle("master","exception","exception on master module",str(excp))  
            



        
    def getRegUserDetails(self,sessionkey):
        print("sesssion.............................................",sessionkey)
        wantlist = ["clientid","companyname","username","userid","employeeid","status"]
        try:
            responseData =  self.masterDb.fetchData("regusers",wantlist)
            self.log.logEvent("Master",0,"list all registered company details","master",sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"master"},"Body":{"message":"register user details","data":responseData},"Signature":{"signature":"","Key":""}}
            return response                      
        except Exception as excp:
            self.log.logEvent("Master",0,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   


    def clienteditList(self,msgDict,sessionkey):
        try:
            cond = {"clientid":msgDict["clientId"]}
            responseData = self.masterDb.fetchData("regusers",["companyname","clientid","fullname","employeeid","userid"],cond)
            self.log.logEvent("master",2,"editlist listed","master",sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client users list","data":responseData},"Signature":{"signature":"","Key":""}}
            return response      
        except Exception as excp:
            self.log.logEvent("Master",1,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])  
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))                  

    
    def rejectClients(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        master = Master()
        condition = {"clientid":msgDict["clientId"]}
        cancle = " set status = 'rejected' where "
        try:
            if self.masterDb.updateTable(cancle,"regusers",condition):
                self.log.logEvent("Master",3,msgDict["clientId"]+"rejected registered client","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client rejected successfully" ,"data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("master","3",msgDict["clientId"]+"client canot berejected","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":" client can't rejected","data":""},"Signature":{"signature":"","Key":""}}
                return response              
        except Exception as excp:
            self.log.logEvent("Master",1,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   
    
    def clientApprove(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        master = Master()
        condition = {"clientid":msgDict["clientId"]}
        cancle = " set status = 'approved' where "
        try:
            if self.masterDb.updateTable(cancle,"regusers",condition):
                self.log.logEvent("Master",3,msgDict["clientId"]+"Approved client company","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client approved successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response          
            else:
                self.log.logEvent("Master",3,msgDict["clientId"]+"canot Approved client company","master",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"client company canot approved","data":""},"Signature":{"signature":"","Key":""}}
                return response        
        except Exception as excp:
            self.log.logEvent("Master",1,"occured exception is "+str(excp),"master",sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   



    def editClient(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        condition = {"clientid":msgDict["clientId"]}
        changDist = {}
        for key in msgDict:
            if key == "clientId":
                continue
            elif key == "userId":
                continue
            else:
                changDist[key.lower()] = (msgDict[key])
        try:

            if self.masterDb.editData("regusers",changDist,condition):
                ma = Master()
                password = self.masterDb.fetchData("regusers",["password"],condition)
                admindb = DatabaseAgent(msgDict["clientId"],msgDict["clientId"],conf.host,password[0][0],conf.port)
                admindb.initConnection()
                adminDict ={}
                for key in msgDict:
                    if key in ["clientId","employeeId","userId"]:
                        continue
                    else:
                        adminDict[key.lower()] = (msgDict[key])
                print("admin dict",adminDict)
                if admindb.editData("clientusers",adminDict,{"employeeid":msgDict["userId"]}):
                    self.log.logEvent("Master",2,msgDict["clientId"]+"user details edited successfully","master",sessionMange.session[sessionkey]["userid"])     
                    response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client data is edited successfully" ,"data":""},"Signature":{"signature":"","Key":""}}
                    return response   
                else:
                    self.log.logEvent("Master",2,msgDict["clientId"]+"user details can't edited ","master",sessionMange.session[sessionkey]["userid"])     
                    response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client data is edited successfully but client db error occured" ,"data":""},"Signature":{"signature":"","Key":""}}
                    return response                       

                          
            else:
                self.log.logEvent("Master",2,msgDict["clientId"]+"canot edit client user details",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"canot client user edit ","data":""},"Signature":{"signature":"","Key":""}}
                return response    
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),sessionMange.session[sessionkey]["userid"])   
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))                     


    def deleteClient(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        datdict = {"clientid":msgDict["clienId"]}
        delete = " set delete = 'True' where " 
        for key in msgDict:
            datdict[key.lower()] = (msgDict[key])
        try:
            if self.masterDb.updateTable(delete,"regusers",datdict):
                self.log.logEvent("Master",2,msgDict["clientId"]+"delete client user",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client deleted successfully" ,"data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Master",2,msgDict["clientId"]+"delete client error",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message":"user cant deleted","data":""},"Signature":{"signature":"","Key":""}}
                return response  
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   


    def archiveClient(self,msgDict,sessionkey):
        print("sesssion.............................................",sessionkey)
        archive = " set archive = 'True' where " 
        datdict = {"clientid":msgDict["clientId"]}
    
        try:
            if self.masterDb.updateTable(archive,"regusers",datdict):
                master = Master()
                self.log.logEvent("Master",2,msgDict["clientId"]+"archived client user",sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"master"},"Body":{"message":"client archived successfully","data":""},"Signature":{"signature":"","Key":""}}
                return response              
            else:
                self.log.logEvent("Master",2,msgDict["clientId"]+"archived client user error")
                response = {"Header":{"status":"fail","module":"master"},"Body":{"message": "user canot archived","data":""},"Signature":{"signature":"","Key":""}}
                return response   
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   
        



#######################################################logs########################################################
    def fetchAppLogs(self,msgData,sessionkey):
        print("sesssion.............................................",sessionkey)
        try:
            if not msgData.__contains__("type"):
                msgData["type"] = ""
            if not msgData.__contains__("id"):
                msgData["id"] = 0
            responseData =  self.masterDb.fetchAppLogs(msgData["type"],msgData["id"])
            response = {"Header":{"status":"success","module":"master"},"Body":{"message":" applogs","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as excp:
            self.log.logEvent("Master",2,"occured exception is "+str(excp),sessionMange.session[sessionkey]["userid"])
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))   

    def fetchSysLogs(self,msgDict):
        try:
            if not msgDict.__contains__("type"):
                msgDict["type"] = ""
            if not msgDict.__contains__("id"):
                msgDict["id"] = 0
            responseData =  self.masterDb.totalSysloggs(msgDict["type"],msgDict["id"])
            print("response",responseData)
            response = {"Header":{"status":"success","module":"master"},"Body":{"message":" syslogs","data":responseData},"Signature":{"signature":"","Key":""}}
            return response       
        except Exception as excp:
            print("exception is",excp)
            self.log.logEvent("Master",2,"occured exception is "+str(excp),"sessionMange.session[sessionkey][userid]")
            # self.syslog.eventHandle("master","exception","exception on master module",str(excp))          









##############################################test part####################################################################
# master = Master()
# print(master.fetchAppLogs({"type":"","id":""},"karthiban"))
# print("system loggs",master.fetchSysLogs({"type":"","id":""}))
# master.fetchSysLogs({"type":"","id":""})
# master.getRegUserDetails()
# message1 = {"clientid":"kec101","username":"karthiban007"}
# print(master.editClient(message1))
# # print(master.deleteClient(message1))




















