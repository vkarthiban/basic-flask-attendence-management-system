import psycopg2
from psycopg2.extensions import AsIs
import re
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Exceptions import DbException

class DatabaseAgent:
    '''
    Module Name       : DBAgent
    Description       : Class definition for database management. This module acts as a wrapper for the PsycoPG 2 library. 
                        There will be basic functions for 
    '''
    def __init__(self, dbName, userName, host, password, port):
        self.database = dbName
        self.userName = userName
        self.host = host
        self.password = password
        self.port = port

    def initConnection(self):
        '''
        
        '''
        try:
            self.connection = psycopg2.connect(database = self.database, user = self.userName, host = self.host, password = self.password, port = self.port)
            self.cursor = self.connection.cursor()
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))    

    def createDefaultConnection(self):
        return psycopg2.connect(database = self.database, user = self.userName, host = self.host, password = self.password, port = self.port)

    def createDatabase(self,databaseName):
        try:
            con = psycopg2.connect(user = self.userName,host=self.host,password = self.password) 
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            xval = cur.execute('CREATE DATABASE ' + databaseName)
            cur.close()
            con.close()
            if xval == None:
                return True
            else:
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  
    
    def createTable(self,tableName,vars,extracontent):
        try:
            query = "CREATE TABLE "+ tableName +"( "+" VARCHAR(250),".join(vars) + " Varchar(250)" + extracontent +" );"
            print("jfdjkskj ",query)
            try:
                res = self.cursor.execute(query)
                self.connection.commit()
            except DbException as db:
                print("database exceptionis ",db)
            print("res value is",res)
            if res == None:
                print ("table created")
                return True
            else:
                print("table can not created")
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  


    def pushData(self,tableName, fields, values): 
        try:
            '''
            Function Name : *pushData*
            Arguments     : **tableName** Type: string, *Description:* name of the table to insert data to
                            **fields** *Type:* List, *Description:* Denotes the columns in a table
                            **values** *Type:* List, *Description:* Denotes the values to be inserted into the table
            Returns       : True if successful, False otherwise
            '''
            query = 'INSERT INTO '+ tableName +'(%s) VALUES %s'
            val= self.cursor.execute(query, (AsIs(','.join(fields)), tuple(values)))
            self.connection.commit()

            if val == None:
                print ("data inserted")
                return True
            else:
                print("data canot be inserted",val)
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  
    
    def fetchData(self, tableName, fields, conditions = dict()): 
        try:
            '''
            Function Name : *fetchData*
            Arguments     : * **tableName** *Type:* string, *Description:* The name of the table to fetch data from
                            * **fields** *Type:* List, *Description:* Denotes the columns in the table to fetch data from
                            * **conditions** *Type:* Dictionary, *Description:* The conditions 
            '''
            query = "SELECT "
            ctr = 0
            for fieldName in fields:
                query += "{0}".format(fieldName)
                ctr += 1
                if ctr != len(fields):
                    query += ", "
            query+= " FROM " + tableName

            if len(conditions) > 0:
                query += " WHERE "
                keys = list(conditions.keys())
                for key in keys:
                    query += str(key) + " = '" + str(conditions[key]) + "' "
                    if key != keys[-1]:
                        query += " AND "

                query +=" AND delete = False "

            else:
                query += " WHERE delete = False"

            #print("querty",query)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.commit()
            return result
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))              


    def editData(self, tableName, dataDist,cols = {}):
        try:
            query = "UPDATE " + str(tableName) + " SET "
            datakeys = list(dataDist.keys())
            for datakey in datakeys:
                query += datakey +" = '" + dataDist[datakey] + "'"
                if datakey != datakeys[-1]:
                    query +=","
            query += " where "
            colNames = list(cols.keys())
            for key in colNames:
                query += key + " = '" + cols[key] + "'"
                if key != colNames[-1]:
                    query += ", "
            print("edit query is ",query)
            data = self.cursor.execute(query)
            self.connection.commit()
            if data ==None:
                return True
            else:
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  
                
        
        


    def updateTable(self,updatecontent,table_name,condist):
        try:
            query = "update " + table_name + updatecontent   #" set delete = 'True' where " 
            keys = list(condist.keys())
            for key in keys:
                query += key +" = '"+condist[key] +"'"
                if key != keys[-1]:
                    query += ","
            query +=";"
            print("query ===============.......",query)
            data = self.cursor.execute(query)
            self.connection.commit()
            if data == None:
                return True
            else:
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                          


    def roleCreate(self,username,password):
        try:
            query = " create user " + username + " with password '" +password +"';"
            val = self.cursor.execute(query)
            self.connection.commit()
            if val == None:
                return True
            else:
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  



    def deleteDb(self, db_name):
        try:
            query = "drop database " + db_name
            newConn = self.createDefaultConnection() 
            newCur = newConn.cursor()
            newConn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            val = newCur.execute(query)
            newConn.commit()
            newConn.close()
            if val == None:
                return True
            else:
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  
        
    # def alterTable(self, tableName, colomname):
    #     query = "ALTER TABLE "+ tableName+" DROP COLUMN "+colomname+";"
    #     self.cursor.execute(query)
    #     self.connection.commit()
    
    def createSequnce(self,seqname):
        try:
            query = "CREATE SEQUENCE "+seqname
            self.cursor.execute(query)
            query1 = "select setval('"+seqname+"',1000"+")"
            val = self.cursor.execute(query1)
            self.connection.commit()
            if val == None:
                return True
            else:
                return False
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))                  

    def executeQuery(self,query):
        try:        
            val = self.cursor.execute(query)
            self.connection.commit()
            return val
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))              

    def fetchAppLogs(self, type = "", id = 0):
        try:
            if type == "":
                query = "select * from applogs order by id desc limit 100"
            elif type == "previous":
                query = "select * from applogs where id > " + id + " order by id desc limit 100"
            elif type == "next":
                query = "select * from applogs where id < " + id + " order by id desc limit 100"

            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.commit()
            return result
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))  

    def fetchSyslogg(self):
        try:
            self.cursor.execute("select entryid from syslogg order by id desc limit 1")
            result = self.cursor.fetchall()
            self.connection.commit()
            return result     
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))  

    def totalSysloggs(self,type ="",id= 0):
        try:
            if type == "":
                query = "select * from syslogg order by id desc limit 100"
            elif type == "previous":
                query = "select * from syslogg where id > " + id + " order by id desc limit 100"
            elif type == "next":
                query = "select * from syslogg where id < " + id + " order by id desc limit 100"

            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.commit()
            return result
        except DbException as dbx:
            print("execption",dbx)
            # self.syslog.eventHandle("DBagent","exception","exception on DBagent module",str(dbx))          


    

