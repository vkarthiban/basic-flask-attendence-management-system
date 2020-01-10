


# class companyMangae
        
#     def companyProfile(self,sessionkey):
#         # print("sesssion.............................................",sessionMange[sesessionkey])
#         #adminDb = DatabaseAgent(sessionMange[sessionkey]["dbName"],sessionMange[sessionkey]["userName"],sessionMange[sessionkey]["host"],sessionMange[sessionkey]["password"],sessionMange[sessionkey]["port"])
#         adminDb = DatabaseAgent("admin", "admin", "127.0.0.1", "admin123", 5432)
#         adminDb.initConnection()
#         compnydata = self.fetchCompanySummary(adminDb)

#         projectsColl = self.fetchProjectsSummary(adminDb)

#         finalList = []
#         finalList.append(list(compnydata))
#         finalList.append(list(projectsColl))
#         self.log.logEvent("Admin", 2, "Company pofile sended sucessfully")
#         return  finalList

#     def fetchCompanySummary(self, dbAgent):
#         dataList = ["companyname", "fullname", "employeeid", "designation"]
#         return dbAgent.fetchData("clients", dataList)

#     def fetchProjectsSummary(self, dbAgent):
#         projCollection = []
#         projectData= dbAgent.fetchData("projects", ["Projectname"])
#         # print("\n\n\n")
#         for i in range(len(projectData)):
#             cond ={"projectname":projectData[i][0]}
#             curSite = dbAgent.fetchData("projects", ["sitenames"], cond)
#             lCount = dbAgent.fetchData("projects", ["numOfLabourers"], cond)
#             # print("\n\n\nSites:::::::::::: ", curSite)
#             # print("\nSites:::::::::::::: ", curSite[0])
#             # print("\nSites:::::::::::::: ", curSite[0][0])
#             projectSummary = [[], []]

#             for j in range(len(curSite)):
#                 # print ("\n\n\n\nJ:::::::    ", j)
#                 sitesList = curSite[j][0]
#                 labourerList = lCount[j][0]
#                 projectSummary[-1].append(sitesList)
#                 projectSummary[-2].append(labourerList)
            
#             projectSummary.insert(0, projectData[i][0])            
#             projCollection.append(projectSummary)
#             #del labourerList[:]
#             #del sitesList[:]
#             # print("Project Summary:::::::::::::::::::::::::::::::: ", projectSummary)
#             # print("sites..........  ",sitesList)
#             # print("lab........................  ",labourerList)
#             # print("\n\n\n")

#         print("PROJECTS CONTAINER:::::::::::::::::::::::::: ", projCollection)
        
#         return projCollection

