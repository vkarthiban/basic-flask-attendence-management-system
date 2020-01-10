from flask import Flask, request , jsonify
import json
from Communication import Communication
# from sysloggeer import syslogger

app = Flask(__name__)

comObj = Communication()

@app.route('/')
def index():
    return '{"karthi"}'
######################_MASTER-MODULE_#############################
@app.route('/master/register',methods=["POST"])
def masterRegister():
    data = request.data
    userid = "masterregister"
    return jsonify(comObj.receiveRequest(data,userid,'master/register'))
    

@app.route('/master/login',methods=["POST"])
def masterLogin():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/login'))
    #return "sucess"

@app.route('/master/user/add',methods=["POST"])
def masterUserAdding():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/add'))

@app.route('/master/user/delete',methods=["POST"])
def masterDeleteUser():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/delete'))

@app.route('/master/user/list',methods= ["POST"])
def masterListUser():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/list'))

@app.route('/master/user/editlist',methods= ["POST"])
def masterEditListUser():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/editlist'))    

@app.route('/master/user/save',methods=["POST"])
def masterSaveUser():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/save'))

@app.route('/master/user/archive',methods=["POST"])
def masterArchiveUser():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/archive'))

@app.route('/master/user/unarchive',methods=["POST"])
def masterunArchiveUser():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/user/unarchive'))

@app.route('/master/logout',methods=["POST"])
def masterLogout():
    data = request.data
    userid = ""
    return jsonify(comObj.receiveRequest(data,userid,'/logout'))
    #return "sucess"


@app.route('/master/app/logs',methods=["POST"])
def masterLogsApp():
    data = request.data
    userid = "master"
    resdata = comObj.receiveRequest(data,userid,'master/app/logs')
    print("respesdata..............................................",resdata)
    return jsonify(resdata)

###############################_client-module_########################################
# @app.route('/register', methods=['POST'])
# def adminRegister():
#     data = request.data
#     clientid = 'signup'
# return jsonify(comObj.receiveRequest(data,userid,'ma))

@app.route('/master/clients/approve',methods=["POST"])
def masterApprove():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/clients/approve'))

@app.route('/master/clients/reject',methods=["POST"])
def masterReject():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/clients/reject'))
    
@app.route('/master/clients/delete',methods=["POST"])
def masterDeleteClient():
    data = request.data
    userid = "master"
    return comObj.receiveRequest(data,userid,'master/clients/delete')

@app.route('/master/clients/archive',methods=["POST"])
def masterArchiveClient():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/clients/archive'))

@app.route('/master/clients/save',methods=["POST"])
def masterSaveClient():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/clients/save'))
    return "masterDeleteClient"

@app.route('/master/clients/list',methods=["POST"])
def masterListClient():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/clients/list'))

@app.route('/master/clients/editlist',methods=["POST"])
def masterEditList():
    data = request.data
    userid = "master"
    return jsonify(comObj.receiveRequest(data,userid,'master/clients/editlist'))    


###############################_Admin-module_########################################
@app.route('/register', methods=['POST'])
def adminRegister():
    data = request.data
    clientid = 'signup'
    return jsonify(comObj.receiveRequest(data,clientid,'/register'))

@app.route('/<clientid>/login',methods=["POST"])
def adminLogin(clientid):
    print("clientid==",clientid)
    data = request.data
    return jsonify(comObj.receiveRequest(data,clientid,'/login'))

@app.route('/<clientid>/logout',methods=["POST"])
def adminLogout(clientid):
    print("clientid==",clientid)
    data = request.data
    return jsonify(comObj.receiveRequest(data,clientid,'/logout'))    

@app.route('/<clientid>/user/add',methods=["POST"])
def adminAddUser(clientid):
    print("clientid==",clientid)
    data = request.data
    return jsonify(comObj.receiveRequest(data,clientid,'/user/add'))
    
@app.route('/<clientid>/user/delete',methods=["POST"])
def adminDeleteUser(clientid):
    data = request.data
    return jsonify(comObj.receiveRequest(data,clientid,'/user/delete'))

@app.route('/<clientid>/user/archive',methods=["POST"])
def adminArchiveClient(clientid):
    data = request.data
    return jsonify(comObj.receiveRequest(data,clientid,'/user/archive'))

@app.route('/<clientid>/user/unarchive',methods=["POST"])
def adminunArchiveClient(clientid):
    data = request.data
    return jsonify(comObj.receiveRequest(data,clientid,'/user/unarchive'))

@app.route('/<clientid>/user/list',methods=["POST"])
def adminListUser(clientid):
    data = request.data
    dbData = comObj.receiveRequest(data,clientid,'/user/list')
    return jsonify(dbData)

@app.route('/<clientid>/user/save',methods=["POST"])
def adminSaveUser(clientid):
    data = request.data
    dbData = comObj.receiveRequest(data,clientid,'/user/save')
    return jsonify(dbData)

@app.route('/<clientid>/user/editlist',methods=["POST"])
def editList(clientid):
    data = request.data
    dbData = comObj.receiveRequest(data,clientid,'/user/editlist')
    return jsonify(dbData)


@app.route('/<clientid>/user/roles',methods=["POST"])
def roleList(clientid):
    data = request.data
    dbData = comObj.receiveRequest(data,clientid,'/user/roles')
    return jsonify(dbData)

@app.route('/<clientid>/attendance/list', methods=["POST"])
def adminListAttendance(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/attendance/list')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/payments',methods=["POST"])
def adminPayment():
    return "adminPayment"

@app.route('/<clientid>/user/list',methods=["POST"])
def adminUserListt():
    return "adminUserListt"

