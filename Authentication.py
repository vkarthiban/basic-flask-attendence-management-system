import nacl.utils
from nacl.public import PrivateKey,Box
import nacl.encoding
from ApplicationLogger import Logger
from nacl.encoding import Base64Encoder
import base64
import nacl.signing
import nacl.secret
import libnacl.public
import nacl.pwhash
import hashlib
import base64
import uuid
import sessionMange

#   import bin
#import Communication
from DBAgent import DatabaseAgent

class Authentication:
    
    def  __init__(self):
        self.log = Logger()

    def signatureVerify(self, rVerifyKey, signature, plainMsg):
        print("Signature Verification-------")
        print(rVerifyKey)
        print("verfykey",type(rVerifyKey))
        print("sign",type(signature),"----*")
        print(signature)
        print("plaintext........",plainMsg[:7])
        print("plain",type(plainMsg))
        print("Plain Message: ", plainMsg)
        
        
        verifyKey = nacl.signing.VerifyKey(rVerifyKey, encoder=nacl.encoding.HexEncoder)
        sign = bytes.fromhex(signature)
        print(type(verifyKey))
        print(type(sign))

        # print("sign",sign.decode("utf-8"))
        data = plainMsg.encode("utf-8")
        
        print("type of data     ", type(data))
        print(",.......",data)
        
        try:
            verifiedMsg = verifyKey.verify(sign)
            if plainMsg.encode('utf-8') == verifiedMsg:
                return True
            else:
                print("Plain and Verified Message Mismatch")
                return False
        except Exception as ex:
            print("Error Occurred in signature verification: ", ex)
            return False

        return True


    def generateKeys(self):
        Priva_key = PrivateKey.generate()
        authDictkey = ["UserId", "privateKey", "publicKey"] 
        authDictvalue = []
        tablename = "userkeys"
        userid = 1557
        print("actual key=",Priva_key)
        encoPrivateKey = Priva_key.encode(Base64Encoder).decode('utf8')
        print("publickey",Priva_key.public_key)
        encopubk_key = Priva_key.public_key.encode(Base64Encoder).decode('utf8')
        authDictvalue.append(userid)
        authDictvalue.append(encoPrivateKey)
        authDictvalue.append(encopubk_key)
        dbagent = DatabaseAgent(conf.mdbName,conf.muserName,conf.host,conf.mdbPassword,conf.port)
        dbagent.pushData(tablename,authDictkey,authDictvalue)
 
    def publicVerification(self):
        dbagent = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        key =[] 
        cond = {"userid":"1557"}
        key.append("PrivateKey")
        dbprivatekey = dbagent.fetchData(key,"userkeys",cond)
        prvk = base64.b64decode(str(data).encode('utf8'))
        print("actual key2",prvk)


    def encrypt(self,msg,pubkey,cond):
        dbagent = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        key = ["PrivateKey",]
        dbPrivatekey = dbagent.fetchData(key,"userkeys",cond)
        utf8PriKey = base64.b64decode(str(dbPrivatekey).encode('utf8'))
        print(type(utf8PriKey))
        key_box = libnacl.public.Box(utf8PriKey,pubkey)
        messageEncoded = bytes(msg, 'utf-8')
        cipher = key_box.encrypt(messageEncoded)
        return cipher


    def decrypt(self,encmsg,pubkey,cond):
        dbagent = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        key = ["PrivateKey",]
        dbPrivateKey = dbagent.fetchData(key,"userkeys",cond)
        utf8PriKey = base64.b64decode(str(dbprivatekey).encode('utf8'))
        key_box = libnacl.public.Box(utf8PriKey,pubkey)
        dec_mess = key_box.decrypt(encmsg)
        plainTxt = str(dec_mess,'utf-8')
        return plainTxt


        
    def login(self,msg,tableName,fileds,dbConfig,sessionkey):
        val = False
        try:
            username = msg["userName"]
            password = msg["password"]
            #username.replace(" ","")
            condition = {"username":username}
            dbagent = DatabaseAgent(dbConfig[0],dbConfig[1],"127.0.0.1",dbConfig[2],dbConfig[3])
            dbagent.initConnection()
            value = dbagent.fetchData(tableName,fileds, condition)
            print("totals...",value)
            salt = bytes(value[0][1])
            print("sal.....................",salt)
            hashPassword = hashlib.sha512(password.encode() + salt).hexdigest()
            print("databse hash value",bytes(value[0][0]))
            print("hashedpassword",hashPassword.encode())
            sign = []
            if hashPassword.encode() == bytes(value[0][0]):
                val = True 
                sessionMange.session[sessionkey] = {}
                sessionMange.session[sessionkey]["userid"] =(value[0][2])
                sessionMange.session[sessionkey]["userrole"] = (value[0][3])
                sign_key = nacl.signing.SigningKey.generate()
                verifyKey = sign_key.verify_key
                sessionMange.session[sessionkey]["signkey"] = (sign_key)
                sessionMange.session[sessionkey]["verifykey"] = (verifyKey)
            else:
                val = False
            return val
        except Exception as excp:
            print("occured exceptio is ",excp)

    def logout(self,msgDict,key):
        print("session is begign",sessionMange.session)
        # sessionkey = msgDict["sessionKey"]
        del sessionMange.session[key]
        print("session is next",sessionMange.session)
        if not key in sessionMange.session:
            response = {"Header":{"status":"success","module":"Authendication"},"Body":{"message":"user logout successfully","data":""},"Signature":{"signature":"","Key":""}}
            return response             
        else:
            response = {"Header":{"status":"fail","module":"Authendication"},"Body":{"message":"user lout error","data":""},"Signature":{"signature":"","Key":""}}
            return response            


        
    def signUp(self,password):
        salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        hashPassword = hashlib.sha512(password.encode() + salt).hexdigest()
        signobj = {}
        signobj["hashPassword"] = hashPassword
        print("salt type...................",type(salt))
        signobj["salt"] = salt
        print("hashedpassword",hashPassword)
        print("salt---",salt)
        dbagent = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
        dbagent.initConnection()
        fileds = ["username","password","salt"]
        datas = ["karthiban",hashPassword,salt]
        dbagent.pushData("users",fileds,datas)

        return signobj
        

    def uRolePermissionCheck(self,clientid,apiEndPoint,sessionkey):
            if sessionMange.session[sessionkey]["userrole"] == "Admin":

                return True

            else:

                masterDb = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", 5432)
                masterDb.initConnection()
                dblist = []
                cond = {"clientid":clientid}
                dbData = masterDb.fetchData("regusers",["password"],cond)
                password = dbData[0][0]                
                adminDb = DatabaseAgent(clientid, clientid, "127.0.0.1",password, 5432)
                adminDb.initConnection()
                # condition = {"roleid":"role1001"} 
                condition = {"rolename":sessionMange.session[sessionkey]["userrole"]}
                dbroleList = adminDb.fetchData("permission",["permissions"],condition)
                print("dbrolelist",dbroleList)
                permissions = (bytes(dbroleList[0][0])).decode("utf-8").split("&&")
                print("datas ..",permissions)                

                if apiEndPoint in permissions:
                    self.log.logEvent("Communication",2,"client permission granted")
                    return True

                else:
                    self.log.logEvent("Communication",2,"wrong user access")
                    return False
                    
                

        # return True


    
    
################################################################################testing################################################
    # def testing(self):
    #     dbagent = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")
    #     dbagent.initConnection()
    #     value = dbagent.fetchData("users",["password","salt"]) 
    #     salt = value[0][1]
    #     print("sal type........",salt)
    #     # hashPassword = hashlib.sha512(password.encode() + salt.encode()).hexdigest()
    #     #print("producing hash value",hashPassword)
    #     print("databse hash value",bytes(value[0][0]))

        
    
        


# auth = Authentication()
# print("reval is....",auth.uRolePermissionCheck("kec136","/user/archieve"))