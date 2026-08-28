from typing import  Any, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Course(BaseModel):
    id:str
    name: str
    section: Optional[str] = None
    subject: Optional[str] = None
    room: Optional[str] = None
    course_state: str = "ACTIVE"
    alternate_link: Optional[str] = None
    owner_id: Optional[str] = None
    calendar_id: Optional[str] = None
    course_group_email: Optional[str] = None
    creation_time: Optional[datetime] = None
    update_time: Optional[datetime] = None    

class Assignment(BaseModel):
    id: str
    title: str
    courseId: str
    coursename:str
    description: str | None = None
    dueDate: datetime | None = None
    materials: list[dict[str, Any]] = Field(default_factory=list)
    due_date_status: Literal["Pending", "Due", "WithoutDueDate"]

class ALLassignments(BaseModel):
    assignments :list[Assignment]

class ALLcourses(BaseModel):
    courses :list[Course]