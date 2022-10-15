from typing import List
from pydantic import BaseModel, Field

class Project(BaseModel):
    project_id: str | None = Field(description="unique id of each project")
    class_id: str = Field(description="id of class")
    members: List[str] = Field(description="List of member ids, where each member is a user")
    poster_image: str = Field(description="Poster image in the form of png, jpeg or pdf")
    report: str = Field(description="pdf of the report in Base64")
    description: str = Field(description="The description of the project in the form of markdown")
    youtube_link: str = Field(description="Link to project youtube video")
    github_link: str = Field(description="Link to github project")