from datetime import datetime
from threading import Timer
import schedule
import time
import calendar

x=datetime.today()
z = x.month

def work():
    x=datetime.today()
    print("printing",x.minute)

def workhour():
    x = datetime.today()
    print("hourvalue",x.hour)

def workweek():
    x=datetime.today()
    print("printingweek",x.weekday)

def workmonth():
    x=datetime.today()
    print("printingmonth",z)

def datime():
    schedule.every().minute.do(work)
    schedule.every().week.do(workweek)
    schedule.every().day.do(work)
    schedule.every().hour.do(work)


    while 1:
        schedule.run_pending()
        time.sleep(1)


def monthly(she):
    monthlist31 = [1,3,5,7,8,10,]
    monthlist30 = [4,6,11]
    if she in monthlist31:
        schedule.every(31).days.do(workmonth)
        print("31")
    elif she in monthlist30:
        schedule.every(30).days.do(workmonth)
        print("30")
    elif she == 2:
        schedule.every(28).days.do(workmonth)
        print("28")
    elif she == 12:
        schedule.every(29).days.do(workmonth)
        print("29")
    else:
        print("Error")
    while 1:
        schedule.run_pending()
        # time.sleep(1)

    

#datime()
monthly(z)



































# import hashlib
# import base64
# import uuid

# password = "karthiban"
# salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
# hashPassword = hashlib.sha512(password.encode() + salt).hexdigest()
# print("salt:",salt)
# print("hashvalue",hashPassword)