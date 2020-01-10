import nacl.utils
from nacl.public import PrivateKey,Box
import nacl.encoding
import nacl.signing
import nacl.hash
from Authentication import Authentication



# private_key = PrivateKey.generate()
# key_box = Box(private_key,private_key.public_key)
# message = input(str("enter your message"))
# cipher1 = bytes(message, 'utf-8')
# cipher = key_box.encrypt(cipher1)
# #encr_mess ="somthin"
# sign_key = nacl.signing.SigningKey.generate()
# print("sign key" , sign_key)
# signedData = sign_key.sign(cipher1)

# verify_key = sign_key.verify_key
# print("verify key", verify_key)
# # print(type(verify_key))
# # print(type(signedData))
# #recivedata = verify_key.encode(encoder=nacl.encoding.HexEncoder)

# auth = Authentication()
# print("data", auth.signatureVerfy(verify_key,signedData,message ))
#auth.generateKeys()
# auth.publicVerification()





# pubkey = b'\x1aA)\x16\xf3\x03\x0f!\xdc/#:\xd7n\xb2\xf1\x03\x8f\xd2\xfa\x80.\x12\xf8HG\x85\xe3\x14\x0b\x159'
# # msg = "karthiban"
# cond = {"userid":"1551"}
# # data = auth.encrypt(msg,pubkey,cond)
# # print("karthihack",data)
# encmsg =  b'\x91\x12n\xd9\xdd\x19\x1d\xcd\xe6\x87\xcd\x037\x01\xa4\xbc\xbb\xf6\xda\xb9\xfaI\xa0]\xacA\xdb\xeb\xcc\xd3\x8a\x7f\xdf\xe3\xeb\xec\xad\xb2\xd9\x1f\x8d\xcfm;\x8b\x87\xfc\xc3W'
# realtext = auth.decrypt(encmsg,pubkey,cond)
# print("text",realtext)

#signup test
auth = Authentication()
#some = auth.signUp("karthiban")
auth.testing()
# print("returnvalue",some["salt"])
# print("msge=",some["hashPassword"])


# #login
# msg = {}
# msg["username"] = "karthi"
# msg["password"] = "karthiban1"
# tt = auth.login(msg)
# print("fg ",tt)

# print("session" ,console.sessions[sessid][0][3])