################################################projects management##################################################################
@app.route('/<clientid>/projects/list',methods=["POST"])
def projectsList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/list')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/projects/add',methods=["POST"])
def projectsAdd(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/add')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/projects/save',methods=["POST"])
def projectsSave(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/save')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/projects/delete',methods=["POST"])
def projectsDelete(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/delete')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/projects/siteadd',methods=["POST"])
def siteadd(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/siteadd')
    print("respdata",respdata)
    return jsonify(respdata)    

@app.route('/<clientid>/projects/sitedelete',methods=["POST"])
def sitedelete(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/sitedelete')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/projects/editList',methods=["POST"])
def projecteditList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/editList')
    print("respdata",respdata)
    return jsonify(respdata)    


@app.route('/<clientid>/projects/idList',methods=["POST"])
def projectIdList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/projects/idList')
    print("respdata",respdata)
    return jsonify(respdata)    


##############################_registeration-module_###########################################
# @app.route('/<client-id>/labourer/register/load-page',methods=['POST'])
#     def listProjects(clientid):
#     data = request.data
#     respdata = comObj.receiveClientRequest(data,clientid,'/attendance/list')
#     print("respdata",respdata)
#     return jsonify(respdata)

@app.route('/<clientid>/labourer/info',methods=["POST"])
def labourerInfo(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/info')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/list',methods=["POST"])
def labourerList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/list')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/save',methods=["POST"])
def labourerAdding(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/save')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/delete',methods=["POST"])
def labourerDelete(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/delete')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/delete',methods=["POST"])
def labbourerAddlist(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/delete')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/labourer/attendance',methods=["POST"])
def labourerattendance(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/attendance')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/companyprofile',methods=["POST"])
def companyprofile(clientid):
    data = request.data

    respdata = comObj.receiveRequest(data,clientid,'/companyprofile')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/userprofile',methods=["POST"])
def userprofile(clientid):
    data = request.data

    respdata = comObj.receiveRequest(data,clientid,'/userprofile')
    print("respdata",respdata)
    return jsonify(respdata)
#################################################shiftmanage########################################

@app.route('/<clientid>/labourer/shift/add', methods=["POST"])
def shiftAdding(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/shift/add')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/shift/list',methods=["POST"])
def shiftList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/shift/list')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/shift/delete',methods=["POST"])
def shiftDelete(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/shift/delete')
    print("respdata",respdata)
    return jsonify(respdata)

####################################################class manage#######################################
@app.route('/<clientid>/labourer/class/add',methods=["POST"])
def classAddd(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/class/add')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/class/list',methods=["POST"])
def classlist(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/class/list')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/class/delete',methods=["POST"])
def classDelete(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/class/delete')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/labourer/addlist',methods=["POST"])
def addList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/addlist')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/labourer/update',methods=["POST"])
def labourerupdate(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/update')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/labourer/personalInfo',methods=["POST"])
def labpersonalInfo(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/personalInfo')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/labourer/employeeInfo',methods=["POST"])
def labemployeeInfo(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/employeeInfo')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/labourer/identityInfo',methods=["POST"])
def labidentityInfo(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/identityInfo')
    print("respdata",respdata)
    return jsonify(respdata)


@app.route('/<clientid>/labourer/bankInfo',methods=["POST"])
def labBankInfo(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/labourer/bankInfo')
    print("respdata",respdata)
    return jsonify(respdata)
#####################################################rolemanagement##############################

@app.route('/<clientid>/userrole/add',methods=["POST"])
def roleAdd(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/userrole/add')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/userrole/list',methods=["POST"])
def rolelist(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/userrole/list')
    print("respdata",respdata)
    return jsonify(respdata)

@app.route('/<clientid>/userrole/update',methods=["POST"])
def roleUpdae(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/userrole/update')
    print("respdata",respdata)
    return jsonify(respdata)


#######################################################################paymetdesk###########################################

@app.route('/<clientid>/paymentDesk/apply',methods=["POST"])
def advanceApply(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/apply')
    print("respdata",respdata)
    return jsonify(respdata)    


@app.route('/<clientid>/paymentDesk/applyList',methods=["POST"])
def advanceApplyLIst(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/applyList')
    print("respdata",respdata)
    return jsonify(respdata) 

@app.route('/<clientid>/paymentDesk/payList',methods=["POST"])
def advancpaylist(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/payList')
    print("respdata",respdata)
    return jsonify(respdata)  


@app.route('/<clientid>/paymentDesk/approveCodeList',methods=["POST"])
def advancapproveCodeList(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/approveCodeList')
    print("respdata",respdata)
    return jsonify(respdata)  


@app.route('/<clientid>/paymentDesk/payment',methods=["POST"])
def paymentadvance(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/payment')
    print("respdata",respdata)
    return jsonify(respdata)  

@app.route('/<clientid>/paymentDesk/status',methods=["POST"])
def advanceStatus(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/status')
    print("respdata",respdata)
    return jsonify(respdata) 

@app.route('/<clientid>/paymentDesk/approve',methods=["POST"])
def advanceApprove(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/approve')
    print("respdata",respdata)
    return jsonify(respdata) 

@app.route('/<clientid>/paymentDesk/reject',methods=["POST"])
def advanceReject(clientid):
    data = request.data
    respdata = comObj.receiveRequest(data,clientid,'/paymentDesk/reject')
    print("respdata",respdata)
    return jsonify(respdata) 


########################################################
    
# @app.route('/master/xml',methods=["POST"])
# def talytest():
#     data = request.data
#     print(data)
#     return data

# @app.after_request  
# def after(response):
#     print("responseis...................")
#     print("responseis...................",response.status)
#     print("responseis...................",response.headers)
#     print("responseis...................",response.get_data)
#     # syslogger.eventHandle("serverModule","response","reponse for all requst",)
#     return response



def startServer():
    app.run(port=8080)
    #app.run(host='192.168.0.152',port=80)
