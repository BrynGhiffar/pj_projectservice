from typing import List
from pydantic import BaseModel

EVEN = "EVEN"
ODD = "ODD"

class Class(BaseModel):
    class_id: str
    lecturer_id: str
    students: List[str]
    year: str
    semester: EVEN | ODD