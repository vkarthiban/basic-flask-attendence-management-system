import re
import json

class dataVerify:


    def verifyData(self,data):
        returnval = False
        print("data type",type(data))
        # print("data",json.dumps(data))
        print("bool value in json",data)
        # if not bool(data):
        #     print("trure is empty dictonary of jason...............")
        #     returnval = True
        # else:
        #     for key in data:
        #         print("keys are list",key)
        #         if key in ["password"]:
        #             if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,}$", data[key]):
        #                 print("...............................................1t")
        #                 returnval = True
        #             else:
        #                 print("...............................................1f")
        #                 returnval = False
        #                 break
        #         elif key in ["bloodGroup"]:
        #             if re.match(r"^(A|B|AB|O)(|1)[-+]$",data[key]):
        #                 print("...............................................2t")
        #                 returnval = True
        #             else:
        #                 print("...............................................2f")
        #                 returnval = False
        #                 break
        #         elif key in ["emailId"]:
        #             if re.match(r"^(?=.*[a-z])(?=.*[@#$])[\w\d@#$]*(\.[a-z]{2,4})$",data[key]):
        #                 print("...............................................3t")
        #                 returnval = True
        #             else:
        #                 print("...............................................3f")
        #                 returnval = False   
        #                 break
        #         elif key in ["userName","siteNames","projectName","roleName","labourerClass","branchName","ifscCode","companyName","userRole"]:
        #             if re.match(r"^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]*$",data[key]):
        #                 print("...............................................4t")
        #                 returnval = True
        #             else:
        #                 print("...............................................4f")
        #                 returnval = False
        #                 break 

        #         elif key in ["designation","fullName","labourerName","callByName","fatherName","nextOfKin","motherTounge","village","state","country","gender","nameInBank","bankName","nameAsPerDoc","siteOfJoining","migrantWorker","documentType","retention","advance","concreteCharges","compensation","reasonType",'type']:
        #             if re.match(r"^[a-zA-Z. ]+$",data[key]):
        #                 print("...............................................5t")
        #                 returnval = True
        #             else:
        #                 print("...............................................5f")
        #                 returnval = False 
        #                 break

        #         elif key in ["address","addressLine1","addressLine2","addressLine3","reasonForRequest","recoveryPeriod"]:
        #             if re.match(r"^[0-9a-zA-Z.,]+$",data[key]):
        #                 print("...............................................6t")
        #                 returnval = True
        #             else:
        #                 print("...............................................6f")
        #                 returnval = False 
        #                 break

        #         elif key in ["shiftId","labourerId","siteId","projectId","roleId","labourerClassId","employeeId","classId","userId","clientId"]:
        #             if re.match(r"^[0-9a-zA-Z]+$",data[key]):
        #                 returnval = True
        #             else:
        #                 returnval = False 
        #                 break

        #         elif key in ["number","contactNumberOfNextOfKin","mobileNumber","phoneNumber","residancePhoneNumber","emergencyPhoneNumber","pinCode","designation","labourerClass","documentNumber","bankAccountNumber","compensationDays","numOfLabourer",'id']:
        #             if re.match(r"^[0-9]+$",data[key]):
        #                 print("...............................................7t")
        #                 returnval = True
        #             else:
        #                 print("...............................................7f")
        #                 returnval = False 
        #                 break

        #         elif key in ["time","shiftStart","shiftEnd","break1Start","break1End","lunchBreakStart","lunchBreakEnd","break2Start","break2End"]:
        #             if re.match(r"[\d]{2}:[\d]{2}$",data[key]):
        #                 print("...............................................8t")
        #                 returnval = True
        #             else:
        #                 print("...............................................8f")
        #                 returnval = False  
        #                 break 
        #         elif key in ["dateOfBirth","dateOfJoining"]:
        #             if re.findall(r"[\d]{4}-[\d]{1,2}-[\d]{1,2}",data[key]):
        #                 print("...............................................9t")
        #                 returnval = True
        #             else:
        #                 print("...............................................9")
        #                 return False
        #                 break

        #         elif key in ["compensationAmount","concreteAmount","wageClass","fundAuthorized"]:
        #             if re.findall(r"\d\.\d",data[key]):
        #                 print("...............................................10t")
        #                 returnval = True
        #             else:
        #                 print("...............................................10")
        #                 return False
        #                 break
        #         else:
        #             print("wrong name and vale in the dictonary")
        #             print("...............................................t")
        #             returnval = False
        #             break
        # return returnval
        return True

# verfy = dataVerify()
# # # data = {'projectName': 'TYHGH', 'location': 'TVM', 'labourers': '453534', 'compensationDays': '25', 'compensationAmount': '2000.00', 'concreteAmount': '100.00'}
# print(verfy.verifyData({'emailId': 'noth00@gmail.com'}))