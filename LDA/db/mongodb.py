from pymongo import MongoClient
import os

class Database():
    
    def __init__(self,dbname):
        self.dbname = dbname
        self.client = MongoClient('mongodb', 27017)

    def mongo(self):
        return self.client[self.dbname]