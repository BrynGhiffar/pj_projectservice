import os
from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("MONGO_DB_NAME")

    client = MongoClient(CONNECTION_STRING)

    return client[DB_NAME]