from pymongo import MongoClient

class Database():
    
    def __init__(self,dbname):
        self.dbname = dbname
        self.client = MongoClient('localhost', 27017)

    def mongo(self):
        return self.client[self.dbname]