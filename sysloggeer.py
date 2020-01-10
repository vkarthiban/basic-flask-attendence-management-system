import sys
import socket
import datetime
import hashlib
import base64
import json

class syslogger:

    def init(self):
        pass
    def socketCreation(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_address = './log'
        print(sys.stderr, 'connecting to %s' %self.server_address)

    def socketConnection(self):
        try:
            self.sock.connect(self.server_address)
        except socket.error as soc:
            print("system errors",soc)
            sys.exit(1)

    def eventHandle(self,moduleid,modeKey,event,blob):
        logBin = {}
        logBin["progId"] = ("kec-erp")
        logBin["timeStamp"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logBin["ModuleId"] = (moduleid)
        logBin["ModeKey"] = (modeKey)
        logBin["Event"] = (event)
        logBin["blob"] = (blob)
        bigstr = ""
        for key in logBin:
            bigstr += logBin[key]
        sign = hashlib.md5(bigstr.encode("utf-8")).hexdigest()
        print("signature is",sign)
        logBin["FinSig"] = str(sign)
        

        self.socketCreation()
        self.socketConnection()
        try:
            passData = json.dumps(logBin)
            message = passData.encode("utf-8")              #'i am the karthiban0007'
            print(sys.stderr, 'sending "%s"' % message)
            self.sock.sendall(message)
            amount_received = 0
            amount_expected = len(message)

            # while amount_received < amount_expected:
            #     data = self.sock.recv(25000)
            #     amount_received += len(data)
            #     print(sys.stderr, 'received "%s"' % data)

        finally:
            print(sys.stderr, 'closing socket')
            self.sock.close()




log = syslogger()
log.eventHandle("moduleid","modeKey","event","somthing")











































# import sys
# import socket

# sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
# serverAddress = './loggs1'
# sock.connect(serverAddress)
# message = "i am the karthiban"
# sock.sendall(bytes(message.encode('utf-8')))
# amount_initial = 0
# amount_received = len(message)
# while amount_initial < amount_received:
#     data = sock.recv(16)
#     amount_received += len(data)
#     print(sys.stderr, 'received "%s"' % data)


# sock.close()