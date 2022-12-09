import os
from pymongo import MongoClient
import certifi

def get_database():
    ca = certifi.where()
    CONNECTION_STRING = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("MONGO_DB_NAME")

    client = MongoClient(CONNECTION_STRING)
    # use this for accessing a mongodb+srv database instead
    # client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)
    if not DB_NAME:
        DB_NAME = "mongodb://localhost:27017/"
    return client[DB_NAME]