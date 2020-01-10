import json
from Authentication import Authentication
from DBAgent import DatabaseAgent
from ApplicationLogger import Logger
import re
import nacl.signing
import nacl.encoding
from flask import Flask, request , jsonify
from ModuleLauncher import ModuleLauncher
from  dataVerify import dataVerify      
import sessionMange
import binascii
def getDict(o):
    return o.__dict__

class Communication:  
    def __init__(self):
        self.auth = Authentication()
        self.log = Logger()
        self.rejx = dataVerify()
        # self.modulauncher = ModuleLauncher()
        # self.launcher = ModuleLauncher()
    # def seralize(self,dicto):
    #     #self.deseralize(data_json)
    #     obj = json.dumps(dicto,default=getDict)
    #     return obj
        

    def deserialize(self, jsonData):
        try:
            deserialized = json.loads(jsonData)
            print(deserialized)
            return deserialized
        except Exception as expc:
            self.log.logEvent("communication deserialize",2,"exception ocureed"+str(expc))            

    def verifyStructure(self, msgDict):
        try:
            containsHeader = False
            containsBody = False
            containsExtraField = False
            containsSignature = False
            for key in msgDict:
                if key == "Header":
                    containsHeader = True
                elif key == "Body":
                    containsBody = True
                elif key == "Signature":
                    containsSignature = True
                else:
                    containsExtraField = True
                    break

            return containsHeader and containsSignature and containsBody and not containsExtraField
        except Exception as expc:
            self.log.logEvent("communication verify structure function",2,"exception ocureed"+str(expc))
            

    def createMessage(self, dictData, message):
        try:
            message.header = dictData["Header"]
            message.body = dictData["Body"]
            message.Signature = dictData["Signature"]
        except Exception as expc:
            self.log.logEvent("communication at create message function",2,"exception ocureed"+str(expc))            

    def sanitizeBody(self,msgBody):
        try:
            success = False
            for key in msgBody:
                if self.sanitizeString(key):
                    if type(msgBody[key]) is dict:
                        if not self.sanitizeBody(msgBody[key]):
                            return False
                        else:
                            success = True
                        self.sanitizeBody(msgBody[key])
                    else:
                        if self.sanitizeString(msgBody[key]):
                            success = True
                            continue

                        else:
                            success = False     
                else:
                    return False

            return success
        except Exception as expc:
            self.log.logEvent("communication at sanatizeBody function",2,"exception ocureed"+str(expc))

    def sanitizeHeader(self,msgheader):
        try:        
            success = True
            for msg in msgheader:
                if self.sanitizeString(msg):
                    if self.sanitizeString(msgheader[msg]):
                        continue
                    else:
                        success = False
                else:
                    success = False

            return success
        except Exception as expc:
            self.log.logEvent("communication at sanitizeHeader function",2,"exception ocureed"+str(expc))            

        

    def sanitizeString(self, stringData):
        try:
            text = str(stringData)
            print("data is" + text)
            ignore_words = [';','"','$','&&','../','*','<','>','%3C','%3E','\'','--','1,2','\x00','`','(',')','file://','input://'] 
            for ch in ignore_words: 
                if ch in text:
                    print("1false")
                    return False
            return True
        except Exception as expc:
            self.log.logEvent("communication at sanitizeString function",2,"exception ocureed"+str(expc))             
            

