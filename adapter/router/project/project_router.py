from fastapi import APIRouter, Body, UploadFile
import adapter.router.project.example as EXAMPLE
from adapter.router.project import project_handler
import base64
import io
from starlette.responses import StreamingResponse

from domain.project.project_entity import Project
router = APIRouter()

@router.get(
        "/{project_id}",
        response_model=project_handler.FindProjectByIdResponse,
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
        response_model=project_handler.CreateProjectResponse,
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
    response_model=project_handler.UpdateProjectResponse
)
def update_project(project: Project):
    return project_handler.update_project(project)

@router.put(
    "/poster/{project_id}"
)
def update_project_poster(project_id: str, poster: UploadFile) :
    # posterbase64 = base64.b64encode(file.file.read())
    # return StreamingResponse(content=io.BytesIO(base64.b64decode(posterbase64)), media_type="image/jpeg")
    return project_handler.update_project_poster(project_id, poster)

@router.get("/poster/{project_id}")
def find_project_poster_by_id(project_id: str):
    return project_handler.find_project_poster_by_id(project_id)