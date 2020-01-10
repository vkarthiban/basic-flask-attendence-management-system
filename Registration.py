from DBAgent import DatabaseAgent
class Registration:
    
    def labourRegistration(self,msgobj):
        dbobj = DatabaseAgent("kunnel", "kunnel", "127.0.0.1", "kunnel123", "5432")

        keys = []
        labregkey = True
        labregval = True
        values = []

        keylist = ["labourName","callByName","gender","dateOfBirth","fatherName","bloodGroup","nextOfKin",
        "contactNumberOFNextOfKin","motherTounge","addressLine1","addressLine2","addressLine3","village",
        "state","country","pincode","mobileNumber","residancePhoneNumber","emergencyPhoneNumber","dateOfJoining",
        "migrantWorker","siteId","siteOfJoining","designation","labourerClass","wageClass","documentType",
        "documentNumber","nameAsPerDoc","bankName","IFSCcode","backAccountNumber","brancName","nameInBank"]

        for key,value in msgobj.items():
            keys.append(key)
            values.append(value)
        for check in keylist:
            if check in keys:
                print("success",check)

            else:
                print("error")
                break
                labregkey = False
        if "" in values:
            print("error througing")
            labregval = False
        else:
            print("sucess througing")
        #print("values",values)


        personalDataKey = []
        personalDataVal = []
        for num in range(0,19):
            personalDataKey.append(keys[num])
            personalDataVal.append(values[num])
        #print("personkey",personalDataKey)
        # print("persondata",personalDataVal)
        dbobj.pushData("labourerdata",personalDataKey,personalDataVal)


        empDatakey = []
        empDataVal = []
        for num in range(19,26):
            empDatakey.append(keys[num])
            empDataVal.append(values[num])
        # print("empkey",empDatakey)
        # print("empvalue",empDataVal)
        dbobj.pushData("empdata",empDatakey,empDataVal)

        identyKey = []
        identyVal = []
        for num in range(26,29):
            identyKey.append(keys[num])
            identyVal.append(values[num])
        # print("identykey",identyKey)
        # print("identydetails",identyVal)
        dbobj.pushData("laboureridenty",identyKey,identyVal)


        bankDetailsKey = []
        bankDetailsVal = []
        for num in range(29,34):
            bankDetailsKey.append(keys[num])
            bankDetailsVal.append(values[num])
        # print("bankkey",bankDetailsKey)
        # print("bankdetails=",bankDetailsVal)
        dbobj.pushData("labourerbank",bankDetailsKey,bankDetailsVal)

        return labregkey and labregval
