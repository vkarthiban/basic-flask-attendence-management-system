import sys
import socket
import os
import time
import threading 
import json
import hashlib
import conf
from DBAgent import DatabaseAgent
class syslogserver():
    
    def __init__(self):
        self.storage = []
        self.key = time.time()

    def socketCreation(self):
        self.serverAddres = './log'
        try:
            os.unlink(self.serverAddres)
        except OSError as soc:
            print("oserror in ",soc)
            if os.path.exists(self.serverAddres):
                raise
    def socketConnection(self):
        self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.sock.bind(self.serverAddres)
        self.sock.listen(1)

    def handler(self):
        self.socketCreation()
        self.socketConnection()
        while True:
            self.conn,self.addr = self.sock.accept()
            self.dataRecive()
            self.fincheck()
            self.clearData()


    # def connectionManage(self):
    #     self.socketCreation()
    #     self.socketConnection()     
    #     self.dataRecive()           


    def dataRecive(self):
        try:
            print("connection from ",self.addr)
            while True:
                data = self.conn.recv(25000)
                if data:
                    # self.conn.sendall(b'200')
                    self.storage.append(data)
                    print("datas are ",self.storage)
                    
                else:
                    print("nomore clients here",self.addr)
                    break
        finally:
            self.conn.close()

    def fincheck(self):
        recdict = bytes(self.storage[0]).decode("utf-8")
        print("nomore clients here/////////",recdict)
        dataDict = json.loads(recdict)
        bigstr = ""
        nameLs = []
        valueLs = []
        for key in dataDict:
            if key == "FinSig":
                nameLs.append(key)
                valueLs.append(dataDict[key])
                continue
            else:
                bigstr += dataDict[key]
                nameLs.append(key)
                valueLs.append(dataDict[key])
        print("nomore clients here/////////",bigstr)
        sign = hashlib.md5(bigstr.encode("utf-8")).hexdigest()

        print("sign value is",sign)
        if dataDict["FinSig"] == sign:
            masterDb = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
            masterDb.initConnection()
            if not masterDb.fetchSyslogg():
                entry = sign+"GEN000000X"
            else:
                dbEntryId = masterDb.fetchSyslogg()
                # decoEntryId = bytes(dbEntryId[0][0]).decode("utf-8")
                # print("entryid",str(decoEntryId))
                entry = sign+dbEntryId[0][0]

            hash = hashlib.md5(entry .encode()).hexdigest()
            firstChar = hash[0]        
            while firstChar != "0":
                hash = hashlib.md5(hash .encode()).hexdigest()
                print("Entry ID hash: Current hash = ", hash)
                firstChar = hash[0]            
                print("true")
            nameLs.append("entryid")
            valueLs.append(hash[:10])
            masterDb.pushData("syslogg",nameLs,valueLs)

        else:
            print("fing signature is wrong")



    def clearData(self):
        print("present is",self.storage)
        dict1 = self.storage
        print("dict1 is.........",dict1)
        del self.storage[:]
        print("to checking....................",self.storage)



log = syslogserver()

# if __name__ == "__main__":
#     t1 = threading.Thread(target=log.connectionManage)
#     t2 = threading.Thread(target=log.fincheck)
#     t3 = threading.Thread(target=log.clearData)
#     t1.start()
#     t2.start()
#     t3.start()
#     t1.join()
#     t2.join()
#     t3.join()

log.handler()








































