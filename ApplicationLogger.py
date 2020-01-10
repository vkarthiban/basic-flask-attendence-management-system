import Constants
import conf
import datetime
from DBAgent import DatabaseAgent

class Logger:
    def __init__(self):
        self.curTime = datetime.datetime.now()
        self.db = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        self.db.initConnection()

    def finalizeLogger(self):
        self.db.dbFinalize()

    def logEvent(self, moduleName, severityLevel, message, clientId = "", userId = ""):
        if severityLevel not in range(Constants.LOG_SEVERITY_LOW, Constants.LOG_SEVERITY_CRITICAL):
            return False

        logSeverity = ["LOG_SEVERITY_LOW","LOG_SEVERITY_MEDIUM","LOG_SEVERITY_HIGH","LOG_SEVERITY_CRITICAL"]
        
        logData  = "<" + moduleName + " : " + str(self.curTime) + ">   " + message
        logYear  = self.curTime.year
        logDay  = self.curTime.day
        logMonth = self.curTime.month
        print("data::::",logData)

        fields = ["module_name", "day", "month", "year", "log_severity", "message","clientid","userid"]
        values   = [moduleName, logDay, logMonth, logYear, logSeverity[severityLevel], logData,clientId,userId]
        self.db.pushData("applogs", fields, values)



# log = Logger()

# log.logEvent("admin",1,"master login")