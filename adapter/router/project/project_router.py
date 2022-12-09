from fastapi import APIRouter, Body, UploadFile
import adapter.router.project.example as EXAMPLE
from adapter.router.project.project_handler import ProjectHandler
from domain.project.project_service import ProjectService
from adapter.repository.project_repository import ProjectRepository
from adapter.repository.config.config import get_database
from adapter.router.project.project_handler import FindProjectByIdResponse, \
                                                    CreateProjectResponse, \
                                                    UpdateProjectResponse, \
                                                    FindProjectPosterByIdResponse

from domain.project.project_entity import Project
from domain.notification.notification_service import NotificationService
from adapter.discord.api import DiscordApi
from adapter.discord.config import get_webhook


router = APIRouter()
project_handler = ProjectHandler(
    project_service=ProjectService(
        project_repository=ProjectRepository(
            project_repository_config=lambda: get_database()["project"]
        ),
        notification_service=NotificationService(
            api=DiscordApi(
                webhook_url = get_webhook()
            )
        )
    )
)

@router.get(
        "/{project_id}",
        response_model=FindProjectByIdResponse,
        responses={
            200: {
                "description": "Project found",
                "content": {
                    "application/json": {
                        "example": EXAMPLE.FIND_PROJECT_BY_ID_RESPONSE
                    }
                }
            }
        }
    )
def find_project_by_id(project_id: str):
    return project_handler.find_project_by_id(project_id)

@router.post(
        "/",
        response_model=CreateProjectResponse,
        responses={
            200: {
                "description": "Project successfully created",
                "content": {
                    "application/json": {
                        "example": EXAMPLE.CREATE_PROJECT_RESPONSE
                    }
                }
            }
        }
    )
def create_project(project: Project = Body(example=EXAMPLE.CREATE_PROJECT_REQUEST_BODY)):
    return project_handler.create_project(project)

@router.put(
    "/",
    response_model=UpdateProjectResponse,
    responses={
        200: {
            "description": "Project successfully updated",
            "content": {
                "application/json": {
                    "example": EXAMPLE.UPDATE_PROJECT
                    }
                }
            }
        }
)
def update_project(project: Project):
    return project_handler.update_project(project)

@router.put(
    "/poster/{project_id}",
    response_model=UpdateProjectResponse,
    responses={
        200: {
            "description": "Project Poster successfully created",
            "content": {
                "application/json": {
                    "example": EXAMPLE.UPDATE_PROJECT_POSTER
                    }
                }
            }
        }
)
def update_project_poster(project_id: str, poster: UploadFile) :
    # posterbase64 = base64.b64encode(file.file.read())
    # return StreamingResponse(content=io.BytesIO(base64.b64decode(posterbase64)), media_type="image/jpeg")
    return project_handler.update_project_poster(project_id, poster)

@router.get(
    "/poster/{project_id}", 
    response_model=FindProjectPosterByIdResponse,
    responses={
            200: {
                "description": "Project poster found",
                "content": {
                    "application/json": {
                        "example": EXAMPLE.FIND_PROJECT_POSTER_BY_ID_RESPONSE
                    }
                }
            }
        }
    )
def find_project_poster_by_id(project_id: str):
    return project_handler.find_project_poster_by_id(project_id)

@router.get("/user/{user_id}")
def find_project_by_user_id(user_id: str):
    return project_handler.find_project_by_user_id(user_id)