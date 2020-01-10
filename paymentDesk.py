from DBAgent import DatabaseAgent
import conf
import random
import datetime
import hashlib
import sessionMange
from ApplicationLogger import Logger
class paymentDesk:

    def __init__(self):
        self.log = Logger()

    def requstList(self,clientId,sessionkey):
        try:
            masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterdb.initConnection()
            dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
            password = dbpass[0][0]
            admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
            admindb.initConnection()
            listAdvance = admindb.fetchData("accountinfo",["labourerid","phonenumber","reson","recoveryPeriod","approvestatus","approveid"])
            listpayment = admindb.fetchData("payment",["timestamp","projectid","siteid","amount","debitaccountid","resontype","creditaccountid"])
            totalLs =[]
            finalLS = []
            print("payment......",listpayment)
            print("advnavce list...........",listAdvance)
            for cnt in range(len(listAdvance)):
                totalLs = list(listAdvance[cnt]) + list(listpayment[cnt])
                finalLS.append(totalLs)

            response = {"Header":{"status":"success","module":"labfinace"},"Body":{"message":"labourer requstedAdvance list","data":finalLS},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
            print("exception is occured at",str(expc))


    def advancePayList(self,clientId,sessionkey):
        try:
            masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterdb.initConnection()
            dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
            password = dbpass[0][0]
            admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
            admindb.initConnection()
            listAdvance = admindb.fetchData("accountinfo",["labourerid","reson","recoveryPeriod","approvestatus","approveid","paystatus"])
            listpayment = admindb.fetchData("payment",["timestamp","projectid","siteid","amount"])
            totalLs =[]
            finalLS = []
            print("payment......",listpayment)
            print("advnavce list...........",listAdvance)
            for cnt in range(len(listAdvance)):
                totalLs = list(listAdvance[cnt]) + list(listpayment[cnt])
                finalLS.append(totalLs)

            response = {"Header":{"status":"success","module":"labfinace"},"Body":{"message":"labourer Advancepay list","data":finalLS},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
            print("exception is occured at",str(expc))


    def approvecodeList(self,clientId,msgDict,sessionkey):
        try:
            masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterdb.initConnection()
            dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
            password = dbpass[0][0]
            admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
            admindb.initConnection()
            listAdvance = admindb.fetchData("accountinfo",["labourerid","reson","recoveryPeriod","approvestatus","approveid","paystatus"],{"approveid":msgDict["approveId"]})
            timeStamp = admindb.fetchData("accountinfo",["timestamp"],{"approveid":msgDict["approveId"]})[0][0]
            print("time stamp............................",timeStamp)
            listpayment = admindb.fetchData("payment",["timestamp","projectid","siteid","amount"],{"timestamp":timeStamp})
            print("payment......",listpayment)
            print("advnavce list...........",listAdvance)
            totalLs =[]
            finalLS = []            
            for cnt in range(len(listAdvance)):
                totalLs = list(listAdvance[cnt]) + list(listpayment[cnt])
                finalLS.append(totalLs)

            response = {"Header":{"status":"success","module":"labfinace"},"Body":{"message":"labourer Advancepay list","data":finalLS},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
            print("exception is occured at",str(expc))            



    def payProcess(self,clientId,msgDict,sessionkey):
        try:
            masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterdb.initConnection()
            dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
            password = dbpass[0][0]
            admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
            admindb.initConnection()
            accountDb = admindb.fetchData("accountinfo",["labourerid","timestamp"],{"approveid":msgDict["approveId"]})
            print("accoutndb........................",accountDb)
            timeStamp = accountDb[0][1]
            labourerId = accountDb[0][0]
            print("time stamp............................",timeStamp)            
            admindb.connection
            hash = hashlib.md5(str(datetime.datetime.now()) .encode()).hexdigest()
            transationId = hash[:10]
            accinfoCont = " set paystatus =' paid ' "+" where  "
            accountcont = " set transationid = '"+str(transationId) +" ' where "
            payflag = " set payflag = 'True'"+", issuer = '"+sessionMange.session[sessionkey]["userid"]+"',reciverid = '"+labourerId +"',transationid = '"+str(transationId)+"' where  "
            if admindb.updateTable(accinfoCont,"accountinfo",{"approveid":msgDict["approveId"]}):
                if admindb.updateTable(payflag,"payment",{"timestamp":timeStamp}):
                    if admindb.updateTable(accountcont,"account",{"timestamp":timeStamp}):
                        response = {"Header":{"status":"success","module":"labfinace"},"Body":{"message":"amount payed sucessfully","data":""},"Signature":{"signature":"","Key":""}}
                        return response                           
            else:
                response = {"Header":{"status":"fail","module":"labfinace"},"Body":{"message":"amout can't paid","data":""},"Signature":{"signature":"","Key":""}}
                return response   
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
            print("exception is occured at",str(expc))            
        
            
            
    
    def requstApprove(self,clientId,msgDist,sessionkey):
        masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterdb.initConnection()
        dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
        password = dbpass[0][0]
        admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
        admindb.initConnection()
        randomid = str(random.randint(10000000000,1000000000000))[:8]
        approveCont = " set approvestatus = 'approved', approveid = "+randomid+" where "
        try:
            if admindb.updateTable(approveCont,"accountinfo",{"labourerid":msgDist["labourerId"]}):
                response = {"Header":{"status":"success","module":"labfinace"},"Body":{"message":"labourer requst is approved","data":""},"Signature":{"signature":"","Key":""}}
                return response                
            else:
                response = {"Header":{"status":"fail","module":"labfinace"},"Body":{"message":"labourer requst is can't approved","data":""},"Signature":{"signature":"","Key":""}}
                return response   
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])   


    def requstReject(self,clientId,msgDist,sessionkey):
        masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterdb.initConnection()
        dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
        password = dbpass[0][0]
        admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
        admindb.initConnection()
        approveCont = " set approvestatus = 'rejected' where "
        try:
            if admindb.updateTable(approveCont,"accountinfo",{"labourerid":msgDist["labourerId"]}):
                self.log.logEvent("advanceapply",2,"rejustreject",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"success","module":"labfinace"},"Body":{"message":"labourer requst is rejected","data":""},"Signature":{"signature":"","Key":""}}
                return response                
            else:
                self.log.logEvent("advanceapply",2,"can't reject",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labfinace"},"Body":{"message":"labourer requst is can't rejected","data":""},"Signature":{"signature":"","Key":""}}
                return response   
        except Exception as expc:
            # self.syslog.eventHandle("labourerclassManage","exception","exception on labourerclassManage module",str(expc))  
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"])  

##################################################################labourer phase#########################################################



    def advanceApply(self,clientId,msgDict,sessionkey):
        masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        masterDb.initConnection()
        cond = {"clientid":clientId}
        dbData = masterDb.fetchData("regusers",["password"],cond)
        password = dbData[0][0]
        adminDb = DatabaseAgent(clientId, clientId, conf.host,password, 5432)
        adminDb.initConnection()
        # try:
        if adminDb.fetchData("labourer",["labourerid"],{"siteid":msgDict["siteId"],"labourerid":msgDict["labourerId"]}):
            timestamp = datetime.datetime.now()
            if adminDb.pushData("accountinfo",["labourerid","timestamp","phonenumber","siteid","recoveryperiod","reson"],[msgDict["labourerId"],timestamp,msgDict["phoneNumber"],msgDict["siteId"],msgDict["recoveryPeriod"],msgDict["reasonForRequest"]]):
                sitedbData = adminDb.fetchData("sites",[ "projectid","siteid ","creditaccountid","debitaccountid"],{"siteid":msgDict["siteId"]})
                print("............ls",sitedbData)
                adminDb.pushData("account",["timestamp","projectid","siteid ","creditaccountid","debitaccountid"],[timestamp,sitedbData[0][0],sitedbData[0][1],sitedbData[0][2],sitedbData[0][3]])
                adminDb.pushData("payment",["timestamp","projectid","siteid ","creditaccountid","debitaccountid","amount","resontype"],[timestamp,sitedbData[0][0],sitedbData[0][1],sitedbData[0][2],sitedbData[0][3],msgDict["fundAuthorized"],msgDict["reasonType"]])
                response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labbouerAdavnce request placed sucessfully","data":""},"Signature":{"signature":"","Key":""}}
                return response             
            else:
                self.log.logEvent("laboureradvance",2,"advanceapply canot apply",clientId,sessionMange.session[sessionkey]["userid"])
                response = {"Header":{"status":"fail","module":"labourerManage"},"Body":{"message":"labbouerAdavnce request can't be placed","data":""},"Signature":{"signature":"","Key":""}}
                return response  
        else:
            response = {"Header":{"status":"fail","module":"labourerManage"},"Body":{"message":"labbouer can't exist this site","data":""},"Signature":{"signature":"","Key":""}}
            return response  
        # except Exception as expc:
        #     # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))  
        #     self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
        #     print("exception is occured at",str(expc))                  

    def advanceRespo(self,clientId,msgDict,sessionkey):
        try:
            masterdb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterdb.initConnection()
            dbpass = masterdb.fetchData("regusers",["password"],{"clientid":clientId})
            password = dbpass[0][0]
            admindb = DatabaseAgent(clientId,clientId,conf.host,password,conf.port)
            admindb.initConnection()
            listAdvance = admindb.fetchData("laboureradvance",["status","advanceid"],{"labourerid":msgDict["labourerId"]})
            self.log.logEvent("paymentDesk",2,"advancerespo",clientId,sessionMange.session[sessionkey]["userid"])
            response = {"Header":{"status":"success","module":"labourerManage"},"Body":{"message":"labourer requstedAdvance satus check","data":listAdvance},"Signature":{"signature":"","Key":""}}
            return response
        except Exception as expc:
            # self.syslog.eventHandle("labourerManage","exception","exception on labourerManage module",str(expc))
            self.log.logEvent("labourerclassManage",2,"occured expection is"+str(expc),clientId,sessionMange.session[sessionkey]["userid"]) 
            print("exception is occured at",str(expc))

# labad = paymentDesk()
# # print("total advance list",labad.requstList("kec166"))
# print("approvelist",labad.requstApprove("kec166",{"labourerId":"lab1001"}))
# # print("approvelist",labad.requstReject("kec166",{"labourerId":"lab1001"}))