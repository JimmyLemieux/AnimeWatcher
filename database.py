import pymongo


class DataBase():
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client['testdb']
        mycol = mydb['customers']
        mycol.insert_one({"name" : "John", "address": "Highway"})
        print client.list_database_names()
        
