from fastapi import Body, FastAPI
from pydantic import BaseModel
import datetime
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from adapter.router.project import project_router as project
from dotenv import load_dotenv

import os

# load_dotenv()
BASE_PATH = os.getenv("BASE_PATH")
VERSION_1 = os.getenv("VERSION_1")
FE_URL = os.getenv("FE_URL")

app = FastAPI()
app.include_router(
    project.router,
    prefix=f"{BASE_PATH}{VERSION_1}"
)
origins = [
    FE_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    now = datetime.datetime.now()
    return f"[{str(now)}] project_service is ok"

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Project Service",
        version="1.0.0",
        description="Schema for the project service",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi