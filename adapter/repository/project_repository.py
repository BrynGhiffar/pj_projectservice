from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from domain.project.project_entity import Project
from pymongo.errors import ServerSelectionTimeoutError

class ProjectRepositoryError:

    def __init__(self):
        self.name = "GENERIC_PROJECT_REPOSITORY_ERROR"
        self.message = "An unknown error occurred, please contact developer"

class ProjectRepositoryErrorExtra(ProjectRepositoryError):

    def __init__(self):
        super().__init__()
        self.extra_message = "Something must have gone wrong"
    
class TimeoutConnectionError(ProjectRepositoryErrorExtra):

    def __init__(self, extra_message: str):
        super().__init__()
        self.name = "PROJECT_REPOSITORY_TIMEOUT_ERROR"
        self.message = "Connection with the database has timed out"
        self.extra_message = extra_message

class ProjectRepository:

    def __init__(self, project_repository_config):
        self.get_project_collection = project_repository_config

    def create_project(self, project: Project) -> Project \
                                                    | TimeoutConnectionError \
                                                    :
        project_dict = project.dict()
        del project_dict["project_id"]
        try:
            res = self.get_project_collection().insert_one(project_dict)
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        project.project_id = str(res.inserted_id)
        return project

    def find_project_by_id(self, project_id: str) -> Project \
                                                    | TimeoutConnectionError \
                                                    | None:
        try:
            _id = ObjectId(project_id)
            try:
                res = self.get_project_collection().find_one({"_id": _id})
            except ServerSelectionTimeoutError as e:
                return TimeoutConnectionError(extra_message=e._message)

            if not res:
                return None
            
            res["project_id"] = str(res["_id"])

            project = Project.parse_obj(res)
            return project
        except InvalidId:
            return None

    def update_project(self, project: Project) -> Project \
                                                    | TimeoutConnectionError \
                                                    | None:
        try:
            _id = ObjectId(project.project_id)
            try:
                res = self.get_project_collection().find_one_and_replace({"_id": _id}, project.dict(), return_document=ReturnDocument.AFTER)
            except ServerSelectionTimeoutError as e:
                return TimeoutConnectionError(extra_message=e._message)
            if not res:
                return None
            res["project_id"] = str(res["_id"])
            project = Project.parse_obj(res)
            return project
        except InvalidId:
            return None
    
    def find_project_by_user(self, user_id: str) -> list[Project] \
                                                    | TimeoutConnectionError:
        try:
            res = self.get_project_collection().find({"members": user_id})
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        ret = []
        try:
            for project in res:
                project["project_id"] = str(project["_id"])
                ret.append(Project.parse_obj(project))
            return ret[::-1]
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)

    def find_all_projects(self) -> list[Project] \
                                                    | TimeoutConnectionError:
        try:
            res = self.get_project_collection().find()
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        ret = []
        try:
            for project in res:
                ret.append(Project.parse_obj(project))
            return ret
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)

