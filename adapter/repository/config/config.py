import os
from pymongo import MongoClient
import certifi

def get_database():
    ca = certifi.where()
    CONNECTION_STRING = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("MONGO_DB_NAME")

    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    return client[DB_NAME]