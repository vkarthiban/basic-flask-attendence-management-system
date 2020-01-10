from DBAgent import DatabaseAgent
from ApplicationLogger import  Logger

class Attendance:

    def __init__(self):
        self.log = Logger()
        self.dbobj = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        self.dbobj.initConnection()

    def getAttendace(self):#to be filled from the call site (module launcher)
        dataFields = ["labourerid","labourername","labouercategory","labourertype","intime","outtime","numberofhours","overtimeallocated","overtimeworked","siteid","projectid"]
        tableName = "attendance"
        condition = {"siteid":"siteamerica"}
        dbattendance = self.dbobj.fetchData(tableName,dataFields,condition)
        print("dictonary",dbattendance)
        self.log.logEvent("Admin",2,"attendance listed sucess fully")
        return dbattendance
# atten = Attendance()
# print("attandence",atten.getAttendace())