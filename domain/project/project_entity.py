from typing import List
from pydantic import BaseModel, Field


class ProjectFile(BaseModel):
    name: str = Field(description = "name of the file")
    base64: str = Field(description = "base 64 string of the file")
    ext: str = Field(description = "extension of the file")
    size: str = Field(description = "size of the file")

class Project(BaseModel):
    project_id: str | None = Field(description="unique id of each project")
    class_id: str = Field(description="id of class")
    name: str = Field(description="Name of the project")
    members: List[str] = Field(description="List of member ids, where each member is a user")
    poster_image: ProjectFile = Field(description="Poster image in the form of png, jpeg")
    report: ProjectFile = Field(description="pdf of the report in Base64")
    short_description: str = Field(description="A one sentence description of the project")
    description: str = Field(description="The description of the project in the form of markdown")
    youtube_link: str = Field(description="Link to project youtube video")
    github_link: str = Field(description="Link to github project")
    grade : int = Field(description="Project Grade")
    course_code : str = Field(description="Course code of the class")
    lecturer_name : str = Field(description="Lecturer name")