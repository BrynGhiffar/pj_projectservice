import os
from pymongo import MongoClient
import certifi

def get_database():
    ca = certifi.where()
    CONNECTION_STRING = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("MONGO_DB_NAME")

    client = MongoClient(CONNECTION_STRING)
    if (not (CONNECTION_STRING is None)) and ("mongodb+srv" in CONNECTION_STRING):
        client = MongoClient(CONNECTION_STRING)
    if not DB_NAME:
        DB_NAME = "ProjectService"
    return client[DB_NAME]