#######################################################################master handle#######################################################################33
    def receiveRequest(self,data,clientid,apiEndPoint):
        # try:
        print("JSON : ",data)
        msg = Message()
        signString = str(data).split("Body")[1]
        plainMsg = ((signString.split("Signature")[0])[:-2])[2:]
        dictData = self.deserialize(data)
        if self.verifyStructure(dictData):
            self.createMessage(dictData, msg)
            print("MESSAGE HEADER: ")
            for key in msg.Signature:
                print("keys ", key)
                if key == "signature":
                    print(" encrypetedkey will be there")
                elif key == "Key":
                    print("verfykey will  be there")
                else:
                    self.log.logEvent("Communication",3,"signatrue part is missing")
                    print("signature missing  there")
                    return "signature missing  there"
            verifyKey = msg.Signature["Key"]
            signature = msg.Signature["signature"]
            contStr = ""            
            # print("signString..........................",plainMsg)
            # sigtest = self.auth.signatureVerify(verifyKey, signature,plainMsg)
            # print("Signature Verified::::::::::::::::::::::::::::::::::::::", sigtest)
            if self.auth.signatureVerify(verifyKey, signature,plainMsg):
                if self.rejx.verifyData(msg.body):
                    if clientid == "signup" :
                        modLauncher = ModuleLauncher(clientid, msg.body,verifyKey,'/register')
                        return modLauncher.handleRequest()
                    elif clientid == "masterregister":
                        modLauncher = ModuleLauncher(clientid,msg.body,verifyKey, apiEndPoint)
                        return modLauncher.handleRequest()                        
                    elif clientid == "master":
                        modLauncher = ModuleLauncher(clientid,msg.body,verifyKey, apiEndPoint)
                        # return modLauncher.handleRequest()
                        resDict =  modLauncher.handleRequest()
                        body = resDict["Body"]
                        print("body part is....",body)
                        jsnfyBody = json.dumps(body)
                        print("jsnfyBody) = ",jsnfyBody)
                        if resDict["Header"]["status"] == "success":
                            signkey1 = sessionMange.session[verifyKey]["signkey"]
                            verifykey1 = sessionMange.session[verifyKey]["verifykey"]
                            print("verifykey type",type(verifykey1))
                            verify_key_hex =verifykey1.encode(encoder=nacl.encoding.HexEncoder)
                            print("signature private key type",type(signkey1))
                            print("type(jsnfyBody) = ", type(jsnfyBody))
                            sessionSign = signkey1.sign(jsnfyBody.encode("utf-8"))
                            print("sessionkey type",type(sessionSign))
                            print("sessionkey ............on backend",sessionSign)
                            sHexSignature = binascii.hexlify(bytes(sessionSign))
                            resDict["Signature"]["signature"] = (sHexSignature)
                            resDict["Signature"]["Key"] = (verify_key_hex)
                            print("siggened signature message................................",resDict)
                            return resDict                        
                    elif apiEndPoint == "/login":
                        # modLauncher = ModuleLauncher(clientid,msg.body,verifyKey, apiEndPoint)
                        # return modLauncher.handleRequest()
                        try:
                            modLauncher = ModuleLauncher(clientid,msg.body,verifyKey, apiEndPoint)
                            resDict =  modLauncher.handleRequest()
                            body = resDict["Body"]
                            print("body part is....",body)
                            jsnfyBody = json.dumps(body)
                            print("jsnfyBody) = ",jsnfyBody)
                            if resDict["Header"]["status"] == "success":
                                signkey1 = sessionMange.session[verifyKey]["signkey"]
                                verifykey1 = sessionMange.session[verifyKey]["verifykey"]
                                print("verifykey type",type(verifykey1))
                                verify_key_hex =verifykey1.encode(encoder=nacl.encoding.HexEncoder)
                                print("signature private key type",type(signkey1))
                                print("type(jsnfyBody) = ", type(jsnfyBody))
                                sessionSign = signkey1.sign(jsnfyBody.encode("utf-8"))
                                print("sessionkey type",type(sessionSign))
                                print("sessionkey ............",sessionSign)
                                sHexSignature = binascii.hexlify(bytes(sessionSign))
                                resDict["Signature"]["signature"] = (sHexSignature)
                                resDict["Signature"]["Key"] = (verify_key_hex)

                            return resDict 
                        except Exception as expc:
                            print("expection",expc)                      
                            response = {"Header":{"status":"fail","module":"communication"},"Body":{"message":"wrong username or password","data":""},"Signature":{"signature":"","Key":""}}
                            return response                          
                    elif apiEndPoint == "/logout":
                        modLauncher = ModuleLauncher(clientid,msg.body,verifyKey, apiEndPoint)
                        return modLauncher.handleRequest()                    
                        # resDict =  modLauncher.handleRequest()
                        # body = resDict["Body"]
                        # print("body part is....",body)
                        # jsnfyBody = str(jsonify(body))
                        # signkey1 = sessionMange.session[verifyKey]["signkey"]
                        # verifykey1 = sessionMange.session[verifyKey]["verifykey"]
                        # verify_key_hex =verifykey1.encode(encoder=nacl.encoding.HexEncoder)
                        # print("signature private key type",type(signkey1))
                        # print("type(jsnfyBody) = ", type(jsnfyBody))
                        # sessionSign = signkey1.sign(jsnfyBody.encode("utf-8"))
                        # print("sessionkey type",type(sessionSign))
                        # sHexSignature = binascii.hexlify(bytes(sessionSign))
                        # resDict["Signature"]["signature"] = (sHexSignature)
                        # resDict["Signature"]["Key"] = (verify_key_hex)
                        # return resDict                    
                    elif self.auth.uRolePermissionCheck(clientid,apiEndPoint,verifyKey) :
                        # try:
                        modLauncher = ModuleLauncher(clientid,msg.body,verifyKey, apiEndPoint)
                        resDict =  modLauncher.handleRequest()
                        body = resDict["Body"]
                        print("body part is....",body)
                        jsnfyBody = json.dumps(body)
                        print("jsnfyBody) = ",jsnfyBody)
                        if resDict["Header"]["status"] == "success":
                            signkey1 = sessionMange.session[verifyKey]["signkey"]
                            verifykey1 = sessionMange.session[verifyKey]["verifykey"]
                            print("verifykey type",type(verifykey1))
                            verify_key_hex =verifykey1.encode(encoder=nacl.encoding.HexEncoder)
                            print("signature private key type",type(signkey1))
                            print("type(jsnfyBody) = ", type(jsnfyBody))
                            sessionSign = signkey1.sign(jsnfyBody.encode("utf-8"))
                            print("sessionkey type",type(sessionSign))
                            print("sessionkey ............",sessionSign)
                            sHexSignature = binascii.hexlify(bytes(sessionSign))
                            resDict["Signature"]["signature"] = (sHexSignature)
                            resDict["Signature"]["Key"] = (verify_key_hex)
                        return resDict     
                        # except Exception as expc:
                        #     print("expection",expc) 
                        #     self.log.logEvent("communication",2,"role checking function ")        
                else:
                    print(">>............................wrong datastructure")
                    return " wrong datastructure at communication"                           
                    
            else:
                self.log.logEvent("Communication",3,"signature is wrong")
                return "error occured"            
        elif self.sanitizeBody(msg.body) and self.sanitizeHeader(msg.header):
            print("Message body verified")
        else:
            self.log.logEvent("Communication",3,"invalied requst formate")
            print("Invalid body structure format ")
            return "Invalid body structure format "
        # except Exception as expc:
        #     self.log.logEvent("communication at reciveRequest function",2,"exception ocureed"+str(expc))         



        
            


class Message:
    def __init__(self):
        self.header = {}    
        self.body = {}
        self.Signature = {}



