import http.client
from dicttoxml import dicttoxml
# import requests
# res = requests.post("http://127.0.0.1:8080/kec181/login/ ",json.dumps({'Header': {'host': '192.168.0.161'}, 'Body': {'employeeId': 'user1001'}, 'Signature': {'signature': 'e5371701e1884d330ff99101a0a92fc19d284e5c9b30abbc0ba56dd97567d59ef644c04be478071781f1e8ad5e273a682b2090897700a9d055f9425ed96ff5097b22656d706c6f7965654964223a227573657231303031227d', 'Key': '4ae448876cc0059cc9e59c9337765921d941f9181daee37fa0ebd4f18e3a5b2f'}}) )
def xmlconstruct(headerDict,bodyDict,dataDict):
    data1 = {"ENVELOPE":{"HEADER":{"VERSION":headerDict["VERSION"],"TALLYREQUEST":headerDict["TALLYREQUEST"],"TYPE":["TYPE"],"SUBTYPE":headerDict["SUBTYPE"],"ID":headerDict["ID"]},"BODY":{"DESC":{"STATICVARIABLES":bodyDict["STATICVARIABLES"],"REPEATVARIABLES":bodyDict["REPEATVARIABLES"],"FETCHLIST":bodyDict["FETCHLIST"],"FUNCPARAMLIST":bodyDict["FUNCPARAMLIST"],"TDL":bodyDict["TDL"]},"DATA":dataDict}}}
    data2 = {"ENVELOPE":{"HEADER":headerDict},"BODY":{"DESC":bodyDict,"DATA":dataDict}}
    xml = dicttoxml(data2)
    print("xml contente",xml)
    h1 = http.client.HTTPConnection("localhost",8080)
    h1.request("POST", "/master/xml",xml)
    h2 = h1.getresponse()
# print(h2.read())

def example():
    headerDict = {"VERSION":"1.0","TALLYREQUEST":"import","TYPE":"Data","SUBTYPE":"object","ID":"kunneltech"}
    bodyDict = {"STATICVARIABLES":"Static Variables Specification","REPEATVARIABLES":"Repeat Variables Specification","FETCHLIST":"Fe4Integration - The Overall Perspectivetch Specification","FUNCPARAMLIST":"Parameter Specification in the case of function type","TDL":"TDL Information"}
    dataDict = {"ENVELOPE":{'projectName': 'TYHGH', 'location': 'TVM', 'labourers': '453534', 'compensationDays': '25', 'compensationAmount': '2000.00', 'concreteAmount': '100.00'}}
    xmlconstruct(headerDict,bodyDict,dataDict)

example()