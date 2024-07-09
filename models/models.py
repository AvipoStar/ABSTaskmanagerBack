from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class LoginClass(BaseModel):
    login: str
    password: str


class Task(BaseModel):
    id: Optional[int]
    name: str
    column_id: int
    serial_number: int
    creation_date_time: datetime
    priority_id: int
    deadline: Optional[datetime]
    is_done: bool
    description: Optional[str]
    creator_id: int


class Attachment2Task(BaseModel):
    id: int
    path: str
    task_id: int


class Priority(BaseModel):
    id: int
    name: str
    color: str


class Column(BaseModel):
    id: Optional[int]
    name: str
    project_id: int
    serial_number: int


class Project(BaseModel):
    id: Optional[int]
    name: str
    direction_id: int
    team_id: int


class ProjectDirection(BaseModel):
    id: int
    name: str


class Worker(BaseModel):
    id: Optional[int]
    login: str
    password: str
    fio: str
    mail: Optional[str]


class Worker2Direction(BaseModel):
    id: int
    worker_id: int
    direction_id: int


class Worker2Team(BaseModel):
    id: int
    team_id: int
    worker_id: int


class Team(BaseModel):
    id: Optional[int]
    name: str


class AttachToTeam(BaseModel):
    user_id: int
    team_id: int
