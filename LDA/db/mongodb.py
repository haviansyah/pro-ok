from pymongo import MongoClient
import os

class Database():
    
    def __init__(self,dbname):
        self.dbname = dbname
        self.client = MongoClient(os.environ['MONGODB_HOSTNAME'], 27017)

    def mongo(self):
        return self.client[self.dbname]