import pyodbc
# server = r"192.168.0.212\KEC-31\SQLEXPRESS,9900"
# database = 'att_test'
# username = 'karthi_test'
# password = 'karthiban123'
# driver= '{ODBC Driver 17 for SQL Server}'
# cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=tcp:192.168.0.212,1433;DATABASE=att_test;UID=karthi_test;PWD=karthiban123;')
cursor = cnxn.cursor()
cursor.execute("select @@version")
cursor.commit()
cnxn.close()
