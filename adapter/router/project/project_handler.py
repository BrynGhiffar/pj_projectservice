import io
from fastapi import UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from domain.project import project_service
from domain.project.project_entity import Project
from pydantic import BaseModel
import base64

class FindProjectByIdResponse(BaseModel):
    message: str
    project: Project | None

class CreateProjectResponse(BaseModel):
    message: str
    project: Project | None

class UpdateProjectResponse(BaseModel):
    message: str
    project: Project | None

class UpdateProjectPosterResponse(BaseModel):
    message: str
    poster_base64: str | None

def find_project_by_id(project_id: str) -> JSONResponse:
    res = project_service.find_project_by_id(project_id)
    if isinstance(res, project_service.ProjectServiceError):
        if isinstance(res, project_service.ProjectNotFound):
            find_project_by_id_response = jsonable_encoder(FindProjectByIdResponse(
                message="project not found",
            ))
            return JSONResponse(content=find_project_by_id_response, status_code=404, media_type="application/json")
        else:
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message="unknown error occurred"
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
    else:
        project = res
        find_project_by_id_response = jsonable_encoder(FindProjectByIdResponse(
            message="project found",
            project=project
        ))
        return JSONResponse(content=find_project_by_id_response, status_code=200, media_type="application/json")

def create_project(project: Project) -> JSONResponse:
    res = project_service.create_project(project)
    project = res
    create_project_response = jsonable_encoder(CreateProjectResponse(
        message="project was successully created",
        project=project
    ))
    return JSONResponse(content=create_project_response, status_code=200, media_type="application/json")

def update_project(project: Project) -> JSONResponse:
    res = project_service.update_project(project)
    if isinstance(res, project_service.ProjectServiceError):
        if isinstance(res, project_service.ProjectNotFound):
            update_project_response = jsonable_encoder(UpdateProjectResponse(
                message="project not found"
            ))
            return JSONResponse(content=update_project_response, status_code=404, media_type="application/json")
        else:
            update_project_response = jsonable_encoder(UpdateProjectResponse(
                message="unknown error occurred"
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
    else:
        project = res
        update_project_response = jsonable_encoder(UpdateProjectResponse(
            message="project was successfully updated",
            project=project
        ))
        return JSONResponse(content=update_project_response, status_code=200, media_type="application/json")
 
def update_project_poster(project_id: str, poster: UploadFile) -> JSONResponse:
    posterbase64 = str(base64.b64encode(poster.file.read()))[2:-1]
    res = project_service.update_project_poster(project_id, posterbase64)

    if isinstance(res, project_service.ProjectServiceError):
        if isinstance(res, project_service.ProjectNotFound):
            update_project_response = jsonable_encoder(UpdateProjectPosterResponse(
                message="project was not found"
            ))
            return JSONResponse(content=update_project_response, status_code=404, media_type="application/json")
        else:
            update_project_response = jsonable_encoder(UpdateProjectPosterResponse(
                message="unknown error occurred"
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
    else:
        update_project_response = jsonable_encoder(UpdateProjectPosterResponse(
            message="poster was successfully updated",
            poster_base64=res
        ))
        return JSONResponse(content=update_project_response, status_code=200, media_type="application/json")

def find_project_poster_by_id(project_id: str) -> StreamingResponse | JSONResponse:
    res = project_service.find_project_poster_by_id(project_id)
    if isinstance(res, project_service.ProjectServiceError):
        if isinstance(res, project_service.ProjectNotFound):
            find_project_poster_by_id_response = jsonable_encoder(UpdateProjectPosterResponse(
                message="project was not found"
            ))
            return JSONResponse(content=find_project_poster_by_id_response, status_code=404, media_type="application/json")
        else:
            find_project_poster_by_id_response = jsonable_encoder(UpdateProjectPosterResponse(
                message="unknown error occurred"
            ))
    else:
        return StreamingResponse(content=io.BytesIO(base64.b64decode(res)), status_code=200, media_type="image/jpeg")