import pymongo


class DataBase():
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__mydb = client['animewatcher'] # making a new database
        self.__showCol = self.__mydb['SHOWS']

    def getDatabase(self):
        if(self.__mydb):
            return self.__mydb
        else:
            return None

    def getShowCollection(self):
        if self.__showCol:
            return self.__showCol
        return None


    def findShowByName(self, showName):
        pass
    
    def saveShow(self, showObj):
        # if there is no collection name with the showTitle, then make a new collection with the __showCol variable
        self.__showCol.insertOne(showObj)
        print showObj['showTitle'] + ' was inserted into the database'

    def deleteAllShows(self):
        x = self.__showCol.delete_many({})
        print "successfully deleted " + x.deleted_count
    
    def sortAllShowsByName(self):
        shows = self.__showCol.find().sort("showName")
        for i in shows:
            print i

    