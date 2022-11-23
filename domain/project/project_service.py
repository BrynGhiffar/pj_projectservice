from adapter.repository.project_repository import ProjectRepository, TimeoutConnectionError
from domain.project.project_entity import Project
import io, base64, binascii

class ProjectServiceError:

    def __init__(self):
        self.name = "GENERIC_PROJECT_SERVICE_ERROR"
        self.message = "Unknown error occurred"

class ProjectServiceErrorExtra(ProjectServiceError):

    def __init__(self):
        super().__init__()
        self.extra_message = "Something bad happened"

class ProjectNotFound(ProjectServiceError):

    def __init__(self, project_id: str):
        super().__init__()
        self.name = "PROJECT_NOT_EXIST"
        self.message = f"project with id '{project_id}' was not found"

class ProjectPosterEncodingError(ProjectServiceError):

    def __init__(self, poster_id: str):
        super().__init__()
        self.name = "PROJECT_POSTER_ENCODING_ERROR"
        self.message = f"there was a problem decoding the project poster with id '{poster_id}', please contact the developer"

class DatabaseConnectionError(ProjectServiceErrorExtra):

    def __init__(self, extra_message: str):
        super().__init__()
        self.name = "DATABASE_CONNECTION_ERROR"
        self.message = "There was a problem connecting to the database"
        self.extra_message = extra_message

class ProjectService:

    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def find_project_by_id(self, project_id: str) -> Project | ProjectServiceError:
        project = self.project_repository.find_project_by_id(project_id)
        if isinstance(project, TimeoutConnectionError):
            return DatabaseConnectionError(project.extra_message)
        if not project:
            return ProjectNotFound(project_id)
        
        return project

    def create_project(self, project: Project) -> Project | ProjectServiceErrorExtra:

        # for now projects could always be created
        res = self.project_repository.create_project(project)
        if isinstance(res, TimeoutConnectionError):
            return DatabaseConnectionError(res.extra_message)
        return res

    def update_project(self, project: Project) -> Project | ProjectServiceError:
        updated_project = self.project_repository.update_project(project)
        if isinstance(updated_project, TimeoutConnectionError):
            return DatabaseConnectionError(updated_project.extra_message)
        
        if not updated_project:
            return ProjectNotFound(project.project_id)
        return updated_project

    def update_project_poster(self, project_id: str, poster_base64: str) -> str | ProjectServiceError:
        project = self.find_project_by_id(project_id)
        if isinstance(project, TimeoutConnectionError):
            return DatabaseConnectionError(project.extra_message)
        
        if isinstance(project, ProjectNotFound):
            return ProjectNotFound(project_id)

        project.poster_image = poster_base64

        new_project = self.update_project(project)
        if isinstance(new_project, ProjectServiceError):
            return new_project
        
        return new_project.poster_image

    def find_project_poster_by_id(self, project_id: str) -> io.BytesIO | ProjectServiceError:

        project = self.find_project_by_id(project_id)
        if isinstance(project, TimeoutConnectionError):
            return DatabaseConnectionError(project.extra_message)
        
        if isinstance(project, ProjectNotFound):
            return ProjectNotFound(project_id)

        image_str = project.poster_image

        try:
            image_bytes = io.BytesIO(base64.b64decode(image_str))
        except binascii.Error as _:
            return ProjectPosterEncodingError(project_id)
        return image_bytes
    
    def find_project_by_user_id(self, user_id: str) -> list[Project] | ProjectServiceError:
        projects = self.project_repository.find_project_by_user(user_id)
        if isinstance(projects, TimeoutConnectionError):
            return DatabaseConnectionError(projects.extra_message)
        
        return projects
        