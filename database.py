import pymongo


class DataBase():
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = client['testdb']
        self.mycol = mydb['customers']
        self.ancol = mycol['someOther']
        # ancol.insert_one({"name": "james"})
        # for x in ancol.find():
        #     print x
        print mydb.list_collection_names()

    def createDatabase(self, dbName):
        pass

    def findShowByName(self, showName):
        pass
    
    def saveShow(self, showObj):
        pass


    def deleteAllShows(self):
        x = self.ancol.delete_many({})
        print "successfully deleted " + x.deleted_count

    