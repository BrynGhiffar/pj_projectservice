from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from adapter.repository.config.config import get_database
from domain.project.project_entity import Project

project_collection = lambda: get_database()["project"]

class ProjectRepository:

    def __init__(self, project_repository_config):
        self.get_project_collection = project_repository_config

    def create_project(self, project: Project) -> Project | None:
        project_dict = project.dict()
        del project_dict["project_id"]
        res = self.get_project_collection().insert_one(project_dict)
        project.project_id = str(res.inserted_id)
        return project

    def find_project_by_id(self, project_id: str) -> Project | None:
        try:
            _id = ObjectId(project_id)
            res = self.get_project_collection().find_one({"_id": _id})

            if not res:
                return None
            
            res["project_id"] = str(res["_id"])

            project = Project.parse_obj(res)
            return project
        except InvalidId:
            return None

    def update_project(self, project: Project) -> Project | None:
        try:
            _id = ObjectId(project.project_id)
            res = self.get_project_collection().find_one_and_replace({"_id": _id}, project.dict(), return_document=ReturnDocument.AFTER)
            if not res:
                return None
            res["project_id"] = str(res["_id"])
            project = Project.parse_obj(res)
            return project
        except InvalidId:
            return None
        

