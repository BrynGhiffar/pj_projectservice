from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from adapter.repository.config.config import get_database
from domain.class_.class_entity import Class

class_collection = lambda: get_database()["class"]

def create_class(class_: Class) -> Class | None:
    class_dict = class_.dict()
    del class_dict["class_id"]
    res = class_collection().insert_one(class_dict)
    class_.project_id = str(res.inserted_id)
    return class_

def find_class_by_id(class_id: str) -> Class | None:
    try:
        _id = ObjectId(class_id)
        res = class_collection().find_one({"_id": _id})

        if not res:
            return None
        
        res["class_id"] = str(res["_id"])

        class_ = Class.parse_obj(res)
        return class_
    except InvalidId:
        return None

def update_class(class_: Class) -> Class | None:
    try:
        _id = ObjectId(class_.class_id)
        res = class_collection().find_one_and_replace({"_id": _id}, class_.dict(), return_document=ReturnDocument.AFTER)
        if not res:
            return None
        res["class_id"] = str(res["_id"])
        class_ = Class.parse_obj(res)
        return class_
    except InvalidId:
        return None