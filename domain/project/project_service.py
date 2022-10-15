from adapter.repository import project_repository
from domain.project.project_entity import Project

class ProjectServiceSuccess:
    pass

class ProjectServiceError:
    pass

class ProjectNotFound(ProjectServiceError):
    pass

def find_project_by_id(project_id: str) -> Project | ProjectServiceError:
    project = project_repository.find_project_by_id(project_id)
    if not project:
        return ProjectNotFound()
    
    return project

def create_project(project: Project) -> Project:

    # for now projects could always be created
    res = project_repository.create_project(project)
    return res

def update_project(project: Project) -> Project | ProjectServiceError:
    project = project_repository.update_project(project)
    if not project:
        return ProjectNotFound()
    return project

def update_project_poster(project_id: str, poster_base64: str) -> str | ProjectServiceError:
    project = find_project_by_id(project_id)
    if isinstance(project, ProjectNotFound):
        return ProjectNotFound()
    project.poster_image = poster_base64
    new_project = update_project(project)
    return new_project.poster_image

def find_project_poster_by_id(project_id: str) -> str | ProjectServiceError:
    project = find_project_by_id(project_id)
    if isinstance(project, ProjectNotFound):
        return ProjectNotFound()
    return project.poster_image