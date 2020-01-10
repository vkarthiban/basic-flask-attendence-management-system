import multiprocessing
from Admin import Admin
from roleManage import roleManage
from attendanceManage import attendanceManage
from projectManage import projectManage
from labourerManage import labbourerManage
from labourerClass import labourerClass
from shiftManage import shiftManage
# from Attendance import Attendance
from Authentication import Authentication
from ApplicationLogger import Logger
from Master import Master
from DBAgent import DatabaseAgent
import sessionMange
from paymentDesk import paymentDesk

class ModuleLauncher:
    def __init__(self,clientId,data,verifykey,apiEndPoint):
        self.message = data
        self.sessionkey = verifykey
        self.apiEndPoint = apiEndPoint
        self.splitUrl = apiEndPoint.split('/')
        self.auth = Authentication()
        self.master = Master()
        self.admin = Admin()
        self.role = roleManage()
        self.attendance = attendanceManage()
        self.project = projectManage()
        self.labourer = labbourerManage()
        self.labclass = labourerClass()
        self.shift = shiftManage()
        self.log = Logger()
        self.paymentDesk = paymentDesk()
        self.clientId = clientId

    def handleRequest(self):
        if self.splitUrl[0] == "master":
            return self.handleMaster()
        elif self.apiEndPoint == "/register":
            return  self.master.adminRegister(self.message,self.sessionkey)

        elif self.apiEndPoint == "/companyprofile":
            return self.admin.companyProfile(self.clientId,self.sessionkey)

        elif self.apiEndPoint == "/userprofile":

            return self.admin.userProfile(self.clientId,self.message,self.sessionkey) 

        else:
            return self.handleClient(self.splitUrl[0])

    def handleClient(self, clientId):
        if self.splitUrl[1] == "login":
            return self.admin.login(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[1] == "user":
            return self.handleClientUser()
        
        elif self.splitUrl[1] == "projects":
            return self.handleProjects()
        
        elif self.splitUrl[1] == "paymentDesk":
            return self.handlePaymentDesk()
            
        elif self.splitUrl[1] == "userrole":
            return self.roleManage()
        
        elif self.splitUrl[1] == "labourer":
            return self.handleLabourer()

        elif self.splitUrl[1] == "attendance":
            if self.splitUrl[2] == "list":
                return self.attendance.getAttendace(self.clientId,self.sessionkey)
        elif self.splitUrl [1] == "logout":
            return self.auth.logout(self.message,self.sessionkey)                
                
        elif self.splitUrl[1] == "payments":
            pass

        else:
            self.log.logEvent("ModuleLauncher",3,"wrong url acess")
        return "url does not defined"




    def handleMaster(self):
        if self.splitUrl[1] =="login":
            return self.master.login(self.message,self.sessionkey)
            
        elif self.splitUrl[1] =="register":
            # digest = self.auth.signUp(self.message["password"])
            # self.message["password"] = digest["hashPassword"]
            # self.message["salt"] = digest["salt"]
            # print("message",self.message)
            # return self.master.createMaster(self.message)
            # self.log.logEvent("ModuleLauncher",3,"Master registerd")
            return self.master.createMaster(self.message,self.sessionkey)
            #return "sucess"

        elif self.splitUrl[1] == "user":
            return self.handleMasterUser()

        elif self.splitUrl[1] == "app":

            if self.splitUrl[2] == "logs":
                return self.master.fetchAppLogs(self.message,self.sessionkey)

        elif self.splitUrl [1] == "clients":
            return self.handleMasterclients()
        elif self.splitUrl [1] == "logout":
            return self.auth.logout(self.message,self.sessionkey)

        else:
            print("master can't have  this endpoint")
            self.log.logEvent("ModuleLauncher",3,"master can't have  this endpoint")
            return "master can't have  this endpoint"


    def handleMasterUser(self):
        if self.splitUrl[2] == "add":
            return self.master.addUser(self.message,self.sessionkey)

        elif self.splitUrl[2] == "delete":
            return self.master.deleteUser(self.message,self.sessionkey)

        elif self.splitUrl[2] == "list":
            return self.master.listUser(self.sessionkey)

        elif self.splitUrl[2] == "editlist":
            return self.master.mastereditList(self.message,self.sessionkey)

        elif self.splitUrl[2] == "save":
            return self.master.editUser(self.message,self.sessionkey)

        elif self.splitUrl[2] == "archive":
            return self.master.archiveUser(self.message,self.sessionkey)

        elif self.splitUrl[2] == "unarchive":
            return self.master.unArchiveUser(self.message,self.sessionkey)

        else:
            self.log.logEvent("ModuleLauncher",3,"master_user can't have  this endpoint")
            return "wrong url access1"
    def handleMasterclients(self):
        if self.splitUrl[2] == "list":
            return self.master.getRegUserDetails(self.sessionkey)

        elif self.splitUrl[2] == "editlist":
            return self.master.clienteditList(self.message)       

        elif self.splitUrl[2] == 'delete':
            return self.master.deleteClient(self.message,self.sessionkey)

        elif self.splitUrl[2] == "archive":
            return self.master.archiveClient(self.message,self.sessionkey)

        elif self.splitUrl[2] == "save":
            return self.master.editClient(self.message,self.sessionkey)

        elif self.splitUrl[2] == "approve":
            return self.master.clientApprove(self.message,self.sessionkey)

        elif self.splitUrl[2]== "reject":
            self.master.rejectClients(self.message,self.sessionkey)
            
        else:
            self.log.logEvent("ModuleLauncher",3,"master_client can't have  this endpoint")
            return "url access error"

    def handleClientUser(self):
        if self.splitUrl[2] == "add":
            return self.admin.addUser(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "delete":
            return self.admin.deleteUser(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "save":
            return self.admin.editUser(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "archive":
            return self.admin.archiveUser(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "unarchive":
            return self.admin.unArchiveUser(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "list":
            return self.admin.listClientUser(self.clientId,self.sessionkey)
        elif self.splitUrl[2] == "roles":
            return self.admin.roleList(self.clientId,self.sessionkey)
        elif self.splitUrl[2] == "editlist":
            return self.admin.editList(self.clientId,self.message,self.sessionkey)

        else:
            self.log.logEvent("ModuleLauncher",3,"client_user can't have  this endpoint")
            return "wrong url access2"

    def handleProjects(self):
        if self.splitUrl[2] == "list":
            return self.project.listProjects(self.clientId,self.sessionkey)

        elif self.splitUrl[2] == "add":
            return self.project.projectsAdding(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "siteadd":
            return self.project.addSites(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "editList":
            return self.project.editList(self.clientId,self.message,self.sessionkey)        
        elif self.splitUrl[2] == "sitedelete":
            return self.project.deletSites(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "idList":
            return self.project.projectIdList(self.clientId,self.sessionkey)
        else:
            self.log.logEvent("ModuleLauncher",3,"client_user can't have  this endpoint")
            return "wrong url access2"


    def handleLabourer(self):
        if self.splitUrl[2] == "info":
            return self.labourer.labourerInfo(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "list":
            return self.labourer.labouerList(self.clientId,self.sessionkey)
            
        elif self.splitUrl[2] == "personalInfo":
            return self.labourer.personalInfo(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "employeeInfo":
            return self.labourer.employeeInfo(self.clientId,self.message,self.sessionkey)            

        elif self.splitUrl[2] == "identityInfo":
            return self.labourer.identityInfo(self.clientId,self.message,self.sessionkey)            

        elif self.splitUrl[2] == "bankInfo":
            return self.labourer.bankInfo(self.clientId,self.message,self.sessionkey)            
            
        elif self.splitUrl[2]== "save":
            return self.labourer.labourerReg(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2]== "update":
            return self.labourer.editLabourer(self.clientId,self.message,self.sessionkey)            

        elif self.splitUrl[2] == "delete":
            return self.labourer.deleteLabourer(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "attendance":
            return self.labourer.getAttendacePers(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "class":
            return self.classManage()
        elif self.splitUrl[2] == "addlist":
            return self.labourer.labbourerAddlist(self.clientId,self.sessionkey)
        
        elif self.splitUrl[2] == "shift":
            return self.shiftManage()

        else:
            return "wrong url access"
    def shiftManage(self):
        if self.splitUrl[3] == "add":
            return self.shift.shiftCreation(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[3] == "list":
            return self.shift.shiftList(self.clientId,self.sessionkey)

        elif self.splitUrl[3] == "delete":
            return self.shift.shiftDeleted(self.clientId,self.message,self.sessionkey)
        else:
            return "wrong url acess"
        
    def classManage(self):
        if self.splitUrl[3] == "list":
            return self.labclass.classList(self.clientId,self.sessionkey)

        elif self.splitUrl[3] == "add":
            return self.labclass.classAdding(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[3] == "delete":
            return self.labclass.classDelete(self.clientId,self.message,self.sessionkey)

        else:
            return "wrong url acess"
    def roleManage(self):
        if self.splitUrl[2] == "add":
            return self.role.createRoles(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "list":
            return self.role.listRoles(self.clientId,self.sessionkey)
        elif self.splitUrl[2] == "update":
            return self.role.editRoles(self.clientId,self.message,self.sessionkey)
        else:
            return "wrong url acess"

    def handlePaymentDesk(self):
        if self.splitUrl[2] == "apply":
            return self.paymentDesk.advanceApply(self.clientId,self.message,self.sessionkey)
        elif self.splitUrl[2] == "applyList":

            return self.paymentDesk.requstList(self.clientId,self.sessionkey)
        elif self.splitUrl[2] == "payList":

            return self.paymentDesk.advancePayList(self.clientId,self.sessionkey)   
                 
        elif self.splitUrl[2] == "approveCodeList":
            return self.paymentDesk.approvecodeList(self.clientId,self.message,self.sessionkey)   

        elif self.splitUrl[2] == "payment":
            return self.paymentDesk.payProcess(self.clientId,self.message,self.sessionkey)   

        elif self.splitUrl[2] =="status":
            return self.paymentDesk.advanceRespo(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "approve":
            return self.paymentDesk.requstApprove(self.clientId,self.message,self.sessionkey)

        elif self.splitUrl[2] == "reject":
            return self.paymentDesk.requstReject(self.clientId,self.message,self.sessionkey)

        else:
            return "wrong url acess"        